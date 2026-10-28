# CR – Lesson 3: SAS Programming 2 Review

Source: Certification Review player (id=238), text mode transcripts. Captured 2026-10-28. Paraphrased; short quotes in quotation marks.

## 3.1 Controlling DATA Step Processing

### Understanding DATA Step Processing (video 7:16)
- Programming 2 focused on data preparation with the DATA step; understanding what happens behind the scenes is critical for the exam and for messy real data.
- Re-examines the earlier DATA step on cr.orders (WHERE valid delivery date; UPCASE Customer_Country; negative Quantity → missing; new columns Profit, ShipDays, Age_Range; Order_Source conditional on Order_Type).
- **Compilation phase:** SAS checks syntax and prepares code for execution; builds the **program data vector (PDV)**, which processes one row at a time; each column's required attributes (name, type, length) are defined there; other compile-time statements set rules for execution.
  - DATA statement defines the output table name/type. SET adds all cr.orders columns and attributes to the PDV. LENGTH (compile-time) adds Order_Source as character length 8. WHERE (compile-time) flags Delivery_Date and Order_Date so only rows meeting the condition are read into the PDV during execution. New columns Profit, ShipDays, Age_Range are added to the PDV (narrator calls them "new numeric columns" [VERIFY – Age_Range comes from SUBSTR, so character]); FORMAT assigns a currency format to Profit. DROP flags columns to drop when rows are written out. End of compilation: the descriptor portion of the output table is created.
- **Execution phase:** rows are read into the PDV one at a time, processed per compile-time rules, and written to the output table. Demo uses the DATA step debugger in SAS Enterprise Guide (no interface questions on the exam, but there are questions requiring you to think through compilation/execution).
  - At the start every PDV column is missing except **_N_** and **_ERROR_**, which are automatic: present in the PDV during execution but **not written** to the output table. _N_ = DATA step iteration number; _ERROR_ = 1 if a data error occurs for the row, otherwise 0 (a note with details goes to the log).
  - Executing SET fills the input columns; the debugger skips LENGTH and WHERE (compile-time, already did their job) and jumps to the Customer_Country assignment. Customer_Country "be" → "BE"; Profit, ShipDays, Age_Range computed; IF: Order_Type is 1 → "Retail", remaining ELSE IFs skipped. DROP skipped (compile-time).
  - At the RUN statement (step boundary) there is an **implicit output** writing the PDV as a row, then SAS loops back to the top.
  - New (computed) columns are **reinitialized to missing** at the top of each iteration; _N_ becomes 2; SET overwrites PDV values with the next row meeting the WHERE condition; repeats until the end of the input table.

### Directing DATA Step Output (video 2:48)
- Explicit **OUTPUT** statement overrides the implicit output and tells SAS when and where to write rows.
- Forecast example on cr.profit_summary (total profit by product line and category), 5% growth for two years: table `growth`; Year=1; increase total profit 5%; OUTPUT (PDV values kept); Year=2; increase again; OUTPUT → two rows written for every row read.
- Conditional output to multiple tables: DATA `sports` `nonsports`; after SET cr.profit_summary, IF product line is Sports THEN OUTPUT sports; ELSE OUTPUT nonsports.

### Review Quiz: Controlling DATA Step Processing (read-only; all 10 read from screenshots, never answered)
- **Q1.** Which of the following is not created during the compilation phase? — a. the data set descriptor portion · b. the first observation · c. the program data vector · d. the **_N_** and **_ERROR_** automatic variables
- **Q2.** During the compilation phase, SAS scans each statement in the DATA step, looking for syntax errors. Which of the following is not considered a syntax error? — a. incorrect data values · b. invalid options or formats · c. missing or invalid punctuation · d. missing or misspelled keywords
- **Q3.** Unless otherwise directed, how many times does the DATA step loop execute? — a. once for each compilation phase · b. once for each DATA step statement · c. once for each row in the input file · d. once for each column in the input file
- **Q4.** At the beginning of the execution phase, the value of **_N_** is 1, the value of **_ERROR_** is 0, and the values of the remaining variables are set to which of the following? — a. 0 · b. 1 · c. undefined · d. missing
- **Q5.** Suppose you run a program that causes three data errors. What is the value of the automatic variable **_ERROR_** when the row that contains the third error is processed? — a. 0 · b. 1 · c. 2 · d. 3
- **Q6.** Which of the following actions occurs at the beginning of an iteration of the DATA step? — a. The automatic variables **_N_** and **_ERROR_** are incremented by 1. · b. The DATA step stops execution. · c. The descriptor portion of the data set is written. · d. The values of variables created in programming statements are reset to missing in the program data vector.
- **Q7.** Consider the following DATA step. Based on the sample input file below, in what order are the variables stored in the new **fin2** table? — a. Name, Raise, NewSalary, Date · b. SSN, Name, Salary, Date, Raise, NewSalary · c. Name, Date, Raise, NewSalary · d. Salary, NewSalary, Name, Raise

```sas
data fin2;
    set finance;
    keep Name Raise NewSalary Date;
    if Salary>25000 then Raise=0.03;
    else Raise=0.05;
    NewSalary=(Salary*Raise)+Salary;
run;
```
Input finance (SSN, Name, Salary, Date): 029-46-9261 Rudelich 35000 02JAN17 · 074-53-9892 Vincent 35000 02JAN17 · 228-88-9649 Benito 28000 16JAN17 · 442-21-8075 Sirignano 5000 06FEB17 · 446-93-2122 Harbinger 33900 06FEB17 · 776-84-5391 Phillipon 29750 06JUN16 · 929-75-0218 Gunter 27500 06JUN16
- **Q8.** If the input table contains five columns, which PUTLOG statements create the following results in the SAS log?

```text
NOTE: Begin DATA Step
Name=Alfred Sex=M Age=14 Height=69 Weight=112.5 _ERROR_=0 _N_=1
```
```sas
/* a */ putlog "NOTE: Begin DATA Step";
        putlog _all_;
/* b */ putlog NOTE="Begin DATA Step";
        putlog _all_;
/* c */ putlog "NOTE: Begin DATA Step";
        putlog Name Sex Age Height Weight _ERROR_ _N_;
/* d */ putlog NOTE(Begin DATA Step);
        putlog all;
```
- **Q9.** After this program runs, how many rows are in the **forecast** table, assuming that there are 10 rows in the **sales** table — a. 10 · b. 30 · c. 40 · d. unknown

```sas
data forecast;
    set sales;
    Qtr=1;
    Sales=Sales*1.01;
    output;
    Qtr=2;
    Sales=Sales*1.01;
    output;
    Qtr=3;
    Sales=Sales*1.01;
    output;
    Qtr=4;
    Sales=Sales*1.01;
run;
```
- **Q10.** After this code runs, how many columns are in the **Canada** table if there are 10 columns in the input **customer** table? — a. 5 · b. 6 · c. 7 · d. 10

```sas
data Canada(drop=State Zip) US(drop=Province);
    set customer(keep=ID Name Country Status
                 Sales State Zip Province);
    if Country="Canada" then output canada;
    else if Country="US" then output us;
    drop Country;
run;
```

### Programming Question 3.01
Open `p201q1.sas` and fix it so that: Country values are all uppercase in the outputs; rows with missing TermDate are included; Country US → emp_US table; AU → emp_AU table. Qs: rows in emps_US? rows in emps_AU? [table names appear as both emp_ and emps_ in the source]

