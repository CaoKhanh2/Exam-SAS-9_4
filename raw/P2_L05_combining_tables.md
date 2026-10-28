# P2 – Lesson 5: Combining Tables

Source: SAS Programming 2 player (course id=235), text mode + screenshots. Captured 2026-10-28. Paraphrased; short quotes in quotation marks. Code copied from screenshots.

## 5.0 Lesson Overview
- Combining tables with the DATA step: concatenate tables, merge tables, identify matching and nonmatching rows.

## 5.1 Concatenating Tables

### Concatenating Tables with Matching Columns (1:04)
```
DATA output-table;
    SET input-table1 input-table2 ...;
    <. . . additional statements . . .>
RUN;
```
- Same column names, lengths, types → list the tables in SET. SAS reads all rows of the first table and writes them, then all rows of the second, etc. Other statements in the step manipulate rows from all tables.
```sas
data class_current;
    set sashelp.class pg2.class_new;
run;
```
- sashelp.class (19 rows) + pg2.class_new (Kelly, Scott, Trevor) → class_current has **22 rows**; the three new students at the end.

### Demo: Concatenating Tables (3:08) – p205d01.sas, from screenshots
- Syntax: `DATA output-table; SET input-table1(rename=(current-colname=new-colname)) input-table2 ...; RUN;`
```sas
data storm_complete;
    set pg2.storm_summary pg2.storm_2017;
    Basin=upcase(Basin);
run;

proc sort data=storm_complete;
    by descending StartDate;
run;
```
- storm_summary = one row per storm 1980–2016; storm_2017 = 2017 season. Log: work.storm_complete **3172 rows and 9 columns**, sorted by descending StartDate.
- 2017 rows: Year populated (2017), Location has values, Season missing; storm_summary rows (from row 55): Season populated, Year and Location missing → same information, different names.
```sas
data storm_complete;
    set pg2.storm_summary pg2.storm_2017(rename=(Year=Season) drop=Location);
    Basin=upcase(Basin);
run;
```
- RENAME= Year → Season so values align; DROP= Location. Result: **3172 rows and 7 columns**; Location and Year not included; Season has 2017 and all prior years.

### Activity (p205a01.sas) – with answers
1. Concatenate sashelp.class and pg2.class_new2: differences between the first 19 rows and the last 3? "Student names are in separate columns (Name and Student). Height and Weight are missing in the last 3 rows."
2. `data class_current; set sashelp.class pg2.class_new2(rename=(Student=Name)); run;` → log: "WARNING: Multiple lengths were specified for the variable Name by input data set(s). This can cause truncation of data."
3. PROC CONTENTS: "Name has a length of 8 in sashelp.class. Student has a length of 9 in pg2.class_new2."

### Handling Column Attributes (0:45) – from screenshot
- With multiple tables in SET, columns from the **first table** are added to the PDV with their attributes (Name $8). When SAS reads the second table, attributes of columns already in the PDV **cannot be changed** – Name's length is already set.
```sas
data class_current;
    length Name $ 9;
    set sashelp.class
        pg2.class_new2(rename=(Student=Name));
run;
```
- The LENGTH statement explicitly defines Name as character length 9; it must come **before SET** so the length is established in the PDV before Name is read from sashelp.class.

### Practice (05_1_p) [pop-up not opened – Gap]

## 5.2 Merging Tables

### What is a Merge? (1:43)
- Merging (joining) combines columns from multiple tables. PROC SQL can join, but the DATA step merges efficiently; they work differently behind the scenes, each has strengths – know both.
- A merge matches values of a **common column**. Scenarios: **one-to-one** (each row matches a single row in the other table), **one-to-many** (one row matches one or more rows in the other table), and **non-matches**.
- Party example: Invited vs Attending lists – matching is hard when unsorted, easy when both lists are alphabetized.

### Think About It (05_2_q1) – with answer
- Two unsorted lists are difficult to match; when both are sorted they are much easier to match up (sorted Invited: Caroline, Drew, George, Kristin, Lani, Mansfield, Michael; Attending: Caroline, Drew, Kristin, Lani, Michael).

### Processing a One-to-One Merge (2:29)
- sashelp.class (Name, Sex, Age, Height, Weight) and pg2.class_teachers (Name, Grade, Teacher), both sorted by Name; each Name in both → one-to-one.
```
DATA output-table;
    MERGE input-table1 input-table2 ...;
    BY BY-column(s);
RUN;
```
- Use **MERGE** instead of SET; list multiple tables as long as each has the common column in the **BY** statement. With BY, the data must be **in sorted order** – typically PROC SORT the inputs by the matching column first.
```sas
data class2;
    merge sashelp.class pg2.class_teachers;
    by name;
run;
```
- Result class2: Name, Sex, Age, Height, Weight, Grade, Teacher (Alfred M 14 69 112.5 8 Thomas …).
- SAS compares rows sequentially, matching on the common column. **Compilation:** all columns of the **first** table on MERGE with attributes are added to the PDV; then any additional columns from the second table not already in the PDV; then new columns from other statements; then other compile-time statements.
- **Execution:** compare the BY value of the first row in each table; if they match, both rows are read into the PDV, statements execute, row written at the end; return to top, advance to row 2 in both tables, and so on until all rows are read from every table.

