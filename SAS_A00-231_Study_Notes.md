# SAS 9.4 Base Programming (A00-231) – Study Notes

Source: SAS Programming Learning Subscription (learn.sas.com), SAS9.4v2, English.
Content is paraphrased from the course unless labeled **[Supplementary – not from course]**. Uncertain details are marked **[VERIFY]**.

---

## Progress

| # | Course – Lesson | Status | Notes / open gaps |
|---|---|---|---|
| 0 | P1 – Course Overview & Data Setup | ✅ Done | Setup pop-ups (environment install steps) skipped – not exam content |
| 1 | P1 – L1 Essentials | ✅ Done (backfilled) | — |
| 2 | P1 – L2 Accessing Data | ✅ Done | Demo "Exploring Automatic SAS Libraries" video-only → supplementary note added |
| 3 | P1 – L3 Exploring and Validating Data | ✅ Done | No gaps (all 27 pages + 10 practices + review + quiz questions read) |
| 4 | P1 – L4 Preparing Data | ⏳ Next | |
| 5 | P1 – L5 Analyzing and Reporting on Data | ☐ | |
| 6 | P1 – L6 Exporting Results | ☐ | |
| 7 | P1 – L7 Using SQL in SAS | ☐ | |
| 8 | P2 – L1 Controlling DATA Step Processing | ☐ | |
| 9 | P2 – L2 Summarizing Data | ☐ | |
| 10 | P2 – L3 Manipulating Data with Functions | ☐ | |
| 11 | P2 – L4 Creating Custom Formats | ☐ | |
| 12 | P2 – L5 Combining Tables | ☐ | |
| 13 | P2 – L6 Processing Repetitive Code | ☐ | |
| 14 | P2 – L7 Restructuring Tables | ☐ | |
| — | Final Deliverables | ☐ | |

Quizzes: questions are **read only** (never answered/submitted); summarized under "Quiz insights".

---

## SAS® Programming 1 – Course Overview + Lesson 1: Essentials

**Exam domain:** D3 (primary) · D1 (program structure) · light D4 (TITLE)

### Key concepts
- **Programming process (course framework):** access → explore → prepare → analyze/report → export. Course data: international storm data (Storm.xlsx: Storm_Summary [wind MPH], Storm_Detail [6-hourly, knots], Storm_Damage [US storms > $1B], Storm_Range [Wind1–Wind4], Storm_2017, lookup sheets Basin_Codes/SubBasin_Codes/Type_Codes). The intro demo exposes dirty data on purpose (a lowercase basin code; MinPressure = -9999).
- **Interfaces:** SAS windowing environment (part of SAS), Enterprise Guide (PC client → local/remote server), SAS Studio (browser → server). All provide an editor, a **log**, and results/output data. SAS Studio tabs: Code, Log, Results, Output Data.
- **Running code:** Run / F3. Highlight a selection to run only that part (EG: Run ▸ Run Selection).
  - In **SAS Studio and EG**, rerunning **replaces** the log, results, and output data.
  - In the **SAS windowing environment**, rerunning **appends** to the log and results. (Lesson Review)
- **Program structure:** a program = sequence of **steps**; only two kinds: **DATA** and **PROC**. Steps = statements; most statements begin with a keyword; **every statement ends with `;`**. DATA step = read/process data → create a table (also filter, compute, join). PROC step = predefined processing (reports, graphs, stats). Most steps end with `RUN;`, a few PROCs with `QUIT;`. Missing RUN → the next DATA/PROC boundary ends the previous step. **Global statements** (`TITLE`, `FOOTNOTE`, `OPTIONS`, `LIBNAME`) live outside steps and need no RUN.
- **Syntax rules:** free format (spacing/line breaks irrelevant; several statements per line OK); unquoted names/keywords are case-insensitive; Format Code (Studio icon; EG Edit ▸ Format Code / Ctrl+I).
- **Comments:** `* … ;` hides one statement (up to its semicolon); `/* … */` hides any block (Ctrl+/ in Studio).
- **Syntax errors:** misspelled keywords, unmatched quotes, missing semicolons, invalid options → WARNING or ERROR in the log. Color coding helps (keywords bold blue). Read the log top-down; if an underlined word is valid, look **immediately before** it.
- **Practice "Exploring SAS Studio" (backfilled):** Studio = navigation pane + work area; use the SAS Programmer perspective; autocomplete prompts list valid keywords/options (toggle via Preferences ▸ Code and Log; Ctrl+Space shows it on demand); a DATA step alone produces Log + Output Data but an **empty Results tab** (no report); results can be opened as HTML/PDF/Word; Save As adds `.sas` automatically.