### Programming Question 3.02
New program: read sashelp.heart, split into `dead` and `alive` by Status; drop Status from both, and DeathCause and AgeAtDeath from alive. Qs: (1) rows in dead? (2) Cholesterol for row 100 of alive? (3) number of columns in alive?

### Programming Question 3.03
New program: from cr.employee_current create summary table `salary` with TotalSalary (sum of Salary) per Department, one row per Department. Then table `salaryforecast` reading salary: write 3 rows per input row – Year=1 with TotalSalary × 1.03, then Year=2 and Year=3 each increased by another 3%; display TotalSalary as currency rounded to whole numbers. Qs: (1) Strategy department total salary before the forecast (rounded)? (2) Rows in salaryforecast? (3) Engineering forecast for year 3?

## 3.2 Summarizing Data

### Summarizing Data (video 7:08)
- Key concepts: creating/accumulating totals and processing data in groups.
- Computed columns are reset to missing at the top of each iteration by default. **RETAIN** keeps a column's value in the PDV for the next iteration.
- Demo: simple DATA step converting height (inches → centimeters, HeightCM) with **PUTLOG** statements (write messages to the log during execution – useful to understand processing and diagnose logic errors) before SET, after the calculation, and at the end; `obs=3` data set option on SET limits processing. Without RETAIN, HeightCM is missing at the top of each iteration. With `RETAIN HeightCM`, the value at the start of iteration 2 equals the end of iteration 1. An initial value can be given in RETAIN (log then shows 0 instead of missing at the start).
- December running total: PROC SORT to temporary table `decDaily`, filter month of Order_Date = 12, BY Order_Date. DATA step: MTDSales = previous MTDSales + Profit with `RETAIN MTDSales 0`; FORMAT as currency; KEEP to limit columns. Result: running total but one row per order.
- Goal: one row per day with MTDSales (accumulating all month) and DailySales (reset each day).
  - **SUM statement** `MTDSales+Profit;` – creates and retains the column on the left, adds the value each row, ignores missing values → RETAIN no longer needed.
  - `DailySales+Profit;` with a **BY Order_Date** statement, which processes groups and creates **FIRST.** and **LAST.** variables in the PDV flagging the start/end of each day. Before the sum statement: IF first.Order_Date = 1 THEN DailySales = 0.
  - **Subsetting IF** `if last.Order_Date=1;` – if true, the rest of the iteration (including implicit output) runs; if false, SAS goes to the next iteration without outputting the row.
  - Result: one row per day, MTDSales accumulating, DailySales reset daily.

### Review Quiz: Summarizing Data (read-only; all 10 read from screenshots, never answered)
- **Q1.** Which of the following statements about the RETAIN statement is false? — a. The placement of the RETAIN statement in the DATA step might impact the order of columns in the PDV. · b. The RETAIN statement can be used to establish an initial value for a column at the beginning of the execution phase. · c. The RETAIN statement can be used with IF-THEN syntax to retain a column value in the PDV only if a condition is true during the execution phase. · d. The RETAIN statement can include both numeric and character columns.
- **Q2.** Which statement contains valid syntax for the RETAIN statement? — a. `retain city $ "Cary";` · b. `retain city="Cary";` · c. `retain city "Cary";` · d. `retain city("Cary");`
- **Q3.** True or False: In this example, both the RETAIN and sum statements are required to create the **Total** column. — a. True · b. False

```sas
data retailTotal;
    set retail;
    retain Total 0;
    Total+Sales;
run;
```
Output shown (Sales, Total): 100 100 · 200 300 · . 300 · 300 600
- **Q4.** Given this input table and code, what is the value of **Total** at the end of the third iteration of the DATA step? (input Sales: 100, 200, ., 300) — a. . (missing) · b. 300 · c. 400 · d. 600

```sas
data retailTotal;
    set retail;
    retain Total 100;
    Total+Sales;
run;
```
- **Q5.** Which of the following statements about using the BY statement with the SET statement is false? (stray "display") — a. The data sets listed in the SET statement must be indexed or sorted by the values of the BY variable or variables. · b. The DATA step automatically creates two variables, **FIRST.** and **LAST.**, for each variable in the BY statement. · c. **FIRST.** and **LAST.** identify the first and last observation in each BY group, respectively. · d. **FIRST.** and **LAST.** are stored in the data set.
- **Q6.** True or False: Each of the following statements perform the same action. — a. True · b. False

```sas
if First.Make;
if First.Make=1;
where First.Make;
where First.Make=1;
```
- **Q7.** What is the value of **First.Make** and **Last.Make** for row 167 if **sashelp.cars** is sorted by **Make**? — a. First.Make=1 and Last.Make=1 · b. First.Make=1 and Last.Make=0 · c. First.Make=0 and Last.Make=1

```sas
data cars;
    set sashelp.cars(keep=Model Make Type);
    by Make;
run;
```
Rows shown (Make, Model, Type): 165 Honda Odyssey EX Sedan · 166 Honda S2000 convertible 2dr Sports · 167 Hummer H2 SUV · 168 Hyundai Santa Fe GLS SUV · 169 Hyundai Accent 2dr hatch Sedan · 170 Hyundai Accent GL 4dr Sedan
- **Q8.** What is the value of **First.Type** and **Last.Type** for row 168 if **sashelp.cars** is sorted by **Make** and **Type**? (same rows as Q7) — a. First.Type=1 and Last.Type=1 · b. First.Type=1 and Last.Type=0 · c. First.Type=0 and Last.Type=1

```sas
data cars;
    set sashelp.cars(keep=Model Make Type);
    by Make Type;
run;
```
- **Q9.** Which statement must be added to this DATA step to reset the value of **TotalSales** for each new BY group? — a. `TotalSales=0;` · b. `if First.Region=1 then TotalSales=0;` · c. `if Last.Region=0 then TotalSales=0;` · d. `if First.Region=1 and Last.Region=1 then TotalSales=0;`

```sas
data shoetotal;
    set sashelp.shoes;
    by Region;
    <insert statement>
    TotalSales+Sales;
    if last.Region;
run;
```
- **Q10.** Which statement creates the table **carsMax** that includes the highest MSRP for each value of **Make** and the calculated profit? — a. `if first.Make;` · b. `if first.Make then output;` · c. `if last.Make;` · d. `if last.Make then output;`

```sas
proc sort data=sashelp.cars
          out=carsPrice;
    by Make MSRP;
run;

data carsMax;
    set carsPrice;
    by Make;
    <insert statement>
    Profit=MSRP-Invoice;
run;
```

### Programming Question 3.04
New program: read sashelp.stocks → `stocks_total`, only Date in year 2005; accumulating column YTDVolume = running total of Volume for each stock. Qs: (1) rows in stocks_total? (2) YTDVolume for Intel on 01AUG2005?

### Programming Question 3.05
New program: read sashelp.shoes → `highlow` with one row for the lowest Sales per Product and one for the highest Sales per Product; column HighLow = "High"/"Low". Qs: (1) rows in highlow? (2) subsidiary with the highest Sales for Sandals? (3) region with the lowest Sales for Boot?

### Programming Question 3.06
Open `p202q3.sas` and fix it so that: one row per Department in `dept_salary`; TotalDeptSalary = total Salary within each department; LowSalaryJob = job title for the minimum salary in each department; HighSalaryJob = job title for the maximum salary in each department. Qs: (1) TotalDeptSalary for Accounts? (2) LowSalaryJob for Engineering? (3) HighSalaryJob for Logistics Management?

## 3.3 Manipulating Data with Functions