### Activity (p205a02.sas) – with answers
1. teachers_sort has **one row per Name**; test2_sort has **two rows per Name**.
2. `data class2; merge teachers_sort test2_sort; by Name; run;` → **38 rows**, two rows per Name.

### Processing a One-To-Many Merge (1:29)
```sas
data class2;
    merge teachers_sort test2_sort;
    by name;
run;
```
- teachers_sort: Alfred 8 Thomas; Alice 7 Evans; Barbara 6 Smith. test2_sort: Alfred Math 82; Alfred Reading 79; Alice Math 71; Alice Reading 67 [header of the score column displayed as "Teacher"; text calls it TestScore].
- Rows 1 match → both read into the PDV, implicit output, return. "Similar to the SET statement, values read from the tables in the MERGE statement are **automatically retained**."
- Next rows: BY values don't match, so SAS checks whether either matches the current PDV value; Alfred in test2_sort matches → reads that row, overwriting Name, Subject, TestScore; Grade and Teacher from the first table are **retained**; implicit output.
- Next iteration neither matches the PDV. When SAS has finished reading all values for a BY group, the **PDV is reinitialized** (all columns set to missing); BY values compared again; match → both rows read.

### Demo: Merging Tables (3:20) – p205d02.sas, from screenshots
```
PROC SORT DATA=input-table OUT=output-table;
    BY BY-column;
RUN;

DATA output-table;
    MERGE input-table1 input-table2 ...;
    BY BY-column(s);
RUN;
```
```sas
proc sort data=pg2.storm_summary out=storm_sort;
    by Basin;
run;

proc sort data=pg2.storm_basincodes out=basincodes_sort;
    by BasinCode;
run;

data storm_summary2;
    merge storm_sort basincodes_sort(rename=(BasinCode=Basin));
    by Basin;
run;
```
- storm_sort has **3118 rows**; basincodes_sort has **6 rows** (lookup table of two-letter basin codes and basin names). Code column named Basin in one table and BasinCode in the other → RENAME= on basincodes_sort. "This will be a one-to-many merge."
- BasinName values matched to each Basin code. At the end of storm_summary2, rows with lowercase **na** have missing BasinName – lowercase na occurs only in storm_sort, not in basincodes_sort.

## 5.3 Identifying Matching and Nonmatching Rows

### Merging Tables with Nonmatching Rows (2:14)
```sas
data class2;
    merge pg2.class_update pg2.class_teachers;
    by name;
run;
```
- class_update: Alfred, Alice, Barbara, **David**, Henry … ; class_teachers: Alfred, Alice, Barbara, **Carol**, Henry … (Carol moved out, David moved in; change made only in class_update).
- Output class2: Carol row has missing Sex/Age/Height/Weight with Grade 8, Teacher Thomas; David row has his class values with missing Grade/Teacher. "Although both of the input tables have **19 rows**, the output table class2 has **20 rows**."
- Execution: after the Barbara match is output, the next BY values don't match Barbara → **entire PDV set to missing**. SAS compares the BY values, they don't match → reads the row from the table whose BY value **comes first in sorted sequence** (Carol before David); writes Name, Grade, Teacher; other columns stay missing.
- Next iteration: still on David in class_update (not yet read); compare with next unread in class_teachers (Henry); either is a new BY group → PDV reset; David first → read from class_update; Grade/Teacher missing. Then Henry matches Henry, and so on until all rows are read.

### Identifying Matches and Nonmatches (1:43) – from screenshot
```
DATA output-table;
    MERGE input-table1(IN=variable)
          input-table2(IN=variable) ...;
    BY BY-column(s);
RUN;
```
```sas
data class2;
    merge pg2.class_update(in=inUpdate)
          pg2.class_teachers(in=inTeachers);
    by name;
run;
```
- **IN=** data set option follows a table in MERGE and names a **temporary** variable added to the PDV (included during execution, **not written** to the output). Each IN= variable is associated with the table it follows; assigned **0 or 1** – 0 = that table does not include the BY value for that row, 1 = it does.
- class2 rows: Alfred/Alice/Barbara inUpdate 1, inTeachers 1; Carol 0 and 1; David 1 and 0.

