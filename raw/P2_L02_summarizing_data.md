# P2 – Lesson 2: Summarizing Data

Source: SAS Programming 2 player (course id=235), text mode + screenshots. Captured 2026-10-28. Paraphrased; short quotes in quotation marks. Code copied from screenshots.

## 2.0 Lesson Overview
- New syntax to alter default DATA step behavior: create an accumulating column (running total); process data in groups to act when each group begins or ends.

## 2.1 Creating an Accumulating Column

### Demo: Creating an Accumulating Column (3:32) – p202d01.sas, EG debugger
```sas
data houston_rain;
    set pg2.weather_houston;
    keep Date DailyRain YTDRain;
    YTDRain=YTDRain+DailyRain;
run;
```
- Daily rainfall in Houston 2017; goal YTDRain = previous YTDRain + DailyRain. Output: YTDRain **all missing**.
- Debugger: the assignment adds missing + .01 → with the plus symbol, "a missing plus a known value is always missing" (first problem).
- Editing YTDRain to 0 in the debugger → 0.01 (correct). Iteration 2: back at the top, all new/computed columns reset to missing (Note: "By default, all computed columns are reset to missing each time that the PDV is reinitialized"); entering .01 manually → YTDRain becomes 1.3 [as stated] – accumulation of days 1 and 2.
- Two issues to solve programmatically: initial value 0, and keep the value across iterations.

### Retaining Values in the PDV (1:03) – from screenshot
- YTDRain is computed → reset to missing at reinitialization; need initial value 0 instead of missing, and keep the value instead of resetting.
- Syntax: `RETAIN column <initial-value>;`
```sas
data houston2017;
    set pg2.weather_houston;
    retain YTDRain 0;
    YTDRain=YTDRain+DailyRain;
run;
```
- RETAIN is a **compile-time** statement that sets a rule for one or more columns to keep their value each time the PDV is reinitialized, rather than resetting to missing; optionally sets an initial value in the PDV before the first iteration.

### Activity (p202a01.sas) – with answers
1. Retain TotalRain with initial value 0 → `retain TotalRain 0;`
2. Why are all TotalRain values missing after row 4? `TotalRain=TotalRain+Rain_mm;` – **Rain_mm is missing in row 5**, so all subsequent TotalRain values are missing.
3. Use SUM instead of plus:
```sas
data zurich2017;
    set pg2.weather_zurich;
    retain TotalRain 0;
    TotalRain=sum(TotalRain,Rain_mm);
run;
```
   "The SUM function ignores missing values."

### Using the Sum Statement (0:58) – from screenshot
- RETAIN + SUM-function assignment works; the DATA step offers a shortcut. Syntax: `column+expression;`
```sas
data zurich2017;
    set pg2.weather_zurich;
    TotalRain+Rain_mm;
run;
```
- Accumulating column name on the left, column or constant to add on the right. The **sum statement** automatically: (1) creates the accumulating column to the left of the plus sign and **sets the initial value to 0**; (2) automatically retains its value in the PDV; (3) adds the value of the column or constant on the right to the accumulating column for each row; (4) ignores missing values.

### Question (02_1_q2) – with answer
- Add a sum statement creating DayNum (1, 2, 3, …) to `data zurich2017; set pg2.weather_zurich; YTDRain_mm+Rain_mm; ??? run;` (sample: Rain_mm 4.3/4.8/39.9/1.8/./0 → YTDRain_mm 4.3/9.1/49/50.8/50.8/50.8, DayNum 1–6) → **`DayNum+1;`**

### Practice (02_1_p) – Level 1: Producing a Running Total; Level 2: Producing Multiple Totals; Challenge: Determining Maximum Amounts [pop-ups not opened – Gap]

## 2.2 Processing Data in Groups

### Answering Questions about Groups (0:43)
- The DATA step processes rows one at a time in input order; if the input is sorted in groups, it can process data within groups – e.g., max wind per storm; first storm in each basin; is each storm name used once per season?

### Processing Sorted Data in Groups (1:12) – from screenshot
```
PROC SORT DATA=input-table <OUT=sorted-output-table>;
    BY <DESCENDING> col-name(s);
RUN;

DATA output-table;
    SET sorted-output-table;
    BY <DESCENDING> col-name(s);
RUN;
```
- First create an output table sorted by the grouping column, then use the same BY statement in the DATA step to process in groups.
- With a BY statement, two special columns **FIRST.by-column** and **LAST.by-column** are added to the PDV (example `data storm2017_max; set storm2017_sort; by Basin; run;` → first.basin, last.basin).
- During execution they are assigned 0 or 1: FIRST. = 1 for the first row within a group, 0 otherwise; LAST. = 1 for the last row within a group, 0 otherwise. Temporary – usable before they are dropped when a row is written.

