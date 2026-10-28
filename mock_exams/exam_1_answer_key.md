# Mock Exam 1 – Answer Key

Domain counts: D1 10 · D2 16 · D3 8 · D4 9

---

## Question 1

- **Answer:** A. It generally reads data from an input source, processes it, and creates a SAS table.
- **Domain:** D1 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 6/13 SAS Program Structure

**Worked solution (two independent passes):**

```text
The course defines a DATA step as one that "generally reads data from an input source, processes it, and creates a SAS table" (it may also filter rows, compute columns, join tables).
Pass 2: re-read the PROC definition on the same page – PROCs process a SAS table in a predefined way – confirming A is the DATA step and B the PROC step.
```

**Why the other options are wrong:**

- **B.** This is the course definition of a PROC step, not a DATA step.
- **C.** Global statements (TITLE, OPTIONS, LIBNAME) are outside steps; a DATA step is a step.
- **D.** Most steps end with RUN; only a few PROC steps end with QUIT.

---

## Question 2

- **Answer:** 3
- **Domain:** D2 · **Difficulty:** medium · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 6/13 (DATA step adds a column), Page 11/13 Activity (WHERE in a DATA step)

**Worked solution (two independent passes):**

```text
Pass 1 – scan Dept for "IT":
Row  EmpID Dept   Salary Bonus  Salary+Bonus
1    E01   Sales  52000  3000   55000
2    E02   Sales  48000  2000   50000
3    E03   IT     61000  4000   65000
4    E04   IT     57000  1000   58000
5    E05   HR     45000  2500   47500
6    E06   Sales  50000  5000   55000
7    E07   IT     65000  3000   68000
8    E08   HR     47000  1500   48500
Rows with Dept=IT: E03, E04, E07 → 3 rows.
Pass 2 – count by department: Sales = E01,E02,E06 (3); HR = E05,E08 (2); IT = 8−3−2 = 3. ✔
```

**Reference solution code:**

```sas
data itstaff;
    set staff;
    where Dept="IT";
    Total=Salary+Bonus;
run;
```

---

## Question 3

- **Answer:** A. A WARNING says SAS assumed DATA was misspelled; the step runs and work.cars2 is created.
- **Domain:** D3 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 10/13 Demo: Finding and Resolving Syntax Errors

**Worked solution (two independent passes):**

```text
In the demo, DAAT produced a warning: SAS assumed DATA was simply misspelled and "goes ahead and successfully runs the DATA step".
Pass 2: the demo contrasts this with the missing-semicolon and invalid-option errors, where the step "did not run" – so only the misspelled DATA keyword is forgiven with a WARNING. ✔
```

**Why the other options are wrong:**

- **B.** That is what happens for the missing semicolon / invalid option cases, not for DAAT.
- **C.** A WARNING is written to the log; it is not silent.
- **D.** Errors stop only the step that contains them, not later steps.

---

## Question 4

- **Answer:** B. The first PROC PRINT report and the PROC MEANS report
- **Domain:** D4 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 6/13 (global statements define a setting for the session, no RUN), Page 9/13 (title; at end of program)

**Worked solution (two independent passes):**

```text
TITLE is a global statement that defines a setting for the SAS session and needs no RUN, so it applies to every report until changed. The null statement `title;` clears it, as at the end of the demo programs.
Trace: PRINT #1 → title on; MEANS → title still on; `title;` clears; PRINT #2 → no title.
Pass 2: count reports produced after TITLE and before `title;` = 2 (PRINT, MEANS). ✔
```

**Why the other options are wrong:**

- **A.** The title is not reset after the first step; it stays in effect.
- **C.** `title;` clears the title before the last PROC PRINT.
- **D.** Global statements do not need a RUN statement.

---

## Question 5

- **Answer:** 3
- **Domain:** D1 · **Difficulty:** medium · **Type:** Short answer
- **Source:** P1_L01_essentials.md – Page 6/13 SAS Program Structure

**Worked solution (two independent passes):**

