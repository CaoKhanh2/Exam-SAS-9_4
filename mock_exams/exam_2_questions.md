# Mock Exam 2 – SAS 9.4 Base Programming (A00-231 practice)

45 questions · 135 minutes · Unofficial practice exam built from the course capture.

For performance items: paste the data program into SAS, run it, write the requested code, then answer.

---

## Question 1

Which LIBNAME statement uses a valid libref?

- **A.** libname salesdata2024 "s:/workshop/data";
- **B.** libname 2024data "s:/workshop/data";
- **C.** libname sales_24 xlsx "s:/workshop/data/sales.xlsx";
- **D.** libname sales-24 "s:/workshop/data";

---

## Question 2

A programmer submits:  
  
libname crb2 "s:/workshop/ECRBM6/daat";  
  
The folder name is misspelled and the folder does not exist. What appears in the log?

- **A.** An ERROR, and the LIBNAME statement is not executed.
- **B.** A WARNING that the path is invalid.
- **C.** A NOTE that the libref was successfully assigned, and the library contains the course tables.
- **D.** Only a NOTE saying the library does not exist – no error and no warning.

---

## Question 3

Inside a PROC IMPORT step that reads a CSV file with many missing values, which statement makes SAS use every row of the file to decide each column's type?

- **A.** replace;
- **B.** guessingrows=max;
- **C.** dbms=csv;
- **D.** options validvarname=v7;

---

## Question 4

What does this step display?  
  
proc contents data=cr._all_ nods;  
run;

- **A.** The descriptor portion of the first table in the CR library only.
- **B.** The data rows of every table in the CR library.
- **C.** A list of all tables in the CR library followed by the full descriptor portion of each table.
- **D.** A list of all tables in the CR library, without the descriptor portion of each table.

---

## Question 5

```sas
data jan;
    input Item $ Units;
    datalines;
Pen 5
Ink 3
Pad 7
;
run;

data feb;
    input Item $ Qty;
    datalines;
Pen 4
Pad 6
Ink 2
Tape 9
;
run;
```

Run the program above. Then write a DATA step that concatenates jan and feb (jan first) into work.q1 without using any data set options.  
  
How many columns does work.q1 have?

Answer: ______________

---

## Question 6

```sas
data jan;
    input Item $ Units;
    datalines;
Pen 5
Ink 3
Pad 7
;
run;

data feb;
    input Item $ Qty;
    datalines;
Pen 4
Pad 6
Ink 2
Tape 9
;
run;
```

Modify your concatenation so that the Qty values from feb are stored in the Units column (work.q1 should then have only Item and Units).  
  
What is the total of Units across all rows of work.q1?

Answer: ______________

---

## Question 7

```sas
data emp;
    input EmpID $ Name $ Dept $;
    datalines;
E1 Ava Sales
E2 Bo IT
E3 Cal Sales
E4 Di HR
E5 Ed IT
E6 Flo HR
;
run;

data don;
    input ID $ Q1 Q2 Q3 Q4;
    datalines;
E5 10 . 20 5
E2 15 15 15 15
E7 5 5 . .
E1 . . 30 .
E3 20 10 . 10
;
run;
```

Run the program above. Table don is not sorted and stores the employee ID in a column named ID.  
  
Create work.donors that contains only employees who appear in BOTH emp and don, with a new column TotalDonation = the sum of Q1–Q4 (missing values ignored).  
  
How many rows are in work.donors?

Answer: ______________

---

## Question 8

```sas
data emp;
    input EmpID $ Name $ Dept $;
    datalines;
E1 Ava Sales
E2 Bo IT
E3 Cal Sales
E4 Di HR
E5 Ed IT
E6 Flo HR
;
run;

data don;
    input ID $ Q1 Q2 Q3 Q4;
    datalines;
E5 10 . 20 5
E2 15 15 15 15
E7 5 5 . .
E1 . . 30 .
E3 20 10 . 10
;
run;
```

Using your work.donors table from the previous question, what is the value of TotalDonation for the employee named Cal?

Answer: ______________

---

## Question 9

```sas
data emp;
    input EmpID $ Name $ Dept $;
    datalines;
E1 Ava Sales
E2 Bo IT
E3 Cal Sales
E4 Di HR
E5 Ed IT
E6 Flo HR
;
run;

data don;
    input ID $ Q1 Q2 Q3 Q4;
    datalines;
E5 10 . 20 5
E2 15 15 15 15
E7 5 5 . .
E1 . . 30 .
E3 20 10 . 10
;
run;
```

