# -*- coding: utf-8 -*-
"""
AnalyticsExam SAS 9.4 (A00-231) Incremental Question Harvester & Deduplicator
=============================================================================
Standalone tool with both a Tkinter GUI and CLI mode to:
1. Automatically take a new exam attempt on AnalyticsExam (/node/9586/take),
   smartly selecting untested options to maximize explanation/feedback coverage,
   and scrape + deduplicate/merge results into analyticsexam_9586_questions.json.
2. Run N batch attempts sequentially with optional Smart Stop (auto-stop when M
   consecutive attempts yield 0 new unique questions).
3. Sync any unscanned "More..." attempt result links from /node/9586/myresults.
"""

import argparse
import ctypes
from ctypes import wintypes
import html
import json
import os
import random
import re
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
from urllib.parse import urlencode, urljoin

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    HAS_TK = True
except ImportError:
    HAS_TK = False

# ---------------------------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "analyticsexam_9586_questions.json")
BACKUP_PATH = os.path.join(BASE_DIR, "analyticsexam_9586_questions.backup.json")
COOKIE_CACHE_PATH = os.path.join(BASE_DIR, ".analyticsexam_session.json")
SIMULATOR_HTML_PATH = os.path.join(BASE_DIR, "sas_exam_simulator.html")

BASE_URL = "https://www.analyticsexam.com"
LOGIN_URL = "https://www.analyticsexam.com/user/login"
TAKE_URL = "https://www.analyticsexam.com/node/9586/take"
MYRESULTS_URL = "https://www.analyticsexam.com/node/9586/myresults"
EXAM_TITLE = "(SAMPLE) SAS 9.4 Base Programming - Performance-Based Exam (A00-231)"

DEFAULT_USERNAME = "caokhanh"
DEFAULT_EMAIL = "khanhvinhcaoii@gmail.com"
DEFAULT_PASSWORD = "Ckl21!232!"
DEFAULT_PROXY = "socks5h://127.0.0.1:1080"


# ---------------------------------------------------------------------------
# HTML Parsing & Normalization Helpers (Exact Match to Validated Logic)
# ---------------------------------------------------------------------------
def clean_html_to_text(raw_html: str) -> str:
    """Convert an HTML fragment into clean text preserving paragraphs, lists, and code blocks."""
    if not raw_html:
        return ""
    s = raw_html
    s = re.sub(r'<li[^>]*>\s*', '- ', s, flags=re.IGNORECASE)
    s = re.sub(r'</li>', '\n', s, flags=re.IGNORECASE)
    s = re.sub(r'</p>', '\n', s, flags=re.IGNORECASE)
    s = re.sub(r'<br\s*/?>', '\n', s, flags=re.IGNORECASE)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    s = s.replace('\xa0', ' ')
    lines = [line.strip() for line in s.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines).strip()


def extract_images(raw_html: str) -> list:
    """Return a list of absolute image URLs from an HTML fragment (excluding UI feedback icons)."""
    imgs = []
    if not raw_html:
        return imgs
    for m in re.finditer(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\'][^>]*>', raw_html, flags=re.IGNORECASE):
        src = html.unescape(m.group(1)).strip()
        if '/modules/quiz/question_types/multichoice/theme/images/' in src:
            continue
        abs_url = urljoin(BASE_URL, src)
        if abs_url not in imgs:
            imgs.append(abs_url)
    return imgs