```text
Steps are DATA or PROC steps only: DATA work.temps, PROC PRINT, PROC MEANS = 3. OPTIONS and TITLE are global statements, not steps. PROC PRINT has no RUN, but "the beginning of a new DATA or PROC step signals the end of the previous step".
Pass 2: count the keywords that begin a step (DATA, PROC, PROC) = 3. ✔
```

---

## Question 6

- **Answer:** 3
- **Domain:** D2 · **Difficulty:** medium · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 9/13 (AvgMPG=mean(...)), Page 6/13 (heightcm=height*2.54), Page 8/13 (where Age<13)

**Worked solution (two independent passes):**

```text
Pass 1 – test Test1 > 79 per row: Ana 80 yes; Ben 72 no; Cy 95 yes; Dee 60 no; Eli 88 yes; Fay 79 no (79 is not greater than 79) → 3.
Pass 2 – rows failing: Ben, Dee, Fay = 3 of 6 → 6−3 = 3. ✔
Trap: using >= would include Fay (4 rows).
```

**Reference solution code:**

```sas
data scores2;
    set scores;
    where Test1 > 79;
    Avg=mean(Test1, Test2);
    HeightCm=HeightIn*2.54;
run;
```

---

## Question 7

- **Answer:** B. The DATA step runs and work.orders2 is created, but neither PROC PRINT nor PROC MEANS produces a report.
- **Domain:** D3 · **Difficulty:** hard · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 10/13 Demo: Finding and Resolving Syntax Errors (same three error types)

**Worked solution (two independent passes):**

```text
Three errors, each handled as in the demo:
1. `daat` → WARNING, SAS assumes DATA and runs the step → orders2 created.
2. PROC PRINT statement has no semicolon → VAR read as an invalid option → step not processed → no PRINT report.
3. `average` is not a valid PROC MEANS option → ERROR → step does not run → no MEANS report.
Pass 2: map each step to the demo outcome (DATA: ran; PRINT: did not run; MEANS: did not run) → B. ✔
```

**Why the other options are wrong:**

- **A.** The missing semicolon and invalid option are ERRORs and those steps do not run.
- **C.** Errors stop only their own step; the DATA step ran (DAAT is only a warning).
- **D.** The missing semicolon after data=orders2 stops PROC PRINT too.

---

## Question 8

- **Answer:** C. Miles=Km*0.621;
- **Domain:** D2 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 6/13 SAS Program Structure

**Worked solution (two independent passes):**

```text
The course: "The assignment statement creates a new column and it doesn't start with a keyword." DATA, SET, RUN are keywords.
Pass 2: of the four statements only one has the form column=expression → C. ✔
```

**Why the other options are wrong:**

- **A.** DATA is a keyword; it names the output table.
- **B.** SET is a keyword; it reads the input table.
- **D.** RUN is a keyword that ends the step.

---

## Question 9

- **Answer:** 50000
- **Domain:** D4 · **Difficulty:** medium · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 5/13 Practice (PROC MEANS … mean …; var; class region;), Page 9/13

**Worked solution (two independent passes):**

```text
CLASS Dept computes the statistics separately for each Dept value.
Pass 1: Sales salaries = 52000, 48000, 50000 → sum 150000 / 3 = 50000.
Pass 2: deviations from 50000 are +2000, −2000, 0 → sum 0, so the mean is exactly 50000. ✔ (Output may show 50000.00 – same value.)
```

**Reference solution code:**

```sas
proc means data=staff mean;
    var Salary;
    class Dept;
run;
```

---

## Question 10

- **Answer:** 4
- **Domain:** D1 · **Difficulty:** medium · **Type:** Short answer
- **Source:** P1_L01_essentials.md – Page 6/13 SAS Program Structure

**Worked solution (two independent passes):**

```text
DATA statement, SET statement, assignment statement (TempF=…), RUN statement = 4 – the same structure the course counts in its own example ("This DATA step has four statements").
Pass 2: count semicolons between `data work.temps;` and `run;` inclusive = 4. ✔
```

