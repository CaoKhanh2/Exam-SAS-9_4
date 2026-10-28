# Mock Exam 1 – SAS 9.4 Base Programming (A00-231 practice)

43 questions · 135 minutes · Unofficial practice exam built from the course capture.

For performance items: paste the data program into SAS, run it, write the requested code, then answer.

---

## Question 1

Which statement best describes a DATA step?

- **A.** It generally reads data from an input source, processes it, and creates a SAS table.
- **B.** It processes an existing SAS table in a predefined way, for example to produce a report.
- **C.** It is a global statement that sets an option for the whole SAS session.
- **D.** It must always end with a QUIT statement.

---

## Question 2

```sas
data staff;
    input EmpID $ Dept $ Salary Bonus;
    datalines;
E01 Sales 52000 3000
E02 Sales 48000 2000
E03 IT 61000 4000
E04 IT 57000 1000
E05 HR 45000 2500
E06 Sales 50000 5000
E07 IT 65000 3000
E08 HR 47000 1500
;
run;
```

Run the program to create work.staff. Then write a DATA step that reads work.staff and creates work.itstaff containing only the rows where Dept is IT, and adds a column Total = Salary + Bonus.  
  
How many rows are in work.itstaff?

Answer: ______________

---

## Question 3

```sas
daat work.cars2;
    set sashelp.cars;
run;
```

You submit the program above. What happens?

- **A.** A WARNING says SAS assumed DATA was misspelled; the step runs and work.cars2 is created.
- **B.** An ERROR is written and the step is not processed.
- **C.** No message is written; SAS silently corrects the keyword.
- **D.** An ERROR is written and every later step in the program is skipped.

---

## Question 4

```sas
title "Quarterly Report";
proc print data=sashelp.class;
run;
proc means data=sashelp.class;
    var Height;
run;
title;
proc print data=sashelp.shoes;
run;
```

Which reports display the title "Quarterly Report"?

- **A.** Only the first PROC PRINT report
- **B.** The first PROC PRINT report and the PROC MEANS report
- **C.** All three reports
- **D.** None, because the TITLE statement is not followed by RUN

---

## Question 5

```sas
options nodate;
data work.temps;
    set work.raw;
    TempF=TempC*1.8+32;
run;
title "Temperatures";
proc print data=work.temps;
proc means data=work.temps;
    var TempF;
run;
title;
```

How many steps does this program contain? Enter a number.

Answer: ______________

---

## Question 6

```sas
data scores;
    input Student $ Test1 Test2 HeightIn;
    datalines;
Ana 80 90 60
Ben 72 75 65
Cy 95 88 70
Dee 60 71 62
Eli 88 88 68
Fay 79 84 55
;
run;
```

Run the program to create work.scores. Then create work.scores2 from work.scores that keeps only rows where Test1 is greater than 79, and adds:  
- Avg = the mean of Test1 and Test2 (use the MEAN function)  
- HeightCm = HeightIn * 2.54  
  
How many rows are in work.scores2?

Answer: ______________

---

## Question 7

```sas
data orders;
    input OrderID $ Region $ Qty Price;
    datalines;
O1 East 2 15
O2 West 1 40
O3 East 5 8
O4 North 3 20
O5 West 4 12
O6 East 1 30
;
run;

daat orders2;
    set orders;
    Amount=Qty*Price;
run;

title "East Orders";
proc print data=orders2
    var OrderID Amount;
    where Region="East";
run;

proc means data=orders2 average maxdec=1;
    var Amount;
    class Region;
run;
title;
```

Submit this program exactly as written (do not fix it). Which statement describes the result?

- **A.** Only WARNINGs are written; all steps run and both reports are produced.
- **B.** The DATA step runs and work.orders2 is created, but neither PROC PRINT nor PROC MEANS produces a report.
- **C.** Nothing after the first error runs, so work.orders2 is not created.
- **D.** work.orders2 is created and the PROC PRINT report appears, but PROC MEANS fails.

---

## Question 8

```sas
data trip;
    set work.raw;
    Miles=Km*0.621;
run;
```