In the same DATA step, also create work.nodonor containing employees from emp that have NO matching row in don.  
  
How many rows are in work.nodonor?

Answer: ______________

---

## Question 10

```sas
data shop;
    input OrderID $ Store $ Channel $ Qty Price;
    datalines;
A01 North Web 3 20
A02 South Phone 1 55
A03 North Store 4 12
A04 West Web 2 35
A05 South Web 5 12
A06 North Phone 2 40
A07 West Store 6 9
A08 South Store 2 30
A09 North Web 1 84
A10 West Phone 3 25
;
run;
```

Run the program above, then submit:  
  
data shop3;  
    set shop;  
    if Channel="Web" then Source="Online";  
    else Source="In person";  
run;  
  
What value of Source is stored for OrderID A02? (Type the value exactly as stored.)

Answer: ______________

---

## Question 11

```sas
data shop;
    input OrderID $ Store $ Channel $ Qty Price;
    datalines;
A01 North Web 3 20
A02 South Phone 1 55
A03 North Store 4 12
A04 West Web 2 35
A05 South Web 5 12
A06 North Phone 2 40
A07 West Store 6 9
A08 South Store 2 30
A09 North Web 1 84
A10 West Phone 3 25
;
run;
```

Using work.shop, create work.big with a new column Amount = Qty * Price, keeping only the rows where Amount is at least 60.  
  
How many rows are in work.big?

Answer: ______________

---

## Question 12

```sas
data shop;
    input OrderID $ Store $ Channel $ Qty Price;
    datalines;
A01 North Web 3 20
A02 South Phone 1 55
A03 North Store 4 12
A04 West Web 2 35
A05 South Web 5 12
A06 North Phone 2 40
A07 West Store 6 9
A08 South Store 2 30
A09 North Web 1 84
A10 West Phone 3 25
;
run;
```

In one DATA step, read work.shop and write the rows with Channel = "Web" to work.web and all other rows to work.other.  
  
How many rows are in work.other?

Answer: ______________

---

## Question 13

```sas
data shop;
    input OrderID $ Store $ Channel $ Qty Price;
    datalines;
A01 North Web 3 20
A02 South Phone 1 55
A03 North Store 4 12
A04 West Web 2 35
A05 South Web 5 12
A06 North Phone 2 40
A07 West Store 6 9
A08 South Store 2 30
A09 North Web 1 84
A10 West Phone 3 25
;
run;
```

Create work.storetot with exactly one row per Store and a column StoreAmt = the total of Qty*Price for that store.  
  
What is StoreAmt for West?

Answer: ______________

---

## Question 14

```sas
data shop;
    input OrderID $ Store $ Channel $ Qty Price;
    datalines;
A01 North Web 3 20
A02 South Phone 1 55
A03 North Store 4 12
A04 West Web 2 35
A05 South Web 5 12
A06 North Phone 2 40
A07 West Store 6 9
A08 South Store 2 30
A09 North Web 1 84
A10 West Phone 3 25
;
run;
```

Sort work.shop by Qty*Price in ascending order (create Amount first), then create a running total RunAmt that accumulates Amount from the first row to the last.  
  
What is RunAmt in row 4?

Answer: ______________

---

## Question 15

```sas
data running;
    set shop_amt;
    RunAmt=sum(RunAmt, Amount);
run;
```

shop_amt contains a numeric column Amount with no missing values. There is no RETAIN statement. What values does RunAmt contain?

- **A.** A running total of Amount.
- **B.** Missing on every row.
- **C.** The same value as Amount on every row.
- **D.** The total of all Amount values on every row.

---

## Question 16

```sas
data shop;
    input OrderID $ Store $ Channel $ Qty Price;
    datalines;
A01 North Web 3 20
A02 South Phone 1 55
A03 North Store 4 12
A04 West Web 2 35
A05 South Web 5 12
A06 North Phone 2 40
A07 West Store 6 9
A08 South Store 2 30
A09 North Web 1 84
A10 West Phone 3 25
;
run;
```

Create a custom numeric format AMTCAT: values below 50 = "Low", 50 up to (but not including) 75 = "Mid", 75 and above = "High". Compute Amount = Qty*Price for work.shop and use PROC FREQ with your format to count Amount by category.  
  
How many rows fall in the "Mid" category?

Answer: ______________

---

## Question 17

Which PROC FORMAT step correctly creates a format for the character column Channel?