### Using Numeric and Date Functions (video 7:46)
- SAS has over 600 functions and CALL routines. You don't need all of them for the exam: the **certification content guide lists the specific functions** to know.
- Table qtr_sales (customers, birth dates, quarterly purchase totals):
  - `TotalPurchase` = **SUM** of the qtr columns. With a column list in a function, you must start with the keyword **OF**; shortcut `qtr:` = all columns starting with "qtr". Other summary functions: MEAN, MEDIAN, MIN, MAX, …
  - `AvgPurchase` = **MEAN**(of qtr:) wrapped in **ROUND**(…, 0.01) → two decimal places. FORMAT both as currency.
  - `Customer_Age` = **YRDIF**(BirthDate, **TODAY**(), "age") – arguments: start date, end date, basis ("age" in quotes). Result is very precise; wrapped in **INT** to truncate (not round) to the integer part.
  - `Promo_Date` = **MDY**(**MONTH**(BirthDate), 1, **YEAR**(TODAY())) – first day of the birth month in the current year; numeric SAS date, formatted `mmddyy10.`.
  - `FirstName` = **SCAN**(Name, 1, ' ') – by default spaces, hyphens and other punctuation are delimiters; the optional third argument restricts the delimiter list (here only a space), so hyphenated first names (row 24) stay intact.
  - `ID` = **PUT**(Customer_ID, **z5.**) – PUT converts numeric to character; z5. writes leading zeros to 5 positions.
  - DROP statement removes some columns.
- Column order = the order columns are added to the PDV during compilation. To reorder, use a separate DATA step with a **RETAIN statement before SET** listing columns in the desired order; it's strongly recommended not to do other processing in that step.

### Using the INTNX and INTCK Functions (video 3:16)
- WHERE Order_Date > **INTNX**('month', TODAY(), -6): arg1 interval, arg2 start date, arg3 number of intervals (positive = forward, negative = backward). Demo date: November 9, 2018 → May.
- INTNX by default aligns to the **beginning** of the interval (orders from the start of May). Optional 4th argument alignment: 'same' (same day), also beginning, middle, end → with 'same', orders from May 9, 2018 on.
- `BusDays` = **INTCK**('weekday', Order_Date, Delivery_Date) [interval spoken as "weekdays" – exact keyword VERIFY]: arg1 interval in quotes, arg2 start, arg3 end → number of Monday–Friday days between.
- Narrator: thorough review of exam functions, but check the content guide for others.

### Review Quiz: Manipulating Data with Functions (read-only; all 10 read from screenshots, never answered)
- **Q1.** Which statement calculates the sum of **SalesQ1**, **SalesQ2**, **SalesQ3**, and **SalesQ4**? (table columns in order: Office, SalesYear, SalesQ1, SalesQ2, SalesQ3, SalesQ4; e.g. San Francisco 2018 $8,850 $12,046 $8,695 $9,425; London, Toyko [sic], Sydney)
  - a. `TotalSales=sum(of SalesQ1--SalesQ4);`
  - b. `TotalSales=sum(of Sales:);`
  - c. `TotalSales=sum(SalesQ1-SalesQ4);`
  - d. all of the above
- **Q2.** Which assignment statement extracts *2019* from the **Text** variable? — a. `Year=scan(Text, -1);` · b. `Year=scan(Text, 6);` · c. `Year=scan(Text, 6, ', ');` [delimiter string shown as quote-comma-space-quote; exact characters UNCLEAR] · d. all of the above

```sas
data Scan_Quiz;
    Text="New Year's Day, January 1st, 2019";
run;
```
- **Q3.** Which statement or statements store the rounded value of **HeightCM** with one decimal place? (Name, Height, HeightCM: Alfred 69 175.3 · Alice 56.5 143.5 · Barbara 65.3 165.9 · Carol 62.8 159.5 · Henry 63.5 161.3)
  - a. `HeightCM=round(Height*2.54, 1);`
  - b. `HeightCM=round(Height*2.54, .1);`
  - c. `HeightCM=Height*2.54; format HeightCM 5.1;`
  - d. all of the above
- **Q4.** In the program below, the assignment statement successfully concatenates **Title**, **First**, and **Last** to create **FullName**. Which statement produces the same result? (rows: Ms. Farr Sue → "Ms. Sue Farr"; Dr. Cox Kay B. → "Dr. Kay B. Cox"; Mr. Mason Ron; Ms. Ruth G. H.; Prof. Florentino Helen-Ash → "Prof. Helen-Ash Florentino")

```sas
data names;
    set customers;
    FullName=trim(Title)||" "||trim(First)||" "||trim(Last);
run;
```
  - a. `FullName=catx(" ", Title, First, Last);`
  - b. `FullName=cats(" ", Title, First, Last);`
  - c. `FullName=cats(Title, First, Last);`
  - d. `FullName=cat(Title, " ", First, " ", Last);`
- **Q5.** Based on the following program and results, which statement is false? (CurrentDate 21515; CurrentTime 42168.653; CurrentDateTime 1858938168.7) — a. **CurrentDate** represents the number of days from January 1, 1960. · b. **CurrentTime** represents the number of seconds from 12pm (noon). · c. **CurrentDateTime** represents the number of seconds from 12am (midnight) on January 1, 1960.

```sas
data current;
    CurrentDate=today();
    CurrentTime=time();
    CurrentDateTime=datetime();
run;
```
- **Q6.** True or False: Based on the data below, the **doctor1** and **doctor2** tables have the same rows. — a. True · b. False

Data customers (Title, Name): Ms. Farr,Sue · Dr. Cox,Kay B. · Mr. Mason,Ron · Ms. Ruth,G. H. · Ms. Van Allsburg,Jan F. · DR. Mitchell,Marc J. · Ms. Mills,Dorothy E. · Dr. Webb,Jonathan W.
```sas
data doctor1;
    set customers;
    Title=upcase(Title);
    where Title="DR.";
run;

data doctor2;
    set customers;
    where upcase(Title)="DR.";
run;
```
- **Q7.** Which of the following assignment statements returns the SAS date value for February 26, 2019?
  - a. `Date=mdy("FEB", 26, 2019` (no closing parenthesis/semicolon as shown)
  - b. `Date=mdy("26FEB2019"d);`
  - c. `Date=mdy(2, 26, 2019);`
  - d. all of the above
- **Q8.** Which expression correctly converts numeric **ID** values to character strings? — a. `put(ID, $5.)` · b. `put(ID, 5.)` · c. `input(ID, $5.)` · d. `input(ID, 5.)`
- **Q9.** Which of the following statements converts the character values of **Service** to numeric SAS date values? (values 03JUN2018, 08MAR2018, 12SEP2018, 11JUN2018, 07SEP2018)
  - a. `ServiceDate=input(Service, date9.);`
  - b. `ServiceDate=input(Service, anydtdte.);`
  - c. `ServiceDate=input(Service, mmddyy9.);`
  - d. a and b
  - e. all of the above
- **Q10.** Assuming the **ID** column in the **employees** table is numeric, which statement is true? — a. **ID** is converted to a character column. · b. A syntax error is generated and the step fails. · c. The step runs, but **ID** is not converted to a character column.

```sas
data convert;
    set employees;
    ID=put(ID, 5.);
run;
```

### Programming Question 3.07
New program: sashelp.fish → temporary `fish`; Length = mean of Length1–Length3, stored rounded to the nearest hundredth; summary report of average Length per Species, rounded to 2 decimals. Qs: (1) Length in row 2 of fish? (2) How many Perch were measured? (3) Average length of all Pike?