---

## Question 11

- **Answer:** 58000
- **Domain:** D2 · **Difficulty:** easy · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 6/13 (assignment statement), Page 11/13 (Profit=Sales-Returns)

**Worked solution (two independent passes):**

```text
Pass 1: E04 Salary 57000 + Bonus 1000 = 58000.
Pass 2: E04 is Dept IT, so it is in itstaff; 58000 − 57000 = 1000 = Bonus. ✔
```

**Reference solution code:**

```sas
data itstaff;
    set staff;
    where Dept="IT";
    Total=Salary+Bonus;
run;
```

---

## Question 12

- **Answer:** B. The problem is just before VAR: the PROC PRINT statement has no semicolon, so VAR is read as an invalid option and the step is not processed.
- **Domain:** D3 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 10/13 Demo: Finding and Resolving Syntax Errors

**Worked solution (two independent passes):**

```text
Demo rule: when an underlined item is valid syntax, look immediately before it. Without the semicolon SAS treats VAR as a continuation of the PROC PRINT statement; VAR is not a valid option, and "the SAS system did not process the step".
Pass 2: VAR is used validly in the corrected demo code, so the defect must be elsewhere → the missing ; → B. ✔
```

**Why the other options are wrong:**

- **A.** VAR is valid in PROC PRINT (used in the demo solution).
- **C.** SAS does not insert semicolons; the step is not processed.
- **D.** Column names are unquoted in VAR statements.

---

## Question 13

- **Answer:** 172.72
- **Domain:** D2 · **Difficulty:** medium · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 6/13 (heightcm=height*2.54)

**Worked solution (two independent passes):**

```text
Eli: Test1 = 88 > 79 → kept. HeightCm = 68 × 2.54.
Pass 1: 68 × 2.54 = 68×2 + 68×0.54 = 136 + 36.72 = 172.72.
Pass 2: 70 × 2.54 = 177.8; minus 2 × 2.54 = 5.08 → 172.72. ✔
```

**Reference solution code:**

```sas
data scores2;
    set scores;
    where Test1 > 79;
    Avg=mean(Test1, Test2);
    HeightCm=HeightIn*2.54;
run;
proc print data=scores2;
run;
```

---

## Question 14

- **Answer:** D. VAR
- **Domain:** D1 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 6/13, Page 13/13 Lesson Review

**Worked solution (two independent passes):**

```text
The course lists TITLE, OPTIONS and LIBNAME as global statements that can sit outside steps. VAR is used inside PROC steps (PROC PRINT, PROC MEANS).
Pass 2: the Lesson Review shows exactly TITLE, OPTIONS, LIBNAME as the global examples. ✔
```

**Why the other options are wrong:**

- **A.** TITLE is listed as a global statement.
- **B.** OPTIONS is listed as a global statement.
- **C.** LIBNAME is listed as a global statement.

---

## Question 15

- **Answer:** title;
- **Domain:** D4 · **Difficulty:** easy · **Type:** Short answer
- **Source:** P1_L01_essentials.md – Page 9/13 and 10/13 (solution code ends with title;)

**Worked solution (two independent passes):**

```text
The demo solutions end with `title;` – a TITLE statement with no text, which removes the title for later output.
Pass 2: both Page 9 and Page 10 solution programs end with exactly this statement. ✔
```

---

## Question 16

- **Answer:** 60750
- **Domain:** D2 · **Difficulty:** hard · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 6/13, Page 8/13 (WHERE), Page 5/13 Practice (MAXDEC=)

**Worked solution (two independent passes):**

```text
Pass 1 – Bonus >= 3000: E01 (3000), E03 (4000), E06 (5000), E07 (3000) → Totals 55000, 65000, 55000, 68000. Sum = 243000; 243000 / 4 = 60750.
Pass 2 – mean Salary of the 4 = (52000+61000+50000+65000)/4 = 228000/4 = 57000; mean Bonus = (3000+4000+5000+3000)/4 = 3750; 57000 + 3750 = 60750. ✔
Trap: Bonus > 3000 drops E01 and E07 → (65000+55000)/2 = 60000.
```