- **A.** proc format; value chan "Web"="Online" other="Offline"; run;
- **B.** proc format; value $chan "Web"="Online" other="Offline"; run;
- **C.** proc format; value chan. "Web"="Online" other="Offline"; run;
- **D.** proc format; value $chan. "Web"="Online" other="Offline"; run;

---

## Question 18

```sas
data people;
    length FullName $ 20 Joined $ 10;
    input FullName $ Joined $;
    datalines;
Lee,Mary-Ann 03/15/2019
Park,Jin 11/02/2020
Ortiz,Ana-Sofia 07/30/2018
Smith,Tom 01/05/2021
;
run;
```

Run the program above. Create a column Display that shows the first name, one space, then the last name (for example, "Jin Park"). Hyphenated first names must stay intact.  
  
What is Display for row 3?

Answer: ______________

---

## Question 19

FullName has the value "Lee,Mary-Ann". What does scan(FullName, 2) return (no third argument)?

- **A.** Mary
- **B.** Lee
- **C.** Mary-Ann
- **D.** Ann

---

## Question 20

```sas
data people;
    length FullName $ 20 Joined $ 10;
    input FullName $ Joined $;
    datalines;
Lee,Mary-Ann 03/15/2019
Park,Jin 11/02/2020
Ortiz,Ana-Sofia 07/30/2018
Smith,Tom 01/05/2021
;
run;
```

Joined is a character column. Create a numeric SAS date column JoinDate from Joined.  
  
What is the stored (unformatted) value of JoinDate for Park,Jin?

Answer: ______________

---

## Question 21

```sas
data pay;
    length Salary $ 10;
    input EmpID $ Salary $;
    datalines;
P1 $42,500
P2 $38,000
P3 $51,250
;
run;
```

Salary is stored as character text such as "$42,500". Create a numeric column SalNum from Salary, then use PROC MEANS with MAXDEC=0 to compute the mean of SalNum.  
  
What mean is displayed?

Answer: ______________

---

## Question 22

```sas
data growth;
    Balance=1000;
    do until (Balance > 2000);
        Year+1;
        Balance=Balance*1.10;
        output;
    end;
run;
```

Run the program. How many rows are written to work.growth?

Answer: ______________

---

## Question 23

```sas
/* No input data is needed for this question. */
```

Write a DATA step that creates work.savings:  
- Balance starts at 0.  
- For each Year from 1 to 3, and inside it each Month from 1 to 12: add 100 to Balance, then add one month of interest: Balance = Balance * (1 + .06/12);  
- Write one row per year.  
  
What is Balance in the row for Year 3, rounded to the nearest whole number?

Answer: ______________

---

## Question 24

```sas
data t;
    do Year=1 to 5;
        Total+10;
    end;
run;
```

What does work.t contain?

- **A.** 5 rows, Year = 1 to 5.
- **B.** 5 rows, each with Total = 10.
- **C.** 1 row: Year = 5, Total = 50.
- **D.** 1 row: Year = 6, Total = 50.

---

## Question 25

X equals 10 before each loop below. How many times does each loop body execute?  
  
Loop 1: do while (X < 5); X+1; end;  
Loop 2: do until (X >= 5); X+1; end;

- **A.** Loop 1: 0 times · Loop 2: 1 time
- **B.** Loop 1: 1 time · Loop 2: 0 times
- **C.** Both: 0 times
- **D.** Both: 1 time

---

## Question 26

```sas
data emp;
    input EmpID $ Name $ Dept $;
    datalines;
E1 Ava Sales
E2 Bo IT
E3 Cal Sales
E4 Di HR
E5 Ed IT
E6 Flo HR
;
run;

data don;
    input ID $ Q1 Q2 Q3 Q4;
    datalines;
E5 10 . 20 5
E2 15 15 15 15
E7 5 5 . .
E1 . . 30 .
E3 20 10 . 10
;
run;
```

Restructure don into a narrow table work.don_narrow with one row per ID per quarter column (Q1–Q4). Rows whose value is missing must still be included. Use PROC TRANSPOSE.  
  
How many rows are in work.don_narrow?

Answer: ______________

---

## Question 27

Which statement about _N_ and _ERROR_ is true?

- **A.** They exist in the PDV during execution but are not written to the output table.
- **B.** They are written to the output table unless dropped.
- **C.** _N_ counts the rows written so far; _ERROR_ counts syntax errors.
- **D.** They are created only when a BY statement is used.

---

## Question 28