### Programming Question 3.08
New program: sashelp.baseball → `outfield`, only players whose Position has F as the **second letter**; Player = Name rearranged as "first last" separated by a space; BatAvg = nHits/nAtBat rounded to 3 decimals; sort by descending BatAvg. Qs: (1) rows in outfield? (2) Player in row 1? (3) BatAvg for Kirby Puckett?

### Programming Question 3.09
Open `p203q3.sas` and fix it so that HireDate is converted to a numeric SAS date and Salary is the numeric equivalent of the character column AnnualSalary. Qs: (1) Raw value of HireDate in row 2 of emp_new? (2) Which informat can be used in the INPUT function to create Salary?

## 3.4 Creating and Using Custom Formats

### Creating and Using Custom Formats (video 6:19)
- Custom formats via **PROC FORMAT**, used in DATA or PROC steps.
- ShipDays ranges: 0 = "Same day", 1–3 = "1 - 3 days", 4–7, 8 or more. `PROC FORMAT; VALUE shiprange …;` – numeric format because it applies to numeric values; **character format names must start with `$`**. Labels up to **32,767** characters. Keyword **HIGH** for the open-ended top range; good practice to label missing values too. The log confirms the format was output – by default to the **Work** library.
- Three ways to use it:
  1. DATA step `profit2` from cr.profit with `FORMAT ShipDays shiprange.;` → permanently associated with the column. When applied, the format name must end with a **period**.
  2. **PUT** function: new column `ShipRange = put(ShipDays, shiprange.)` – keeps the raw values and adds a character column of formatted values.
  3. FORMAT statement inside a procedure: PROC FREQ TABLE ShipDays with the FORMAT statement → counts per formatted range (report only).
- Format from a lookup table: create a table with columns **FmtName** (format name, here `$ctryfmt`), **Start** (raw value = Country_Key) and **Label** (display value = Country_Name) from cr.country_clean, keeping only those three; then `PROC FORMAT CNTLIN=` that table [transcript says "CNTLINE="; quiz Q10 shows `cntlin=` – confirmed] creates the format. Applied to Customer_Country → full names displayed.

### Review Quiz: Creating Custom Formats (title on quiz page: "Review Quiz: Creating Custom Formats"; read-only; all 10 read from screenshots, never answered)
- **Q1.** Which of the following statements about the name of a format in the VALUE statement is false? — a. The name cannot end with a number or include a period. · b. The name cannot be the name of a SAS format. · c. The name cannot be the name of a data set variable. · d. The name must begin with a dollar sign ($) if used with a character variable.
- **Q2.** Which of the following FORMAT procedures is written correctly?

```sas
/* a */
proc format value colorfmt;
    1='Red'
    2='Green'
    3='Blue'
run;
/* b */
proc format;
    value colorfmt
    1='Red'
    2='Green'
    3='Blue';
run;
/* c */
proc format;
    value colorfmt;
    1='Red'
    2='Green'
    3='Blue';
run;
/* d */
proc format;
    value colorfmt
    1='Red';
    2='Green';
    3='Blue';
run;
```
- **Q3.** How many characters can be used in a format label? — a. 96 · b. 200 · c. 256 · d. 32,767
- **Q4.** Which keyword can be used to label missing numeric values as well as any values that are not specified in a range? — a. LOW · b. MISS · c. MISSING · d. OTHER
- **Q5.** In the VALUE statement, labels are assigned to a range of data values. Which statement about specifying a range is false? — a. a range can include a single value, such as 24 or 'S' · b. a range can include numeric values, such as 0-1500 · c. a range can include character values, such as 'A'-'M' · d. a range of values for a numeric format can include a list of numeric and character values separated by commas, such as 90,'135',180,'215',270
- **Q6.** You can place the FORMAT statement in either a DATA step or a PROC step. What happens when you place it in a DATA step? — a. You temporarily associate the formats with variables. · b. You permanently associate the formats with variables. · c. You replace the original data with the format labels. · d. You make the formats available to other data sets.
- **Q7.** Suppose the format JOBFMT was created in a FORMAT procedure. Which FORMAT statement applies it to the variable **JobTitle** in the program output? — a. `format jobtitle jobfmt;` · b. `format jobtitle jobfmt.;` · c. `format jobtitle=jobfmt;` · d. `format jobtitle='jobfmt';`
- **Q8.** Suppose you do not specify the LIBRARY= option when creating a custom format. How long does the format exist? — a. only for the current procedure · b. only for the current DATA step · c. only for the current SAS session · d. permanently
- **Q9.** Which of the following statements store your formats in a permanent location?

```sas
/* a */
libname fmtlib 'c:\formats';
proc format lib=fmtlib;
   ...;
/* b */
libname fmtlib 'c:\formats';
format lib=fmtlib;
   ...;
/* c */
fmtlib='c:\formats';
proc format fmtlib;
   ...;
/* d */
fmtlib='c:\formats';
proc format;
library=fmtlib;
   ...;
```
- **Q10.** Which column is not required in the **country** table to build a custom format with the following program? — a. **Fmtname** · b. **Start** · c. **Value** · d. **Label**

```sas
proc format cntlin=country;
run;
```

### Programming Question 3.10
Numeric format **BMIRANGE**: < 18.5 Underweight; 18.5–24.9 Normal; 25–29.9 Overweight; 30 or more Obese. Frequency report on BMI in sashelp.bmimen for Age ≥ 21 with BMIRANGE applied. Qs: count Overweight? count Underweight?

### Programming Question 3.11
Use cr.continent_codes to build numeric format **CONTFMT** (Code = values, Continent = labels). From sashelp.demographics, sum Pop for each Cont with CONTFMT applied. Qs: (1) countries in the European continent? (2) total population in Africa?

### Programming Question 3.12
Open `p204q3.sas` and fix it: custom formats for Status (M, S, O) and for Salary ranges, applied in the PROC FREQ step. Qs: (1) employees in the Other category? (2) San Diego employees making $50K–$100K?

## 3.5 Combining Tables

### Concatenating Tables (video 3:57)
- Concatenate rows: DATA step with several tables in the SET statement – assumes they share columns and attributes; demo shows what happens when names/attributes don't match.
- cr.orders (2018) + cr.orders2017 (previous year) added to the SET statement of the Profit-cleaning step.
- Log **WARNING: multiple lengths were specified** for Customer_Continent. Lengths: 19 in Orders, 20 in Orders2017. Attributes are inherited implicitly from the **first table listed in SET**. Fix: **LENGTH statement before SET** setting Customer_Continent to 20 → warning gone, no truncation risk.
- Different column names: rows from cr.orders have missing Line/Category; rows from orders2017 have missing Product_Line/Product_Category (same data, different names). Fix: **RENAME=** data set option after cr.orders2017: `(rename=(Line=Product_Line Category=Product_Category))` – parentheses around the data set options and around the rename pairs. Result: no warnings, columns aligned.

### Merging Tables (video 4:49)
- Goal: add product names from `products` to Profit, and find products never ordered.
- Rules: each table needs at least one **common column** whose values determine matches (Product_ID); each input must be **sorted by the matching column** (DATA step merge compares rows sequentially) → PROC SORT both into temporary `profit_sort` and `products_sort`.
- DATA `profit_detail` `product_nosales`; `MERGE profit_sort(in=inProf) products_sort(in=inProd); BY Product_ID;` – **IN=** creates temporary columns in the PDV (not output) with 1/0 per row: both 1 = match; one 1 and the other 0 = non-match.
- `if inProf=1 and inProd=1 then output profit_detail;` `if inProf=0 and inProd=1 then output product_nosales;` (IDs in products but not in profit).
- Results: profit_detail has all **10,781** orders with product name ("still sorted by product name" as spoken [VERIFY – likely Product_ID]); product_nosales has **441** rows, all columns from both tables but only Product_ID and Product_Name have values → add **KEEP=** data set option on product_nosales to keep only those two.