### Must-know syntax
| Syntax | What it does / default |
|---|---|
| `data out; set in; run;` | DATA step: read `in` row by row, write `out`. |
| `proc print data=tbl; run;` | List rows/columns. Without DATA= → most recently created table. |
| `var c1 c2;` | PRINT: columns + order. MEANS: numeric analysis columns. |
| `where expr;` | Filter rows (PROC or DATA step). |
| `proc means data=t mean min max maxdec=1;` | Summary stats; keywords choose stats; MAXDEC= decimals. No keywords → N, Mean, Std Dev, Min, Max. |
| `class col;` | MEANS: statistics per value of `col`. |
| `title "t";` / `footnote "f";` / `title;` | Global; persists until replaced; `title;` clears. |
| `new = expr;` | Assignment statement (no leading keyword). |

### Code examples
```sas
title "Teen Students";                 /* global, no RUN                  */
data teens;                            /* DATA step                       */
    set sashelp.class;
    where Age >= 13;
    BMI = Weight / Height**2 * 703;    /* assignment: no keyword          */
run;
proc print data=teens; var Name Age BMI; run;      /* 3 statements       */
proc means data=teens mean max maxdec=2; var BMI; class Sex; run;
title;                                 /* clear title                     */
```
```sas
*proc print data=teens; run;   /* only PROC PRINT stmt hidden; RUN; still there */
/* proc print data=teens;
   run; */                     /* both hidden                                    */
```

### Common errors & log messages
| Faulty code | Log behaviour | Fix |
|---|---|---|
| `daat mycars;` | **WARNING** – SAS assumes DATA was misspelled; **step runs**. (`WARNING 14-169: Assuming the symbol DATA was misspelled as daat.` [VERIFY number]) | Fix spelling. |
| `proc print data=x` (no `;`) then `var …;` | `VAR` underlined: "Syntax error, expecting one of the following: ;, …"; VAR read as an invalid PROC PRINT option → **step not run**. (`ERROR 22-322` / `ERROR 76-322` [VERIFY]; `NOTE: The SAS System stopped processing this step because of errors.`) | Add `;` before the underlined word. |
| `proc means … average …` | `average` underlined; error lists valid options; **step not run** (`ERROR 22-322` + `ERROR 202-322` [VERIFY]). | Use `MEAN`. |
| `where region="Canada;` | Unbalanced quote: rest of program shows as string color; later statements misparsed. Format Code exposes it. | Close the quote. |

### Exam traps
1. Misspelled keyword = WARNING & still runs; missing `;`/invalid option = ERROR & that step skipped (other steps still run).
2. Underlined valid keyword → the bug is just before it (usually `;`).
3. Counting statements: RUN counts; assignment counts; comments are **not** statements; global statements are not part of steps.
4. TITLE/FOOTNOTE persist until changed/cleared.
5. `*` comment ends at the first `;` — a `;` inside a `/* */` comment is harmless.
6. Unquoted names any case; quoted values case-sensitive. Table names are not case-sensitive (`NATIONAL` = `national`).
7. Rerun in Studio/EG replaces output; windowing environment appends.

### Quiz insights (Lesson 1 quiz – 10 questions, read only)
- **Counting steps vs. statements:** two questions give a short program and ask for the number of steps or statements. One mixes a `*` comment line, TITLE and FOOTNOTE global statements, and a PROC PRINT with WHERE/VAR split across lines → you must know comments don't count, globals do count as statements, and a statement spanning lines is still one statement.
- **What a run produces:** log, output data, results.
- **Syntax requirements:** only the semicolon rule is mandatory; distractors are column-1 starts, one statement per line, blank lines between steps.
- **DATA vs PROC roles:** which step type generates reports/graphs (distractors include RUN and a PROC name).
- **Block comment containing a `;`** across several lines — tests that `/* */` can span lines and may contain semicolons.
- **Missing semicolon** at the end of PROC PRINT before RUN — predict log vs. report vs. table creation.
- **Misspelled `porc`** (PROC) — tests whether SAS auto-corrects a misspelled PROC keyword the way it did for DAAT; do not assume every misspelling is forgiven. [VERIFY by running: expect `ERROR 180-322: Statement is not valid or it is used out of proper order.`]
- **Case of table names** (`national` vs `NATIONAL`) — tests case-insensitivity of names.
- **Interface identification:** a made-up product name mixed with EG, Studio, windowing environment.