```sas
data shop;
    input OrderID $ Store $ Channel $ Qty Price;
    datalines;
A01 North Web 3 20
A02 South Phone 1 55
A03 North Store 4 12
A04 West Web 2 35
A05 South Web 5 12
A06 North Phone 2 40
A07 West Store 6 9
A08 South Store 2 30
A09 North Web 1 84
A10 West Phone 3 25
;
run;

data shop2
    set shop;
    Amount=Qty*Price;
    where Amount>=60;
    if Channel="Web" then Source="Online";
    else Source="Offline";
    length Source $ 7;
    format Amount dollar8;
run;
```

The second step should: keep only rows where Amount (Qty*Price) is at least 60; set Source to "Online" for Web orders and "Offline" otherwise, without truncation; and display Amount with a dollar format. It contains several errors.  
  
Fix the program and run it. How many rows of work.shop2 have Source = "Offline"?

Answer: ______________

---

## Question 29

```sas
data shop;
    input OrderID $ Store $ Channel $ Qty Price;
    datalines;
A01 North Web 3 20
A02 South Phone 1 55
A03 North Store 4 12
A04 West Web 2 35
A05 South Web 5 12
A06 North Phone 2 40
A07 West Store 6 9
A08 South Store 2 30
A09 North Web 1 84
A10 West Phone 3 25
;
run;

title "Store Quantities;
proc print data=shop label noobs
    by Store;
    var OrderID Qty;
    sum Qty;
    label Qty="Units Sold";
run;
title;
```

The report should list OrderID and Qty grouped by Store, with a Qty subtotal for each store and the label "Units Sold". Fix every error and run it.  
  
What Qty subtotal is shown for North?

Answer: ______________

---

## Question 30

```sas
data profit2;
    set profit;
    format Profit dollar12;
run;
```

The step runs. What does the log show and what is the result?

- **A.** An ERROR because the FORMAT statement is invalid; no table is created.
- **B.** A WARNING; SAS adds the missing period automatically.
- **C.** No error or warning, but a NOTE that dollar12 is uninitialized; Profit is not formatted as dollars.
- **D.** No messages; Profit is formatted with DOLLAR12.

---

## Question 31

```sas
data big;
    set shop;
    Amount=Qty*Price;
    where Amount>=60;
run;
```

shop has no column named Amount. What happens, and how should it be fixed?

- **A.** An ERROR that Amount is not in the input table; replace WHERE with a subsetting IF placed after the assignment.
- **B.** The step runs because the WHERE statement comes after the assignment.
- **C.** A WARNING; SAS converts the WHERE statement into an IF statement automatically.
- **D.** An ERROR; fix it by moving the WHERE statement before the SET statement.

---

## Question 32

```sas
data orders2;
    set orders;
    if Order_Type in (1,2,3) then Order_Source="Known";
    else Order_Source="Unknown";
    length Order_Source $ 7;
run;
```

What is the result?

- **A.** No messages; Order_Source has length 7.
- **B.** An ERROR; the table is not created.
- **C.** A WARNING that the length was already set; the LENGTH statement has no effect and "Unknown" is stored as "Unkno".
- **D.** A NOTE only; "Unknown" is stored correctly.

---

## Question 33

What is the PUTLOG statement used for?

- **A.** To write the PDV to the output table at that point.
- **B.** To send the log to a PDF file.
- **C.** To stop the DATA step when an error occurs.
- **D.** To write messages or column values to the log during DATA step execution, which helps find logic errors.

---

## Question 34

```sas
data emp_US emp_AU;
    set crb.employee(drop=Country);
    if Country="US" then output emp_US;
    else output emp_AU;
run;
```

The programmer wants Country removed from both output tables. What is wrong and what is the fix?

- **A.** Nothing is wrong; DROP= on the input table takes effect after the IF statement.
- **B.** Country is never read into the PDV, so the IF condition cannot use it (errors/warnings appear). Use a DROP statement or DROP= on the output tables instead.
- **C.** DROP= cannot be used in a SET statement; use KEEP= instead.
- **D.** The DATA statement may list only one table; split it into two steps.

---

## Question 35

During DATA step execution, the automatic variable _ERROR_ is set to 1 for a row. What does this mean?

- **A.** A data error occurred while processing that row; a note with details is written to the log.
- **B.** A syntax error was found during compilation.
- **C.** The row was not written to the output table.
- **D.** The step will stop after this row.

---

## Question 36