Which statement in this DATA step creates a new column and does not begin with a SAS keyword?

- **A.** data trip;
- **B.** set work.raw;
- **C.** Miles=Km*0.621;
- **D.** run;

---

## Question 9

```sas
data staff;
    input EmpID $ Dept $ Salary Bonus;
    datalines;
E01 Sales 52000 3000
E02 Sales 48000 2000
E03 IT 61000 4000
E04 IT 57000 1000
E05 HR 45000 2500
E06 Sales 50000 5000
E07 IT 65000 3000
E08 HR 47000 1500
;
run;
```

Run the program to create work.staff. Then run:  
  
proc means data=staff mean;  
    var Salary;  
    class Dept;  
run;  
  
What is the mean Salary for Dept = Sales? Enter the number without commas.

Answer: ______________

---

## Question 10

```sas
options nodate;
data work.temps;
    set work.raw;
    TempF=TempC*1.8+32;
run;
title "Temperatures";
proc print data=work.temps;
proc means data=work.temps;
    var TempF;
run;
title;
```

How many statements are in the DATA step of this program? Enter a number.

Answer: ______________

---

## Question 11

```sas
data staff;
    input EmpID $ Dept $ Salary Bonus;
    datalines;
E01 Sales 52000 3000
E02 Sales 48000 2000
E03 IT 61000 4000
E04 IT 57000 1000
E05 HR 45000 2500
E06 Sales 50000 5000
E07 IT 65000 3000
E08 HR 47000 1500
;
run;
```

Using work.staff, create work.itstaff with only Dept = IT rows and Total = Salary + Bonus (same as the earlier task if you already did it).  
  
What is the value of Total for EmpID E04?

Answer: ______________

---

## Question 12

```sas
proc print data=sashelp.class
    var Name Age;
run;
```

The log underlines the word VAR. Which explanation is correct?

- **A.** VAR is not valid in PROC PRINT and must be deleted.
- **B.** The problem is just before VAR: the PROC PRINT statement has no semicolon, so VAR is read as an invalid option and the step is not processed.
- **C.** SAS adds the missing semicolon, prints Name and Age, and writes a WARNING.
- **D.** The column names Name and Age must be enclosed in quotation marks.

---

## Question 13

```sas
data scores;
    input Student $ Test1 Test2 HeightIn;
    datalines;
Ana 80 90 60
Ben 72 75 65
Cy 95 88 70
Dee 60 71 62
Eli 88 88 68
Fay 79 84 55
;
run;
```

Create work.scores2 from work.scores keeping rows where Test1 > 79, with Avg = mean of Test1 and Test2 and HeightCm = HeightIn * 2.54.  
  
What is HeightCm for Student Eli? Enter the value exactly as SAS displays it.

Answer: ______________

---

## Question 14

Which of these is NOT a global statement?

- **A.** TITLE
- **B.** OPTIONS
- **C.** LIBNAME
- **D.** VAR

---

## Question 15

Write the complete statement (including the semicolon) that clears all titles, as used at the end of the course demo programs.

Answer: ______________

---

## Question 16

```sas
data staff;
    input EmpID $ Dept $ Salary Bonus;
    datalines;
E01 Sales 52000 3000
E02 Sales 48000 2000
E03 IT 61000 4000
E04 IT 57000 1000
E05 HR 45000 2500
E06 Sales 50000 5000
E07 IT 65000 3000
E08 HR 47000 1500
;
run;
```

Using work.staff, create work.big that keeps only rows where Bonus is at least 3000 and adds Total = Salary + Bonus. Then run:  
  
proc means data=big mean maxdec=0;  
    var Total;  
run;  
  
What mean Total is displayed?

Answer: ______________

---

## Question 17

```sas
data orders;
    input OrderID $ Region $ Qty Price;
    datalines;
O1 East 2 15
O2 West 1 40
O3 East 5 8
O4 North 3 20
O5 West 4 12
O6 East 1 30
;
run;

daat orders2;
    set orders;
    Amount=Qty*Price;
run;

title "East Orders";
proc print data=orders2
    var OrderID Amount;
    where Region="East";
run;

proc means data=orders2 average maxdec=1;
    var Amount;
    class Region;
run;
title;
```