def normalize_for_dedup(text: str) -> str:
    """Strictly normalize text for deduplication:
    - Strip leading question labels/numbers (e.g. 'Question 1', 'Q1:', '1.')
    - Convert HTML entities and normalize whitespace/newlines
    - Lowercase and strip leading/trailing punctuation noise
    """
    if not text:
        return ""
    s = html.unescape(text)
    # Strip leading question prefixes like "Question 1", "Q1:", "1."
    s = re.sub(r'^(?:question\s*\d+|q\d+|\d+[\.\:\)])\s*', '', s.strip(), flags=re.IGNORECASE)
    # Collapse all whitespace and newlines
    s = re.sub(r'[\r\n\t]+', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip().lower()
    # Strip trailing punctuation
    s = re.sub(r'[\.\:\;\?\!]+$', '', s).strip()
    return s


def make_question_key(question_text: str, options: list) -> tuple:
    """Create a canonical deduplication key from normalized question_text and normalized sorted options."""
    norm_q = normalize_for_dedup(question_text)
    norm_opts = tuple(sorted(normalize_for_dedup(o) for o in options))
    return (norm_q, norm_opts)


def parse_existing_explanation_map(explanation_text: str, options: list, correct_answer_str: str) -> dict:
    """Reconstruct option -> feedback mapping from an existing formatted explanation string."""
    fb_map = {}
    if not explanation_text:
        return fb_map
    text = explanation_text.strip()
    if not text:
        return fb_map

    # Match blocks starting with [Correct - <opt>]: or [Incorrect - <opt>]:
    pattern = re.compile(r'\[(Correct|Incorrect)\s*-\s*(.*?)\]:\s*(.*?)(?=\n\n\[(?:Correct|Incorrect)\s*-\s*|\Z)', flags=re.DOTALL)
    matches = list(pattern.finditer(text))
    if matches:
        for m in matches:
            opt_text = m.group(2).strip()
            fb_text = m.group(3).strip()
            if opt_text and fb_text:
                fb_map[opt_text] = fb_text
    else:
        # Single plain explanation (associated with correct_answer if single)
        correct_list = [c.strip() for c in correct_answer_str.split(" | ") if c.strip()]
        if len(correct_list) == 1:
            fb_map[correct_list[0]] = text
        else:
            fb_map["_general"] = text
    return fb_map


def build_explanation(option_feedback_map: dict, correct_answers_list: list, dd2_text: str = "") -> str:
    """Build a comprehensive explanation string from collected option feedbacks."""
    parts = []
    # Put feedback for correct option(s) first
    for ca in correct_answers_list:
        if ca in option_feedback_map:
            fb = option_feedback_map[ca]
            if len(option_feedback_map) > 1 or len(correct_answers_list) > 1:
                parts.append(f"[Correct - {ca}]: {fb}")
            else:
                parts.append(fb)
    # Then put feedback for incorrect option(s)
    for opt, fb in option_feedback_map.items():
        if opt == "_general":
            continue
        if opt not in correct_answers_list:
            if len(option_feedback_map) > 1 or parts:
                parts.append(f"[Incorrect - {opt}]: {fb}")
            else:
                parts.append(fb)
    if "_general" in option_feedback_map and option_feedback_map["_general"] not in parts:
        parts.append(option_feedback_map["_general"])
    if dd2_text and dd2_text not in parts:
        parts.append(dd2_text)
    return "\n\n".join(parts)


def parse_attempt_html(html_content: str) -> list:
    """Parse all questions from a single attempt result page (/node/9586/myresults/<id>)."""
    dl_match = re.search(r'<dl class="quiz-report">(.*?)</dl>', html_content, flags=re.DOTALL | re.IGNORECASE)
    if not dl_match:
        return []
    dl_inner = dl_match.group(1)

    pattern = re.compile(
        r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>(?:\s*<dd>(.*?)</dd>)?',
        flags=re.DOTALL | re.IGNORECASE
    )

    questions = []
    for q_idx, m in enumerate(pattern.finditer(dl_inner), start=1):
        dt_html, dd1_html, dd2_html = m.group(1), m.group(2), m.group(3) or ""
        is_skipped = 'quiz-report-skipped' in dt_html

        q_split = re.split(r'<p class="quiz-report-question">.*?</p>', dt_html, flags=re.DOTALL | re.IGNORECASE)
        q_body_html = q_split[1] if len(q_split) > 1 else dt_html

        question_text = clean_html_to_text(q_body_html)
        question_images = extract_images(q_body_html) + extract_images(dd1_html) + extract_images(dd2_html)
        seen_imgs = []
        for img in question_images:
            if img not in seen_imgs:
                seen_imgs.append(img)
        question_images = seen_imgs

        tbody_match = re.search(r'<tbody>(.*?)</tbody>', dd1_html, flags=re.DOTALL | re.IGNORECASE)
        tbody_html = tbody_match.group(1) if tbody_match else dd1_html
        tr_list = re.findall(r'<tr\b[^>]*>(.*?)</tr>', tbody_html, flags=re.DOTALL | re.IGNORECASE)

        options = []
        correct_answers = []
        user_answers = []
        option_feedback_map = {}
        current_opt_text = None

        for tr_inner in tr_list:
            if 'class="selector-td"' in tr_inner:
                tds = re.findall(r'<td\b[^>]*>(.*?)</td>', tr_inner, flags=re.DOTALL | re.IGNORECASE)
                if len(tds) >= 2:
                    selector_html = tds[0]
                    opt_html = tds[1]
                    opt_text = clean_html_to_text(opt_html)
                    options.append(opt_text)
                    current_opt_text = opt_text

                    if 'images/correct.png' in selector_html:
                        correct_answers.append(opt_text)
                        user_answers.append(opt_text)
                    elif 'images/should.png' in selector_html:
                        correct_answers.append(opt_text)
                    elif 'images/wrong.png' in selector_html:
                        user_answers.append(opt_text)
            elif 'quiz_answer_feedback' in tr_inner:
                fb_match = re.search(r'<div class="quiz_answer_feedback">(.*?)</div>', tr_inner, flags=re.DOTALL | re.IGNORECASE)
                fb_html = fb_match.group(1) if fb_match else tr_inner
                fb_text = clean_html_to_text(fb_html)
                if fb_text and current_opt_text:
                    option_feedback_map[current_opt_text] = fb_text

        dd2_text = clean_html_to_text(dd2_html)
        correct_answer_str = " | ".join(correct_answers) if len(correct_answers) > 1 else (correct_answers[0] if correct_answers else "")
        if is_skipped and not user_answers:
            user_answer_str = "(skipped)"
        else:
            user_answer_str = " | ".join(user_answers) if len(user_answers) > 1 else (user_answers[0] if user_answers else "")

        questions.append({
            "question_number_original": f"Q{q_idx}",
            "question_text": question_text,
            "question_images": question_images,
            "options": options,
            "correct_answer": correct_answer_str,
            "user_answer": user_answer_str,
            "_option_feedback_map": option_feedback_map,
            "_correct_answers_list": correct_answers,
            "_dd2_text": dd2_text,
        })

    return questions


# ---------------------------------------------------------------------------
# Session Cookie Discovery & HTTP Client (via curl.exe + SOCKS5/direct fallback)
# ---------------------------------------------------------------------------
def extract_chrome_session_cookies() -> list:
    """Scan running Chrome NetworkService process memory for active Drupal SESS cookies."""
    if os.name != "nt":
        return []
    cookies = set()
    try:
        # Find Chrome NetworkService PIDs via tasklist/wmic or PowerShell
        cmd = [
            "powershell", "-NoProfile", "-Command",
            "Get-CimInstance Win32_Process -Filter \"Name = 'chrome.exe'\" | "
            "Where-Object { $_.CommandLine -match 'NetworkService' } | "
            "Select-Object -ExpandProperty ProcessId"
        ]
        out = subprocess.check_output(cmd, text=True, timeout=8, stderr=subprocess.DEVNULL)
        pids = [int(line.strip()) for line in out.splitlines() if line.strip().isdigit()]
    except Exception:
        pids = []

    if not pids:
        return []

    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010
    MEM_COMMIT = 0x1000
    PAGE_READWRITE = 0x04
    PAGE_READONLY = 0x02

    class MEMORY_BASIC_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BaseAddress", ctypes.c_void_p),
            ("AllocationBase", ctypes.c_void_p),
            ("AllocationProtect", wintypes.DWORD),
            ("PartitionId", wintypes.WORD),
            ("RegionSize", ctypes.c_size_t),
            ("State", wintypes.DWORD),
            ("Protect", wintypes.DWORD),
            ("Type", wintypes.DWORD),
        ]

    k32 = ctypes.WinDLL('kernel32', use_last_error=True)
    k32.VirtualQueryEx.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.POINTER(MEMORY_BASIC_INFORMATION), ctypes.c_size_t]
    k32.VirtualQueryEx.restype = ctypes.c_size_t
    k32.ReadProcessMemory.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
    k32.ReadProcessMemory.restype = wintypes.BOOL

    for pid in pids:
        h = k32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
        if not h:
            continue
        addr = 0
        mbi = MEMORY_BASIC_INFORMATION()
        while k32.VirtualQueryEx(h, addr, ctypes.byref(mbi), ctypes.sizeof(mbi)):
            if mbi.State == MEM_COMMIT and (mbi.Protect in (PAGE_READWRITE, PAGE_READONLY)) and mbi.RegionSize <= 50 * 1024 * 1024:
                buf = ctypes.create_string_buffer(mbi.RegionSize)
                read = ctypes.c_size_t()
                if k32.ReadProcessMemory(h, addr, buf, mbi.RegionSize, ctypes.byref(read)):
                    data = buf.raw[:read.value]
                    if b'SESS' in data:
                        # HTTPS Drupal names it SSESS...; without S? the leading S gets cut off.
                        for m in re.findall(b'S?SESS[a-f0-9]{32}=[a-zA-Z0-9_-]{20,40}', data):
                            cookies.add(m.decode('ascii'))
            addr += mbi.RegionSize
            if addr >= 0x7FFFFFFFFFFF:
                break
        k32.CloseHandle(h)

    return sorted(cookies)


