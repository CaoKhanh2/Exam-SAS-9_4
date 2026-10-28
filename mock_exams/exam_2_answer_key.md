# Mock Exam 2 – Answer Key

Domain counts: D1 10 · D2 17 · D3 8 · D4 10

---

## Question 1

- **Answer:** C. libname sales_24 xlsx "s:/workshop/data/sales.xlsx";
- **Domain:** D1 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** CR_01_L1_P1_review.md – 1.2 Directly Accessing Structured Data (libref ≤ 8 characters, SAS naming conventions); 1.1 Required Column Attributes (name rules)

**Worked solution (two independent passes):**

```text
Pass 1: a libref must follow SAS naming rules and be 8 characters or less. sales_24 = 8 characters, starts with a letter, letters/digits/underscore only → valid; the XLSX engine and a quoted path + file name are the documented form.
Pass 2: check each other option against the same two rules – salesdata2024 is 13 characters (too long); 2024data starts with a digit; sales-24 contains a hyphen. Only C passes both rules. ✔
```

**Why the other options are wrong:**

- **A.** 13 characters – a libref may be at most 8.
- **B.** Names must start with a letter or underscore, not a digit.
- **D.** A hyphen is not allowed in SAS names.

---

## Question 2

- **Answer:** D. Only a NOTE saying the library does not exist – no error and no warning.
- **Domain:** D1 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_05_L5_challenging_topics.md – Creating Libraries (nonexistent folder)

**Worked solution (two independent passes):**

```text
Pass 1: the L5 demo with the typo …/daat produced "no warning, no error – only a NOTE 'Library CRB2 does not exist.'" → D.
Pass 2: the lesson's point is "No error ≠ correct code"; A and B contradict the demo, C describes the corrected path. ✔
```

**Why the other options are wrong:**

- **A.** The demo produced no error.
- **B.** The demo produced no warning.
- **C.** That happens only after the path is fixed.

---

## Question 3

- **Answer:** B. guessingrows=max;
- **Domain:** D1 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** CR_02_L2_TSA_case_study.md – Solution for Accessing Data (GUESSINGROWS=MAX)

**Worked solution (two independent passes):**

```text
Pass 1: TSA solution: "GUESSINGROWS=MAX statement: use every row to determine column types, because the CSV has many missing values." → B.
Pass 2: REPLACE only overwrites an existing output table; DBMS= names the file type (and is an option on the PROC statement); VALIDVARNAME is a global OPTIONS setting for column names. ✔
```

**Why the other options are wrong:**

- **A.** REPLACE overwrites the output table if it already exists.
- **C.** DBMS= tells SAS the file type.
- **D.** VALIDVARNAME=V7 controls column names, not types, and is a global statement.

---

## Question 4

- **Answer:** D. A list of all tables in the CR library, without the descriptor portion of each table.
- **Domain:** D1 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** CR_01_L1_P1_review.md – 1.2 Viewing Table Properties with PROC CONTENTS; PQ 1.03

**Worked solution (two independent passes):**

```text
Pass 1: _ALL_ gives a list of all tables then the descriptor portion for each; "Adding the NODS option after _ALL_ suppresses the descriptor portions, leaving only the list." → D.
Pass 2: C is _ALL_ without NODS; PROC CONTENTS never prints data rows (B); A ignores _ALL_. PQ 1.03 uses exactly this step to count tables in the library. ✔
```

**Why the other options are wrong:**

- **A.** _ALL_ covers every table in the library.
- **B.** PROC CONTENTS reports properties, not data values.
- **C.** That is the output without NODS.

---

## Question 5

- **Answer:** 3
- **Domain:** D1 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_03_L3_P2_review.md – 3.5 Concatenating Tables (different column names → separate columns with missing values)

**Worked solution (two independent passes):**

```text
Pass 1: jan has Item, Units; feb has Item, Qty. SET combines the columns by name: Item, Units, Qty → 3 columns (rows from jan have missing Qty, rows from feb have missing Units).
Pass 2: same pattern as the course demo where Line/Category and Product_Line/Product_Category became separate columns until RENAME= was added. 7 rows, 3 columns. ✔
```

**Reference solution code:**

```sas
data q1;
    set jan feb;
run;
```

---

## Question 6

- **Answer:** 36
- **Domain:** D1 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_03_L3_P2_review.md – 3.5 Concatenating Tables (RENAME= data set option); PQ 3.13

**Worked solution (two independent passes):**

```text
Pass 1: jan Units 5+3+7 = 15; feb Qty → Units 4+6+2+9 = 21; total 36.
Pass 2: list all 7 rows: Pen 5, Ink 3, Pad 7, Pen 4, Pad 6, Ink 2, Tape 9 → 5+3=8, +7=15, +4=19, +6=25, +2=27, +9=36. ✔
```

**Reference solution code:**

```sas
data q1;
    set jan feb(rename=(Qty=Units));
run;

proc means data=q1 sum;
    var Units;
run;
```