This program contains syntax errors. Fix every error so that all steps run, then run it.  
  
In the PROC MEANS output, what is the mean Amount for Region = East? Enter the value as displayed (MAXDEC=1).

Answer: ______________

---

## Question 18

```sas
options nodate;
data work.temps;
    set work.raw;
    TempF=TempC*1.8+32;
run;
title "Temperatures";
proc print data=work.temps;
proc means data=work.temps;
    var TempF;
run;
title;
```

How many global statements does this program contain? Enter a number.

Answer: ______________

---

## Question 19

```sas
data kids;
    set sashelp.class;
    /* where Age<13;
    Ratio=Weight/Height; */
    *drop Height;
run;
```

SASHELP.CLASS has 19 rows and 5 columns (Name, Sex, Age, Height, Weight). What does work.kids contain?

- **A.** 19 rows and 5 columns
- **B.** Fewer than 19 rows and 6 columns
- **C.** 19 rows and 4 columns
- **D.** Fewer than 19 rows and 5 columns

---

## Question 20

```sas
data staff;
    input EmpID $ Dept $ Salary Bonus;
    datalines;
E01 Sales 52000 3000
E02 Sales 48000 2000
E03 IT 61000 4000
E04 IT 57000 1000
E05 HR 45000 2500
E06 Sales 50000 5000
E07 IT 65000 3000
E08 HR 47000 1500
;
run;
```

Using work.staff, run:  
  
proc means data=staff mean maxdec=1;  
    var Bonus;  
    class Dept;  
run;  
  
What mean Bonus is displayed for Dept = Sales?

Answer: ______________

---

## Question 21

```sas
proc means data=sashelp.class average max maxdec=1;
    var Height;
run;
```

What happens when this step is submitted?

- **A.** An ERROR is written because AVERAGE is not a valid option; the step does not run. Use MEAN instead.
- **B.** A WARNING is written; SAS assumes MEAN and the step runs.
- **C.** The step runs, ignores AVERAGE, and displays only the maximum.
- **D.** An ERROR is written because MAXDEC= must come before the statistic keywords.

---

## Question 22

```sas
data scores;
    input Student $ Test1 Test2 HeightIn;
    datalines;
Ana 80 90 60
Ben 72 75 65
Cy 95 88 70
Dee 60 71 62
Eli 88 88 68
Fay 79 84 55
;
run;
```

Create work.scores2 from work.scores keeping rows where Test1 > 79, with Avg = mean of Test1 and Test2 and HeightCm = HeightIn * 2.54.  
  
What is Avg for Student Cy?

Answer: ______________

---

## Question 23

```sas
proc print data=sashelp.class;
proc means data=sashelp.class;
    var Age;
run;
```

The PROC PRINT step has no RUN statement. What happens?

- **A.** The PROC MEANS statement ends the PROC PRINT step, and both steps run.
- **B.** PROC PRINT is ignored because it has no RUN statement.
- **C.** An ERROR is written and neither step runs.
- **D.** The two procedures are combined into a single step.

---

## Question 24

```sas
data staff;
    input EmpID $ Dept $ Salary Bonus;
    datalines;
E01 Sales 52000 3000
E02 Sales 48000 2000
E03 IT 61000 4000
E04 IT 57000 1000
E05 HR 45000 2500
E06 Sales 50000 5000
E07 IT 65000 3000
E08 HR 47000 1500
;
run;
```

Using work.staff, run a PROC PRINT step that lists only rows where Dept is Sales and Salary is at least 50000.  
  
How many rows are listed?

Answer: ______________

---

## Question 25

```sas
data pets;
    input Name $ Species $ Age Weight;
    datalines;
Max Dog 5 30
Bella Cat 3 9
Rocky Dog 8 35
Luna Cat 10 11
Coco Bird 2 1
Duke Dog 1 20
Milo Cat 6 12
;
run;

data seniors set pets;
    where Age>=6;
    WeightLb=Weight*2.2;
run;

title "Senior Pets;
prc print data=seniors;
run;
title;
```