class AnalyticsExamClient:
    """HTTP Client using curl.exe with automatic SOCKS5 proxy detection and cookie management."""

    def __init__(self, log_fn=print, proxy=DEFAULT_PROXY):
        self.log = log_fn
        self.proxy = proxy
        self.session_cookie = self._load_cached_cookie()

    def _load_cached_cookie(self) -> str:
        if os.path.exists(COOKIE_CACHE_PATH):
            try:
                with open(COOKIE_CACHE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("cookie", "")
            except Exception:
                pass
        return "SESSba01a545bdbb11362ac5ae32a624caa7=ovdb159q0bicvnecutb8a4bh27"

    def save_cookie(self, cookie_str: str):
        self.session_cookie = cookie_str.strip()
        try:
            with open(COOKIE_CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump({"cookie": self.session_cookie, "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")}, f, indent=2)
        except Exception:
            pass

    def request(self, url: str, method: str = "GET", data: dict = None, retries: int = 3) -> tuple:
        """
        Perform HTTP GET or POST using curl.exe.
        Returns (final_url, html_body).
        """
        last_err = None
        for attempt in range(1, retries + 1):
            for use_proxy in ([True, False] if self.proxy else [False]):
                cmd = [
                    "curl.exe",
                    "-s",
                    "-L",
                    "--max-time", "20",
                    "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                    "-w", "\n__EFFECTIVE_URL__:%{url_effective}",
                ]
                if use_proxy and self.proxy:
                    cmd.extend(["-x", self.proxy])
                if self.session_cookie:
                    cmd.extend(["-b", self.session_cookie])
                if method.upper() == "POST" and data is not None:
                    encoded = urlencode(data, doseq=True)
                    cmd.extend(["-X", "POST", "-H", "Content-Type: application/x-www-form-urlencoded", "--data-raw", encoded])
                cmd.append(url)

                try:
                    proc = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        timeout=25,
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                    )
                    if proc.returncode == 0 and proc.stdout:
                        out = proc.stdout
                        eff_url = url
                        if "\n__EFFECTIVE_URL__:" in out:
                            body, eff_part = out.rsplit("\n__EFFECTIVE_URL__:", 1)
                            eff_url = eff_part.strip()
                        else:
                            body = out
                        if body.strip():
                            return eff_url, body
                    last_err = f"curl exit {proc.returncode}: {proc.stderr.strip()}"
                except Exception as e:
                    last_err = str(e)
            if attempt < retries:
                time.sleep(1.5)
        raise RuntimeError(f"Network request failed for {url} after {retries} retries ({last_err})")

    def ensure_authenticated(self, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD) -> bool:
        """
        Verify authentication by requesting MYRESULTS_URL.
        1. Try cached session cookie.
        2. If not logged in, auto-extract active cookie from running Chrome NetworkService.
        3. If still not logged in, attempt direct form login to /user/login.
        """
        self.log("Verifying session authentication on AnalyticsExam...")
        try:
            eff_url, body = self.request(MYRESULTS_URL)
            if self._is_logged_in(body, eff_url):
                self.log("Authenticated session verified (active cookie valid).")
                self.save_cookie(self.session_cookie)
                return True
        except Exception as e:
            self.log(f"Initial check warning: {e}")

        # Try extracting live cookie from running Chrome
        self.log("Scanning active Chrome browser session for SESS cookie...")
        live_cookies = extract_chrome_session_cookies()
        for ck in live_cookies:
            self.session_cookie = ck
            try:
                eff_url, body = self.request(MYRESULTS_URL)
                if self._is_logged_in(body, eff_url):
                    self.log(f"Recovered valid session cookie from Chrome: {ck[:20]}...")
                    self.save_cookie(ck)
                    return True
            except Exception:
                pass

        # Try direct login POST (works if CAPTCHA is not enforced on current IP/session)
        self.log(f"Attempting direct login for '{username}'...")
        try:
            _, login_html = self.request(LOGIN_URL)
            build_id_m = re.search(r'name="form_build_id"\s+id="[^"]+"\s+value="([^"]+)"', login_html)
            form_build_id = build_id_m.group(1) if build_id_m else ""
            for login_name in [username, DEFAULT_EMAIL]:
                payload = {
                    "name": login_name,
                    "pass": password,
                    "form_build_id": form_build_id,
                    "form_id": "user_login",
                    "op": "Log in",
                }
                eff_url, res_html = self.request(LOGIN_URL, method="POST", data=payload)
                if self._is_logged_in(res_html, eff_url):
                    self.log("Direct login succeeded.")
                    return True
        except Exception as e:
            self.log(f"Direct login attempt failed: {e}")

        return False

    @staticmethod
    def _is_logged_in(html_body: str, eff_url: str = "") -> bool:
        if not html_body or "/user/login" in eff_url:
            return False
        # Anonymous pages carry body class "not-logged-in", which contains "logged-in".
        if "not-logged-in" in html_body:
            return False
        if "Access denied" in html_body or "You are not authorized" in html_body:
            return False
        return "/logout" in html_body