---

## Question 7

- **Answer:** 4
- **Domain:** D1 · **Difficulty:** hard · **Type:** Performance
- **Source:** CR_03_L3_P2_review.md – 3.5 Merging Tables (sorted inputs, same BY column, IN=); CR_05 – Finding Non-matches (RENAME= on PROC SORT output); PQ 3.15

**Worked solution (two independent passes):**

```text
Pass 1 (trace):
EmpID  in emp  in don  Q1 Q2 Q3 Q4  sum(of Q1-Q4)
E1     1       1       .  .  30 .   30
E2     1       1       15 15 15 15  60
E3     1       1       20 10 .  10  40
E4     1       0
E5     1       1       10 .  20 5   35
E6     1       0
E7     0       1       5  5  .  .   (not output)
Rows with both flags = 1: E1, E2, E3, E5 → 4.
Pass 2: emp IDs E1–E6; don IDs E5, E2, E7, E1, E3. Intersection = {E1, E2, E3, E5} → 4 rows. ✔
```

**Reference solution code:**

```sas
proc sort data=don out=don_sort(rename=(ID=EmpID));
    by ID;
run;

data donors nodonor;
    merge emp(in=inE) don_sort(in=inD);
    by EmpID;
    if inE=1 and inD=1 then do;
        TotalDonation=sum(of Q1-Q4);
        output donors;
    end;
    else if inE=1 and inD=0 then output nodonor;
run;
```

---

## Question 8

- **Answer:** 40
- **Domain:** D1 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_03_L3_P2_review.md – 3.3 Using Numeric and Date Functions (SUM with OF list); PQ 3.15

**Worked solution (two independent passes):**

```text
Pass 1: Cal = E3; don row E3: Q1=20, Q2=10, Q3=., Q4=10 → SUM ignores the missing value → 40.
Pass 2: if missing were not ignored the result would be missing, not a number; the SUM function skips missing → 20+10+10 = 40. ✔
```

**Reference solution code:**

```sas
proc sort data=don out=don_sort(rename=(ID=EmpID));
    by ID;
run;

data donors nodonor;
    merge emp(in=inE) don_sort(in=inD);
    by EmpID;
    if inE=1 and inD=1 then do;
        TotalDonation=sum(of Q1-Q4);
        output donors;
    end;
    else if inE=1 and inD=0 then output nodonor;
run;
```

---

## Question 9

- **Answer:** 2
- **Domain:** D1 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_03_L3_P2_review.md – 3.5 Merging Tables (non-matches: one IN= flag 1, the other 0); PQ 3.15

**Worked solution (two independent passes):**

```text
Pass 1: emp-only IDs (inE=1, inD=0): E4 (Di), E6 (Flo) → 2.
Pass 2: emp has 6 rows; 4 matched (previous question) → 6 − 4 = 2. E7 is in don only and goes to neither table. ✔
```

**Reference solution code:**

```sas
proc sort data=don out=don_sort(rename=(ID=EmpID));
    by ID;
run;

data donors nodonor;
    merge emp(in=inE) don_sort(in=inD);
    by EmpID;
    if inE=1 and inD=1 then do;
        TotalDonation=sum(of Q1-Q4);
        output donors;
    end;
    else if inE=1 and inD=0 then output nodonor;
run;
```

---

## Question 10

- **Answer:** In per
- **Domain:** D1 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_01_L1_P1_review.md – 1.4 Using the DATA Step (truncation, length set by first assigned value); CR_05 – Using the LENGTH Statement

**Worked solution (two independent passes):**

```text
Pass 1: the first appearance of Source is the assignment "Online" (6 characters) → length 6. A02 is Phone → "In person" truncated to 6 characters → "In per".
Pass 2: count: I-n-space-p-e-r = 6 characters. Same mechanism as the course demos ("Retail" → length 6; "Known" → "Unkno"). No error or warning is written. ✔
```

**Reference solution code:**

```sas
data shop3;
    set shop;
    length Source $ 9;   /* fix: declare the length before first use */
    if Channel="Web" then Source="Online";
    else Source="In person";
run;
```

---

## Question 11

- **Answer:** 7
- **Domain:** D2 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_05_L5_challenging_topics.md – Comparing WHERE and IF Statements (only IF filters new columns); PQ 5.02

**Worked solution (two independent passes):**

```text
Pass 1 (trace):
OrderID Store Channel Qty Price  Amount=Qty*Price
A01     North Web     3   20     60
A02     South Phone   1   55     55
A03     North Store   4   12     48
A04     West  Web     2   35     70
A05     South Web     5   12     60
A06     North Phone   2   40     80
A07     West  Store   6   9      54
A08     South Store   2   30     60
A09     North Web     1   84     84
A10     West  Phone   3   25     75
Amount >= 60: A01 60, A04 70, A05 60, A06 80, A08 60, A09 84, A10 75 → 7.
Pass 2: rows below 60: A02 55, A03 48, A07 54 → 3; 10 − 3 = 7. A WHERE statement cannot be used because Amount is not in the input table – a subsetting IF after the assignment is required. ✔
```