**Reference solution code:**

```sas
data big;
    set staff;
    where Bonus>=3000;
    Total=Salary+Bonus;
run;

proc means data=big mean maxdec=0;
    var Total;
run;
```

---

## Question 17

- **Answer:** 33.3
- **Domain:** D3 · **Difficulty:** hard · **Type:** Performance – debugging
- **Source:** P1_L01_essentials.md – Page 10/13 Demo: Finding and Resolving Syntax Errors

**Worked solution (two independent passes):**

```text
Fixes (as in the demo): daat→data; add ; after `proc print data=orders2`; `average`→`mean`.
Pass 1 – Amount=Qty*Price:
OrderID Region Qty Price  Amount=Qty*Price
O1      East   2   15     30
O2      West   1   40     40
O3      East   5   8      40
O4      North  3   20     60
O5      West   4   12     48
O6      East   1   30     30
East: 30, 40, 30 → 100/3 = 33.333… → MAXDEC=1 → 33.3.
Pass 2: East rows O1, O3, O6; 2×15=30, 5×8=40, 1×30=30; 100/3 = 33.33 → 33.3. ✔
```

**Reference solution code:**

```sas
data orders2;
    set orders;
    Amount=Qty*Price;
run;

title "East Orders";
proc print data=orders2;
    var OrderID Amount;
    where Region="East";
run;

proc means data=orders2 mean maxdec=1;
    var Amount;
    class Region;
run;
title;
```

---

## Question 18

- **Answer:** 3
- **Domain:** D1 · **Difficulty:** medium · **Type:** Short answer
- **Source:** P1_L01_essentials.md – Page 6/13, Page 7/13 Activity (counting global statements)

**Worked solution (two independent passes):**

```text
Global statements outside steps: `options nodate;`, `title "Temperatures";`, `title;` = 3.
Pass 2: every statement that is not part of the DATA/PRINT/MEANS steps: options, title, title = 3. ✔
```

---

## Question 19

- **Answer:** A. 19 rows and 5 columns
- **Domain:** D2 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 8/13 SAS Program Syntax (comments), Page 3/13 (SASHELP.CLASS 19 rows)

**Worked solution (two independent passes):**

```text
`/* … */` comments out both the WHERE and the Ratio statements; `*drop Height;` comments out the DROP statement. Only DATA, SET, RUN execute → an exact copy: 19 rows, 5 columns.
Pass 2: no active statement filters rows, adds a column, or removes a column → 19 × 5. ✔
```

**Why the other options are wrong:**

- **B.** The WHERE and the Ratio assignment are inside /* */ and do not run.
- **C.** *drop Height; is a comment, so Height is kept.
- **D.** The WHERE is commented out, so all 19 rows are read.

---

## Question 20

- **Answer:** 3333.3
- **Domain:** D4 · **Difficulty:** medium · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 5/13 Practice (MAXDEC= rounds statistics), Page 9/13 (maxdec=1)

**Worked solution (two independent passes):**

```text
Pass 1: Sales bonuses 3000, 2000, 5000 → 10000/3 = 3333.333… → one decimal → 3333.3.
Pass 2: 3 × 3333.3 = 9999.9 ≈ 10000 ✔; second decimal is 3 (<5), so it rounds down to 3333.3. ✔
```

**Reference solution code:**

```sas
proc means data=staff mean maxdec=1;
    var Bonus;
    class Dept;
run;
```

---

## Question 21

- **Answer:** A. An ERROR is written because AVERAGE is not a valid option; the step does not run. Use MEAN instead.
- **Domain:** D3 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 10/13 Demo: Finding and Resolving Syntax Errors

**Worked solution (two independent passes):**

```text
Demo: "average is underlined, and the error message indicates what valid options there are for the PROC MEANS statement… must be corrected to use the proper option, MEAN. This step also did not run."
Pass 2: the corrected demo code uses `mean min max maxdec=1` – keyword order is free, confirming D is wrong and A right. ✔
```