This program contains several syntax errors after the first DATA step. Fix all of them (tip: fix before submitting), then run it.  
  
How many rows are in work.seniors?

Answer: ______________

---

## Question 26

In SAS Studio you submit a program that contains only a DATA step that creates a table. Which tab stays empty?

- **A.** Log
- **B.** Output Data
- **C.** Results
- **D.** Code

---

## Question 27

```sas
data staff;
    input EmpID $ Dept $ Salary Bonus;
    datalines;
E01 Sales 52000 3000
E02 Sales 48000 2000
E03 IT 61000 4000
E04 IT 57000 1000
E05 HR 45000 2500
E06 Sales 50000 5000
E07 IT 65000 3000
E08 HR 47000 1500
;
run;
```

Using work.staff, create work.staff2 that is a copy of work.staff with a new column Total = Salary + Bonus.  
  
What is Total for EmpID E06?

Answer: ______________

---

## Question 28

You submit a program, then submit it again. What happens to the log and results?

- **A.** In SAS Studio and Enterprise Guide they are replaced; in the SAS windowing environment they are appended.
- **B.** They are appended in every interface.
- **C.** SAS Studio appends; Enterprise Guide replaces.
- **D.** They are replaced in every interface.

---

## Question 29

```sas
data scores;
    input Student $ Test1 Test2 HeightIn;
    datalines;
Ana 80 90 60
Ben 72 75 65
Cy 95 88 70
Dee 60 71 62
Eli 88 88 68
Fay 79 84 55
;
run;
```

Run this DATA step after creating work.scores:  
  
data scores2;  
    set scores;  
    *where Test1 > 79;  
    Avg=mean(Test1, Test2);  
    HeightCm=HeightIn*2.54;  
run;  
  
How many rows are in work.scores2?

Answer: ______________

---

## Question 30

```sas
data scores;
    input Student $ Test1 Test2 HeightIn;
    datalines;
Ana 80 90 60
Ben 72 75 65
Cy 95 88 70
Dee 60 71 62
Eli 88 88 68
Fay 79 84 55
;
run;
```

Create work.scores2 (rows where Test1 > 79; Avg = mean of Test1 and Test2; HeightCm = HeightIn * 2.54). Then run:  
  
proc means data=scores2 mean maxdec=2;  
    var Avg;  
run;  
  
What mean is displayed?

Answer: ______________

---

## Question 31

```sas
data canada;
    set sashelp.shoes;
    where Region="Canada;
run;
```

What is wrong with this step, and what does the course suggest for spotting it before you run the code?

- **A.** An unmatched quotation mark; the editor's color coding (or Format Code) shows the rest of the program being treated as a quoted string.
- **B.** A missing RUN statement; check the Results tab.
- **C.** Region must be written in uppercase; use Format Code to fix the case.
- **D.** WHERE is not allowed in a DATA step; check the Output Data tab.

---

## Question 32

```sas
data orders;
    input OrderID $ Region $ Qty Price;
    datalines;
O1 East 2 15
O2 West 1 40
O3 East 5 8
O4 North 3 20
O5 West 4 12
O6 East 1 30
;
run;

daat orders2;
    set orders;
    Amount=Qty*Price;
run;

title "East Orders";
proc print data=orders2
    var OrderID Amount;
    where Region="East";
run;

proc means data=orders2 average maxdec=1;
    var Amount;
    class Region;
run;
title;
```

Fix the syntax errors in this program and run it.  
  
In work.orders2, what is Amount for OrderID O5?

Answer: ______________

---

## Question 33

How many rows does the sample table SASHELP.CLASS contain? Enter a number.

Answer: ______________

---

## Question 34

```sas
/* Program A */
data copy1;set sashelp.class;run;

/* Program B */
data copy2;
    set sashelp.class;
run;
```

How do the tables created by Program A and Program B compare?