**Reference solution code:**

```sas
data big;
    set shop;
    Amount=Qty*Price;
    if Amount>=60;
run;
```

---

## Question 12

- **Answer:** 6
- **Domain:** D2 · **Difficulty:** easy · **Type:** Performance
- **Source:** CR_03_L3_P2_review.md – 3.1 Directing DATA Step Output (conditional OUTPUT to multiple tables); PQ 3.01

**Worked solution (two independent passes):**

```text
Pass 1: Web rows = A01, A04, A05, A09 → 4; other = 10 − 4 = 6.
Pass 2: count non-Web directly: A02 Phone, A03 Store, A06 Phone, A07 Store, A08 Store, A10 Phone → 6. ✔
```

**Reference solution code:**

```sas
data web other;
    set shop;
    if Channel="Web" then output web;
    else output other;
run;
```

---

## Question 13

- **Answer:** 199
- **Domain:** D2 · **Difficulty:** hard · **Type:** Performance
- **Source:** CR_03_L3_P2_review.md – 3.2 Summarizing Data (BY, FIRST./LAST., sum statement, subsetting IF last.); PQ 3.06, PQ 5.07

**Worked solution (two independent passes):**

```text
Pass 1: West rows A04 70, A07 54, A10 75 → 70+54 = 124, +75 = 199.
Pass 2: all stores: North 60+48+80+84 = 272, South 55+60+60 = 175, West 199; 272+175+199 = 646 = total of all 10 Amounts (60+55+48+70+60+80+54+60+84+75 = 646). ✔
```

**Reference solution code:**

```sas
proc sort data=shop out=shop_sort;
    by Store;
run;

data storetot;
    set shop_sort;
    by Store;
    if first.Store then StoreAmt=0;
    StoreAmt+Qty*Price;
    if last.Store;
    keep Store StoreAmt;
run;
```

---

## Question 14

- **Answer:** 217
- **Domain:** D2 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_05_L5_challenging_topics.md – Creating an Accumulating Column (RETAIN / SUM); PQ 5.06

**Worked solution (two independent passes):**

```text
Pass 1: sorted Amounts: 48, 54, 55, 60, 60, 60, 70, 75, 80, 84. Running totals: 48, 102, 157, 217 → row 4 = 217.
Pass 2: the three tied 60s can be in any order, but row 4 is the first 60 regardless: 48+54+55+60 = 217. ✔
```

**Reference solution code:**

```sas
data shop_amt;
    set shop;
    Amount=Qty*Price;
run;

proc sort data=shop_amt;
    by Amount;
run;

data running;
    set shop_amt;
    RunAmt+Amount;
run;
```

---

## Question 15

- **Answer:** C. The same value as Amount on every row.
- **Domain:** D2 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_05_L5_challenging_topics.md – Creating an Accumulating Column ("alone it does not accumulate"); CR_03 3.1 (new columns reset to missing)

**Worked solution (two independent passes):**

```text
Pass 1: RunAmt is created by an assignment, so it is reset to missing at the top of each iteration. SUM ignores missing → sum(., Amount) = Amount.
Pass 2: the L5 demo shows the same statement "alone does not accumulate"; adding RETAIN … 0 makes it accumulate. B ignores that SUM skips the missing argument. ✔
```

**Why the other options are wrong:**

- **A.** Needs RETAIN (or a sum statement) to accumulate.
- **B.** SUM ignores the missing RunAmt, so the result is Amount.
- **D.** Nothing totals the whole table on each row.

---

## Question 16

- **Answer:** 6
- **Domain:** D2 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_03_L3_P2_review.md – 3.4 Creating and Using Custom Formats; PQ 3.10 (low-< ranges, FORMAT in PROC FREQ)

**Worked solution (two independent passes):**

```text
Pass 1: Amounts 60, 55, 48, 70, 60, 80, 54, 60, 84, 75 → Low: 48 (1); Mid: 60, 55, 70, 60, 54, 60 (6); High: 80, 84, 75 (3).
Pass 2: 1 + 6 + 3 = 10 rows ✔; 75 is the boundary → "50-<75" excludes it, "75-high" includes it, so 75 is High. ✔
```

**Reference solution code:**

```sas
proc format;
    value amtcat low-<50="Low"
                 50-<75="Mid"
                 75-high="High";
run;

data shop_amt;
    set shop;
    Amount=Qty*Price;
run;

proc freq data=shop_amt;
    tables Amount;
    format Amount amtcat.;
run;
```

---

## Question 17

- **Answer:** B. proc format; value $chan "Web"="Online" other="Offline"; run;
- **Domain:** D2 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** CR_03_L3_P2_review.md – 3.4 Creating and Using Custom Formats (character format names start with $; period only when applied); PQ 3.12

**Worked solution (two independent passes):**