# ---------------------------------------------------------------------------
# Dataset Manager (Load, Backup, Deduplicate, Enrich, Save)
# ---------------------------------------------------------------------------
class DatasetManager:
    def __init__(self, json_path=JSON_PATH, backup_path=BACKUP_PATH):
        self.json_path = json_path
        self.backup_path = backup_path
        self.data = self.load()

    def load(self) -> dict:
        if os.path.exists(self.json_path):
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {
                "exam_title": EXAM_TITLE,
                "source_url": MYRESULTS_URL,
                "scanned_attempt_ids": ["157993", "157994"],
                "total_attempts_scanned": 0,
                "total_questions_raw": 0,
                "total_unique_questions": 0,
                "questions": [],
            }

        # Ensure scanned_attempt_ids exists and is pre-populated with ["157993", "157994"]
        if "scanned_attempt_ids" not in data or not isinstance(data["scanned_attempt_ids"], list):
            data["scanned_attempt_ids"] = ["157993", "157994"]
        else:
            for init_id in ("157993", "157994"):
                if init_id not in data["scanned_attempt_ids"] and data.get("total_attempts_scanned", 0) >= 2:
                    data["scanned_attempt_ids"].append(init_id)

        self.data = data
        return data

    def create_backup(self):
        if os.path.exists(self.json_path):
            shutil.copy2(self.json_path, self.backup_path)

    def get_known_tested_options(self) -> dict:
        """
        Return a lookup mapping normalized question_text -> set of normalized option texts
        that already have feedback or were already selected as user_answer.
        Used during exam taking to pick untested options and uncover new explanations!
        """
        tested_map = {}
        for q in self.data.get("questions", []):
            norm_q = normalize_for_dedup(q.get("question_text", ""))
            tested_opts = set()
            # Parse options already present in explanation
            fb_map = parse_existing_explanation_map(
                q.get("explanation", ""),
                q.get("options", []),
                q.get("correct_answer", ""),
            )
            for opt_text in fb_map.keys():
                if opt_text != "_general":
                    tested_opts.add(normalize_for_dedup(opt_text))
            # Also add previous user_answer(s) and known correct_answer(s)
            for ua in q.get("user_answer", "").split(" | "):
                ua = ua.strip()
                if ua and ua != "(skipped)":
                    tested_opts.add(normalize_for_dedup(ua))
            tested_map[norm_q] = tested_opts
        return tested_map

    def merge_attempt_questions(self, attempt_id: str, extracted_questions: list) -> dict:
        """
        Deduplicate and merge extracted questions from a single attempt into self.data.
        Creates a .backup.json copy before saving.
        Returns stats dict: {new_added, existing_enriched, total_unique, total_raw, total_attempts}
        """
        self.load()
        self.create_backup()

        questions_list = self.data.get("questions", [])
        key_to_rec = {}
        for rec in questions_list:
            k = make_question_key(rec.get("question_text", ""), rec.get("options", []))
            key_to_rec[k] = rec

        new_added = 0
        existing_enriched = 0

        for q in extracted_questions:
            k = make_question_key(q["question_text"], q["options"])
            if k not in key_to_rec:
                explanation = build_explanation(
                    q["_option_feedback_map"],
                    q["_correct_answers_list"],
                    q["_dd2_text"],
                )
                new_rec = {
                    "id": len(questions_list) + 1,
                    "question_number_original": q["question_number_original"],
                    "question_text": q["question_text"],
                    "question_images": list(q["question_images"]),
                    "options": list(q["options"]),
                    "correct_answer": q["correct_answer"],
                    "user_answer": q["user_answer"],
                    "explanation": explanation,
                }
                questions_list.append(new_rec)
                key_to_rec[k] = new_rec
                new_added += 1
            else:
                existing = key_to_rec[k]
                changed = False

                if not existing.get("correct_answer") and q["correct_answer"]:
                    existing["correct_answer"] = q["correct_answer"]
                    changed = True

                if (not existing.get("user_answer") or existing.get("user_answer") == "(skipped)") and q["user_answer"] and q["user_answer"] != "(skipped)":
                    existing["user_answer"] = q["user_answer"]
                    changed = True

                for img in q["question_images"]:
                    if img not in existing.get("question_images", []):
                        existing.setdefault("question_images", []).append(img)
                        changed = True

                # Reconstruct existing option feedback map and merge new feedbacks
                existing_correct_list = [
                    c.strip() for c in existing.get("correct_answer", "").split(" | ") if c.strip()
                ]
                for ca in q["_correct_answers_list"]:
                    if ca not in existing_correct_list:
                        existing_correct_list.append(ca)

                fb_map = parse_existing_explanation_map(
                    existing.get("explanation", ""),
                    existing.get("options", []),
                    existing.get("correct_answer", ""),
                )

                for opt_k, fb_v in q["_option_feedback_map"].items():
                    # Match opt_k against existing options by normalized text so minor order/formatting aligns
                    norm_target = normalize_for_dedup(opt_k)
                    canonical_opt = opt_k
                    for ex_opt in existing.get("options", []):
                        if normalize_for_dedup(ex_opt) == norm_target:
                            canonical_opt = ex_opt
                            break
                    if canonical_opt not in fb_map or len(fb_v) > len(fb_map[canonical_opt]):
                        fb_map[canonical_opt] = fb_v

                new_explanation = build_explanation(fb_map, existing_correct_list, q["_dd2_text"])
                if new_explanation != existing.get("explanation", "") and len(new_explanation) >= len(existing.get("explanation", "")):
                    existing["explanation"] = new_explanation
                    changed = True

                if changed:
                    existing_enriched += 1

        # Re-number sequential IDs cleanly
        for idx, rec in enumerate(questions_list, start=1):
            rec["id"] = idx

        scanned_ids = self.data.setdefault("scanned_attempt_ids", [])
        if str(attempt_id) not in scanned_ids:
            scanned_ids.append(str(attempt_id))
            self.data["total_attempts_scanned"] = max(
                int(self.data.get("total_attempts_scanned", 0)) + 1,
                len(scanned_ids),
            )
            self.data["total_questions_raw"] = int(self.data.get("total_questions_raw", 0)) + len(extracted_questions)
        else:
            self.data["total_attempts_scanned"] = max(
                int(self.data.get("total_attempts_scanned", 0)),
                len(scanned_ids),
            )

        self.data["total_unique_questions"] = len(questions_list)
        self.data["questions"] = questions_list

        # Save with exact required schema ordering
        ordered_output = {
            "exam_title": self.data.get("exam_title", EXAM_TITLE),
            "source_url": self.data.get("source_url", MYRESULTS_URL),
            "scanned_attempt_ids": self.data["scanned_attempt_ids"],
            "total_attempts_scanned": self.data["total_attempts_scanned"],
            "total_questions_raw": self.data["total_questions_raw"],
            "total_unique_questions": self.data["total_unique_questions"],
            "questions": self.data["questions"],
        }

        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(ordered_output, f, ensure_ascii=False, indent=2)

        self.data = ordered_output

        # Automatically run strict deduplication and clean, then sync simulator
        self.deduplicate_and_clean_json(create_backup=False)

        return {
            "attempt_id": str(attempt_id),
            "raw_extracted": len(extracted_questions),
            "new_added": new_added,
            "existing_enriched": existing_enriched,
            "total_unique": self.data["total_unique_questions"],
            "total_raw": self.data["total_questions_raw"],
            "total_attempts": self.data["total_attempts_scanned"],
        }

    def deduplicate_and_clean_json(self, create_backup: bool = True) -> dict:
        """
        Strictly deduplicate and clean analyticsexam_9586_questions.json:
        1. Backs up to .backup.json (if create_backup=True).
        2. Normalizes question_text and sorted options to group duplicates.
        3. Merges richer fields into one surviving record per group and deletes duplicate records.
        4. Re-numbers sequential IDs, updates total_unique_questions, and saves UTF-8 indent=2.
        5. Syncs embedded question bank into sas_exam_simulator.html.
        Returns dict with {before_count, removed_count, unique_count}.
        """
        self.load()
        if create_backup:
            self.create_backup()

        raw_questions = self.data.get("questions", [])
        before_count = len(raw_questions)

        grouped = {}  # key -> list of question dicts
        for q in raw_questions:
            k = make_question_key(q.get("question_text", ""), q.get("options", []))
            grouped.setdefault(k, []).append(q)

        surviving_list = []
        for k, q_list in grouped.items():
            # Base record is the first one
            survivor = dict(q_list[0])
            survivor["options"] = list(survivor.get("options", []))
            survivor["question_images"] = list(survivor.get("question_images", []))

            # Build collective correct answers list and option feedback map
            merged_correct_list = [
                c.strip() for c in survivor.get("correct_answer", "").split(" | ") if c.strip()
            ]
            fb_map = parse_existing_explanation_map(
                survivor.get("explanation", ""),
                survivor.get("options", []),
                survivor.get("correct_answer", ""),
            )

            # Merge any richer data from other occurrences in this group
            for other in q_list[1:]:
                # Correct answer
                other_correct_list = [
                    c.strip() for c in other.get("correct_answer", "").split(" | ") if c.strip()
                ]
                for ca in other_correct_list:
                    if ca not in merged_correct_list:
                        merged_correct_list.append(ca)

                # User answer (if survivor was skipped or missing)
                if (not survivor.get("user_answer") or survivor.get("user_answer") == "(skipped)") and other.get("user_answer") and other.get("user_answer") != "(skipped)":
                    survivor["user_answer"] = other.get("user_answer")

                # Images
                for img in other.get("question_images", []):
                    if img not in survivor["question_images"]:
                        survivor["question_images"].append(img)

                # Explanations / Option-level feedback
                other_fb = parse_existing_explanation_map(
                    other.get("explanation", ""),
                    other.get("options", []),
                    other.get("correct_answer", ""),
                )
                for opt_k, fb_v in other_fb.items():
                    norm_target = normalize_for_dedup(opt_k)
                    canonical_opt = opt_k
                    for ex_opt in survivor.get("options", []):
                        if normalize_for_dedup(ex_opt) == norm_target:
                            canonical_opt = ex_opt
                            break
                    if canonical_opt not in fb_map or len(fb_v) > len(fb_map[canonical_opt]):
                        fb_map[canonical_opt] = fb_v

            # Update correct answer string
            if merged_correct_list:
                survivor["correct_answer"] = " | ".join(merged_correct_list)

            # Re-build combined explanation
            survivor["explanation"] = build_explanation(fb_map, merged_correct_list)
            surviving_list.append(survivor)

        # Re-index sequential IDs
        for idx, rec in enumerate(surviving_list, start=1):
            rec["id"] = idx

        removed_count = before_count - len(surviving_list)
        self.data["total_unique_questions"] = len(surviving_list)
        self.data["questions"] = surviving_list

        ordered_output = {
            "exam_title": self.data.get("exam_title", EXAM_TITLE),
            "source_url": self.data.get("source_url", MYRESULTS_URL),
            "scanned_attempt_ids": self.data.get("scanned_attempt_ids", []),
            "total_attempts_scanned": self.data.get("total_attempts_scanned", 0),
            "total_questions_raw": self.data.get("total_questions_raw", 0),
            "total_unique_questions": self.data["total_unique_questions"],
            "questions": self.data["questions"],
        }

        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(ordered_output, f, ensure_ascii=False, indent=2)

        self.data = ordered_output
        self.sync_simulator_html()

        return {
            "before_count": before_count,
            "removed_count": removed_count,
            "unique_count": len(surviving_list),
        }

    def sync_simulator_html(self) -> bool:
        """Update embedded JSON question bank inside sas_exam_simulator.html."""
        if not os.path.exists(SIMULATOR_HTML_PATH):
            return False
        try:
            with open(SIMULATOR_HTML_PATH, "r", encoding="utf-8") as f:
                content = f.read()

            open_tag = '<script id="embeddedQuestionBank" type="application/json">'
            close_tag = '</script>'
            idx1 = content.find(open_tag)
            if idx1 == -1:
                return False
            idx2 = content.find(close_tag, idx1)
            if idx2 == -1:
                return False

            new_json_str = "\n" + json.dumps(self.data, ensure_ascii=False, indent=2) + "\n  "
            new_content = content[: idx1 + len(open_tag)] + new_json_str + content[idx2 :]

            with open(SIMULATOR_HTML_PATH, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True
        except Exception:
            return False


# ---------------------------------------------------------------------------
# Harvester Workflows (Workflow A: Auto-Take + Scrape, Workflow B: Sync Links)
# ---------------------------------------------------------------------------
class ExamHarvester:
    def __init__(self, client: AnalyticsExamClient, db: DatasetManager, log_fn=print):
        self.client = client
        self.db = db
        self.log = log_fn

    def parse_take_question_form(self, html_body: str) -> dict:
        """
        Parse the current question answering form on /node/9586/take.
        Returns None if the page is not a question form (e.g., already redirected to results).
        """
        form_m = re.search(
            r'<form[^>]*id="quiz-question-answering-form"[^>]*>(.*?)</form>',
            html_body,
            flags=re.DOTALL | re.IGNORECASE,
        )
        if not form_m:
            return None
        form_html = form_m.group(1)

        # Progress numbers
        q_num_m = re.search(r'<span id="quiz-question-number">(\d+)</span>', html_body)
        q_tot_m = re.search(r'<span id="quiz-num-questions">(\d+)</span>', html_body)
        q_num = int(q_num_m.group(1)) if q_num_m else 1
        q_tot = int(q_tot_m.group(1)) if q_tot_m else 10

        # Question text
        q_body_m = re.search(r'<div class="quiz-question-body">(.*?)</div>\s*<div class="form-item">', form_html, flags=re.DOTALL | re.IGNORECASE)
        q_text = clean_html_to_text(q_body_m.group(1)) if q_body_m else ""

        # Hidden inputs
        hidden_fields = {}
        for hm in re.finditer(r'<input\b[^>]*type="hidden"[^>]*>', form_html, flags=re.IGNORECASE):
            tag = hm.group(0)
            nm = re.search(r'name="([^"]+)"', tag)
            vm = re.search(r'value="([^"]*)"', tag)
            if nm and vm:
                hidden_fields[nm.group(1)] = html.unescape(vm.group(1))

        # Submit button value ("Next" or "Finish" — never "Back" or "Leave blank")
        submit_op = "Next"
        submit_candidates = []
        for sm in re.finditer(r'<input\b[^>]*type="submit"[^>]*>', form_html, flags=re.IGNORECASE):
            tag = sm.group(0)
            if "q-skip-button" in tag or "q-back-button" in tag:
                continue
            vm = re.search(r'value="([^"]+)"', tag)
            if vm:
                val = html.unescape(vm.group(1)).strip()
                if val.lower() not in ("back", "leave blank", "find"):
                    submit_candidates.append(val)
        if submit_candidates:
            # Prefer "Finish" on the final question, otherwise "Next"
            for cand in submit_candidates:
                if cand.lower() in ("finish", "submit"):
                    submit_op = cand
                    break
            else:
                submit_op = submit_candidates[0]

        # Options (radio or checkbox) inside <tr class="multichoice_row ...">
        choices = []
        is_checkbox = False
        for tr_m in re.finditer(r'<tr\b[^>]*class="[^"]*multichoice_row[^"]*"[^>]*>(.*?)</tr>', form_html, flags=re.DOTALL | re.IGNORECASE):
            tr_inner = tr_m.group(1)
            tds = re.findall(r'<td\b[^>]*>(.*?)</td>', tr_inner, flags=re.DOTALL | re.IGNORECASE)
            if len(tds) >= 2:
                inp_m = re.search(r'<input\b[^>]*type="(radio|checkbox)"[^>]*name="([^"]+)"[^>]*value="([^"]+)"', tds[0], flags=re.IGNORECASE)
                if inp_m:
                    inp_type, inp_name, inp_val = inp_m.group(1).lower(), inp_m.group(2), inp_m.group(3)
                    if inp_type == "checkbox":
                        is_checkbox = True
                    opt_text = clean_html_to_text(tds[1])
                    choices.append({
                        "type": inp_type,
                        "name": inp_name,
                        "value": inp_val,
                        "text": opt_text,
                    })

        return {
            "q_num": q_num,
            "q_tot": q_tot,
            "q_text": q_text,
            "hidden_fields": hidden_fields,
            "submit_op": submit_op,
            "choices": choices,
            "is_checkbox": is_checkbox,
        }

    def take_one_new_attempt_and_harvest(self) -> dict:
        """
        Workflow A:
        1. Ensure authenticated.
        2. Navigate to /node/9586/take.
        3. Loop through all questions (preferring untested options for known questions).
        4. Capture the new /node/9586/myresults/<id> page, parse all questions, and merge.
        """
        if not self.client.ensure_authenticated():
            raise RuntimeError(
                "Authentication failed. Please log in to AnalyticsExam in the Chrome browser window or provide a valid session cookie."
            )

        tested_map = self.db.get_known_tested_options()
        self.log(f"Navigating to {TAKE_URL} to start/resume exam attempt...")
        eff_url, html_body = self.client.request(TAKE_URL, method="GET")

        max_steps = 25
        step = 0
        while step < max_steps:
            step += 1
            # Check if we landed on a results page (/node/9586/myresults/<id>)
            res_m = re.search(r'/node/9586/myresults/(\d+)', eff_url)
            if res_m or '<dl class="quiz-report">' in html_body:
                break

            q_form = self.parse_take_question_form(html_body)
            if not q_form:
                raise RuntimeError(f"Could not locate quiz answering form on {eff_url}")

            q_num = q_form["q_num"]
            q_tot = q_form["q_tot"]
            q_text = q_form["q_text"]
            choices = q_form["choices"]
            submit_op = q_form["submit_op"]

            norm_q = normalize_for_dedup(q_text)
            already_tested = tested_map.get(norm_q, set())

            # Pick untested option(s) if available to maximize feedback discovery
            untested_choices = [c for c in choices if normalize_for_dedup(c["text"]) not in already_tested]
            pool = untested_choices if untested_choices else choices

            payload = dict(q_form["hidden_fields"])
            payload["op"] = submit_op

            selected_labels = []
            if choices:
                if q_form["is_checkbox"]:
                    # Choose up to 2 options for multi-select questions
                    num_pick = min(2, len(pool))
                    picked = pool[:num_pick]
                    if len(picked) < 2 and len(choices) >= 2:
                        for c in choices:
                            if c not in picked:
                                picked.append(c)
                            if len(picked) == 2:
                                break
                    for c in picked:
                        payload[c["name"]] = c["value"]
                        selected_labels.append(c["text"][:40])
                else:
                    picked = pool[0]
                    payload[picked["name"]] = picked["value"]
                    selected_labels.append(picked["text"][:40])

            status_tag = "known-untested-opt" if (norm_q in tested_map and untested_choices) else ("known" if norm_q in tested_map else "NEW-Q")
            self.log(f"  [Q{q_num}/{q_tot}] ({status_tag}) -> submitting '{submit_op}'...")

            eff_url, html_body = self.client.request(TAKE_URL, method="POST", data=payload)

        # Determine the attempt_id and result HTML
        res_m = re.search(r'/node/9586/myresults/(\d+)', eff_url)
        attempt_id = res_m.group(1) if res_m else None

        if not attempt_id or '<dl class="quiz-report">' not in html_body:
            # Fallback: check /node/9586/myresults for the newest attempt link
            self.log("Fetching latest attempt ID from /node/9586/myresults...")
            _, myres_html = self.client.request(MYRESULTS_URL, method="GET")
            links = re.findall(r'/node/9586/myresults/(\d+)', myres_html)
            if not links:
                raise RuntimeError("Exam finished, but no result links were found on /node/9586/myresults.")
            attempt_id = links[0]
            _, html_body = self.client.request(f"{BASE_URL}/node/9586/myresults/{attempt_id}", method="GET")

        extracted = parse_attempt_html(html_body)
        if not extracted:
            raise RuntimeError(f"Attempt #{attempt_id} page contained 0 parsable questions.")

        stats = self.db.merge_attempt_questions(attempt_id, extracted)
        self.log(
            f"Attempt #{attempt_id} processed: +{stats['new_added']} new unique questions added, "
            f"{stats['existing_enriched']} existing questions enriched. Total unique: {stats['total_unique']}"
        )
        return stats

    def sync_unscanned_attempts(self) -> dict:
        """
        Button 3 Workflow:
        Check /node/9586/myresults, find any myresults/<id> links not yet in scanned_attempt_ids,
        scrape only those new links, and merge them into analyticsexam_9586_questions.json.
        """
        if not self.client.ensure_authenticated():
            raise RuntimeError(
                "Authentication failed. Please log in to AnalyticsExam in the Chrome browser window or provide a valid session cookie."
            )

        self.db.load()
        scanned_set = set(str(x) for x in self.db.data.get("scanned_attempt_ids", []))

        self.log(f"Checking {MYRESULTS_URL} for unscanned 'More...' links...")
        _, myres_html = self.client.request(MYRESULTS_URL, method="GET")
        all_ids = []
        for m in re.finditer(r'<a href="/node/9586/myresults/(\d+)">More\.\.\.</a>', myres_html):
            aid = m.group(1)
            if aid not in all_ids:
                all_ids.append(aid)

        unscanned = [aid for aid in reversed(all_ids) if aid not in scanned_set]
        if not unscanned:
            self.log(f"All {len(all_ids)} attempt(s) on 'My results' ({', '.join(all_ids)}) are already in scanned_attempt_ids.")
            return {
                "synced_attempts": 0,
                "new_added": 0,
                "existing_enriched": 0,
                "total_unique": self.db.data.get("total_unique_questions", 0),
                "total_raw": self.db.data.get("total_questions_raw", 0),
                "total_attempts": self.db.data.get("total_attempts_scanned", 0),
            }

        self.log(f"Found {len(unscanned)} unscanned attempt(s): {', '.join(unscanned)}")
        total_new = 0
        total_enriched = 0
        for aid in unscanned:
            url = f"{BASE_URL}/node/9586/myresults/{aid}"
            self.log(f"Scraping unscanned attempt #{aid} ({url})...")
            _, attempt_html = self.client.request(url, method="GET")
            extracted = parse_attempt_html(attempt_html)
            stats = self.db.merge_attempt_questions(aid, extracted)
            total_new += stats["new_added"]
            total_enriched += stats["existing_enriched"]
            self.log(
                f"Attempt #{aid} processed: +{stats['new_added']} new unique questions added, "
                f"{stats['existing_enriched']} existing questions enriched. Total unique: {stats['total_unique']}"
            )

        return {
            "synced_attempts": len(unscanned),
            "new_added": total_new,
            "existing_enriched": total_enriched,
            "total_unique": self.db.data.get("total_unique_questions", 0),
            "total_raw": self.db.data.get("total_questions_raw", 0),
            "total_attempts": self.db.data.get("total_attempts_scanned", 0),
        }


# ---------------------------------------------------------------------------
# Tkinter GUI Application
# ---------------------------------------------------------------------------
class HarvesterGUI:
    def __init__(self, root: "tk.Tk"):
        self.root = root
        self.root.title("AnalyticsExam SAS 9.4 (A00-231) Question Harvester")
        self.root.geometry("880x640")
        self.root.minsize(780, 540)

        self.db = DatasetManager()
        self.client = AnalyticsExamClient(log_fn=self.log)
        self.harvester = ExamHarvester(self.client, self.db, log_fn=self.log)
        self.is_running = False
        self.stop_requested = False

        self._build_ui()
        self.refresh_stats()
        self.log("Ready. Loaded dataset from: " + JSON_PATH)

    def _build_ui(self):
        style = ttk.Style()
        try:
            style.theme_use("vista" if os.name == "nt" else "clam")
        except Exception:
            pass

        main_frame = ttk.Frame(self.root, padding=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_lbl = ttk.Label(
            main_frame,
            text=EXAM_TITLE,
            font=("Segoe UI", 12, "bold"),
        )
        header_lbl.pack(anchor=tk.W, pady=(0, 8))

        # Dataset Stats Frame
        stats_frame = ttk.LabelFrame(main_frame, text="Live Dataset Statistics", padding=12)
        stats_frame.pack(fill=tk.X, pady=(0, 10))

        self.var_attempts = tk.StringVar(value="0")
        self.var_raw = tk.StringVar(value="0")
        self.var_unique = tk.StringVar(value="0")

        grid_items = [
            ("Total Attempts Scanned:", self.var_attempts, 0, 0),
            ("Total Raw Questions:", self.var_raw, 0, 2),
            ("Total Unique Questions:", self.var_unique, 0, 4),
        ]
        for label_text, var, r, c in grid_items:
            ttk.Label(stats_frame, text=label_text, font=("Segoe UI", 10)).grid(
                row=r, column=c, sticky=tk.W, padx=(10, 6), pady=4
            )
            ttk.Label(stats_frame, textvariable=var, font=("Segoe UI", 12, "bold"), foreground="#005fb8").grid(
                row=r, column=c + 1, sticky=tk.W, padx=(0, 36), pady=4
            )

        # Controls / Buttons Frame
        ctrl_frame = ttk.LabelFrame(main_frame, text="Harvest & Sync Actions", padding=10)
        ctrl_frame.pack(fill=tk.X, pady=(0, 10))

        # Row 1: Button 1 (+1 Run) and Button 3 (Sync Unscanned)
        row1 = ttk.Frame(ctrl_frame)
        row1.pack(fill=tk.X, pady=(0, 8))

        self.btn_one = ttk.Button(
            row1,
            text="1. Take 1 New Attempt & Fetch Data (+1 Run)",
            command=self.on_take_one,
        )
        self.btn_one.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6), ipady=4)

        self.btn_sync = ttk.Button(
            row1,
            text="3. Sync Unscanned 'More...' Links Only",
            command=self.on_sync_unscanned,
        )
        self.btn_sync.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0), ipady=4)

        # Row 2: Button 2 (Batch N Runs + Smart Stop)
        row2 = ttk.Frame(ctrl_frame)
        row2.pack(fill=tk.X, pady=(2, 0))

        self.btn_batch = ttk.Button(
            row2,
            text="2. Auto-Harvest N Attempts (Batch / Smart Stop)",
            command=self.on_batch_harvest,
        )
        self.btn_batch.pack(side=tk.LEFT, padx=(0, 10), ipady=4)

        ttk.Label(row2, text="Runs (N):").pack(side=tk.LEFT, padx=(4, 4))
        self.var_batch_n = tk.IntVar(value=3)
        self.spin_n = ttk.Spinbox(row2, from_=1, to=50, textvariable=self.var_batch_n, width=5)
        self.spin_n.pack(side=tk.LEFT, padx=(0, 12))

        self.var_smart_stop = tk.BooleanVar(value=True)
        self.chk_smart = ttk.Checkbutton(
            row2,
            text="Auto-stop if 3 consecutive attempts yield 0 new unique questions",
            variable=self.var_smart_stop,
        )
        self.chk_smart.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_stop = ttk.Button(
            row2,
            text="Stop After Current",
            command=self.on_request_stop,
            state=tk.DISABLED,
        )
        self.btn_stop.pack(side=tk.RIGHT, ipady=4)

        # Row 3: Button 4 (Deduplicate & Clean JSON)
        row3 = ttk.Frame(ctrl_frame)
        row3.pack(fill=tk.X, pady=(8, 0))

        self.btn_dedup_clean = ttk.Button(
            row3,
            text="4. Deduplicate & Clean JSON File",
            command=self.on_deduplicate_clean,
        )
        self.btn_dedup_clean.pack(fill=tk.X, ipady=4)

        # Row 4: SAS Learn Practice Exam Simulator Launcher Button
        row4 = ttk.Frame(ctrl_frame)
        row4.pack(fill=tk.X, pady=(10, 2))

        self.btn_open_simulator = tk.Button(
            row4,
            text="🎓 Launch SAS Learn Practice Exam Simulator (A00-231)",
            command=self.on_open_simulator,
            bg="#006699",
            fg="#ffffff",
            activebackground="#032d60",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.btn_open_simulator.pack(fill=tk.X, ipady=6)

        # Session Cookie Override Collapsible / Bar
        cookie_frame = ttk.Frame(main_frame)
        cookie_frame.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(cookie_frame, text="Session Cookie (auto-detected):", font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=(0, 6))
        self.var_cookie = tk.StringVar(value=self.client.session_cookie)
        cookie_entry = ttk.Entry(cookie_frame, textvariable=self.var_cookie, font=("Consolas", 8))
        cookie_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        ttk.Button(cookie_frame, text="Update Cookie", command=self.on_update_cookie).pack(side=tk.LEFT)

        # Real-time Scrolling Log Console
        log_frame = ttk.LabelFrame(main_frame, text="Real-Time Execution Log", padding=6)
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.txt_log = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff",
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True)

    def log(self, message: str):
        timestamp = time.strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}\n"

        def _append():
            self.txt_log.insert(tk.END, line)
            self.txt_log.see(tk.END)

        if threading.current_thread() is threading.main_thread():
            _append()
        else:
            self.root.after(0, _append)

    def refresh_stats(self):
        self.db.load()
        self.var_attempts.set(str(self.db.data.get("total_attempts_scanned", 0)))
        self.var_raw.set(str(self.db.data.get("total_questions_raw", 0)))
        self.var_unique.set(str(self.db.data.get("total_unique_questions", 0)))

    def _set_running_state(self, running: bool):
        self.is_running = running
        state_main = tk.DISABLED if running else tk.NORMAL
        state_stop = tk.NORMAL if running else tk.DISABLED
        self.btn_one.config(state=state_main)
        self.btn_batch.config(state=state_main)
        self.btn_sync.config(state=state_main)
        self.btn_dedup_clean.config(state=state_main)
        self.btn_stop.config(state=state_stop)

    def on_deduplicate_clean(self):
        if self.is_running:
            return
        self.stop_requested = False
        self._set_running_state(True)

        def _worker():
            try:
                self.log("=== Starting JSON Deduplication & Cleaning ===")
                res = self.db.deduplicate_and_clean_json(create_backup=True)
                self.log(
                    f"JSON Deduplication Complete: {res['before_count']} questions before -> "
                    f"Removed {res['removed_count']} duplicates -> "
                    f"{res['unique_count']} unique questions remaining. Synced with sas_exam_simulator.html."
                )
            except Exception as e:
                self.log(f"ERROR: {e}")
            finally:
                self.root.after(0, self.refresh_stats)
                self.root.after(0, lambda: self._set_running_state(False))

        threading.Thread(target=_worker, daemon=True).start()

    def on_open_simulator(self):
        """Open the interactive SAS Learn Exam Simulator HTML in default browser."""
        self.db.sync_simulator_html()
        if os.path.exists(SIMULATOR_HTML_PATH):
            self.log(f"Opening SAS Exam Simulator: {SIMULATOR_HTML_PATH}")
            webbrowser.open(f"file:///{os.path.abspath(SIMULATOR_HTML_PATH)}")
        else:
            self.log(f"ERROR: {SIMULATOR_HTML_PATH} does not exist.")

    def on_update_cookie(self):
        ck = self.var_cookie.get().strip()
        if ck:
            self.client.save_cookie(ck)
            self.log(f"Updated session cookie: {ck[:28]}...")

    def on_request_stop(self):
        if self.is_running:
            self.stop_requested = True
            self.log("Stop requested — will halt as soon as the current attempt finishes.")

    def on_take_one(self):
        if self.is_running:
            return
        self.stop_requested = False
        self._set_running_state(True)

        def _worker():
            try:
                self.log("=== Starting Single Attempt Harvest (+1 Run) ===")
                self.harvester.take_one_new_attempt_and_harvest()
                self.root.after(0, lambda: self.var_cookie.set(self.client.session_cookie))
            except Exception as e:
                self.log(f"ERROR: {e}")
            finally:
                self.root.after(0, self.refresh_stats)
                self.root.after(0, lambda: self._set_running_state(False))

        threading.Thread(target=_worker, daemon=True).start()

    def on_batch_harvest(self):
        if self.is_running:
            return
        try:
            n_runs = max(1, int(self.var_batch_n.get()))
        except Exception:
            n_runs = 3
        smart_stop = bool(self.var_smart_stop.get())

        self.stop_requested = False
        self._set_running_state(True)

        def _worker():
            try:
                self.log(f"=== Starting Batch Harvest: {n_runs} Attempt(s) (Smart Stop: {smart_stop}) ===")
                zero_new_streak = 0
                total_new = 0
                total_enriched = 0
                completed = 0

                for i in range(1, n_runs + 1):
                    if self.stop_requested:
                        self.log("Batch stopped by user.")
                        break
                    self.log(f"--- Batch Run {i} of {n_runs} ---")
                    stats = self.harvester.take_one_new_attempt_and_harvest()
                    completed += 1
                    total_new += stats["new_added"]
                    total_enriched += stats["existing_enriched"]
                    self.root.after(0, self.refresh_stats)
                    self.root.after(0, lambda: self.var_cookie.set(self.client.session_cookie))

                    if stats["new_added"] == 0:
                        zero_new_streak += 1
                    else:
                        zero_new_streak = 0

                    if smart_stop and zero_new_streak >= 3 and i < n_runs:
                        self.log(
                            "Smart Stop triggered: 3 consecutive attempts yielded 0 new unique questions."
                        )
                        break

                self.log(
                    f"=== Batch Complete: {completed} attempt(s) run, +{total_new} new unique questions, "
                    f"{total_enriched} existing questions enriched. Total unique: {self.db.data.get('total_unique_questions', 0)} ==="
                )
            except Exception as e:
                self.log(f"ERROR: {e}")
            finally:
                self.root.after(0, self.refresh_stats)
                self.root.after(0, lambda: self._set_running_state(False))

        threading.Thread(target=_worker, daemon=True).start()

    def on_sync_unscanned(self):
        if self.is_running:
            return
        self.stop_requested = False
        self._set_running_state(True)

        def _worker():
            try:
                self.log("=== Starting Sync of Unscanned 'More...' Links ===")
                self.harvester.sync_unscanned_attempts()
                self.root.after(0, lambda: self.var_cookie.set(self.client.session_cookie))
            except Exception as e:
                self.log(f"ERROR: {e}")
            finally:
                self.root.after(0, self.refresh_stats)
                self.root.after(0, lambda: self._set_running_state(False))

        threading.Thread(target=_worker, daemon=True).start()