### Self-check
1. How many steps / statements in the PROC step?
```sas
options nodate;
data a; set sashelp.class; Ratio = Height/Weight; run;
title "Ratios";
proc print data=a; var Name Ratio; where Age > 12; run;
```
A) 2; 4 B) 2; 5 C) 4; 4 D) 3; 4
2. Predict: `data shoes; set sashelp.shoes; run; proc print data=shoes  var Region Sales; run;`
A) WARNING, report prints B) ERROR; PROC PRINT not run, `shoes` created C) neither step runs D) no issue
3. Which prints with **no** title? A) `title "A"; proc print…` B) `title "A"; *title; proc print…` C) `title "A"; title; proc print…` D) `*title "A"; title "B"; proc print…`

### Gaps
- Lesson quiz answers deliberately not recorded (read-only).
- Demo: The SAS Programming Process – a few long lines clipped at the right edge (no syntax impact).

### Answers
1. **A** – DATA + PROC PRINT; PRINT has PROC PRINT, VAR, WHERE, RUN. OPTIONS/TITLE are global.
2. **B** – missing `;` makes `var` an invalid option; DATA step already ran.
3. **C** – `title;` clears; `*title;` is a comment.

---

## SAS® Programming 1 – Lesson 2: Accessing Data

**Exam domain:** D1 (primary) · D3 (import/library notes)

### Key concepts
- **Structured** data (SAS tables, Access, Oracle/Teradata, Hadoop) → read directly via an **engine**. **Unstructured** data (text, CSV, tab-delimited, JSON, weblogs) → must be **imported** first.
- **SAS table** (`.sas7bdat`) = **descriptor portion** (metadata: name, row count, created/modified date, column names & attributes) + **data portion** (values). Table = data set, column = variable, row = observation.
- **Three required column attributes:** name, type, length.
  - Name: 1–32 chars, start with letter/underscore, then letters/digits/underscores; stored in the case first used, referenced in any case.
  - Type: character or numeric. Numeric values: digits, minus sign, one decimal point, E notation. Character: letters, digits, special chars, blanks.
  - **SAS date = numeric**, days since **01JAN1960** (earlier dates negative). Dates are not a third type.
  - Length: numeric **8 bytes** default (~16 significant digits); character 1–32,767 bytes (1 byte = 1 char).
  - Missing: character = **blank**, numeric = **period (.)**.
- **Libraries:** location + data type behind a **libref**; use `libref.table` (no extension). Active until cleared or session ends; clearing never deletes data. **Work** = temporary, default library. **Sashelp** = sample tables. Admin-defined libraries may already exist.
- **XLSX engine:** needs SAS/ACCESS to PC Files; each worksheet (or named range) = a table; always reads **current** workbook data; Excel dates converted to SAS dates; close the workbook before connecting.
- **PROC IMPORT:** makes a **snapshot** SAS table (refreshed only by rerunning). Column names from row 1, data from row 2; type/length guessed from first **20** rows (GUESSINGROWS=); Excel: one sheet per run, first sheet unless SHEET=.

