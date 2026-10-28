# P2 – Lesson 1: Controlling DATA Step Processing

Source: SAS Programming 2 player (course id=235, scormid=955), text mode (Hide Video → transcript). Captured 2026-10-28. Paraphrased; short quotes in quotation marks. Code copied from screenshots.

## Course overview (non-exam)
- Welcome: course focuses on the DATA step for data preparation; also SAS procedures that shape data. Instructor Stacey Syphus.
- Practicing in This Course: main data = storm data, plus National Park Service data and SAS sample tables. Demos, Activities (short problems), Practices in 3 levels (Level 1 step-by-step, Level 2 less guidance, Challenge may need SAS Help/documentation); all practices have complete solutions.
- Setting Up Your Practice Files: [text blocked by the extension filter; setup only – not captured]

## 1.0 Lesson Overview
- Dig deeper into the DATA step: how it processes data behind the scenes; then control when and where rows are output to new tables.

## 1.1 Understanding DATA Step Processing

### DATA Step Review (0:30) – code from screenshot
```sas
data storm_complete;
    set pg2.storm_summary_small;
    length Ocean $ 8;
    drop EndDate;
    where Name is not missing;

    Basin=upcase(Basin);
    StormLength=EndDate-StartDate;

    if substr(Basin,2,1)="I"
        then Ocean="Indian";
    else if substr(Basin,2,1)="A"
        then Ocean="Atlantic";
    else Ocean="Pacific";
run;
```
- The step reads and writes tables, filters rows, computes new columns, assigns values conditionally, subsets columns – familiar code; now learn how SAS processes it.

### Activity (p201a03.sas) – question text only
- DROP EndDate appears before EndDate is used to compute StormLength: run; is EndDate in the output? Are StormLength values generated?
- Move DROP to just before RUN: did results change?
- Ocean has length 8 in PROC CONTENTS; move the LENGTH statement between DROP and RUN: did results change? [answers not shown in text]

### DATA Step Processing (0:56)
- Order of some statements matters, others can go anywhere – explained by how the DATA step works. Two phases: **compilation** (SAS prepares code, establishes data attributes and rules for execution) and **execution** (SAS follows those rules to read, manipulate, write data).

### DATA Step Processing: Compilation (3:06)
- SAS first checks for syntax errors; if none, builds the **Program Data Vector (PDV)** – an area of memory holding each column referenced in the step with attributes name, type, length. Looks like a one-row table because execution holds/manipulates one row at a time.
- Compilation also sets rules for the PDV (which columns will be dropped, which input rows will be read) and finally creates the **descriptor portion** (table metadata).
- Example uses the code above (unconditional statements on one line each). DATA statement creates Storm_Complete in Work. SAS passes through the step **sequentially**; SET is first, so all columns of storm_summary_small are added with name/type/length: Name $15, Basin $2, MaxWind N8, StartDate N8, EndDate N8.
- Other statements defining new columns add them too: LENGTH defines Ocean $8; StormLength is numeric length 8 (from the arithmetic expression).
- After a column and its attributes are established in the PDV they **cannot be changed** – that's why LENGTH must come before the IF-THEN statements; otherwise `Ocean="Indian"` would define length 6.
- IF expressions are not evaluated during compilation; columns are added in the order they occur in the code.
- Compile-time statements: **DROP** does not remove the column from the PDV – it marks it with a **drop flag**, so EndDate is still available to compute StormLength but dropped from output. **WHERE** defines which rows will be read into the PDV during execution.
- Descriptor portion of work.storm_complete: Name, Basin, MaxWind, StartDate, Ocean, StormLength – EndDate not included.

### DATA Step Processing: Execution (1:16)
- Execution = SAS reads data, processes it in the PDV, outputs it to a new table. Acts like an **automatic loop**: first pass, SET reads row 1, other statements run in sequence manipulating PDV values.
- At RUN (end of step) an **implied OUTPUT** writes the PDV (minus drop-flagged columns) as a row; then SAS loops back to the top, **resets computed columns to missing**, and repeats until all input rows are read.
- Compile-time statements (DROP, LENGTH, WHERE) are not executed for each row, but their rules affect the output table.

