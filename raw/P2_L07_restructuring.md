# P2 – Lesson 7: Restructuring Tables

Source: SAS Programming 2 player (course id=235), text mode + screenshots. Captured 2026-10-28. Paraphrased; short quotes in quotation marks. Code copied from screenshots.

## 7.0 Lesson Overview
- Techniques to transpose/restructure a table: first with the DATA step, then with PROC TRANSPOSE.

## 7.1 Restructuring Data with the DATA Step

### Understanding Table Structure (0:46)
- class_test_wide: Name, Math, Reading (Alfred 82 79; Alice 71 67; Barbara 96 86) – one row per student, measures split into multiple columns = **wide** table.
- class_test_narrow: Name, TestSubject, TestScore (Alfred Math 82; Alfred Reading 79; …) – multiple rows per student, measures stacked in a single column = **narrow** table. Same information, different structure.

### Question (07_1_q1) – interactive "Check My Answer"; NOT answered
- Which table and column(s) could you use with PROC MEANS (`proc means data=???; var ???; run;`) to calculate an average for all test scores combined? a. class_test_wide, Math Reading b. class_test_narrow, TestScore

### Restructuring Data (0:36)
- When the structure isn't what you need for analytics, restructure it. With the DATA step you can read one row and write several rows, or read multiple rows and write one row.

### Demo: Creating a Narrow Table with the DATA Step (2:59) – p207d01.sas, from screenshots
```sas
data class_test_narrow;
    set pg2.class_test_wide;
    keep Name Subject Score;
    length Subject $ 7;
    Subject="Math";
    Score=Math;
    output;
    Subject="Reading";
    Score=Reading;
    output;
run;
```
- Wide input: one row per student, two score columns; goal: one row per score (two rows per student).
- Debugger: Name, Math, Reading from class_test_wide are in the PDV; Subject and Score added by assignment statements; LENGTH sets Subject's attributes (holds Reading or Math). SET loads row 1; assignments for the math test, OUTPUT writes Name, Subject, Score; assignments for reading, OUTPUT again → **two rows written at the end of the first DATA step iteration**; second iteration writes two more rows for Alice. Each student has two rows.

### Creating a Wide Table with the DATA Step (0:44) – from screenshot
- Narrow → wide (one row per student, scores in separate columns):
```sas
if TestSubject="Math" then Math=TestScore;
else if TestSubject="Reading" then Reading=TestScore;
```
- Conditional processing on TestSubject assigns TestScore to Math or Reading; other statements are needed (next activity).

### Activity (p207a02.sas) – with answers
1. Why is RETAIN necessary? "The RETAIN statement holds values in the PDV across multiple iterations of the DATA step. The last row for each student includes both test scores."
2. Subsetting to the last row per student:
```sas
data class_wide;
    set pg2.class_test_narrow;
    by name;
    retain Name Math Reading;
    keep Name Math Reading;
    if TestSubject="Reading" then Reading=TestScore;
    else if TestSubject="Math" then Math=TestScore;
    if last.name=1 then output;
run;
```
3. What must be true of the input table? "The data must be sorted by **Name**."

### Practice (07_1_p) – Level 1: DATA Step Wide to Narrow; Level 2: DATA Step Narrow to Wide; Challenge: Using Arrays to Restructure a Table [pop-ups not opened – Gap]

## 7.2 Restructuring Data with the TRANSPOSE Procedure

### The Transpose Procedure (0:24) – from screenshot
```
PROC TRANSPOSE DATA=input-table <OUT=output-table>;
    <ID col-name;>
    <VAR col-name(s);>
RUN;
```
- PROC TRANSPOSE creates an output table by restructuring values, transposing selected columns into rows; can sometimes achieve the same result as the DATA step with less code.

### Activity (p207a03.sas) – with answers (screenshots)
- PROC PRINT shows sashelp.class rows. Run PROC TRANSPOSE: (a) which columns are transposed into rows? "**Only the numeric columns** are transposed (Age, Height, and Weight)." (b) each output column represents? "Each column corresponds to a student (row) from the input table." (c) output table name? "**work.data1**" (no OUT= given).
- `proc transpose data=sashelp.class out=class_t;`
- Add `id Name;` → "The values of the ID column are assigned as column names."
- Add `var Height Weight;` → "The VAR statement limits the columns that are transposed to rows."