### Must-know syntax
| Syntax | What it does / default |
|---|---|
| `proc contents data=lib.tbl; run;` | Descriptor portion report; "Alphabetic List of Variables and Attributes" (#, name, type, length). DATA= can also be a quoted physical path. |
| `libname lib base "path";` | Global. Libref ≤ **8** chars, letter/underscore first. **BASE** default engine (optional). Path relative to where SAS runs. |
| `libname xl xlsx "path/file.xlsx";` | Excel workbook as a library (full file name + extension). |
| `libname lib clear;` | Deassign libref (keyword is CLEAR). |
| `options validvarname=v7;` | Force SAS naming on Excel names: spaces/specials → `_`, truncate >32 chars. |
| `proc import datafile="f" dbms=csv out=tbl replace; run;` | DATAFILE= full path/name; DBMS= CSV/TAB/DLM/XLSX; OUT= table; REPLACE overwrite. |
| `guessingrows=n\|max;` | Separate statement; default 20; range 1–2147483647 or MAX. |
| `sheet=name;` | Separate statement (DBMS=XLSX). |
| `delimiter="\|";` | Separate statement with DBMS=DLM. |

### Code examples
```sas
libname pg1 "s:/workshop/data";               /* BASE engine implied   */
options validvarname=v7;
libname xlstorm xlsx "s:/workshop/data/storm.xlsx";
proc contents data=xlstorm.storm_summary; run; /* worksheet = table    */
libname xlstorm clear;
```
```sas
proc import datafile="s:/workshop/data/np_traffic.csv"
            dbms=csv out=work.traffic replace;  /* options on PROC stmt */
    guessingrows=max;                           /* own statement        */
run;
```
```sas
proc import datafile="s:/workshop/data/np_traffic.dat"
            dbms=dlm out=traffic2 replace;
    delimiter="|";
    guessingrows=3000;
run;
```

### Common errors & log messages
| Situation | Log | Fix |
|---|---|---|
| LIBNAME OK | `NOTE: Libref PG1 was successfully assigned as follows:` + Engine + Physical Name | — |
| Re-import without REPLACE | **NOTE** (not ERROR): import cancelled, output table already exists, specify REPLACE. (`NOTE: Import cancelled. Output dataset WORK.X already exists. Specify REPLACE option to overwrite it.` [VERIFY wording]) | Add `replace`. |
| Truncated imported values | No message (length guessed from 20 rows) | `guessingrows=max;` |
| Libref > 8 chars / starts with digit | ERROR, libref not assigned [VERIFY wording] | Valid libref. |
| Table not found | `ERROR: File WORK.XYZ.DATA does not exist.` [VERIFY – not shown in lesson] | Check libref/table. |
| Excel names keep spaces in Studio | none – Studio wrapper resets VALIDVARNAME to ANY unless OPTIONS is submitted in the same run | Submit OPTIONS with the step / set preference to V7. |

### Exam traps
1. Libref ≤ 8 chars; column/table names ≤ 32 chars; both start with letter or `_`.
2. Character length fixed at creation → longer values truncated silently (Basin length 2: "East Pacific" → "Ea").
3. Dates are numeric; 01JAN1960 = 0.
4. Missing: blank (char) vs `.` (num) — you can infer column type from how missing values display.
5. One-level name → **Work** → gone at session end.
6. DATAFILE= (IMPORT) vs DATA= (CONTENTS/PRINT); OUT= output.
7. REPLACE/DBMS= are PROC IMPORT statement options; GUESSINGROWS=/SHEET=/DELIMITER= are statements.
8. XLSX engine = live; PROC IMPORT = snapshot. DBMS=CSV is in Base SAS; XLSX needs SAS/ACCESS to PC Files.
9. Deassign with **CLEAR** (not a made-up keyword like "UNASSIGN").

### [Supplementary – not from course] Automatic libraries: WORK vs SASHELP vs SASUSER
*(Replaces the video-only demo "Exploring Automatic SAS Libraries"; general SAS 9.4 knowledge.)*
- **WORK** – created fresh for every SAS session; **temporary**: all tables in it are deleted when the session ends. It is the **default library**: a one-level name such as `data=test` or `data test;` means `work.test`.
- **SASHELP** – SAS-supplied sample tables (e.g., `sashelp.class`, `sashelp.cars`, `sashelp.shoes`) and session metadata views (e.g., `sashelp.vtable`). Read-only for typical users; always available at session start.
- **SASUSER** – a permanent, per-user library for personal settings/profiles (and, in some installs, user-saved items). Often read-only in shared server environments such as SAS Studio. Not where you should normally store project data.
- Exam angles: a table written without a libref will not survive a restart; `sashelp.*` tables are available immediately in a new session; a user-defined libref must be re-submitted each new session (unless assigned automatically by an admin/autoexec).

### Quiz insights (Lesson 2 quiz – 10 questions, read only)
- **Default numeric length** read from a PROC CONTENTS listing (a date column typed Num) — reinforces 8 bytes and that dates are numeric.
- **LIBNAME syntax validity:** quoted path required; libref cannot start with a digit.
- **What exists at the start of a new session:** a one-level (Work) table vs. a Work table created earlier vs. a Sashelp table → only automatic-library content survives.
- **Infer column type from a listing** where a missing value shows as `.` and values are right-aligned → numeric.
- **SAS dates "false statement" question:** trap is the claim that *date* is a third column type.
- **XLSX LIBNAME syntax:** the engine keyword is required and the path must include the `.xlsx` file name.
- **Valid libref** among options with a leading digit, a slash, and one that is 9 characters with an underscore → tests the 8-character limit precisely.
- **Deassigning a libref:** distractor uses a non-existent keyword; correct keyword is CLEAR.
- **What PROC IMPORT does:** creates a Work table once (snapshot); distractors claim auto-refresh or a "CSV engine" reading directly.
- **Descriptor vs data portion:** table name, column type, creation date all live in the descriptor portion.

### Self-check
1. Which LIBNAME fails? A) `libname _sales "c:/data";` B) `libname sales2024 "c:/data";` C) `libname s24 base "c:/data";` D) `libname xl xlsx "c:/data/f.xlsx";`
2. `City` values are 5 chars in rows 1–20; row 300 is "Albuquerque". `proc import … dbms=csv out=cities replace; run;` → A) ERROR B) row 300 stored as "Albuq" C) length auto 11 D) row dropped
3. Same PROC IMPORT run twice without REPLACE after editing the CSV → A) edited data B) original data + NOTE "import cancelled" C) no table + ERROR D) duplicates