### Question (05_3_q1) – interactive "Check My Answer"; NOT answered
- Which statement writes only matching rows? (`merge pg2.class_update(in=inUpdate) pg2.class_teachers(in=inTeachers); by name; ???`) a. `where inUpdate=1 and inTeachers=1;` b. `where inUpdate=1 or inTeachers=1;` c. `if inUpdate=1 and inTeachers=1;` d. `if inUpdate=1 or inTeachers=1;`

### Demo: Merging Tables with Nonmatching Rows (6:55) – p205d03.sas, from screenshots
- Syntax: `DATA output-table; MERGE input-table1(IN=var1) input-table2(IN=var2) ...; BY BY-column(s); RUN;`
- pg2.storm_damage: 38 rows (storms with costs exceeding $1 billion): event, date, summary, cost – but not basin name, max wind, minimum pressure (those are in pg2.storm_final, over 3,000 rows). Goal: keep only matching rows.
- Storm_Damage: Event = type + storm name (last word, proper case), Date = SAS date. Storm_Final: Name in **uppercase**, Season = year. Season and Name must be derived from Date and Event.
```sas
proc sort data=pg2.storm_final out=storm_final_sort;
    by Season Name;
run;

data storm_damage;
    set pg2.storm_damage;
    Season=Year(date);
    Name=upcase(scan(Event, -1));
    format Date date9. Cost dollar16.;
    drop event;
run;

proc sort data=storm_damage;
    by Season Name;
run;
```
- Storm names can be reused across years, but Name is unique within a Season → sort/merge by **both Season and Name**.
```sas
data damage_detail;
    merge storm_final_sort storm_damage;
    by Season Name;
    keep Season Name BasinName MaxWindMPH MinPressure Cost;
run;
```
- Over 3,000 rows (matches and non-matches); most Cost values missing (Cost from Storm_Damage, only 38 storms); row 4 (Allen) is in both tables.
```sas
data damage_detail;
    merge storm_final_sort storm_damage(in=inDamage);
    by Season Name;
    keep Season Name BasinName MaxWindMPH MinPressure Cost;
    if inDamage=1;
run;
```
- inDamage = 1 for rows read from storm_damage, else 0; subsetting IF → if 1, continue and output; otherwise move to next row. Result: **38 rows** – the same 38 storms, plus BasinName, MaxWindMPH, MinPressure from Storm_Final.

### Activity (p205a04.sas) – with answer
```sas
data damage_detail storm_other(drop=Cost);
    merge storm_final_sort(in=inFinal)
          storm_damage(in=inDamage);
    keep Season Name BasinName MaxWindMPH MinPressure Cost;
    by Season Name;
    if inDamage=1 and inFinal=1 then output damage_detail;
    else output storm_other;
run;
```
- storm_other (all nonmatching rows, Cost dropped only from storm_other): **3,054 rows**.

### Merging Tables with Matching Column Names (1:08) – from screenshots
- weather_sanfran2016 and weather_sanfran2017: Month ($14, e.g., "01- January") and AvgTemp (N8) in both.
```sas
data weather_sanfran;
    merge pg2.weather_sanfran2016 pg2.weather_sanfran2017;
    by month;
run;
```
- SAS reads values into the PDV in the order tables are listed on MERGE: January 52.7 (2016) is read, then the 2017 value 50.6 **overwrites** it before the implicit output → only the 2017 values survive.
```sas
data weather_sanfran;
    merge pg2.weather_sanfran2016(rename=(AvgTemp=AvgTemp2016))
          pg2.weather_sanfran2017(rename=(AvgTemp=AvgTemp2017));
    by month;
run;
```
- To keep both, give the non-BY columns unique names with RENAME= → Month, AvgTemp2016, AvgTemp2017.

### Merging Tables without a Common Column (1:27) – from screenshots
- class_update and class_teachers share Name; class_rooms (Teacher, Room: Evans 5, Garcia 8, Jones 12, Smith 1, Thomas 3, Williams 9) shares only Teacher with class_teachers.
- DATA step: break into multiple steps:
```sas
data update_teachers;
    merge pg2.class_update
          pg2.class_teachers;
    by Name;
run;

proc sort data=update_teachers;
    by Teacher;
run;

data class_combine;
    merge update_teachers
          pg2.class_rooms;
    by Teacher;
run;
```
- (1) merge the two tables sharing a column (already sorted by Name) into an intermediate table; (2) sort the intermediate table by the common column with the third table (class_rooms already sorted by Teacher); (3) merge. Final: Name … Grade Teacher Room (David with missing Grade/Teacher/Room; Alice 7 Evans 5; Jane 5 Garcia 8 …).
- Joining three or more tables without a common column is much easier with PROC SQL:
```sas
proc sql;
create table class_combine as
select u.*, t.Grade, t.Teacher, r.Room
    from pg2.class_update as u
    inner join pg2.class_teachers as t
        on u.Name=t.Name
    inner join pg2.class_rooms as r
        on t.Teacher=r.Teacher;
quit;
```