```sas
data shop;
    input OrderID $ Store $ Channel $ Qty Price;
    datalines;
A01 North Web 3 20
A02 South Phone 1 55
A03 North Store 4 12
A04 West Web 2 35
A05 South Web 5 12
A06 North Phone 2 40
A07 West Store 6 9
A08 South Store 2 30
A09 North Web 1 84
A10 West Phone 3 25
;
run;
```

Compute Amount = Qty*Price for work.shop, then use PROC MEANS to show the mean of Amount for each Store, rounded to 1 decimal place.  
  
What mean is displayed for South?

Answer: ______________

---

## Question 37

```sas
data shop;
    input OrderID $ Store $ Channel $ Qty Price;
    datalines;
A01 North Web 3 20
A02 South Phone 1 55
A03 North Store 4 12
A04 West Web 2 35
A05 South Web 5 12
A06 North Phone 2 40
A07 West Store 6 9
A08 South Store 2 30
A09 North Web 1 84
A10 West Phone 3 25
;
run;
```

Create a one-way frequency report of Channel with the values listed from the highest count to the lowest and without cumulative columns.  
  
Which Channel value is listed first?

Answer: ______________

---

## Question 38

```sas
data shop;
    input OrderID $ Store $ Channel $ Qty Price;
    datalines;
A01 North Web 3 20
A02 South Phone 1 55
A03 North Store 4 12
A04 West Web 2 35
A05 South Web 5 12
A06 North Phone 2 40
A07 West Store 6 9
A08 South Store 2 30
A09 North Web 1 84
A10 West Phone 3 25
;
run;
```

Compute Amount = Qty*Price, then submit a PROC MEANS step with NOPRINT, CLASS Store Channel, VAR Amount, an OUTPUT statement that creates work.summ with sum=TotAmt, and a WAYS 1 statement.  
  
How many rows are in work.summ?

Answer: ______________

---

## Question 39

```sas
proc print data=summary noobs;
    var Age_Range TotProfit;
    label TotProfit="Total Profit";
run;
```

The column heading still shows TotProfit instead of "Total Profit". What is the fix?

- **A.** Move the LABEL statement before the VAR statement.
- **B.** Add the LABEL option to the PROC PRINT statement.
- **C.** Remove the NOOBS option.
- **D.** Use a FORMAT statement instead of a LABEL statement.

---

## Question 40

What does the statement ods noproctitle; do?

- **A.** Removes all TITLE statements for the current step only.
- **B.** Closes all ODS destinations.
- **C.** Removes the procedure name heading (for example "The FREQ Procedure") from reports for the rest of the session.
- **D.** Removes the bookmarks from a PDF file.

---

## Question 41

In a PDF created with ODS PDF, each bookmark shows the procedure name. Which statement, placed before a procedure, sets custom bookmark text for that procedure?

- **A.** title "Claims by Year";
- **B.** ods proclabel "Claims by Year";
- **C.** ods pdf pdftoc=1;
- **D.** label "Claims by Year";

---

## Question 42

```sas
ods excel file="&outpath/report.xlsx";
title "Orders by Month";
proc freq data=profit; tables Order_Date; format Order_Date monname.; run;
title "Profit by Age";
proc means data=profit; var Profit; class Age_Range; run;
ods excel close;
```

Using default settings, which describes the workbook?

- **A.** One worksheet containing both reports, with the titles shown.
- **B.** No workbook is created, because ODS EXCEL requires STYLE=.
- **C.** Two worksheets named "Orders by Month" and "Profit by Age".
- **D.** Two worksheets (one per report); the titles are not shown by default.

---

## Question 43

```sas
proc export data=cr.employee_current
    outfile="&outpath/emp_current.csv" dbms=csv replace;
run;
```

Which statement about this step is true?

- **A.** REPLACE overwrites emp_current.csv if it already exists; values that contain a comma are enclosed in quotation marks.
- **B.** REPLACE replaces commas inside values with blanks.
- **C.** The step fails because PROC EXPORT needs a QUIT statement.
- **D.** DBMS=CSV creates an Excel workbook.

---

## Question 44

Which TABLES statement creates a two-way frequency table of Store by Channel that suppresses the row and column percentages?

- **A.** tables Store Channel / norow nocol;
- **B.** tables Store*Channel / nocum;
- **C.** tables Store*Channel / norow nocol;
- **D.** tables Store, Channel / nopercent;

---

## Question 45

%let st=North;  
  
Which TITLE statement displays the text Orders for North?

- **A.** title 'Orders for &st';
- **B.** title "Orders for &st";
- **C.** title "Orders for st";
- **D.** title 'Orders for' &st;

---