### Demo: Identifying the First and Last Row in Each Group (4:08) – p202d02.sas, EG debugger
```sas
proc sort data=pg2.storm_2017 out=storm2017_sort(keep=Basin Name);
    by Basin;
run;

data storm2017_max;
    set storm2017_sort;
    by Basin;
    *First_Basin=first.basin;
    *Last_Basin=last.basin;
run;
```
- First 20 rows of the sorted table have Basin = EP. First.Basin and Last.Basin are in the PDV, temporary, automatically dropped before writing each row.
- Row 1: First.Basin = 1; SAS **looks ahead** to the next row and sees it is not the last EP → Last.Basin = 0. After SET executes, SAS skips to RUN – BY is a **compile-time** statement that adds the First./Last. variables.
- Iteration 2: still EP → both 0. Watchpoint on Last.Basin: stops at _N_ = 20 (last EP row: First 0, Last 1); at _N_ = 21 Basin changes to NA and First.Basin = 1.
- Uncommenting the assignments saves the values in permanent columns: row 21 FIRST.Basin = 1; row 37 LAST.Basin = 1. Normally you don't save them permanently.

### Activity (p202a03.sas) – with answers
1. Sort rows within each Basin by MaxWindMPH: `proc sort data=pg2.storm_2017 out=storm2017_sort; by Basin MaxWindMPH; run;` → the storm with the highest wind is **the last row within each value of Basin**.
2. Add `where last.Basin=1;` right after BY in the DATA step to keep only the last row per Basin – does it run? **No, an error is generated in the log.**

### Subsetting Rows in the Execution Phase (2:29)
- `WHERE expression;` is compile-time: rules for which rows are read **into** the PDV → must use columns that exist in the input table (SET). FIRST./LAST. are not in the input table (assigned after a row is read) → can't be used in WHERE; subset during execution instead.
- `IF expression;` = **subsetting IF**, an executable statement processed in execution in code order; expression can use any PDV values. True → remaining statements run (including explicit OUTPUT or the implicit output at the end). Not true → processing for that iteration stops immediately, likely skipping the output, row not written.
```sas
data storm2017_max;
    set storm2017_sort;
    by Basin;
    if last.Basin=1;
    StormLength=EndDate-StartDate;
    MaxWindKM=MaxWindMPH*1.60934;
run;
```
- If last row for the Basin → StormLength and MaxWindKM computed, implicit output/return. Else remaining statements (incl. implicit output) skipped. The subsetting IF filters output rows **and** prevents unnecessary statements from executing.

### Activity (p202a04.sas) – with answers
1. Change the WHERE statement to a subsetting IF → **five rows, one for each value of Basin**.
2. Move the subsetting IF just before RUN → **five rows, the same**.
3. Optimal placement: "Use the subsetting IF statement as early as possible so that SAS processes additional statements only for rows that will be written to the output table" (IF last.Basin=1 right after BY).

### Demo: Creating an Accumulating Column within Groups (2:60) – p202d03.sas, from screenshots
```sas
data houston_monthly;
    set pg2.weather_houston;
    keep Date Month DailyRain YTDRain;
    YTDRain+DailyRain;
run;
```
- YTDRain = running total for the year (sum statement); data sorted by Month and Date.
```sas
data houston_monthly;
    set pg2.weather_houston;
    keep Date Month DailyRain MTDRain;
    by Month;
    if First.Month=1 then MTDRain=0;
    MTDRain+DailyRain;
run;
```
- BY processes groups by Month; IF resets MTDRain to 0 at the first row of each new Month group. Result: accumulates through January and "at the beginning of February MTDRain is equal to 0" [as stated].

### Activity (p202a05.sas) – with answers
1. Rows in the output table: **365**.
2. Output only the final day of each month: add `if last.Month=1;` after `MTDRain+DailyRain;`. "These are equivalent statements": `if last.Month;` and `if last.Month then output;`
3. Rows: **12, one for each month**.

### Using Multiple BY Columns (1:14)
- Sorting by several columns sorts by the first BY column, then the second within each unique value of the first. pg2.sydney_summary (Name, Date, Rain_mm, Year, Qtr) sorted by Year then Qtr.
```sas
data sydney_summary;
    set pg2.weather_sydney;
    by Year Qtr;
run;
```
- Each BY column gets its own FIRST./LAST. variables: First.Year, Last.Year, First.Qtr, Last.Qtr. FIRST./LAST. for Qtr mark when a quarter begins/ends **within a particular year**.
- Example: row 01-2017 → First.Year 1, Last.Year 0, First.Qtr 1, Last.Qtr 0; 03-2017 → Last.Qtr 1; 12-2017 → Last.Year 1, Last.Qtr 1; 01-2018 → First.Year 1, First.Qtr 1 (not the first Qtr=1 in the table, but the first quarter 1 within 2018); 02-2018 → Last.Year 1, Last.Qtr 1 (end of shown data).

