# CR – Course Overview and Data Setup (3 items)

Source: Certification Review player (id=238), text mode (Alt+W, video hidden → transcript shown). Captured 2026-10-28. Paraphrased; short quotes in quotation marks.

## 1. Course Overview (video 2:07, transcript read)
- Motivation for certification (cites a MONEY/Payscale.com study: SAS skills linked to an average pay boost "of over 6%").
- Two goals of the course: (1) apply the skills from SAS Programming 1 and 2 to realistic problems following the programming process (access → explore/validate → prepare → analyze/report → export); (2) thorough review for the Base Programming exam, showing what to expect and giving many sample questions in the exam's styles: multiple choice, short answer, and applied questions that require writing SAS code.

## 2. About the Exam (video 3:30, transcript read)
- Three SAS programming certification levels: Certified Associate, Certified Specialist, Certified Professional. This course reviews concepts for Associate and Specialist.
- **Associate exam:** for programmers with less than ~3 months experience; multiple choice only; no code writing; no access to SAS software or documentation.
- **Specialist (performance-based) exam:** for ~3–6 months experience; multiple choice + short answer, and some questions require writing code to get the answer; SAS and SAS documentation available throughout. This course targets "SAS Certified Specialist: Base Programming Using SAS 9.4".
- Administered by SAS and Pearson VUE, on a computer, at a test center or via online proctoring.
- **About 45** multiple choice and short answer questions. About half can be answered just by reading the information given; the others require writing or editing SAS code.
- **135 minutes.** Passing score **725** on a 200–1000 scale. The narrator says to check the exam web page because these numbers can change.
- You choose the interface: SAS Studio, SAS Enterprise Guide 7 or 8, or the SAS windowing environment. No questions about the interfaces themselves. SAS is provided by the exam platform. SAS online documentation is available; no other online resources.
- **Question types:**
  - Multiple choice: usually up to four options, always exactly one correct; all info is in the question (no code needed), though you may use SAS — mind the time.
  - Short answer: usually type a number or a single word.
  - Programming: write or edit a program meeting several requirements (example given: create a table, filter rows, compute a new column, sort — via DATA step + PROC SORT or an SQL query). Programs are not graded; you then answer a few MC/short-answer questions about the results.
- Programming 1 and 2 cover both exams' topics; read the official Exam Content Guide to find gaps and topics taught but not tested. Example: the exam has **no specific SQL questions**, but you may use PROC SQL in programming questions.
- Registration: SAS Global Certification Program site → Foundation Tools (Associate and Base Programming Specialist credentials); site also covers exam-day rules and online proctoring.

## 3. Setting Up Data for Practices (text page + pop-ups)
Options: Hands-On Lab (files preloaded), SAS OnDemand for Academics, SAS Viya for Learners, or your own SAS (SAS Studio / SAS Windowing Environment).
- **Lab:** launch lab → SAS Studio → Files and Folders: `S:\ > workshop > ECRBM6` → open `libname.sas`, run (F3) to create the **CR** library; must re-run each time the lab starts. Refresh: "Refresh Data" in the lab block (overwrites all course files) or run `refreshData.sas` in ECRBM6 (recreates only the SAS tables).
- **SAS OnDemand for Academics (SAS Studio):** sign in/register; extract the zip → folder `ECRBM6` with one program `createdataCRB_oda.sas`; in SAS Studio create folder `ECRBM6` (uppercase exactly) under Files (Home), upload the program, open and run it; it creates all course data and lists the tables in Results. ECRBM6 should then contain subfolders `data`, `output`, `programs`.

## Gaps
- Pop-ups for SAS Viya for Learners, own SAS Studio, and SAS Windowing Environment were opened but not transcribed (setup only; not exam content).
- Zip download link not followed.