```text
Pass 1: "character format names must start with $"; the period is added only when the format is applied ("the format name must end with a period" when used). → B.
Pass 2: PQ 3.12 creates `value $statfmt "S"="Single" …` – $ prefix, no period in the VALUE statement. A lacks $; C and D put a period in the name. ✔
```

**Why the other options are wrong:**

- **A.** A character format name must begin with $.
- **C.** No $ and the period does not belong in the VALUE statement.
- **D.** The period is used when applying the format, not when naming it.

---

## Question 18

- **Answer:** Ana-Sofia Ortiz
- **Domain:** D2 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_03_L3_P2_review.md – 3.3 Using Numeric and Date Functions (SCAN with a delimiter list); PQ 3.08 (CATX + SCAN)

**Worked solution (two independent passes):**

```text
Pass 1: row 3 FullName = "Ortiz,Ana-Sofia". scan(…, 2, ",") = "Ana-Sofia" (only the comma is a delimiter, so the hyphen is kept); scan(…, 1, ",") = "Ortiz"; CATX joins with one space → "Ana-Sofia Ortiz".
Pass 2: without the "," argument, the hyphen would be a delimiter and word 2 would be "Ana" – the stem's requirement rules that out. ✔
```

**Reference solution code:**

```sas
data people2;
    set people;
    Display=catx(" ", scan(FullName, 2, ","), scan(FullName, 1, ","));
run;
```

---

## Question 19

- **Answer:** A. Mary
- **Domain:** D2 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_03_L3_P2_review.md – 3.3 Using Numeric and Date Functions (SCAN default delimiters include spaces, hyphens and other punctuation)

**Worked solution (two independent passes):**

```text
Pass 1: default delimiters include the comma and the hyphen → words: "Lee", "Mary", "Ann" → word 2 = "Mary".
Pass 2: the course example keeps hyphenated names intact only by supplying a third argument that limits the delimiters; without it the hyphen splits the name. ✔
```

**Why the other options are wrong:**

- **B.** That is word 1.
- **C.** Only if the hyphen were not a delimiter (third argument ",").
- **D.** That is word 3.

---

## Question 20

- **Answer:** 22221
- **Domain:** D2 · **Difficulty:** hard · **Type:** Performance
- **Source:** CR_05_L5_challenging_topics.md – Converting Column Type (INPUT with MMDDYY10./ANYDTDTE10.); CR_01 1.1 (SAS date = days from 01JAN1960); PQ 1.09 (Boxing Day 2019 = 21909)

**Worked solution (two independent passes):**

```text
Pass 1: 11/02/2020 counted from 01JAN1960 = 22221 (computed: days between 1960-01-01 and 2020-11-02).
Pass 2: anchor from PQ 1.09: 26DEC2019 = 21909. Days 26DEC2019 → 02NOV2020: 6 (to 01JAN2020) + Jan 31 + Feb 29 + Mar 31 + Apr 30 + May 31 + Jun 30 + Jul 31 + Aug 31 + Sep 30 + Oct 31 + 1 = 312 → 21909 + 312 = 22221. ✔
```

**Reference solution code:**

```sas
data people3;
    set people;
    JoinDate=input(Joined, mmddyy10.);
run;

proc print data=people3;
    format JoinDate 10.;   /* shows the raw value */
run;
```

---

## Question 21

- **Answer:** 43917
- **Domain:** D2 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_03_L3_P2_review.md – PQ 3.09 (INPUT with COMMA or DOLLAR informat); CR_05 – Converting Column Type

**Worked solution (two independent passes):**

```text
Pass 1: 42500 + 38000 + 51250 = 131750; /3 = 43916.67 → MAXDEC=0 → 43917.
Pass 2: 3 × 43917 = 131751 ≈ 131750 ✔; the first decimal is 6 (≥5) so it rounds up. The DOLLAR (or COMMA) informat reads the $ and comma. ✔
```

**Reference solution code:**

```sas
data pay2;
    set pay;
    SalNum=input(Salary, dollar10.);
run;

proc means data=pay2 mean maxdec=0;
    var SalNum;
run;
```

---

## Question 22

- **Answer:** 8
- **Domain:** D2 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_03_L3_P2_review.md – 3.6 Iterative and Conditional DO Loops; CR_05 – Using Conditional DO Loops (UNTIL checked at the bottom); PQ 3.18

**Worked solution (two independent passes):**

```text
Pass 1: Balance after each pass: 1100, 1210, 1331, 1464.1, 1610.51, 1771.56, 1948.72, 2143.59 → after pass 8 the condition is true → 8 rows (one OUTPUT per pass).
Pass 2: 1.1^7 × 1000 = 1948.7 ≤ 2000 (continue); 1.1^8 × 1000 = 2143.6 > 2000 (stop) → 8. ✔
```

---

## Question 23

- **Answer:** 3953
- **Domain:** D2 · **Difficulty:** hard · **Type:** Performance
- **Source:** CR_03_L3_P2_review.md – 3.6 Using Nested DO Loops; CR_05 – Using Iterative DO Loops (OUTPUT between the inner END and the outer END)