### Gaps
- Demo "Exploring Automatic SAS Libraries" (3:08): video-only in text mode → covered by supplementary note above.
- In-lesson "Question" (valid column names): read, not checked.

### Answers
1. **B** – 9 characters.
2. **B** – guessed length 5; silent truncation.
3. **B** – NOTE, old table kept.

---

## SAS® Programming 1 – Lesson 3: Exploring and Validating Data

**Exam domain:** D2 (filtering, sorting, de-duplication) · D4 (PRINT/MEANS/FREQ/UNIVARIATE, formats) · D3 (WHERE/macro-quote pitfalls)

### Key concepts
- **Exploration procs (defaults matter):**
  - **PROC PRINT** – all rows & columns; `(OBS=n)` data set option limits rows; VAR limits/orders columns.
  - **PROC MEANS** – every numeric column; default stats **N, Mean, Std Dev, Minimum, Maximum**. Different N across columns ⇒ missing values. Min/Max reveal invalid values (e.g., MinPressure = -9999).
  - **PROC UNIVARIATE** – MEANS-like stats plus distribution detail and an **Extreme Observations** table (5 lowest + 5 highest, with observation numbers). `NEXTROBS=n` changes the count (Challenge).
  - **PROC FREQ** – a one-way table for **every** column by default (Frequency, Percent, Cumulative Frequency, Cumulative Percent). TABLES limits columns. Reveals case inconsistencies/miscodes (e.g., `NA` vs `na`, `PRE` vs `PRESERVE`). `ORDER=FREQ` sorts by descending count (activity).
- **WHERE statement** (works in PRINT, MEANS, FREQ, UNIVARIATE, SORT, and others): row is read if expression is true.
  - Character constants: **quoted, case-sensitive**. Numeric constants: unquoted, digits/decimal/minus only — **no commas or `$`**.
  - **Date constant:** `"ddmmmyyyy"d` (1–2 digit day, 3-letter month any case, 2- or 4-digit year), converted to the SAS date number.
  - Compound: AND / OR; NOT reverses an operator.
  - **Missing numeric values are the smallest possible value** → `MinPressure < 920` also selects missing rows; exclude them with `0 < MinPressure < 920` (or add `is not missing`).
- **Special WHERE operators:** `IN (list)` / `NOT IN` (values separated by commas **or** spaces); `IS MISSING` / `IS NOT MISSING` (char or num); `IS NULL`; `BETWEEN a AND b` (**inclusive**); `LIKE` with `%` = any number of chars, `_` = exactly one char; `=*` sounds-like (Lesson Review).
- **Macro variables:** `%LET name=value;` stores **text** (no quotes needed; quotes would become part of the value). Reference with `&name`. Inside quotes, use **double quotes** — single quotes prevent resolution. Values are case-sensitive once substituted into a WHERE.
- **Formats** change how values **display**, never the stored value. Syntax `<$>name<w>.<d>` — `$` = character format, `w` = total width (incl. symbols/decimals), the **period is required**. Format statement inside a PROC is temporary for that step.
  - Numeric: `w.d` rounds (5. → 12346; 8.1 → 12345.7), `COMMAw.d`, `DOLLARw.d`, `YENw.d`, `EUROXw.d` (swaps `.`/`,`; symbols only, no currency conversion), `Zw.d` (leading zeros: Z8. → 00001350).
  - Date (value 21199 = 15JAN2018): `DATE7.` 15JAN18, `DATE9.` 15JAN2018, `DATE11.` 15-JAN-2018, `MMDDYY10.` 01/15/2018, `MMDDYY8.` 01/15/18, `MMDDYY6.` 011518, `DDMMYY8.` 15/01/18, `MONYY7.` JAN2018, `MONNAME.` January, `WEEKDATE.` Monday, January 15, 2018.
  - **Too-narrow width:** DOLLAR drops commas, then switches to scientific notation; MMDDYY drops the slashes.
  - **Formats group values in procedures:** FREQ on StartDate with MONNAME. → 12 rows (one per month).