**Why the other options are wrong:**

- **B.** Only the misspelled DATA keyword got a warning-and-run treatment in the demo.
- **C.** An invalid option stops the whole step.
- **D.** The demo solution puts MAXDEC= after the statistics; order is not the problem.

---

## Question 22

- **Answer:** 91.5
- **Domain:** D2 · **Difficulty:** easy · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 9/13 (mean function)

**Worked solution (two independent passes):**

```text
Cy: Test1 95 > 79 → kept. mean(95, 88) = 183/2 = 91.5.
Pass 2: midpoint of 88 and 95 = 88 + 7/2 = 91.5. ✔
```

**Reference solution code:**

```sas
data scores2;
    set scores;
    where Test1 > 79;
    Avg=mean(Test1, Test2);
    HeightCm=HeightIn*2.54;
run;
```

---

## Question 23

- **Answer:** A. The PROC MEANS statement ends the PROC PRINT step, and both steps run.
- **Domain:** D1 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 6/13 SAS Program Structure

**Worked solution (two independent passes):**

```text
Course rule: "If you don't use a RUN statement at the end of a step, the beginning of a new DATA or PROC step signals the end of the previous step." So PRINT ends at PROC MEANS and runs; MEANS ends at its RUN.
Pass 2: two step keywords → two steps, each with a boundary → both run. ✔
```

**Why the other options are wrong:**

- **B.** A missing RUN does not discard the step.
- **C.** A missing RUN between steps is not an error.
- **D.** Each PROC keyword starts a new step.

---

## Question 24

- **Answer:** 2
- **Domain:** D2 · **Difficulty:** hard · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 13/13 quiz-code pattern (WHERE … and …), Page 9/13 (WHERE in PROC PRINT)

**Worked solution (two independent passes):**

```text
Pass 1 – Sales rows: E01 52000 (≥50000 yes), E02 48000 (no), E06 50000 (yes, boundary) → 2.
Pass 2 – rows with Salary ≥ 50000 overall: E01, E03, E04, E06, E07; of those, Sales = E01, E06 → 2. ✔
Trap: Salary > 50000 gives 1.
```

**Reference solution code:**

```sas
proc print data=staff;
    where Dept="Sales" and Salary>=50000;
run;
```

---

## Question 25

- **Answer:** 3
- **Domain:** D3 · **Difficulty:** hard · **Type:** Performance – debugging
- **Source:** P1_L01_essentials.md – Page 11/13 Activity (missing semicolon, unbalanced quote, misspelled PROC)

**Worked solution (two independent passes):**

```text
Fixes (same three error types as the course activity): add ; after `data seniors`; close the quote in the TITLE; `prc`→`proc`.
Pass 1 – Age >= 6:
Name  Species Age Weight  Age>=6?  WeightLb=Weight*2.2
Max   Dog     5   30      no
Bella Cat     3   9       no
Rocky Dog     8   35      yes      77
Luna  Cat     10  11      yes      24.2
Coco  Bird    2   1       no
Duke  Dog     1   20      no
Milo  Cat     6   12      yes      26.4
→ Rocky, Luna, Milo = 3.
Pass 2 – rows failing (Age 5,3,2,1) = 4 of 7 → 7−4 = 3. ✔
Trap: Age > 6 drops Milo → 2.
```

**Reference solution code:**

```sas
data seniors;
    set pets;
    where Age>=6;
    WeightLb=Weight*2.2;
run;

title "Senior Pets";
proc print data=seniors;
run;
title;
```

---

## Question 26

- **Answer:** C. Results
- **Domain:** D4 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 5/13 Practice: Exploring SAS Studio, step 4

**Worked solution (two independent passes):**

```text
Practice: "The RESULTS tab is empty because the program did not create a report." The log has notes and Output Data shows the new table.
Pass 2: reports come from PROC steps such as PRINT/MEANS; none were submitted → Results empty. ✔
```

**Why the other options are wrong:**