**Worked solution (two independent passes):**

```text
Pass 1: simulated 36 months: end of year 1 = 1239.72, year 2 = 2555.91, year 3 = 3953.28 → 3953.
Pass 2: annuity-due formula 100 × 1.005 × (1.005^36 − 1)/0.005 = 100 × 1.005 × 39.3361 = 3953.28 → 3953. ✔
```

**Reference solution code:**

```sas
data savings;
    Balance=0;
    do Year=1 to 3;
        do Month=1 to 12;
            Balance=Balance+100;
            Balance=Balance*(1+.06/12);
        end;
        output;
    end;
    format Balance comma12.;
run;
```

---

## Question 24

- **Answer:** D. 1 row: Year = 6, Total = 50.
- **Domain:** D2 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_05_L5_challenging_topics.md – Using Iterative DO Loops (index after loop = stop+1; only implicit output without OUTPUT)

**Worked solution (two independent passes):**

```text
Pass 1: no OUTPUT statement → only the implicit output at RUN → 1 row. The index increases at END; after the 5th pass it becomes 6 and the loop stops → Year = 6. Total is incremented 5 times → 50.
Pass 2: course demo: Month = 13 after do Month=1 to 12, and Year = 6 after do Year=1 to 5 with one row per input row. ✔
```

**Why the other options are wrong:**

- **A.** Rows per year require an OUTPUT inside the loop.
- **B.** There is only one implicit output.
- **C.** The index is incremented once more before the loop ends.

---

## Question 25

- **Answer:** A. Loop 1: 0 times · Loop 2: 1 time
- **Domain:** D2 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_05_L5_challenging_topics.md – Using Conditional DO Loops (WHILE checked at the top, UNTIL at the bottom)

**Worked solution (two independent passes):**

```text
Pass 1: DO WHILE tests at the top: 10 < 5 is false → body never runs. DO UNTIL tests at the bottom: the body runs once (X = 11), then 11 >= 5 is true → stop.
Pass 2: the course says the two give identical results only when the WHILE loop executes at least once – here it does not, so they differ (0 vs 1). ✔
```

**Why the other options are wrong:**

- **B.** Reversed: WHILE is checked first, UNTIL last.
- **C.** UNTIL always executes at least once.
- **D.** WHILE tests before the first pass.

---

## Question 26

- **Answer:** 20
- **Domain:** D2 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_05_L5_challenging_topics.md – Restructuring Data with PROC TRANSPOSE (BY, all numeric non-BY columns by default, missing counts as a value); CR_03 3.7

**Worked solution (two independent passes):**

```text
Pass 1: 5 IDs × 4 numeric columns (Q1–Q4, transposed by default) = 20 rows; missing values still produce rows.
Pass 2: count per ID: E1 4, E2 4, E3 4, E5 4, E7 4 → 20. The input must be sorted by ID first (it is not). ✔
```

**Reference solution code:**

```sas
proc sort data=don out=don_sort;
    by ID;
run;

proc transpose data=don_sort out=don_narrow;
    by ID;
run;
```

---

## Question 27

- **Answer:** A. They exist in the PDV during execution but are not written to the output table.
- **Domain:** D2 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** CR_03_L3_P2_review.md – 3.1 Understanding DATA Step Processing (automatic variables)

**Worked solution (two independent passes):**

```text
Pass 1: "_N_ and _ERROR_ … are automatic: present in the PDV during execution but not written to the output table." → A.
Pass 2: _N_ = DATA step iteration number (not rows written); _ERROR_ = 1 if a data error occurs for the row. FIRST./LAST. (not these) come from BY. ✔
```

**Why the other options are wrong:**

- **B.** They are never written to the output table.
- **C.** _N_ is the iteration number; _ERROR_ flags a data error (1/0).
- **D.** BY creates FIRST./LAST. variables.

---

## Question 28

- **Answer:** 3
- **Domain:** D3 · **Difficulty:** hard · **Type:** Performance – debugging
- **Source:** CR_01_L1_P1_review.md – 1.1 Finding and Resolving Syntax Errors (missing semicolon; missing period = logic error); CR_05 – Comparing WHERE and IF; Using the LENGTH Statement

**Worked solution (two independent passes):**

```text
Errors: (1) no semicolon after DATA shop2 → syntax error; (2) WHERE uses Amount, which is not in the input table → ERROR, use IF after the assignment; (3) LENGTH after the assignments → WARNING, "Offline" truncated to "Offlin" – move LENGTH before them; (4) dollar8 without a period → treated as a column name (NOTE: uninitialized).
Pass 1: rows with Amount ≥ 60: A01 Web, A04 Web, A05 Web, A06 Phone, A08 Store, A09 Web, A10 Phone → Offline = A06, A08, A10 = 3.
Pass 2: 7 rows − 4 Web rows = 3. ✔
```

**Reference solution code:**