### Demo: DATA Step Processing in Action (5:34) – Enterprise Guide DATA step debugger, p201d01.sas (code = the storm_complete step above)
- DATA step markers for debugging (Debug) toolbar button enables the debugger icon next to each DATA step.
- After compilation the PDV shows Variable/Value/Watch; all columns read from storm_summary_small start missing.
- Two extra PDV columns during execution: **_ERROR_** = 0 by default, set to 1 when a data error is encountered (e.g., a value that cannot be read or calculated); **_N_** starts at 1 and increments each time the step loops past the DATA statement = number of iterations.
- Executing SET: WHERE rule (Name not missing) → first two input rows skipped, the third row is read, but _N_ is still 1 (first iteration). Name, Basin, MaxWind, StartDate, EndDate filled.
- LENGTH, DROP, WHERE are compile-time → skipped in execution. Basin already uppercase; StormLength = 6; IF/ELSE → Ocean = Pacific.
- RUN = step boundary → implicit output writes the PDV as row 1 of storm_complete, then return to top. (While debugging, the output table is not created.)
- Iteration 2: _N_ = 2; columns read by SET keep their values until overwritten; computed columns Ocean and StormLength reset to missing = **reinitializing the PDV**. Basin SI → Ocean "Indian", remaining ELSEs skipped; RUN → _N_ = 3, PDV reinitialized.

### Viewing Execution in the Log (1:00) – from screenshot
```sas
PUTLOG _ALL_;
PUTLOG column=;
PUTLOG "message";
```
- Without the EG debugger, add PUTLOG statements at strategic points to examine the PDV. `_ALL_` writes all PDV columns and values to the log; `column=` writes specific columns; or a message.
```sas
data storm_complete;
    set pg2.storm_summary_small(obs=2);
    putlog "PDV After SET Statement";
    putlog _all_;
    ...
```
- OBS= data set option limits the rows SET reads → only two iterations. Log:
```
PDV After SET Statement
Name=AGATHA Basin=EP MaxWind=115 StartDate=09JUN1980
EndDate=15JUN1980 Ocean=  StormLength=. _ERROR_=0 _N_=1
PDV After SET Statement
Name=ALBINE Basin=SI MaxWind=. StartDate=27NOV1979
EndDate=06DEC1979 Ocean=  StormLength=. _ERROR_=0 _N_=2
```

### Activity (p201a04.sas) – with answers (Show Answer)
- Add before RUN: `putlog "PDV Before RUN statement"; putlog _all_;`
- StormLength at the end of iteration 2 = **9**.
- Adding `NOTE:` (uppercase, with colon) at the start of the PUTLOG text (`putlog "NOTE: PDV After SET Statement";`) → the text is **color-coded as a note** in the log.

### Practice (01_1_p)
- Two alternative practices (EG debugger or PUTLOG); open in pop-up windows – not opened [Gap].

## 1.2 Directing DATA Step Output

### Controlling DATA Step Processing (1:20)
- Default rules are sometimes fine; sometimes you alter them. Implicit output: read one row, manipulate, write it. sashelp.shoes (Region, Product, Subsidiary, Sales; e.g., Africa Boot Addis Ababa $29,761). Goal: forecast for each of the next 3 years with 5% annual growth. Q: will this write three rows per row read?
```sas
data forecast;
    set sashelp.shoes;
    keep Region Product Subsidiary Year ProjectedSales;
    format ProjectedSales dollar10.;
    Year=1;
    ProjectedSales=Sales*1.05;
    Year=2;
    ProjectedSales=ProjectedSales*1.05;
    Year=3;
    ProjectedSales=ProjectedSales*1.05;
run;
```

### Activity (p201a05a/b.sas) – answer
- Log: "There were 395 observations read from the data set SASHELP.SHOES." / "The data set WORK.FORECAST has 395 observations and 5 variables." Final PDV values Year=3 and ProjectedSales for year 3; the implicit output at the end writes the PDV.

### Implicit and Explicit Output (1:09)
- By default SAS executes statements sequentially; at the end an **implicit OUTPUT** writes the PDV as a row, then an **implicit RETURN** loops back to the top for the next row. In the forecast program the implicit OUTPUT happens only once → year-3 values.
- **OUTPUT;** – explicit statement forces writing the PDV at specific points. If an explicit OUTPUT appears **anywhere** in the step, there is **no implicit OUTPUT** at the end; the implicit RETURN still returns to the top.