- **PROC SORT:** sorts by BY columns (ascending default; `DESCENDING` goes **before each** column it applies to). Without `OUT=` the **input table is replaced** by the sorted version. No printed output. BY statement is **required**.
  - `NODUPKEY` keeps only the **first** row per unique BY-key value; with `BY _ALL_` it removes **entirely duplicated adjacent** rows. `DUPOUT=` captures the removed rows. Order matters: which row is "first" depends on the incoming order.
- **ODS TRACE ON/OFF** writes output-object names to the log; **ODS SELECT name;** keeps only that object (e.g., `ExtremeObs` for UNIVARIATE). (Challenge practice)
- **KEEP= data set option** on the input table reads only listed columns (Challenge preview).

### Must-know syntax
| Syntax | What it does / default |
|---|---|
| `proc print data=t(obs=10); var a b; run;` | OBS= data set option (in parentheses after the table). |
| `proc means data=t; var x y; run;` | Defaults: N Mean StdDev Min Max; numeric VAR only. |
| `proc univariate data=t nextrobs=10; var x; run;` | Extreme Observations (default 5). |
| `proc freq data=t order=freq; tables a b; run;` | One-way tables; ORDER=FREQ by count. |
| `where x in ("A","B");` / `where x in ("A" "B");` | List match; NOT IN to exclude. |
| `where d >= "01jan2010"d;` | Date constant. |
| `where c like "New%";` / `like "Sant_ %"` | Pattern match. |
| `where x between 20 and 39;` | Inclusive range. |
| `where x is missing;` / `is not missing` | Missing test (num & char). |
| `%let v=Wagon;` → `where Type="&v";` | Macro variable; double quotes. |
| `format d mmddyy10. amt dollar16.;` | Temporary display format in a PROC. |
| `proc sort data=in out=o nodupkey dupout=d; by _all_; run;` | Sort + de-duplicate. |
| `by Reg descending DayVisits;` | Reg asc, DayVisits desc. |
| `ods trace on; … ods trace off;` / `ods select extremeobs;` | Find / select output objects. |
| `where upcase(Location) like '%MAIN ENTRANCE%';` | Case-insensitive compare (data unchanged). |

### Code examples
```sas
/* 1. Validate: missing + invalid values */
proc means data=pg1.storm_summary;          /* N differs → missing values  */
    var MaxWindMPH MinPressure;
run;
proc freq data=pg1.storm_summary order=freq;
    tables Basin Type;                       /* spot "NA" vs "na"           */
run;
```
```sas
/* 2. WHERE + macro variables (note double quotes and the date constant) */
%let BasinCode=NA;
%let Date=01JAN2000;
proc print data=pg1.storm_summary;
    where Basin="&BasinCode" and StartDate>="&Date"d
          and 0 < MinPressure < 920;         /* excludes missing pressure   */
    format StartDate date9.;
run;
```
```sas
/* 3. One row per storm, keep min pressure, log removed duplicates */
proc sort data=pg1.storm_detail out=storm_clean nodupkey dupout=storm_dups;
    by _all_;                                /* drop exact duplicate rows   */
run;
proc sort data=storm_clean out=min_pressure;
    where Pressure is not missing and Name is not missing;
    by descending Season Basin Name Pressure;
run;
proc sort data=min_pressure nodupkey;        /* no OUT= → overwrites input  */
    by descending Season Basin Name;         /* first row = min Pressure    */
run;
```