```sas
data shop2;
    set shop;
    length Source $ 7;
    Amount=Qty*Price;
    if Amount>=60;
    if Channel="Web" then Source="Online";
    else Source="Offline";
    format Amount dollar8.;
run;

proc freq data=shop2;
    tables Source;
run;
```

---

## Question 29

- **Answer:** 10
- **Domain:** D3 · **Difficulty:** medium · **Type:** Performance – debugging
- **Source:** CR_01_L1_P1_review.md – PQ 1.12 (PROC SORT, then PROC PRINT BY/ID/SUM/LABEL); 1.1 Syntax errors; CR_05 – data must be sorted for BY processing

**Worked solution (two independent passes):**

```text
Errors: unmatched quotation mark in TITLE; missing semicolon after the PROC PRINT statement; shop is not sorted by Store, so BY Store needs a PROC SORT first.
Pass 1: North rows A01 3, A03 4, A06 2, A09 1 → 10.
Pass 2: all subtotals: North 10, South 1+5+2 = 8, West 2+6+3 = 11; 10+8+11 = 29 = total Qty (3+1+4+2+5+2+6+2+1+3 = 29). ✔
```

**Reference solution code:**

```sas
proc sort data=shop out=shop_sort;
    by Store;
run;

title "Store Quantities";
proc print data=shop_sort label noobs;
    by Store;
    var OrderID Qty;
    sum Qty;
    label Qty="Units Sold";
run;
title;
```

---

## Question 30

- **Answer:** C. No error or warning, but a NOTE that dollar12 is uninitialized; Profit is not formatted as dollars.
- **Domain:** D3 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_01_L1_P1_review.md – 1.1 Finding and Resolving Syntax Errors (missing period after DOLLAR12)

**Worked solution (two independent passes):**

```text
Pass 1: course demo: missing period after DOLLAR12 → "no error or warning, results produced, but the log NOTE says 'Variable dollar12 is uninitialized'" – SAS treats dollar12 as a column name. It is a logic error. → C.
Pass 2: the lesson: "read notes too, not only errors and warnings" – consistent with C only. ✔
```

**Why the other options are wrong:**

- **A.** The syntax is valid – no error.
- **B.** There is no warning and no automatic fix.
- **D.** The format is not applied, and a NOTE appears.

---

## Question 31

- **Answer:** A. An ERROR that Amount is not in the input table; replace WHERE with a subsetting IF placed after the assignment.
- **Domain:** D3 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_05_L5_challenging_topics.md – Comparing WHERE and IF Statements

**Worked solution (two independent passes):**

```text
Pass 1: demo: WHERE TotalDonations > 50 → "ERROR: variable TotalDonations is not in file …"; changed to IF placed after the assignment → works. → A.
Pass 2: WHERE acts before any other DATA step processing, so its position in the step does not matter (B and D are wrong); only IF can filter new columns. ✔
```

**Why the other options are wrong:**

- **B.** WHERE filters as rows are read, before the assignment runs, regardless of position.
- **C.** There is no automatic conversion.
- **D.** WHERE still cannot see a column that is not in the input table.

---

## Question 32

- **Answer:** C. A WARNING that the length was already set; the LENGTH statement has no effect and "Unknown" is stored as "Unkno".
- **Domain:** D3 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_05_L5_challenging_topics.md – Using the LENGTH Statement (LENGTH placed after the conditional statements)

**Worked solution (two independent passes):**

```text
Pass 1: L5 demo: LENGTH after the conditional statements → WARNING "Length of character variable Order_Source has already been set…"; "The late LENGTH has no effect – length stays 5, values truncated" → "Unkno". → C.
Pass 2: length was set at the first appearance ("Known" = 5 characters); the fix is LENGTH before any other appearance. ✔
```

**Why the other options are wrong:**

- **A.** The late LENGTH statement is ignored.
- **B.** It is a warning, not an error – the table is created.
- **D.** There is a WARNING and the value is truncated.

---

## Question 33

- **Answer:** D. To write messages or column values to the log during DATA step execution, which helps find logic errors.
- **Domain:** D3 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** CR_03_L3_P2_review.md – 3.2 Summarizing Data (PUTLOG demo)

**Worked solution (two independent passes):**

```text
Pass 1: "PUTLOG statements (write messages to the log during execution – useful to understand processing and diagnose logic errors)". → D.
Pass 2: the demo placed PUTLOG before SET, after a calculation and at the end to watch HeightCM reset to missing – diagnosis only. OUTPUT (A) writes rows. ✔
```

**Why the other options are wrong:**

- **A.** That is the OUTPUT statement.
- **B.** ODS sends reports to files; PUTLOG writes to the log.
- **C.** PUTLOG does not stop processing.

---

## Question 34

- **Answer:** B. Country is never read into the PDV, so the IF condition cannot use it (errors/warnings appear). Use a DROP statement or DROP= on the output tables instead.
- **Domain:** D3 · **Difficulty:** hard · **Type:** Multiple choice
- **Source:** CR_05_L5_challenging_topics.md – Using DROP and KEEP Statements