### Review Quiz: Combining Tables (read-only; all 10 read from screenshots, never answered)
- **Q1.** After this code runs, what is the order of the columns in the **empsall** table? — a. Name, Status · b. Name, Status, Country · c. Name, Status, Country, Region · d. The program fails because the tables have different columns.

```sas
data empsall;
    set empscn empsjp;
run;
```
empscn (Name, Status, Country): Chang M China · Li M China · Ming S China. empsjp (Name, Status, Region): Cho F Japan · Tomi M Japan
- **Q2.** Which statement creates the **empsall** table as shown? (empscn as above; empsjp: Cho O Japan · Tomi M Japan with column Region; empsall shows Name, Status, Country with all 5 rows and Japan in Country)
  - a. `set empscn(rename=(Country=Region)) empsjp;`
  - b. `set empscn rename=(Region=Country) empsjp;`
  - c. `set empscn empsjp(rename(Country=Region));`
  - d. `set empscn empsjp(rename=(Region=Country));`
- **Q3.** If the length of **Name** in the **empscn** table is 5, and the length of **Name** in the **empsjp** table is 6, what happens when the following code is submitted? (empsjp: Cho O Japan · Tomi M Japan · Himari S Japan; both tables have Country) — a. A syntax error is generated and the step does not run. · b. The length of **Name** in **empsall** is 6 based on the maximum length of **Name** in the two input tables. All the values of **Name** are stored correctly. · c. The length of **Name** in **empsall** is 5 based on the first table listed in the SET statement. A warning is issued, and the values of **Name** in **empsjp** might be truncated to 5 characters.

```sas
data empsall;
    set empscn empsjp;
run;
```
- **Q4.** Which statement about merging with matching rows is true? — a. The SET statement and the MERGE statement are used together in the DATA step to merge tables. · b. Two or more input tables can be merged in a DATA step. · c. The BY statement in the DATA step names a column to order the output table. · d. By default, the DATA step writes only matching rows to the output table.
- **Q5.** What happens if you submit the following program to merge the **donor1** and **donor2** tables shown below? — a. The merged data set contains some missing values because not all rows have matching rows in the other data set. · b. The merged data set contains eight observations. · c. The DATA step produces errors. · d. Values for **Units** in **donor2** overwrite values of **Units** in **donor1**.

```sas
data combine;
    merge donor1 donor2;
    by ID;
run;
```
donor1 (ID, Type, Units): 2304 0 16 · 1129 A 48 · 1129 A 50 · 1129 A 57 · 2486 B 63. donor2 (ID, Code, Units): 1129 63 32 · 2304 61 45 · 1287 64 67 (as displayed – neither table appears sorted by ID)
- **Q6.** If you merge the tables project and hours by ID and Name, how many rows does the new table contain? — a. three · b. five · c. six · d. nine

project (ID, Name, Dept, Project): 000 Miguel A12 Document · 111 Fred B45 Survey · 222 Diane B45 Document · 888 Monique A12 Document · 999 Vien D03 Survey. hours (ID, Name, Hours): 111 Fred 35 · 222 Diane 40 · 777 Steve 0 · 888 Monique 37
- **Q7.** If you merge the tables **reps**, **close**, and **bonus** by **ID**, what is the value of **Bonus** in the third observation in the new data set? — a. $4,000 · b. $3,000 · c. missing · d. You cannot tell from the information given.

reps (ID, Name): 1 Nay Rong · 2 Kelly Windsor · 3 Julio Meraz. close (ID, Sale): 1 $28,000 · 2 $30,000 · 2 $40,000 · 3 $15,000 · 3 $20,000 · 3 $25,000. bonus (ID, Bonus): 1 $2,000 · 2 $4,000 · 3 $3,000
- **Q8.** Which statement best describes the rows in the output table **combine**? — a. all the matching rows from both **project** and **hours** · b. only the rows from **project** that have no match in **hours** · c. only the rows from **hours** that have no match in **project** · d. all the matching and nonmatching rows from both **project** and **hours**

```sas
data combine;
    merge project(in=p) hours(in=h);
    by ID;
    if p=1 and h=0;
run;
```
- **Q9.** In this merge, how many rows are written to the output table other (same project and hours tables as Q6) — a. unknown · b. one · c. two · d. three

```sas
data match other;
    merge project(in=p) hours(in=h);
    by ID;
    if p=1 and h=1 then output match;
    else output other;
run;
```
- **Q10.** The tables **spring** and **summer** both contain a variable named **blue**. Which step prevents the values of the column **blue** from being overwritten when the two tables are merged?

```sas
/* a */ data merged; merge spring(in=blue) summer; by fabric; run;
/* b */ data merged; merge spring(out=blue) summer; by fabric; run;
/* c */ data merged; merge spring(blue=navy) summer; by fabric; run;
/* d */ data merged; merge spring(rename=(blue=navy)) summer; by fabric; run;
```
(each option shown on separate lines: data / merge / by / run)

### Programming Question 3.13
New program: concatenate cr.m7_sales, cr.m8_sales, cr.m9_sales → `q3_sales`, putting similar columns with different names into one column; frequency report of orders per Order_Type. Qs: (1) rows in q3_sales? (2) columns? (3) orders with Order_Type 1?

### Programming Question 3.14
New program: merge cr.employee and cr.employee_addresses → `emp_full`, including all rows from cr.employee, ordered by EmpID. Qs: (1) rows in emp_full? (2) Emp_ID in row 27? (3) Street_Number in row 20?

### Programming Question 3.15
Open `p205q3.sas` and fix: `donation` table has all EmpID values in both cr.employee and cr.employee_donations; TotalDonation computed in donation; extra table `nodonation` with EmpIDs in cr.employee but not in cr.employee_donations. Qs: (1) rows in donation? (2) TotalDonation for "Hill, Ronald"? (3) rows in nodonation?

## 3.6 Processing Repetitive Code

### Using Iterative and Conditional DO Loops (video 4:39)
- DO loop replaces copy-pasted code. Earlier forecast step (3 OUTPUTs per row of profit summary → Profit_Forecast) rewritten with an **index column**: `do Year=1 to 3;` (range) or `do Year=1, 2, 3;` (list). Range: no need to list values, easy to change to 10. List: allows nonsequential and **character** values; loop runs once per item. Body: assignment + OUTPUT; close with `end;`. DO loops don't make programs faster, just shorter.
- Reserve account example: table Rewards; initial reserve 1,000,000; `do Year=1 to 10;` add 25,000 per year, earn 3% interest, OUTPUT; `end;`; format reserve.
- Rewards = withdrawal of 100,000 created before the loop (negative value), added to reserve inside the loop after contribution and interest → not depleted after 10 years, but declining.
- **DO WHILE (reserve > 0)**: expression evaluated at the **top** of the loop; loop executes again if true. Year now created with a sum statement (`Year+1`) since no index column. Reserve drops below 0 in the **18th** year.