### DATA Step Merge and PROC SQL Join (0:38)
- Different processing methods, different strengths: creating multiple tables of matches and non-matches can be done in a **single DATA step** (PROC SQL would need multiple queries); joining three tables without a single common column can be done in **one PROC SQL query**. Valuable to know both.

### Practice (05_3_p) [pop-up not opened – Gap]

## 5.4 Lesson Review

### Summary of Lesson 5 (Lesson Review pop-up; screenshots + JS text)
- Concatenating: `DATA output-table; SET input-table1(rename=(current-colname=new-colname)) input-table2 ...; RUN;` Multiple tables in SET are concatenated; SAS reads all rows of the first table, then the second, etc. Columns with the same name are automatically aligned; **column properties in the new table are inherited from the first table listed in SET**. Columns not in all tables are also included. RENAME= aligns columns. Additional statements after SET manipulate the data.
- Merging: if needed, `PROC SORT DATA=input-table OUT=output-table; BY BY-column; RUN;` then `DATA output-table; MERGE input-table1 input-table2 ...; BY BY-column(s); RUN;` – all tables in MERGE must be sorted by the same BY column(s); MERGE combines rows where BY values match; works for one-to-one and one-to-many.
- Identifying matches/nonmatches: `MERGE input-table1(IN=var1) input-table2(IN=var2) ...;` – **by default, both matches and nonmatches are written** to the output in a DATA step merge. IN= variables are in the PDV during execution, not written to output; each relates to the table it follows; 0 = the table did not include the BY value for that row, 1 = it did. Subsetting IF or IF-THEN logic subsets matching/nonmatching rows.

### Quiz: Lesson 5 (10 questions; read-only, NOT answered or submitted)
1. Which is true concerning concatenating tables? a. All tables must have the same number of columns. b. Columns in all tables must have matching names and lengths. c. Tables must be in the same library. d. Missing values are generated for columns that exist in one input table and not in another.
2. Which statement renames the existing column Location in work.travel as Destination? a. `set vacations(rename=(Location=Destination)) travel;` b. `set vacations travel(rename=(Destination=Location));` c. `set vacations travel(rename=(Location=Destination));` d. `set vacations travel(rename(Destination=Location));`
3. Which is true concerning merging with matching rows? a. MERGE must refer to temporary input tables. b. The columns in the BY statement can be in only one of the tables. c. Only two input tables can be specified in MERGE. d. The input tables must be sorted by the columns in the BY statement.
4. Rows in output table both? agetable: Bob 12, Sue 15; foodtable: Bob Pizza, Bob Cupcakes, Sue Burgers, Sue Grapes, Sue Brownies. `data both; merge agetable foodtable; by Name; run;` a. two b. three c. four d. five
5. Rows in empsauc? empsau: Togar E 121150; Kylie S 121151; Birin W 121152. phonec: 121150; 121152; 121153 (phones). `data empsauc; merge empsau phonec; by EmpID; run;` a. two b. three c. four d. five
6. Result of the step? donors1 (ID Type Units): 2304 O 16; 1129 A 48; 1129 A 50; 2486 B 63. donors2 (ID Code Units): 1129 63 32; 2304 61 45; 1387 64 67. `data combine; merge donors1 donors2; by ID; run;` a. combine created with four columns and five rows. b. Fails because BY column ID is not properly sorted. c. Fails because Units is in both tables and not the BY column. d. Fails because of duplicate ID values within donors1.
7. Which best describes the output rows? `data bonuses; merge managers(in=M) staff(in=S); by EmpID; if M=0 and S=1; run;` a. all matching rows from both b. only rows from managers with no match in staff c. only rows from staff with no match in managers d. all matching and nonmatching rows from both
8. Values of C and A during the **third** iteration? clients (Name ID): Ankerton 11123; Davis 22298; Masters 33351. amounts (Name Amt): Ankerton 92; Ankerton 43; Masters 27. `data client_amount; merge clients(in=C) amounts(in=A); by Name; run;` a. C=0 and A=0 b. C=1 and A=0 c. C=0 and A=1 d. C=1 and A=1
9. Value of Location in the output? loc1: A France; loc2: A Belgium; loc3: A Italy. `data locALL; merge loc1 loc2 loc3; by Code; run;` a. Italy b. France c. Belgium d. France Belgium Italy
10. A single DATA step can be used to merge these three tables: dataset1 (Student, Test, Score), dataset2 (Subject, Test), dataset3 (Subject, AvgScore). a. True b. False

## Gaps
- Practices (05_1_p, 05_3_p) open in pop-ups – not opened.
- Question 05_3_q1 is interactive ("Check My Answer") – not answered. Activity 05_3_q2 captured (p205a04).
- Quiz answers not available (quiz not submitted, by rule).