**Worked solution (two independent passes):**

```text
Pass 1: "DROP= on the input data set → not read into the PDV, not available for processing"; dropping a column that is used "fails … error and warnings in the log. Use a DROP statement or DROP= on the output tables instead (takes effect after all processing)." → B.
Pass 2: input data set options act before any other processing (A wrong); DROP= on input is valid syntax for unused columns (C wrong); multiple output tables are allowed (D wrong). ✔
```

**Why the other options are wrong:**

- **A.** Input data set options act before processing.
- **C.** DROP= is valid on input; KEEP= has the same timing.
- **D.** A DATA statement can name several output tables.

---

## Question 35

- **Answer:** A. A data error occurred while processing that row; a note with details is written to the log.
- **Domain:** D3 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_03_L3_P2_review.md – 3.1 Understanding DATA Step Processing (_ERROR_)

**Worked solution (two independent passes):**

```text
Pass 1: "_ERROR_ = 1 if a data error occurs for the row, otherwise 0 (a note with details goes to the log)." → A.
Pass 2: syntax errors are found at compilation, before _ERROR_ exists for any row (B); nothing in the course says the row is discarded or the step stops (C, D). ✔
```

**Why the other options are wrong:**

- **B.** Syntax errors are compile-time, not a per-row flag.
- **C.** _ERROR_ does not control output.
- **D.** _ERROR_ does not stop the step.

---

## Question 36

- **Answer:** 58.3
- **Domain:** D4 · **Difficulty:** medium · **Type:** Performance
- **Source:** CR_01_L1_P1_review.md – 1.5 Using PROC MEANS (CLASS, statistics, MAXDEC=)

**Worked solution (two independent passes):**

```text
Pass 1: South rows A02 55, A05 60, A08 60 → 175 / 3 = 58.333 → 58.3.
Pass 2: 3 × 58.3 = 174.9 ≈ 175 ✔; second decimal is 3 → rounds down. (North 272/4 = 68.0, West 199/3 = 66.3.) ✔
```

**Reference solution code:**

```sas
data shop_amt;
    set shop;
    Amount=Qty*Price;
run;

proc means data=shop_amt mean maxdec=1;
    var Amount;
    class Store;
run;
```

---

## Question 37

- **Answer:** Web
- **Domain:** D4 · **Difficulty:** easy · **Type:** Performance
- **Source:** CR_01_L1_P1_review.md – 1.5 Using PROC FREQ (ORDER=FREQ, NOCUM)

**Worked solution (two independent passes):**

```text
Pass 1: Web: A01, A04, A05, A09 = 4; Phone: A02, A06, A10 = 3; Store: A03, A07, A08 = 3 → ORDER=FREQ lists Web first.
Pass 2: 4 + 3 + 3 = 10 rows ✔; Web is the only value with the maximum count, so the tie between Phone and Store does not matter. ✔
```

**Reference solution code:**

```sas
proc freq data=shop order=freq;
    tables Channel / nocum;
run;
```

---

## Question 38

- **Answer:** 6
- **Domain:** D4 · **Difficulty:** hard · **Type:** Performance
- **Source:** CR_01_L1_P1_review.md – 1.5 Using PROC MEANS (OUTPUT, NOPRINT, WAYS); PQ 1.16; CR_03 PQ 3.03

**Worked solution (two independent passes):**

```text
Pass 1: WAYS 1 keeps one row per value of each CLASS column on its own: Store (North, South, West) = 3 + Channel (Phone, Store, Web) = 3 → 6.
Pass 2: WAYS 2 would instead give the Store×Channel combinations (9 present); WAYS 0 a single overall row. Only one-way rows are kept → 6. ✔
```

**Reference solution code:**

```sas
data shop_amt;
    set shop;
    Amount=Qty*Price;
run;

proc means data=shop_amt noprint;
    var Amount;
    class Store Channel;
    output out=summ sum=TotAmt;
    ways 1;
run;
```

---

## Question 39

- **Answer:** B. Add the LABEL option to the PROC PRINT statement.
- **Domain:** D4 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** CR_01_L1_P1_review.md – 1.5 Using PROC MEANS (custom report: "the LABEL option on PROC PRINT is required for labels to show"); PQ 1.12

**Worked solution (two independent passes):**

```text
Pass 1: course: "LABEL statement – and the LABEL option on PROC PRINT is required for labels to show". → B.
Pass 2: PQ 1.12's answer for descriptive headings is the LABEL option (proc print data=baseball_sort label;). Statement order (A), NOOBS (C) and formats (D) do not affect headings. ✔
```

**Why the other options are wrong:**

- **A.** Statement order inside the step does not matter here.
- **C.** NOOBS only removes the Obs column.
- **D.** Formats change how values look, not headings.

---

## Question 40