- **A.** The log always contains the program and notes.
- **B.** Output Data shows the table the DATA step created.
- **D.** The Code tab holds your program.

---

## Question 27

- **Answer:** 55000
- **Domain:** D2 · **Difficulty:** easy · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 6/13 (assignment statement creates a column)

**Worked solution (two independent passes):**

```text
Pass 1: E06 Salary 50000 + Bonus 5000 = 55000.
Pass 2: 55000 − 5000 = 50000 = Salary ✔.
```

**Reference solution code:**

```sas
data staff2;
    set staff;
    Total=Salary+Bonus;
run;
```

---

## Question 28

- **Answer:** A. In SAS Studio and Enterprise Guide they are replaced; in the SAS windowing environment they are appended.
- **Domain:** D1 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 13/13 Lesson Review (Running a SAS Program)

**Worked solution (two independent passes):**

```text
Lesson Review: resubmitting in EG or SAS Studio replaces the log, output data, and results; in the SAS windowing environment it appends the log and results.
Pass 2: the Studio and EG demos both state "the log and results were replaced". ✔
```

**Why the other options are wrong:**

- **B.** Studio and EG replace, they don't append.
- **C.** Studio replaces (demo step 10).
- **D.** The windowing environment appends.

---

## Question 29

- **Answer:** 6
- **Domain:** D2 · **Difficulty:** medium · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 8/13 (asterisk comments out one statement), Page 9/13 (*where … commented out)

**Worked solution (two independent passes):**

```text
The asterisk turns the WHERE statement into a comment, so no rows are filtered: all 6 input rows are written.
Pass 2: work.scores has 6 data lines (Ana…Fay); no active WHERE → 6. ✔
```

**Reference solution code:**

```sas
data scores2;
    set scores;
    *where Test1 > 79;
    Avg=mean(Test1, Test2);
    HeightCm=HeightIn*2.54;
run;
```

---

## Question 30

- **Answer:** 88.17
- **Domain:** D4 · **Difficulty:** hard · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 5/13 Practice (MAXDEC=2 rounds to two decimals), Page 9/13

**Worked solution (two independent passes):**

```text
Pass 1 – scores2 rows and Avg:
Student Test1 Test2 HeightIn  mean(T1,T2)  HeightIn*2.54
Ana     80    90    60        85           152.4
Ben     72    75    65        73.5         165.1
Cy      95    88    70        91.5         177.8
Dee     60    71    62        65.5         157.48
Eli     88    88    68        88           172.72
Fay     79    84    55        81.5         139.7
Kept: Ana 85, Cy 91.5, Eli 88 → 264.5/3 = 88.1666… → 2 decimals → 88.17.
Pass 2 – mean of all six Test values of the kept rows: (80+90+95+88+88+88)/6 = 529/6 = 88.1666… (same, since each Avg weights its two tests equally) → 88.17. ✔
Trap: Test1 ≥ 79 adds Fay (81.5) → 346/4 = 86.5.
```

**Reference solution code:**

```sas
data scores2;
    set scores;
    where Test1 > 79;
    Avg=mean(Test1, Test2);
    HeightCm=HeightIn*2.54;
run;

proc means data=scores2 mean maxdec=2;
    var Avg;
run;
```

---

## Question 31

- **Answer:** A. An unmatched quotation mark; the editor's color coding (or Format Code) shows the rest of the program being treated as a quoted string.
- **Domain:** D3 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 10/13 (color-coded syntax catches unmatched quotation marks), Page 11/13 Activity (Format Code identifies the missing quotation mark)

**Worked solution (two independent passes):**

```text
The closing quote after Canada is missing. The course: unmatched quotation marks can be caught by color-coded syntax; in the activity, formatting the code identifies the missing quotation mark.
Pass 2: the step does have RUN; WHERE is used in DATA steps in the course (Page 8, Page 11) → A. ✔
```

**Why the other options are wrong:**

- **B.** The step ends with run;.
- **C.** Unquoted names are case-insensitive; the problem is the quote.
- **D.** The course uses WHERE inside DATA steps.