### Common errors & log messages
| Situation | Log | Fix |
|---|---|---|
| WHERE in a PROC | `NOTE: There were n observations read from the data set X. WHERE …;` — the course uses this note to count matching rows. [VERIFY exact wording] | — |
| Macro ref in **single** quotes `where Basin='&BasinCode';` | No error; FREQ produced no report — log note says no observations were selected (literal `&BasinCode` compared). [VERIFY: `NOTE: No observations were selected from data set …`] | Use double quotes. |
| `like "%Preserve%"` in double quotes | **WARNING** in the log (the `%P…` is treated as a macro call attempt) — practice note says switch to single quotes. [VERIFY: `WARNING: Apparent invocation of macro PRESERVE not resolved.`] | `like '%Preserve%'`. |
| Numeric constant with symbols `where amt <= $5,000;` | Syntax error [VERIFY message] | `where amt <= 5000;` |
| `proc sort data=t;` with no BY | ERROR – BY statement required [VERIFY wording] | Add BY. |
| Format without period `format d date9;` | Interpreted as a variable name, not a format [VERIFY behaviour] | `date9.` |
| Too-narrow format width | No error; values shown without commas/slashes or in E-notation (or `*`) | Widen `w`. |

### Exam traps
1. **Missing < any number** in comparisons → `x < value` selects missing rows.
2. `BETWEEN` is inclusive; `LIKE "_"` = exactly one character; `%` = zero or more.
3. Character compare is case-sensitive; `UPCASE()` in WHERE doesn't change the data.
4. `%LET` values: no quotes; reference inside **double** quotes; `&` is not used on the left side of `%LET`.
5. **PROC SORT without OUT= overwrites the input** — row count may shrink permanently with NODUPKEY.
6. NODUPKEY keeps the first occurrence — results depend on prior order; `BY _ALL_` only removes **adjacent exact** duplicates (sorting by all columns makes them adjacent).
7. DESCENDING applies only to the **one** column that follows it.
8. Format width counts every character (`$`, commas, decimal point). Period is mandatory; `$` prefix for character formats.
9. Formats in PROC FREQ group values (month names, etc.) without changing data.
10. PROC MEANS VAR must be numeric; FREQ uses TABLES (not VAR).
11. IN list allows commas or spaces; character items need quotes.

### Quiz insights (Lesson 3 quiz – 10 questions, read only)
- **PROC SORT with NODUPKEY and no OUT=** on a small table with repeated IDs → predict row count; tests that the input is overwritten and only one row per BY value survives (exact-duplicate vs key-duplicate distinction).
- **Identify the FORMAT statement from output** showing `11JAN07` and `01/11/07` → must map DATE7. vs DATE9. and MMDDYY8. widths to displayed text.
- **Period delimiter is required** in a format name (true/false).
- **LIKE "Sales%"** against values where "Sales" appears at the start vs. in the middle → `%` after the text anchors the match at the beginning.
- **PROC SORT statement with a stray semicolon** after `DATA=` (OUT= on its own line) → spot the syntax error; distractors about overwriting, descending scope, and BY-only columns.
- **IN operator syntax:** distractors repeat `=` with OR, use OR inside IN, or omit quotes; correct form = quoted values in parentheses.
- **Operator equivalence:** symbol vs mnemonic (`<=` / `LE`, `=` / `EQ`) — all forms are valid.
- **%LET syntax:** distractors put quotes in the value or `&` on the macro name.
- **Which statement lists numeric analysis columns in PROC MEANS** (VAR vs TABLES/VARS/KEEP=).
- **Which proc gives distinct values with counts and percents** → FREQ.

### Self-check
1. `MinPressure` has values 915, 930, and missing. How many rows does `where MinPressure < 920;` return? A) 1 B) 2 C) 3 D) 0
2. Predict:
```sas
%let t=SUV;
proc print data=sashelp.cars; where Type='&t'; run;
```
A) SUV rows B) ERROR C) 0 rows, NOTE in log D) WARNING, all rows
3. `proc sort data=work.sales nodupkey; by Region; run;` — Region has 4 distinct values over 100 rows. Afterward `work.sales` has: A) 100 rows sorted B) 4 rows C) 96 rows D) unchanged; output in a new table

### Gaps
- None. (Try-it page links to external SAS documentation – not followed; course content captured.)

### Answers
1. **B** – 915 and the missing value (missing is smaller than any number).
2. **C** – single quotes stop macro resolution; literal `&t` matches nothing.
3. **B** – no OUT= overwrites the input; NODUPKEY keeps the first row per Region.

---