### Transposing Values within Groups (0:48) – from screenshots
- Narrow storm table: Season, Basin, Name, WindRank (1–4), WindMPH (AGATHA 100/95/90/85; BLAS 50/50/50/45; CELIA 65 ×4) – each Season/Basin/Name group has 4 rows.
- Wanted wide table: one row per Season/Basin/Name with Wind1–Wind4 (1980 EP AGATHA 100 95 90 85; BLAS 50 50 50 45; CELIA 65 65 65 65).
```
PROC TRANSPOSE DATA=input-table <OUT=output-table>;
    <VAR col-name(s);>
    <ID col-name;>
    <BY col-name(s);>
RUN;
```
- **BY** transposes data within groups; the input must first be **sorted by the same BY columns**; each unique combination of BY values creates **one row** in the output.

### Demo: Creating a Wide Table with PROC TRANSPOSE (4:10) – p207d02.sas, from screenshots
- Syntax: `PROC TRANSPOSE DATA=input-table OUT=output-table <PREFIX=column> <NAME=column>; <VAR column(s);> <ID column;> <BY column(s);> RUN;`
- pg2.storm_top4_narrow: multiple rows per storm (unique by Season, Basin, Name), four rows = top four wind speeds.
```sas
proc transpose data=pg2.storm_top4_narrow out=wind_rotate;
    var WindMPH;
    id WindRank;
run;
```
- **Fails**: error says wind_rotate doesn't have any columns; the log says the ID value 1 occurs twice in the input data set – "the values of the columns listed on the ID statement must be unique". Within Season/Basin/Name the WindRank values are unique → add BY:
```sas
proc transpose data=pg2.storm_top4_narrow out=wind_rotate;
    var WindMPH;
    id WindRank;
    by Season Basin Name;
run;
```
- One row per storm; WindRank values (1, 2, 3, 4) become column names for the transposed WindMPH values – not following recommended naming. Note: EG and SAS Studio set **VALIDVARNAME=ANY**, permitting names that don't follow standard rules; with **VALIDVARNAME=V7, underscores are added in front of leading numbers** or in place of spaces/special symbols.
```sas
proc transpose data=pg2.storm_top4_narrow out=wind_rotate
               prefix=Wind name=WindSource;
    var WindMPH;
    id WindRank;
    by Season Basin Name;
run;
```
- **PREFIX=Wind** inserts "Wind" before the transposed numbers (Wind1–Wind4). **NAME=WindSource** replaces the **_NAME_** column (which identifies the source column of the transposed values). WindSource has the same value in every row → not needed (useful only if transposing more than one measure).
```sas
proc transpose data=pg2.storm_top4_narrow
               out=wind_rotate(drop=_name_) prefix=Wind;
    var WindMPH;
    id WindRank;
    by Season Basin Name;
run;
```
- DROP= data set option on the output table drops _NAME_ → wide table, one row per storm, four wind measurements.

### Activity (07_2_q1) – interactive; not captured [Gap]

### Creating a Narrow Table with PROC TRANSPOSE (0:27)
- Wide → narrow: from Wind1–Wind4 per storm, transpose the values for each Season/Basin/Name → 4 rows per storm, one wind measure per row; minor adjustments to the PROC TRANSPOSE code.

### Activity (p207a05.sas) – with answers
- By default PROC TRANSPOSE transposes **all numeric columns** (Wind1–Wind4). `var Wind1 Wind2;` transposes only those. Names of the columns holding the transposed column names and values: **_NAME_ and COL1**.

### Changing Column Names (0:59) – from screenshots
```
PROC TRANSPOSE DATA=input-table <OUT=output-table>;
    <BY col-name(s);>
    <VAR col-name(s);>
RUN;
```
```sas
proc transpose data=pg2.storm_top4_wide;
    by Season Basin Name;
    var wind1-wind4;
run;
```
- Default: new columns get generic names **_NAME_** and **COL1** (AGATHA _NAME_ 1/2/3/4 [as displayed], COL1 100/95/90/85; BLAS 1 50 …).
- `PROC TRANSPOSE DATA=input-table <OUT=output-table> <NAME=column> <PREFIX=column>;`
```sas
proc transpose data=pg2.storm_top4_wide name=WindRank
               prefix=WindMPH;
    by Season Basin Name;
    var wind1-wind4;
run;
```
- NAME=WindRank names the column holding the source column names (Wind1–Wind4). PREFIX=WindMPH → the values column is **WindMPH1** (the number 1 is appended to the prefix).
```sas
proc transpose data=pg2.storm_top4_wide name=WindRank
               out=storm_rotate(rename=(col1=WindMPH));
    by Season Basin Name;
    var wind1-wind4;
run;
```
- To get exactly WindMPH: name the output with OUT= and use the **RENAME=** data set option to change COL1.