### Activity (p201a06.sas) – answers
- OUTPUT after each ProjectedSales assignment → 3 × 395 = **1,185 rows**.
- Comment out the final OUTPUT → rows with Year=3 are **not** written: "When an explicit OUTPUT statement is in a DATA step, the implicit OUTPUT is disabled."

### Sending Output to Multiple Tables (0:27)
- OUTPUT controls when and **where**: list several tables on the DATA statement, then `OUTPUT table-name;`.

### Demo: Directing Row Output (3:12) – p201d02.sas, from screenshots
```sas
data indian atlantic pacific;
    set pg2.storm_summary;
    length Ocean $ 8;
    Basin=upcase(Basin);
    StormLength=EndDate-StartDate;
    MaxWindKM=MaxWindMPH*1.60934;
    if substr(Basin,2,1)="I" then do;
        Ocean="Indian";
        output indian;
    end;
    else if substr(Basin,2,1)="A" then do;
        Ocean="Atlantic";
        output atlantic;
    end;
    else do;
        Ocean="Pacific";
        output pacific;
    end;
    drop MaxWindMPH;
run;
```
- Started from storm_complete (single table); DATA statement changed to three tables; IF-THEN/ELSE changed to DO blocks with OUTPUT to the matching table. Log: three tables, each 10 columns and a different number of rows.
- DROP MaxWindMPH statement → each table has **9** columns (dropped from all three tables).

### Controlling Column Output (0:31) – from screenshot
- `DROP col1 col2 …;` / `KEEP col1 col2 …;` statements flag the column for dropping/keeping in the PDV and apply to **all** tables on the DATA statement.
```sas
data sales_high
     sales_low;
    set sashelp.shoes;
    ...
    drop Inventory Returns;
run;

data sales_high(drop=Returns)
     sales_low(drop=Inventory);
    set sashelp.shoes;
    ...
run;
```
- `table(DROP=col1 col2 …)` / `table(KEEP=col1 col2 …)` data set options give a unique column list per output table; the PDV tracks which columns to drop from which table.

### Demo: Directing Column Output (3:09) – p201d03.sas, EG debugger, from screenshots
- Start: the indian/atlantic/pacific program (with MaxWindKM). Keep one or both wind columns depending on the table:
  `data indian(drop=MaxWindMPH) atlantic(drop=MaxWindKM) pacific;`
- Debugger: MaxWindMPH and MaxWindKM are both in the PDV → available for processing. Output: MaxWindMPH dropped from indian, MaxWindKM from atlantic, pacific has all columns.
- MinPressure not needed anywhere: `set pg2.storm_summary(drop=MinPressure);` → debugger shows MinPressure **not in the PDV** (not read). Dropped from every table.
- Note: "The placement of the DROP= and KEEP= data set options controls what data is read into the PDV, as well as what is written out."

### Columns in the PDV (0:36) – from screenshot
- `SET table(DROP=…)` / `SET table(KEEP=…)`: excluded columns are **not read into the PDV**, so not available for processing.
- `DATA table(DROP=/KEEP=…)` or DROP/KEEP statements: columns **are in the PDV and CAN be used** for processing; they are flagged to be dropped when an implicit or explicit OUTPUT is reached.

### Question (01_2_q3) – with answer
- Q: easiest way to drop EndDate from all three tables in `data indian(drop=MaxWindMPH) atlantic(drop=MaxWindKM) pacific; set pg2.storm_summary; StormLength=EndDate-StartDate; …` → A: "When you want to drop a column from all output tables, use the DROP statement" – add `drop EndDate;` (EndDate still usable for StormLength).

### Practice (01_2_p) – Level 1: Conditionally Creating Multiple Output Tables; Level 2: Conditionally Creating Columns and Output Tables; Challenge: Processing Statements Conditionally with SELECT-WHEN Groups [pop-ups not opened – Gap]

## 1.3 Lesson Review
- Learning More (links only): DATA step programming documentation; multi-threaded DATA step code in SAS Viya; alternative syntax to IF-THEN/ELSE similar to SQL.