### Using Nested DO Loops (video 4:25)
- Monthly contributions and monthly compounding: inside the DO WHILE, after incrementing Year, a nested `do Month=1 to 12;` adds $2,500 and earns 1/12 of 3% interest; rewards paid at the end of each year → a couple of extra years before depletion.
- What-ifs: $5,000 monthly → lasts 50 years; 4% interest → **infinite loop** (reserve never < 0; must cancel the submitted code). Fix: combine an index with a condition – loop from Year=1 to 50 or until reserve < 0, whichever comes first [exact syntax not in transcript – likely `do Year=1 to 50 until(reserve<0)` VERIFY]; the Year sum statement is no longer needed.
- Rates table created in a DATA step with an INPUT statement and **DATALINES** (data typed in the program): four rates. The Rewards step reads each rate; with OUTPUT inside the loop there's one row per year per rate. Removing the OUTPUT statement → implicit output at the end of each iteration (one row per rate); DROP rewards and month → one row per rate with the negative balance and the years until it occurs.

### Review Quiz: Processing Repetitive Code (read-only; all 10 read from screenshots, never answered)
- **Q1.** Which statement about DO loops is false? — a. They can contain conditional clauses. · b. They can generate multiple observations. · c. They can be used to combine DATA and PROC steps. · d. A DO loop can be nested inside another DO loop.
- **Q2.** Which statement about the iterative DO loop is true? (syntax shown: `DO index-column = start TO stop <BY increment> ;`) — a. The start and stop values can be character or numeric values. · b. If an increment value is not specified, the default increment is 1. · c. The index column is incremented at the start of each DO loop. · d. The index column is temporary and is not included in the output table.
- **Q3.** How many times does the DO loop in this code execute? — a. 0 · b. 1 · c. 12 · d. 13
- **Q4.** After this code runs, how many rows are in the **earnings** table? — a. unknown · b. 1 · c. 12 · d. 13
- **Q5.** After this code runs, what is the value of **Month** in the **earnings** table? — a. unknown · b. 1 · c. 12 · d. 13

```sas
/* same program for Q3, Q4, Q5 */
data earnings;
    Amount=1000;
    Rate=.075/12;
    do Month=1 to 12;
        Earned+(amount+earned)*rate;
    end;
run;
```
- **Q6.** Which of the following statements about the program shown below is false? — a. The OUTPUT statement writes the values in the PDV to the **invest** table at the end of each DO loop iteration. · b. The last value for **Year** in the new table is 2005. · c. The OUTPUT statement overrides the implicit OUTPUT at the end of the DATA step. · d. The DO loop performs 15 iterations.

```sas
data work.invest;
    do year=1990 to 2004;
        Capital+5000;
        capital+(capital*.10);
        output;
    end;
run;
```
- **Q7.** Which of the following would you use to compare the result of investing $4,000 a year for five years with interest compounded monthly? — a. DO WHILE statement · b. nested DO loops · c. DO UNTIL statement · d. a DO group
- **Q8.** Which statement about DO UNTIL loops is false? — a. The condition is evaluated at the top of the loop, before the enclosed statements are executed. · b. The enclosed statements are always executed at least once. · c. SAS statements in the DO loop are executed until the specified condition is true. · d. The DO loop must have a closing END statement.
- **Q9.** True or False: These two programs generate the same result. — a. True · b. False

```sas
data work.invest;
    capital=100000;
    do until(Capital gt 500000);
        Year+1;
        capital+(capital*.10);
    end;
run;

data work.invest;
    capital=100000;
    do while(Capital le 500000);
        Year+1;
        capital+(capital*.10);
    end;
run;
```
- **Q10.** In the following program, complete the DO statement so that the program stops generating observations when **Distance** reaches 250 miles or when 10 gallons of fuel have been used. — a. `while(Distance<250)` · b. `when(Distance>250)` · c. `until(Distance=250)` · d. `or until(Distance>=250)`

```sas
data work.go250;
    set cert.cars;
    do gallons=1 to 10 ... ;
        Distance=gallons*mpg;
        output;
    end;
run;
```

### Programming Question 3.16
New program: from cr.shoes_summary create `shoes_future`, writing 5 rows per input row with Year 1–5; increase ProfitPerStore by 3% each year; drop TotalStores and TotalProfit. Qs: (1) rows in shoes_future? (2) ProfitPerStore for Asia in year 5?

### Programming Question 3.17
Open `p206q2.sas`: insert a DO loop computing Wages, Retire, Medical for 10 years with annual increases Wages 6.0%, Retire 1.4%, Medical 9.5%; TotalCost = sum of each year's Wage, Retire, Medical; comma format rounded to whole numbers; one row per year. Qs: (1) Medical when Year = 5? (2) TotalCost when Year = 10?

### Programming Question 3.18
Open `p206q3.sas`: Income starts at 50,000,000 and increases 1% per year; add Year storing the DO loop iteration number; loop stops when TotalCost exceeds Income. Qs: (1) rows in income_expenses? (2) TotalCost when it exceeds Income?

## 3.7 Restructuring Tables

### Using the DATA Step to Restructure Tables (video 4:56)
- **Wide** table (qtr_sales: one row per customer, a column per quarter) suits DATA step functions per customer. **Narrow** table (sales: one Sales column plus a Qtr identifier) suits most reporting/analytics: PROC MEANS, PROC FREQ, graphics.
- Wide → narrow with explicit OUTPUT: after SET, `Qtr="Qtr1"; Sales=Qtr1; output;` repeated for each quarter; KEEP the four needed columns. Then PROC MEANS on Sales with CLASS Qtr, statistics SUM and MEAN, rounded to integers (overall and per class value).
- Narrow → wide (data ordered by Customer_ID): IF-THEN/ELSE IF on Qtr assigning Sales to new columns Qtr1–Qtr4; **RETAIN Qtr1-Qtr4** so earlier quarters persist until the Qtr4 row; **BY Customer_ID** to get FIRST./LAST.; subsetting `if last.Customer_ID=1;`; DROP Qtr and Sales.

### Using PROC TRANSPOSE to Restructure Tables (video 3:15)
- Wide → narrow: `PROC TRANSPOSE DATA=qtr_sales OUT=sales_n;` **VAR** qtr: (columns to turn into a single column); **BY** Customer_ID Name (keeps them with each value). Output has _NAME_ and COL1 columns.
- **NAME=** option renames _NAME_ (to Qtr). **PREFIX=** replaces "COL" but a number (1) is always appended – for a name without a number use the **RENAME=** data set option. **DROP=** data set option removes _LABEL_.
- PROC TRANSPOSE needs less code; the DATA step allows additional manipulation in the same step. Know both.
- Narrow → wide: VAR Sales (transposed into columns), BY creates one row per unique BY value; columns default to COL1–COL4; the **ID** statement uses values of Qtr as the new column names; DROP= removes _NAME_.

### Review Quiz: Restructuring Tables (read-only; all 10 read from screenshots, never answered)
- **Q1.** Which is the better description for the following table? (Employee_ID, Home, Work, Cell – one row per employee: 120106 (02) 2555 5993 · (02) 2555 3888 · 0461 555 555; 120107 … no Cell; 120108 …; 120109; 120110) — a. wide table · b. narrow table
- **Q2.** Which table structure is better to use as input in PROC FREQ to report the count of phone numbers for **Home**, **Work**, and **Cell**? — a. table with Employee_ID, Phone_Type (Home/Work/Cell), Phone – one row per phone · b. table with Employee_ID, Home, Work, Cell – one row per employee
- **Q3.** True or False: The following program writes three rows to the **phone_narrow** table for each row read from the input table. — a. True · b. False