- **Answer:** C. Removes the procedure name heading (for example "The FREQ Procedure") from reports for the rest of the session.
- **Domain:** D4 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** CR_01_L1_P1_review.md – 1.5 Using PROC FREQ (ODS NOPROCTITLE); CR_02 Solution for Exporting Data

**Worked solution (two independent passes):**

```text
Pass 1: "ODS NOPROCTITLE; removes 'The FREQ Procedure' heading; stays off for all reports for the rest of the SAS session." → C.
Pass 2: TSA export solution uses it to remove procedure names above each output; titles are cleared with title; and destinations closed with ODS … CLOSE. ✔
```

**Why the other options are wrong:**

- **A.** TITLE text is unaffected; it is a session-wide setting for procedure titles.
- **B.** Destinations are closed with ODS <destination> CLOSE.
- **D.** Bookmark text is controlled with ODS PROCLABEL.

---

## Question 41

- **Answer:** B. ods proclabel "Claims by Year";
- **Domain:** D4 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_01_L1_P1_review.md – 1.6 Using the Output Delivery System (PDFTOC=1, ODS PROCLABEL); CR_02 Solution for Exporting Data

**Worked solution (two independent passes):**

```text
Pass 1: "change the keyword TITLE to ODS PROCLABEL → bookmarks use report titles instead of procedure names". → B.
Pass 2: TSA export: "ODS PROCLABEL '…' before each procedure … bookmarks show the PROC LABELs". PDFTOC=1 only controls how many bookmark levels are expanded. ✔
```

**Why the other options are wrong:**

- **A.** TITLE changes the report title, not the bookmark.
- **C.** PDFTOC=1 expands only the first bookmark level.
- **D.** LABEL assigns column labels.

---

## Question 42

- **Answer:** D. Two worksheets (one per report); the titles are not shown by default.
- **Domain:** D4 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_01_L1_P1_review.md – 1.6 Using the Output Delivery System (ODS EXCEL: one worksheet per report, titles not shown by default); PQ 1.17

**Worked solution (two independent passes):**

```text
Pass 1: "ODS EXCEL … one worksheet per report, tabs named after procedures, titles not shown by default." → D.
Pass 2: PQ 1.17 answer: titles included in the spreadsheets? "No". Tab names come from procedures unless sheet names are set (C wrong); STYLE= is optional (B wrong). ✔
```

**Why the other options are wrong:**

- **A.** Each report gets its own worksheet.
- **B.** STYLE= is optional.
- **C.** Tabs are named after procedures unless you set sheet names.

---

## Question 43

- **Answer:** A. REPLACE overwrites emp_current.csv if it already exists; values that contain a comma are enclosed in quotation marks.
- **Domain:** D4 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_01_L1_P1_review.md – 1.6 Using PROC EXPORT; PQ 1.19

**Worked solution (two independent passes):**

```text
Pass 1: "REPLACE (overwrite existing file)"; "values containing a comma are enclosed in quotation marks to distinguish them from delimiters". → A.
Pass 2: PQ 1.19: fields in quotes = Name and Salary (values with commas). "Only RUN needed after." DBMS=CSV writes a comma-delimited text file. ✔
```

**Why the other options are wrong:**

- **B.** REPLACE refers to the output file, not the values.
- **C.** Only RUN is needed.
- **D.** CSV is a comma-delimited text file; Excel uses an XLSX DBMS/extension.

---

## Question 44

- **Answer:** C. tables Store*Channel / norow nocol;
- **Domain:** D4 · **Difficulty:** easy · **Type:** Multiple choice
- **Source:** CR_01_L1_P1_review.md – 1.5 Using PROC FREQ (crosstab with *, NOROW, NOCOL); PQ 1.14

**Worked solution (two independent passes):**

```text
Pass 1: "Crosstab: Customer_Continent*Order_Source (asterisk) … NOROW and NOCOL suppress row and column percentages." → C.
Pass 2: A lists two one-way tables (no asterisk); B suppresses cumulative columns, not row/column percentages; D uses a comma and NOPERCENT (overall percent). ✔
```

**Why the other options are wrong:**

- **A.** Without * these are two separate one-way tables.
- **B.** NOCUM removes cumulative columns only.
- **D.** Comma is not crosstab syntax; NOPERCENT removes the overall percent.

---

## Question 45

- **Answer:** B. title "Orders for &st";
- **Domain:** D4 · **Difficulty:** medium · **Type:** Multiple choice
- **Source:** CR_01_L1_P1_review.md – 1.5 Using PROC MEANS (macro variable in double quotation marks); 1.2 (double quotes for macro references)

**Worked solution (two independent passes):**

```text
Pass 1: "Strings containing a macro variable reference must be in double quotation marks for SAS to substitute." → B.
Pass 2: A uses single quotes → the text &st is shown literally; C has no & reference; D puts the reference outside the string. ✔
```

**Why the other options are wrong:**

- **A.** Single quotes prevent substitution – shows "&st".
- **C.** No macro reference – shows "st".
- **D.** The reference is outside the quoted string.

---