### Summary of Lesson 1 (Lesson Review pop-up; JS text + screenshots)
- DATA step processed in two phases: compilation and execution. During compilation SAS creates the PDV and establishes data attributes and rules for execution.
- PDV = memory area established at compilation; includes all columns that will be read or created with their attributes; used in execution to hold and manipulate one row at a time.
- During execution SAS reads, manipulates, writes data; all data manipulation is performed in the PDV. `PUTLOG _ALL_; PUTLOG column=; PUTLOG "message";`
- Directing output: `OUTPUT;` `DATA table1 <table2 …>;` `OUTPUT table1 <table2 …>;` – the end of a DATA step causes an implicit OUTPUT; explicit OUTPUT controls when and where each row is written and **disables** the implicit OUTPUT; one DATA step can create multiple tables; OUTPUT followed by a table name writes the PDV to that table.
- `table(DROP=col1 col2…)` / `table(KEEP=…)` can be added on any table in the DATA statement (DROP= → listed columns not added to that output table; KEEP= → only listed columns added). Dropped columns are flagged in the PDV and not dropped until the row is output → still available for processing.
- DROP= or KEEP= in the SET statement controls the columns read into the PDV; a column not read into the PDV is not available for processing.

### Quiz: Lesson 1 (10 questions; read-only, NOT answered or submitted)
1. Which statement is false concerning the compilation phase of the DATA step? a. Initial values are assigned to the columns. b. The PDV is created. c. The DATA step is checked for syntax errors. d. The descriptor portion of the output table is created.
2. Which statement is not a compile-time-only statement? a. KEEP b. LENGTH c. SET d. WHERE
3. Which statement is true concerning the execution phase? a. Data is processed in the PDV. b. An implied OUTPUT occurs at the top of the DATA step. c. An implied REINITIALIZE occurs at the bottom of the DATA step. d. Columns read from the input table are set to missing when SAS returns to the top of the DATA step.
4. The DATA step debugger in SAS Enterprise Guide can be used with DATA and PROC steps. a. True b. False
5. Which PUTLOG statements create this log? `Name=Alfred Height=69 Weight=112.5 Ratio=0.61 _ERROR_=0 _N_=1` / `Ratio=0.61` — a. `putlog all; putlog Ratio;` b. `putlog all; putlog Ratio=;` c. `putlog _all_; putlog Ratio;` d. `putlog _all_; putlog Ratio=;`
6. Input table Shipping has 5 rows and 3 columns (Product, BoxSize, Rate). Rows and columns in ShippingZones?
```sas
data ShippingZones;
    set Shipping;
    Zone=1;
    output;
    Zone=2;
    Rate=(Rate*1.5);
run;
```
   a. 5 rows and 3 columns b. 5 rows and 4 columns c. 10 rows and 3 columns d. 10 rows and 4 columns
7. sashelp.cars has 428 rows: 123 with Origin = Europe and 305 with other values.
```sas
data Europe Other;
    set sashelp.cars;
    if Origin='Europe' then
       output Europe;
    output Other;
run;
```
   How many rows in Other? a. 0 rows b. 123 rows c. 305 rows d. 428 rows
8. Which statement is false? a. The KEEP statement names the columns to include from the input table. b. The DROP statement names the columns to exclude from the output table. c. The KEEP= option in the DATA statement names the columns to include in the output table. d. The DROP= option in the SET statement names the columns to exclude from being read into the PDV.
9. Which columns are in the final table work.boots?
```sas
data work.boots(drop=Product);
    set sashelp.shoes(keep=Product Subsidiary Sales Inventory);
    where Product='Boot';
    drop Sales Inventory;
    Total=sum(Sales,Inventory);
run;
```
   a. Subsidiary b. Subsidiary and Total c. Product and Subsidiary d. Product, Subsidiary, Sales, and Inventory
10. Result of:
```sas
data work.boots;
    set sashelp.shoes(keep=Product Subsidiary);
    where Product='Boot';
    NewSales=Sales*1.25;
run;
```
   a. work.boots with three columns. b. work.boots with four columns. c. Error due to invalid syntax for the KEEP= option. d. Error because the Sales column is not read in from sashelp.shoes.

## Gaps
- Setting Up Your Practice Files page text blocked by the extension filter (setup only).
- Activity p201a03 (01_1_q1) answers not revealed (question text captured).
- Practices (01_1_p, 01_2_p) open in pop-ups – not opened.
- Quiz answers not available (quiz not submitted, by rule).