---

## Question 32

- **Answer:** 48
- **Domain:** D2 · **Difficulty:** easy · **Type:** Performance – debugging
- **Source:** P1_L01_essentials.md – Page 6/13 (assignment statement), Page 10/13

**Worked solution (two independent passes):**

```text
Pass 1: O5 Qty 4 × Price 12 = 48.
Pass 2: 48 / 12 = 4 = Qty ✔. (The DATA step runs even before the fix – DAAT is only a warning – so the value is the same either way.)
```

**Reference solution code:**

```sas
data orders2;
    set orders;
    Amount=Qty*Price;
run;

title "East Orders";
proc print data=orders2;
    var OrderID Amount;
    where Region="East";
run;

proc means data=orders2 mean maxdec=1;
    var Amount;
    class Region;
run;
title;
```

---

## Question 33

- **Answer:** 19
- **Domain:** D1 · **Difficulty:** easy · **Type:** Short answer
- **Source:** P1_L01_essentials.md – Page 3/13 and 4/13 demos

**Worked solution (two independent passes):**

```text
Both demos state SASHELP.CLASS has 19 rows (one per student).
Pass 2: you can confirm with `proc contents data=sashelp.class; run;` or the PROC PRINT listing. ✔
```

---

## Question 34

- **Answer:** A. They are identical; spacing and line breaks do not matter to SAS.
- **Domain:** D2 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 8/13 SAS Program Syntax

**Worked solution (two independent passes):**

```text
The course shows the same program with and without line breaks and says the two "have exactly the same code" – spacing doesn't matter to SAS.
Pass 2: the Lesson Review repeats "Spacing doesn't matter in a SAS program." ✔
```

**Why the other options are wrong:**

- **B.** Several statements on one line are allowed.
- **C.** Line breaks don't change the data read.
- **D.** There is no column-one requirement.

---

## Question 35

- **Answer:** 24.2
- **Domain:** D3 · **Difficulty:** hard · **Type:** Performance – debugging
- **Source:** P1_L01_essentials.md – Page 11/13 Activity (fix missing semicolon, unbalanced quote, misspelled PROC)

**Worked solution (two independent passes):**

```text
Luna: Age 10 ≥ 6 → kept. WeightLb = 11 × 2.2.
Pass 1: 11 × 2.2 = 22 + 2.2 = 24.2.
Pass 2: 10 × 2.2 = 22; + 2.2 = 24.2 ✔.
```

**Reference solution code:**

```sas
data seniors;
    set pets;
    where Age>=6;
    WeightLb=Weight*2.2;
run;

title "Senior Pets";
proc print data=seniors;
run;
title;
```

---

## Question 36

- **Answer:** 3
- **Domain:** D4 · **Difficulty:** medium · **Type:** Performance – debugging
- **Source:** P1_L01_essentials.md – Page 10/13 Demo (fixing the PROC PRINT semicolon)

**Worked solution (two independent passes):**

```text
After adding the semicolon, the WHERE keeps Region="East": O1, O3, O6 → 3 rows.
Pass 2: Regions = East×3, West×2, North×1 → 3. ✔
```

**Reference solution code:**

```sas
data orders2;
    set orders;
    Amount=Qty*Price;
run;

title "East Orders";
proc print data=orders2;
    var OrderID Amount;
    where Region="East";
run;

proc means data=orders2 mean maxdec=1;
    var Amount;
    class Region;
run;
title;
```

---

## Question 37

- **Answer:** 4700
- **Domain:** D2 · **Difficulty:** medium · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 6/13 (assignment statement), Page 11/13 (WHERE region=…)

**Worked solution (two independent passes):**

```text
Pass 1: E08 is HR; 47000 × 0.1 = 4700.
Pass 2: 4700 × 10 = 47000 ✔.
```

**Reference solution code:**

```sas
data hr;
    set staff;
    where Dept="HR";
    Raise=Salary*0.1;
run;
```

---