# ---------------------------------------------------------------------------
# Entry Point (GUI by default, or CLI flags for automated/headless execution)
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="AnalyticsExam SAS 9.4 (A00-231) Question Harvester & Deduplicator"
    )
    parser.add_argument(
        "--take",
        type=int,
        metavar="N",
        help="Run N new exam attempts via CLI, scrape results, and merge into JSON.",
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Sync any unscanned 'More...' attempt links from /node/9586/myresults.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Deduplicate and clean analyticsexam_9586_questions.json and sync to simulator HTML.",
    )
    parser.add_argument(
        "--smart-stop",
        action="store_true",
        default=True,
        help="When running --take N, stop early if 3 consecutive attempts yield 0 new unique questions.",
    )
    parser.add_argument(
        "--cookie",
        type=str,
        default="",
        help="Optional explicit SESS cookie string.",
    )
    args = parser.parse_args()

    # If CLI action flags are passed, run headless in console
    if args.take is not None or args.sync or args.clean:
        db = DatasetManager()
        client = AnalyticsExamClient(log_fn=print)
        if args.cookie:
            client.save_cookie(args.cookie)
        harvester = ExamHarvester(client, db, log_fn=print)

        if args.clean:
            res = db.deduplicate_and_clean_json(create_backup=True)
            print(
                f"JSON Deduplication Complete: {res['before_count']} questions before -> "
                f"Removed {res['removed_count']} duplicates -> "
                f"{res['unique_count']} unique questions remaining. Synced with sas_exam_simulator.html."
            )

        if args.sync:
            harvester.sync_unscanned_attempts()

        if args.take is not None and args.take > 0:
            zero_streak = 0
            for i in range(1, args.take + 1):
                print(f"\n--- Running Attempt {i} of {args.take} ---")
                stats = harvester.take_one_new_attempt_and_harvest()
                if stats["new_added"] == 0:
                    zero_streak += 1
                else:
                    zero_streak = 0
                if args.smart_stop and zero_streak >= 3 and i < args.take:
                    print("Smart Stop: 3 consecutive attempts yielded 0 new unique questions.")
                    break
        return

    # Otherwise launch Tkinter GUI
    if not HAS_TK:
        print("Error: Tkinter is not available in this Python installation. Use --take 1 or --sync for CLI mode.")
        sys.exit(1)

    root = tk.Tk()
    app = HarvesterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