### Practice (07_2_p) – Level 1: PROC TRANSPOSE Wide to Narrow; Level 2: Narrow to Wide; Challenge: Naming Transposed Columns when the ID Column Has Duplicate Values [pop-ups not opened – Gap]

## 7.3 Lesson Review
- Learning More (links only): SAS documentation and examples for PROC TRANSPOSE; array processing to simplify DATA step restructuring.

### Summary of Lesson 7 (Lesson Review pop-up; screenshots + JS text)
- DATA step restructuring: assignment statements create new columns for stacked values; the explicit OUTPUT statement creates multiple rows per input row; DO loops can be nested.
- `PROC TRANSPOSE DATA=input-table OUT=output-table PREFIX=column <NAME=column>; <VAR columns(s);> <ID column;> <BY column(s);> RUN;`
- OUT= creates or replaces an output table. **By default, all numeric columns** in the input table are transposed into rows. VAR lists the column(s) to transpose.
- The output includes a separate column for each value of the **ID** column. **There can be only one ID column**; ID values must be **unique in the column or BY group**.
- BY transposes within groups; each unique combination of BY values creates one row. PREFIX= gives a prefix for each value of the ID column. NAME= names the column that identifies the source column containing the transposed values.

### Quiz: Lesson 7 (10 questions; read-only, NOT answered or submitted)
1. Better description for a table with Year (Yr1956, Yr1957, Yr1958) and columns Jan Feb Mar Apr May Jun (e.g., 284 277 317 313 318 374)? a. wide table b. narrow table
2. Going wide → narrow with the DATA step, which statement creates multiple rows from a single row? a. WIDE b. NARROW c. RETAIN d. OUTPUT
3. Rows in the final table if work.airwide has three rows?
```sas
data work.airnarrow;
    set work.airwide;
    Month='Jan';
    Air=Jan;
    output;
    Month='Feb';
    Air=Feb;
    output;
    Month='Mar';
    Air=Mar;
    output;
    keep Year Month Air;
run;
```
   a. 3 b. 6 c. 9 d. 12
4. Going narrow → wide with the DATA step, the KEEP statement is needed to hold values in the PDV across multiple iterations. a. True b. False
5. Which statement must be added to include only the last row per Year?
```sas
data work.airwide2(keep=Year Jan Feb Mar);
    set work.airnarrow;
    by Year;
    retain Jan Feb Mar;
    if Month='Jan' then Jan=Air;
    else if Month='Feb' then Feb=Air;
    else if Month='Mar' then Mar=Air;
    ... insert statement here ...
run;
```
   a. `output;` b. `if Last then output;` c. `if Last.Year=1 then output;` d. `if Last.Year=0 then output;`
6. Which statement is false concerning PROC TRANSPOSE? a. Columns are transposed into rows. b. By default, numeric columns are transposed. c. Use a BY statement to sort the data while transposing. d. Use a VAR statement to specify the character and numeric columns to transpose.
7. Which statements are needed (narrow → wide)? Narrow: Day, Meal, Food (Saturday Breakfast Yogurt; Saturday Lunch Sandwich; Saturday Dinner Steak; Sunday Breakfast Pancakes; Sunday Lunch Salad; Sunday Dinner Lasagna). Wide: Day, Breakfast, Lunch, Dinner. a. `by Day; var Meal Food;` b. `id Day; var Food Meal;` c. `by Day; id Food; var Meal;` d. `by Day; id Meal; var Food;`
8. Which statement(s) are needed (wide → narrow)? Wide: Day, Breakfast, Lunch, Dinner. Narrow: _NAME_, COL1, COL2 (Breakfast Yogurt Pancakes; Lunch Sandwich Salad; Dinner Steak Lasagna). a. `by Day;` b. `var Breakfast Lunch Dinner;` c. `id Day;` d. `id Day; var Breakfast Lunch Dinner;`
9. Which option renames the _NAME_ column (input _NAME_, COL1, COL2 → output Meal, COL1, COL2)? a. `_name_=Meal` b. `name=Meal` c. `prefix=Meal` d. `rename=Meal`
10. Which option renames the COL columns (Meal, COL1, COL2 → Meal, Day7, Day1)? a. `out=meals2(COL1=Day7 COL2=Day1)` b. `out=meals2(name=(COL1=Day7 COL2=Day1))` c. `out=meals2(rename=(COL1=Day7 COL2=Day1))` d. `out=meals2(prefix=(COL1=Day7 COL2=Day1))`

## Gaps
- Practices (07_1_p, 07_2_p) open in pop-ups – not opened.
- Questions 07_1_q1 and 07_2_q1/q2 interactive – not answered (07_1_q1 text captured).
- Quiz answers not available (quiz not submitted, by rule).