- **A.** They are identical; spacing and line breaks do not matter to SAS.
- **B.** Program A fails because each statement must be on its own line.
- **C.** Program A creates a table with no rows because of the missing line breaks.
- **D.** Program B fails because statements must start in column one.

---

## Question 35

```sas
data pets;
    input Name $ Species $ Age Weight;
    datalines;
Max Dog 5 30
Bella Cat 3 9
Rocky Dog 8 35
Luna Cat 10 11
Coco Bird 2 1
Duke Dog 1 20
Milo Cat 6 12
;
run;

data seniors set pets;
    where Age>=6;
    WeightLb=Weight*2.2;
run;

title "Senior Pets;
prc print data=seniors;
run;
title;
```

Fix all syntax errors in this program and run it.  
  
In work.seniors, what is WeightLb for Name = Luna? Enter the value as displayed.

Answer: ______________

---

## Question 36

```sas
data orders;
    input OrderID $ Region $ Qty Price;
    datalines;
O1 East 2 15
O2 West 1 40
O3 East 5 8
O4 North 3 20
O5 West 4 12
O6 East 1 30
;
run;

daat orders2;
    set orders;
    Amount=Qty*Price;
run;

title "East Orders";
proc print data=orders2
    var OrderID Amount;
    where Region="East";
run;

proc means data=orders2 average maxdec=1;
    var Amount;
    class Region;
run;
title;
```

Fix the syntax errors in this program and run it.  
  
How many rows does the corrected PROC PRINT report list?

Answer: ______________

---

## Question 37

```sas
data staff;
    input EmpID $ Dept $ Salary Bonus;
    datalines;
E01 Sales 52000 3000
E02 Sales 48000 2000
E03 IT 61000 4000
E04 IT 57000 1000
E05 HR 45000 2500
E06 Sales 50000 5000
E07 IT 65000 3000
E08 HR 47000 1500
;
run;
```

Using work.staff, create work.hr containing only Dept = HR rows and a new column Raise = Salary * 0.1.  
  
What is Raise for EmpID E08?

Answer: ______________

---

## Question 38

```sas
data staff;
    input EmpID $ Dept $ Salary Bonus;
    datalines;
E01 Sales 52000 3000
E02 Sales 48000 2000
E03 IT 61000 4000
E04 IT 57000 1000
E05 HR 45000 2500
E06 Sales 50000 5000
E07 IT 65000 3000
E08 HR 47000 1500
;
run;
```

Using work.staff, create work.staff2 as a copy of work.staff with one new column Total = Salary + Bonus.  
  
How many columns does work.staff2 have?

Answer: ______________

---

## Question 39

```sas
data scores;
    input Student $ Test1 Test2 HeightIn;
    datalines;
Ana 80 90 60
Ben 72 75 65
Cy 95 88 70
Dee 60 71 62
Eli 88 88 68
Fay 79 84 55
;
run;
```

Using work.scores, create work.drop2 that keeps only rows where Test2 is less than Test1.  
  
How many rows are in work.drop2?

Answer: ______________

---

## Question 40

You replace FILEPATH in setup.sas with the path to your EPG1V2/data folder and run it. Which log note confirms the setup worked?

- **A.** Libref PG1 was successfully assigned, followed by the engine and physical name
- **B.** Table PG1 was successfully created
- **C.** WARNING: Libref PG1 is not assigned
- **D.** No note is written when a library is assigned

---

## Question 41

In SAS Studio, after you run a PROC PRINT step, which tab of the program window shows the report? Enter the tab name.

Answer: ______________

---

## Question 42

What does MAXDEC=2 do on a PROC MEANS statement?

- **A.** Rounds the displayed statistics to two decimal places.
- **B.** Limits the analysis to the first two variables in the VAR statement.
- **C.** Allows at most two values for each CLASS variable.
- **D.** Permanently stores the data values in the table with two decimals.

---

## Question 43

Which WHERE statement keeps only the rows where the character column Region has the value East?

- **A.** where Region="East";
- **B.** where Region=East;
- **C.** where Region="East;
- **D.** where "Region"="East";

---