## Question 38

- **Answer:** 5
- **Domain:** D1 · **Difficulty:** medium · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 6/13 (DATA step creates an output table and adds a new column)

**Worked solution (two independent passes):**

```text
work.staff has 4 columns (EmpID, Dept, Salary, Bonus from the INPUT statement); the assignment adds Total → 5.
Pass 2: list them: EmpID, Dept, Salary, Bonus, Total = 5 ✔.
```

**Reference solution code:**

```sas
data staff2;
    set staff;
    Total=Salary+Bonus;
run;
```

---

## Question 39

- **Answer:** 1
- **Domain:** D2 · **Difficulty:** hard · **Type:** Performance
- **Source:** P1_L01_essentials.md – Page 8/13 (where Age<13 comparison)

**Worked solution (two independent passes):**

```text
Pass 1 – Test2 < Test1? Ana 90<80 no; Ben 75<72 no; Cy 88<95 yes; Dee 71<60 no; Eli 88<88 no (equal); Fay 84<79 no → 1 (Cy).
Pass 2 – Test1 − Test2: −10, −3, +7, −11, 0, −5 → only one positive → 1. ✔
Trap: <= would add Eli → 2.
```

**Reference solution code:**

```sas
data drop2;
    set scores;
    where Test2 < Test1;
run;
```

---

## Question 40

- **Answer:** A. Libref PG1 was successfully assigned, followed by the engine and physical name
- **Domain:** D1 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** P1_L00_setup.md – Pop-up 3 (SAS Studio) Task 2 step 7; Pop-up 5 (Windowing Environment) Task 2 step 5

**Worked solution (two independent passes):**

```text
Setup instructions: "Check the log for the note Libref PG1 was successfully assigned, followed by the engine and physical name specification."
Pass 2: the same note is given in both the SAS Studio and Windowing Environment instructions. ✔
```

**Why the other options are wrong:**

- **B.** setup.sas assigns a library (libref), it does not create a table named PG1.
- **C.** That would indicate failure, not success.
- **D.** The instructions say a note is written.

---

## Question 41

- **Answer:** results
- **Domain:** D4 · **Difficulty:** easy · **Type:** Short answer
- **Source:** P1_L01_essentials.md – Page 3/13 Demo: Programming with SAS Studio (steps 5–7)

**Worked solution (two independent passes):**

```text
Demo: the program tab has Code, Log, Results, and Output Data tabs; "Select the Results tab to view the report".
Pass 2: step 10 – after running only PROC PRINT, "The Results tab shows the report that was created from the PROC PRINT code." ✔
```

---

## Question 42

- **Answer:** A. Rounds the displayed statistics to two decimal places.
- **Domain:** D4 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 5/13 Practice: Exploring SAS Studio, step 8

**Worked solution (two independent passes):**

```text
Practice: "Type MAXDEC=2 to round the statistics to two decimal places."
Pass 2: in the demo, maxdec=1 appears with mean/min/max statistics only – it controls the report, not the data. ✔
```

**Why the other options are wrong:**

- **B.** VAR controls which columns are analyzed.
- **C.** CLASS has no such limit option here.
- **D.** PROC MEANS produces a report; it does not change stored data.

---

## Question 43

- **Answer:** A. where Region="East";
- **Domain:** D2 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** P1_L01_essentials.md – Page 11/13 Activity (where region="Canada";), Page 10/13 (unmatched quotes)

**Worked solution (two independent passes):**

```text
The course compares a character column to a quoted value: `where region="Canada";`. Same pattern → A.
Pass 2: C has an unmatched quotation mark (a syntax error from the course); D quotes the column name so it is a text constant, not the column; B leaves the value unquoted. ✔
```

**Why the other options are wrong:**

- **B.** The value is not quoted; the course always quotes character values in WHERE. [Unquoted East would be read as a column name – general SAS behavior.]
- **C.** Unmatched quotation mark – the rest of the program becomes part of the string.
- **D.** Quoting Region makes it a constant string, not the column.

---