```sas
data phone_narrow;
    set phone_w;
    Phone_Type="Home";
    Phone=Home;
    Phone_Type="Work";
    Phone=Work;
    Phone_Type="Cell";
    Phone=Cell;
run;
```
- **Q4.** The following program generates the results shown. Which statement is needed so that the last row for each value of **Employee_ID** includes all known phone numbers for an individual? — a. KEEP · b. VAR · c. OUTPUT · d. RETAIN

```sas
data phone_wide;
    set phone_n;
    if Phone_Type="Home" then Home=Phone;
    else if Phone_Type="Work" then Work=Phone;
    else if Phone_Type="Cell" then Cell=Phone;
run;
```
Results shown: one row per input row; Home/Work/Cell filled only on the matching row (e.g. 120106 Home row has only Home; 120106 Work row has only Work; 120106 Cell row has only Cell).
- **Q5.** Which statement about the TRANSPOSE procedure is false? — a. It can be used to create either narrow or wide tables. · b. By default, all numeric columns are transposed. · c. If a BY statement is used to group the data, the input table must be sorted. · d. By default, PROC TRANSPOSE overwrites the input table with the restructured table.
- **Q6.** The following DATA step creates the sales_wide table. Could PROC TRANSPOSE be used to produce the same result? — a. Yes · b. No

```sas
data sales_wide(drop=Type Amount);
    set qtr_sales;
    retain Goal;
    by Qtr;
    if Type="Goal" then Goal=Amount;
    else Sales=Amount;
    if last.Qtr;
    Difference=Goal-Sales;
run;
```
qtr_sales (Qtr, Type, Amount): 1 Goal 1000 · 1 Sales 1300 · 2 Goal 1200 · 2 Sales 1400 · 3 Goal 1500 · 3 Sales 1400 · 4 Goal 2000 · 4 Sales 2100 → sales_wide (Qtr, Goal, Sales, Difference): 1 1000 1300 -300 · 2 1200 1400 -200 · 3 1500 1400 100 · 4 2000 2100 -100
- **Q7.** Which statement must be added in PROC TRANSPOSE to create the **phone_n** table? — a. `id Employee_ID;` · b. `id Employee_ID Phone_Type;` · c. `by Employee_ID;` · d. `by Employee_ID Phone_Type;`

```sas
proc transpose data=phone_w
               out=phone_n(rename=(col1=Phone))
               name=Phone_Type;
    var Home Work Cell;

run;
```
phone_w (Employee_ID, Home, Work, Cell): 120106, 120107 (no Cell), 120108 → phone_n (Employee_ID, Phone_Type, Phone): 9 rows, three per employee (120107 Cell row has blank Phone)
- **Q8.** What is the result of the following program (sf_temp: Year, Month ("01 - January" …), AvgTemp; 2016 rows Jan–Dec then 2017 rows, e.g. 2016 01 - January 52.7 … 2017 03 - March 56.9; table sorted by Year then Month) — a. The step does not process because of errors. · b. The output table has one row with the transposed values of **AvgTemp**. · c. The output table includes one row for each year and one column for each month. · d. The output table includes one row for each month and one column for each year.

```sas
proc transpose data=sf_temp;
    var AvgTemp;
    by Month;
    id Year;
run;
```
- **Q9.** The following program creates this output table. Which option in the PROC TRANSPOSE statement can be used to rename the new columns as **Year2016** and **Year2017**? (output columns: Month, _NAME_, _2016, _2017; e.g. 01 - January AvgTemp 52.7 50.6) — a. LABEL= · b. NAME= · c. PREFIX= · d. VAR=

```sas
proc transpose data=sf_temp
               out=sf_annual;
    var AvgTemp;
    by Month;
    id Year;
run;
```
- **Q10.** Which statement must be used in a DATA step to create FIRST./LAST. variables in the PDV? — a. BY · b. ID · c. FIRST or LAST · d. KEEP

### Programming Question 3.19
Open `p207q1.sas`: in PROC SORT remove rows with duplicate Region, Subsidiary, Product; in PROC TRANSPOSE transpose Sales into columns by Product values, one row per Region × Subsidiary; drop _NAME_ and _LABEL_. Qs: (1) rows removed by PROC SORT? (2) rows in shoe_sales? (3) columns in shoe_sales? (4) Sandal value for Toronto in the Canada region?

### Programming Question 3.20
New program: cr.employee_training → `training_narrow`, wide to narrow with one row per date value; report counting courses completed by month (hint: MONNAME. format). Qs: (1) rows in training_narrow? (2) courses completed in April? (3) courses with a missing date?

## Programming Question answers and solution code (revealed with "Show Answer"/"Show Solution Code"; read from screenshots)

### PQ 3.01 — answers: (1) rows in emps_US = **235** · (2) rows in emps_AU = **73**
```sas
data emp_US emp_AU;
    set cr.employee(keep=EmpID Name JobTitle Salary Department Country TermDate);
    where TermDate = .;
    Country=upcase(country);
    if Country="US" then output emp_US;
    else output emp_AU;
run;
```

### PQ 3.02 — answers: (1) rows in dead = **1991** · (2) Cholesterol row 100 of alive = **150** · (3) columns in alive = **14**
```sas
data alive(drop=DeathCause AgeAtDeath Status) dead(drop=Status);
    set sashelp.heart;
    if Status="Alive" then output alive;
    else if Status="Dead" then output dead;
run;
```

### PQ 3.03 — answers: (1) Strategy total salary before forecast = **95131** · (2) rows in salaryforecast = **51** · (3) Engineering forecast year 3 = **377380**
```sas
proc means data=cr.employee_current noprint;
    var Salary;
    class Department;
    output out=salary sum=TotalSalary;
    ways 1;
run;

data salaryforecast;
    set salary;
    format TotalSalary dollar12.;
    Year=1;
    TotalSalary=TotalSalary*1.03;
    output;
    Year=2;
    TotalSalary=TotalSalary*1.03;
    output;
    Year=3;
    TotalSalary=TotalSalary*1.03;
    output;
run;
```

### PQ 3.04 — answers: (1) rows in stocks_total = **36** · (2) YTDVolume Intel 01AUG2005 = **513162839**
```sas
proc sort data=sashelp.stocks out=stocks_sort;
    by Stock Date;
    where year(Date)=2005;
run;

data stocks_total;
    set stocks_sort;
    by Stock;
    if first.Stock then YTDVolume=0;
    YTDVolume+Volume;
    format YTDVolume comma15.;
run;
```

### PQ 3.05 — answers: (1) rows in highlow = **16** · (2) subsidiary with highest Sandals sales = **Kingston** · (3) region with lowest Boot sales = **Western Europe**
```sas
proc sort data=sashelp.shoes out=highlow;
    by Product Sales;
run;

data highlow;
    length HighLow $ 4;
    set highlow;
    by Product;
    if first.product then do;
        HighLow="Low";
        output;
    end;
    if last.product then do;
        HighLow="High";
        output;
    end;
    keep Region Product HighLow Sales Subsidiary;
run;
```

### PQ 3.06 — answers: (1) TotalDeptSalary Accounts = **723288** · (2) LowSalaryJob Engineering = **Technician I** · (3) HighSalaryJob Logistics Management = **Director**
```sas
proc sort data=cr.employee_current out=emp_sort;
    by Department Salary;
run;

data dept_salary;
    set emp_sort;
    retain LowSalaryJob;
    by Department;
    if first.Department then do;
        TotalDeptSalary=0;
        LowSalaryJob=JobTitle;
    end;
    TotalDeptSalary+Salary;
    if last.department then do;
        HighSalaryJob=JobTitle;
        output;
    end;
    keep Department TotalDeptSalary HighSalaryJob LowSalaryJob;
    format TotalDeptSalary dollar12.;
run;
```