### Think about It (02_2_q4) – with answer
- When to summarize in groups with the DATA step vs PROC MEANS? DATA step: lets you do other calculations or manipulations at the same time as summarizing. PROC MEANS: might be simpler code and easy to request various statistics.

### Practice (02_2_p) – Level 1: Generating an Accumulating Column within Groups; Level 2: within Multiple Groups; Challenge: Creating Multiple Output Tables Based on Group Values [pop-ups not opened – Gap]

## 2.3 Lesson Review
- Learning More (links only): ask other SAS programmers about the DATA step; EG DATA Step Debugger; more FIRST./LAST. examples.

### Summary of Lesson 2 (Lesson Review pop-up)
- At the start of the first iteration all column values are set to missing. By default all computed columns are reset to missing at the start of each later iteration (**reinitializing the PDV**); **columns read with the SET statement automatically retain their value** in the PDV. To create an accumulating column this default must be modified: `RETAIN column <initial-value>;` or `column+expression;`.
- Processing in groups: data must first be sorted by the grouping column(s) (PROC SORT). The BY statement in the DATA step indicates the grouping; each unique BY value is a separate group. BY creates two temporary variables per BY column: First.bycol and Last.bycol (1 for the first/last row within a group, else 0). `BY <DESCENDING> col-name(s);`
- First./Last. with IF-THEN logic execute statements at the beginning or end of a group.
- The subsetting IF affects which rows are written from the PDV to the output table; expression can use PDV values. True → remaining statements run, including explicit OUTPUT or the implicit OUTPUT at RUN; not true → processing stops for that iteration, row not written. `IF expression;`

### Quiz: Lesson 2 (10 questions; read-only, NOT answered or submitted)
1. Which statement contains valid syntax for the RETAIN statement? a. `retain Year 2018;` b. `retain Year*2018;` c. `retain Year=2018;` d. `retain Year{2018};` [brackets in d as seen – UNCLEAR]
2. Which statement is false concerning the sum statement? a. It ignores missing values. b. It initially sets the accumulator column to missing. c. It adds a numeric value to an accumulator column. d. It automatically retains the value of the accumulating column.
3. Value of Count at the end of the third DATA step iteration? work.nums Tens = 10, 20, 30, 40.
```sas
data newnums;   /* first line partly hidden in screenshot – same as Q4 [UNCLEAR] */
    set nums;
    retain Count 100;
    Count+Tens;
run;
```
   a. . (missing) b. 60 c. 130 d. 160
4. Value of Count at the end of the third iteration? work.nums Tens = 10, 20, . , 40.
```sas
data newnums;
    set nums;
    Count+Tens;
run;
```
   a. . (missing) b. 20 c. 30 d. 70
5. Which step executes successfully without an error, given sashelp.class (Name, Sex, Age, Height, Weight; Height and Weight numeric)?
   - a. `data new; set sashelp.class; Ratio=Height/Weight; where Sex='M' & Ratio>0.6; run;`
   - b. `data new; set sashelp.class; where Sex='M'; Ratio=Height/Weight; where Ratio>0.6; run;`
   - c. `data new; set sashelp.class; where Sex='M'; Ratio=Height/Weight; if Ratio>0.6; run;`
   - d. `data new; set sashelp.class; if Sex='M'; Ratio=Height/Weight; where Ratio>0.6; run;`
6. Which is true given `data work.student; set sashelp.class; by Name; run;`? a. The PDV contains a temporary variable named First.Name. b. work.student contains a column named Last.Name. c. The DATA step sorts the input table by Name. d. An error is produced because BY is not permitted in the DATA step.
7. Correct values of First.Name and Last.Name if the value of Name appears only once (same program)? a. 0 and 0 b. 1 and 1 c. 1 and 0 d. 0 and 1
8. Which statement indicates to continue processing the last row of a BY group? a. `if First.JobTitle;` b. `if Last.JobTitle;` c. `where First.JobTitle=1;` d. `where Last.JobTitle=1;`
9. Which statement resets Total for each new BY group?
```sas
data RegionTotal;
    set Sales;
    by Region;
    ... add statement here ...
    Total+Sales;
    if Last.Region=1 then output;
run;
```
   a. `Total=0;` b. `if Last.Region=0 then Total=0;` c. `if First.Region=0 then Total=0;` d. `if First.Region=1 then Total=0;`
10. Values of First.City and Last.City for the third row, given `data StatePopulation; set Population; by State City; run;` and rows: NC Cary 162320; NC Durham 263016; **NC Greenville 91495** (row 3); SC Greenville 67453; SC Sumter 40723. a. 0 and 0 b. 1 and 0 c. 0 and 1 d. 1 and 1

## Gaps
- Practices (02_1_p, 02_2_p) open in pop-ups – not opened.
- Quiz answers not available (quiz not submitted, by rule).