### PQ 3.07 — answers: (1) Length row 2 = **27.17** · (2) Perch measured = **56** · (3) average Pike length = **45.56**
```sas
data fish;
    set sashelp.fish;
    Length=round(mean(of L:), .01);
run;

proc means data=fish mean maxdec=2;
    var Length;
    class Species;
run;
```

### PQ 3.08 — answers: (1) rows in outfield = **107** · (2) Player in row 1 = **Tim Raines** · (3) BatAvg Kirby Puckett = **.328**
```sas
data outfield;
    set sashelp.baseball;
    where substr(Position, 2, 1)="F";
    Player=catx(" ", scan(Name, 2, ','), scan(Name, 1, ','));
    BatAvg=round(nHits/nAtBat, .001);
    keep Player BatAvg Position;
run;

proc sort data=outfield;
    by descending BatAvg;
run;
```

### PQ 3.09 — answers: (1) raw HireDate row 2 of emp_new = **18643** · (2) informat for Salary = **COMMA or DOLLAR**
```sas
data emp_new;
    set cr.employee_new(rename=(HireDate=CharDate));
    EmpID=substr(EmpID, 4);
    HireDate=input(CharDate, anydtdte10.);
    Salary=input(AnnualSalary, dollar12.);
    drop CharDate;
run;
```

### PQ 3.10 — answers: (1) Overweight count = **521** · (2) Underweight count = **14**
```sas
proc format;
    value bmirange low-<18.5="Underweight"
                   18.5-24.9="Normal"
                   25-29.9="Overweight"
                   30-high="Obese";
run;

proc freq data=sashelp.bmimen;
    where age>=21;
    tables bmi;
    format bmi bmirange.;
run;
```

### PQ 3.11 — answers: (1) countries in Europe = **46** · (2) total population in Africa = **904804386**
```sas
data continentfmt;
    set cr.continent_codes;
    retain fmtname "contfmt";
    Start=Code;
    Label=Continent;
run;

proc format cntlin=continentfmt;
run;

proc means data=sashelp.demographics sum maxdec=0;
    var pop;
    class cont;
    format cont contfmt.;
run;
```

### PQ 3.12 — answers: (1) employees in Other category = **40** · (2) San Diego employees making $50K–$100K = **20**
```sas
proc format;
    value $statfmt "S"="Single"
                   "M"="Married"
                   "O"="Other";
    value salrange low-<50000="Under $50K"
                   50000-100000="50K-100K"
                   100000<-high="Over 100K";
run;

proc freq data=cr.employee;
    tables Status;
    tables City*Salary / nopercent nocol;
    format Status $statfmt. Salary salrange.;
run;
```

### PQ 3.13 — answers: (1) rows in q3_sales = **32** · (2) columns = **6** · (3) orders with Order_Type 1 = **19**
```sas
data q3_sales;
    set cr.m7_sales cr.m8_sales(rename=(Employee_ID=EmpID)) cr.m9_sales;
run;

proc freq data=q3_sales;
    table Order_Type;
run;
```

### PQ 3.14 — answers: (1) rows in emp_full = **424** · (2) Emp_ID row 27 = **120127** · (3) Street_Number row 20 = **46**
```sas
proc sort data=cr.employee_addresses(rename=(Employee_ID=EmpID)) out=address_sort;
    by EmpID;
run;

data emp_full;
    merge cr.employee(in=e) address_sort;
    by EmpID;
    if e;
run;
```

### PQ 3.15 — answers: (1) rows in donation = **124** · (2) TotalDonation for Hill, Ronald = **60** · (3) rows in nodonation = **300**
```sas
proc sort data=cr.employee(keep=EmpID Name Department) out=emp_sort;
    by EmpID;
run;

proc sort data=cr.employee_donations out=donate_sort;
    by EmpID;
run;

data donation nodonation(keep=Name Department);
    merge emp_sort(in=in_emp) donate_sort(in=in_don);
    by EmpID;
    if in_don=1 and in_emp=1 then do;
        TotalDonation=sum(of Qtr1-Qtr4);
        output donation;
    end;
    else if in_don=0 and in_emp=1 then output nodonation;
run;
```

### PQ 3.16 — answers: (1) rows in shoes_future = **50** · (2) ProfitPerStore Asia year 5 = **8014**
```sas
data shoes_future;
    set cr.shoes_summary;
    do year=1 to 5;
        ProfitPerStore=ProfitPerStore*1.03;
        output;
    end;
    drop Total:;
run;
```

### PQ 3.17 — answers: (1) Medical when Year = 5 = **1021681** · (2) TotalCost when Year = 10 = **26692006**
```sas
data future_expenses;
    Wages=12874000;
    Retire=1765000;
    Medical=649000;
    do Year=1 to 10;
        Wages=Wages*1.06;
        Retire=Retire*1.014;
        Medical=Medical *1.095;
        TotalCost=sum(Wages,Retire,Medical);
        output;
    end;
    format Wages Retire Medical TotalCost comma12.;
run;
```

### PQ 3.18 — answers: (1) rows in income_expenses = **26** · (2) TotalCost when it exceeds Income = **67973189**
```sas
data income_expenses;
    Wages=12874000;
    Retire=1765000;
    Medical=649000;
    Income=50000000;
    do until (TotalCost > Income);
        year+1;
        Wages=Wages * 1.06;
        Retire=Retire*1.014;
        Medical=Medical *1.095;
        TotalCost=sum(Wages, Retire, Medical);
        income=Income *1.01;
        output;
    end;
    keep Year Income TotalCost;
    format Income TotalCost comma12.;
run;
```

### PQ 3.19 — answers: (1) rows removed by PROC SORT = **1** · (2) rows in shoe_sales = **53** · (3) columns in shoe_sales = **10** · (4) Sandal for Toronto/Canada = **1190**
```sas
proc sort data=sashelp.shoes out=shoes_sort nodupkey dupout=out;
    by Region Subsidiary Product;
run;

proc transpose data=shoes_sort out=shoes_sales(drop=_name_ _label_);
    var Sales;
    by Region Subsidiary;
    id Product;
run;
```

### PQ 3.20 — answers: (1) rows in training_narrow = **912** · (2) courses completed in April = **97** · (3) courses with missing date = **216**
```sas
proc sort data=cr.employee_training out=training_sort;
    by Name;
run;

/* Either PROC TRANSPOSE or the DATA step will create training_narrow */

proc transpose data=training_sort out=training_narrow(rename=(col1=Date)) name=Course;
    by Name;
    var Compliance_Training Corporate_Security On_the_Job_Safety;
run;

/* OR */

data training_narrow;
    set training_sort;
    Course="Compliance Training";
    Date=Compliance_Training;
    output;
    Course="Corporate_Security";
    Date=Corporate_Security;
    output;
    Course="On_the_Job_Safety";
    Date=On_the_Job_Safety;
    output;
    drop Compliance_Training Corporate_Security On_the_Job_Safety;
    format Date date9.;
run;

proc freq data=training_narrow;
    tables Date;
    format Date monname.;
run;
```

## Gaps
- Demo code visible only in video.
- PQ program/data files not captured. Quizzes and PQ answers/solutions captured from screenshots.
