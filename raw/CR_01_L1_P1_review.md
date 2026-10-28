# CR – Lesson 1: SAS Programming 1 Review

Source: Certification Review player (id=238), text mode (video transcripts). Captured 2026-10-28. Paraphrased; short quotes in quotation marks. Code shown on screen in the videos is NOT in the transcripts → listed under Gaps.

## 1.1 Essentials

### Program Structure and Syntax (video 2:47)
- A program = series of DATA and PROC steps. Demo program has 3 steps: DATA step creating `shoes_profit`, PROC MEANS creating a summary table, PROC PRINT reporting on the summary table.
- Each step ends with RUN; statements that begin/end a step are "step boundaries". Every statement ends with a semicolon.
- Global statements sit outside steps (demo: two TITLE statements; also OPTIONS, LIBNAME). They stay in effect until changed or until the SAS session ends.
- After running: read the log first (notes, warnings, errors), then the output. Demo created two tables (shoes_profit, shoes_summary) and one report.
- Spacing doesn't matter (whole DATA step on one line still runs); consistent spacing helps readability. SAS Studio "Format Code" button auto-formats.
- Comments: `*` at the start of a statement comments out that statement (demo: the LABEL statement in PROC PRINT); `/* … */` comments any length of text; Ctrl+/ wraps the line in comment symbols.

### Required Column Attributes (video 3:33)
- Three required attributes: **name, length, type**.
- Names: 1–32 characters; start with a letter or underscore; then letters, digits, underscores; any case. Some environments allow spaces/special symbols; course recommends standard SAS naming. Table names follow the same rules.
- Type: character or numeric (SAS Studio icons: "A" vs "1,2,3"). Numeric values can include digits 0–9, a minus sign, a single decimal point, and E for scientific notation. Character columns can hold anything you can type (letters, numbers, special characters, blanks).
- Dates: a SAS date is numeric = number of days from **January 1, 1960**. Easy to sort and calculate with; apply a format to display. Demo: copy RawDate to FormattedDate and use a FORMAT statement with `DATE9.` (day-month-year) then `WORDDATE.` (full month name, day, year).
- Length = bytes allocated. Numeric default length **8** (about 16 significant digits). Character length 1 to **32,767** bytes, one byte per character. Demo: Region length 25 (fits "Central America/Caribbean"); Subsidiary length 12.
- Optional attributes: labels and formats. Demo: Profit has a label assigned in the DATA step and format `DOLLAR12.` (dollar sign, commas, rounded to whole number).

### Finding and Resolving Syntax Errors (video 2:04)
- Missing semicolon after the SET statement → syntax error; the log shows SAS trying to read PROFIT as part of a numbered data set list, and lists expected symbols including a semicolon.
- Missing period after `DOLLAR12` in a FORMAT statement → no error or warning, results produced, but the log NOTE says "Variable dollar12 is uninitialized": SAS treats `dollar12` as a column name in the FORMAT statement. Valid syntax but a **logic error**. Lesson: read notes too, not only errors and warnings.

### Review Quiz: Essentials (10 questions; opened read-only, NOT answered or submitted)
All 10 questions read (screenshots + text).

- **Q1.** A SAS program always creates which of the following? (a stray word "display" appears under the stem [UNCLEAR]) — a. log · b. output · c. results · d. all of the above
- **Q2.** Which of the following is a SAS syntax requirement? — a. Begin each statement in column one. · b. Put only one statement on each line. · c. Separate each step with a line space. · d. End each statement with a semicolon.
- **Q3.** How many steps are in this program? — a. one · b. two · c. three · d. four

```sas
libname orion "c:/mydata";

data work.sales;
    set orion.employee;
    where Job_Title like "%Sales%";
    Bonus=Salary*.02;
    format Bonus euro8.;
run;

title "Sales Listing";

proc print data=work.sales;
run;
```
- **Q4.** How many statements does the first step contain? (same program as Q3) — a. 1 · b. 2 · c. 6 · d. 10
- **Q5.** Which of the following statements are considered step boundaries (the end of one step and the beginning of another)? — a. RUN, QUIT, and END · b. RUN, EXIT, and QUIT · c. RUN, END, DATA, and PROC · d. RUN, QUIT, DATA, and PROC
- **Q6.** True/False: "If this program is submitted, the DATA step will not execute because it does not conclude with a RUN statement." — a. True · b. False · c. It depends on the interface.

```sas
libname orion "c:/mydata";

data work.sales;
    set orion.employee;
    where Job_Title like "%Sales%";
    Bonus=Salary*.02;
    format Bonus euro8.;

title "Sales Listing";
proc print data=work.sales;
run;
```
- **Q7.** What generally happens when SAS detects a syntax error? — a. SAS stops processing the entire program. · b. SAS continues to process the step, and the SAS log displays messages about the error. · c. SAS stops processing the step in which the error occurred, and the SAS log displays messages about the error. · d. SAS stops processing the step in which the error occurred, and the Results tab displays messages about the error.
- **Q8.** Does this comment contain syntax errors? — a. No. The comment is correctly specified. · b. Yes. Every comment line must end with a semicolon. · c. Yes. The comment is on more than one line. · d. Yes. There is a semicolon in the middle of the comment.

```sas
*******************************
Report created for budget
presentation; revised October 15.
*******************************;
proc print data=sales;
run;
```
(asterisk-line lengths approximate)
- **Q9.** Based on the program and data shown below, which of the following is true? — a. A syntax error is generated because STATE is uppercase in the program. · b. A syntax error is generated because single quotation marks are used in the WHERE statement. · c. There are no syntax errors, and three rows are printed. · d. There are no syntax errors, but no rows are printed.

```sas
proc print data=cities;
    where STATE='ca';
run;
```
Table cities (State, City): CA Sacramento · OR Eugene · UT Provo · CA Pasadena · NV Reno · CA Palo Alto
- **Q10.** Which statement is true regarding global SAS statements? — a. A SAS global statement can be used anywhere in a SAS program. · b. A RUN statement must follow each global statement. · c. A QUIT statement must follow each global statement. · d. A SAS program must include at least one global statement.

### Programming Question 1.01 (question text only; answers/solution → Visual Queue)
Open `p101q1.sas` from the programs folder, find and fix the syntax errors, run it, then answer: (1) How many rows are in the CanadaSales table? (2) What is the value of Diff for row 5 in CanadaSales?

### Programming Question 1.02
Open `p101q2.sas`, fix the syntax errors, run it, then answer: (1) How many countries are in the EUR region? (2) What is the average population for the AFR region?

## 1.2 Accessing Data

### Overview (video 0:38)
- Review of accessing structured data directly with a LIBNAME statement + engine, and importing unstructured data with PROC IMPORT. Demo data: simple retail sales data stored in a comma-delimited file and an Excel workbook.

### Directly Accessing Structured Data (video 3:38)
- `country_lookup.xlsx`, worksheet Countries: lookup table with two-letter Country_Key, latitude, longitude, full country name.
- Starts the program with a comment line (Ctrl+/).
- `%LET` creates a macro variable named `path` storing the string `s:/workshop`; later `&path` is used and SAS replaces it with `s:/workshop` before the statement executes.
- Reads Excel directly (so programs pick up file updates) with a LIBNAME statement: libref `ctryxl` (libref must follow SAS naming conventions and be **8 characters or less**), engine **XLSX**, then full path + file name + extension in quotes (using `&path`). Other engines read SAS or DBMS tables directly.
- (read from screenshot) If a macro variable is used in a quoted string, you **must use double quotation marks**.
- By default both SAS Studio and SAS Enterprise Guide keep spaces and special symbols in column names when reading data. To enforce standard naming: `options validvarname=v7;`. In **Enterprise Guide** this option persists for the whole SAS session after submission.
- In SAS Studio the `VALIDVARNAME=` option resets to the default **ANY** each time you submit a new program. To enforce standard naming rules in SAS Studio: More application options → Preferences → SAS variable name policy = **V7** → Save.
- Run, then check in the Libraries panel: CTRYXL → COUNTRIES opens.

### Importing Unstructured Data (video 2:43)
- `orders.csv`: comma-delimited, column headings in row 1, one row per order. An unstructured file can't be read directly with LIBNAME → use PROC IMPORT.
- Options: `DATAFILE=` (path and file to read), `OUT=` (new SAS table, here `orders`), `DBMS=` (file type: CSV here; also TAB for tab-delimited, XLSX for Excel), `REPLACE` (overwrite the output table if it exists).
- Log: all **10,786** rows read. Table has an ID, order and delivery dates, item columns, customer columns; some inconsistencies are visible (explored later).
- The table in Work is temporary. Add a LIBNAME statement creating library `cr` ("certification review") pointing to the course output folder, and write `cr.orders` by prefixing the libref → permanent table; confirmed in Libraries panel.

### Viewing Table Properties with PROC CONTENTS (video 2:36)
- One PROC CONTENTS step per table: `cr.orders`, then `ctryxl.countries`.
- Terminology: data set = table, observation = row, variable = column; used interchangeably in SAS and on the exam.
- In cr.orders the two date columns are numeric and automatically formatted `DATE9.`; Cost_Price, Quantity, Retail_Price were read as numeric.
- `ctryxl._ALL_` in PROC CONTENTS: brief list of all tables in the library, then full descriptor portion for each (both worksheets). Adding the **NODS** option after `_ALL_` suppresses the descriptor portions, leaving only the list.
- Program saved as "Sales Analysis".

### Review Quiz: Accessing Data (10 questions; read-only, not answered). All 10 read (Q1–Q5 text, Q6–Q10 screenshots).
- **Q1.** Which data source could be read using a library? — a. Microsoft Excel Workbook · b. tab-delimited file · c. comma-delimited file · d. all of the above
- **Q2.** What type of variable is Salary in the table below? (columns LastName, FirstName, JobTitle, Salary; rows: TORRES JAN Pilot 50000 · LANGKAM SARAH Mechanic 80000 · SMITH MARY Mechanic . · JONES PHILLIP Pilot 7750 · TULLEKEN NADIA [blank JobTitle?] 65000 [UNCLEAR – table layout read as text]) — a. numeric · b. character · c. cannot tell from the data shown · d. either numeric or character
- **Q3.** With the system option VALIDVARNAME=V7, which of the following variable names is valid? — a. 4BirthDate · b. $Cost · c. _Items_ · d. Tax-Rate · e. all of the above
- **Q4.** Which of the following files is a permanent SAS file? — a. Work.PrdSale · b. MySales · c. Certxl.Quarter1 · d. all of the above
- **Q5.** What is the default length of the BillDate column, which contains formatted SAS date values? (values 6/13/2018, 3/8/2018, 9/12/2018, 12/11/2018, 9/7/2018) — a. unknown · b. 8 · c. 9 · d. 10
- **Q6.** Which LIBNAME statement defines the **states** library to read SAS files in the **myfilespopstats** folder on the **C:** drive? — a. `libname states 'c:myfiles\x27;` · b. `libname base states 'c:myfilespopstats';` · c. `libname states sas 'c:myfilespopstats';` · d. `libname states 'c:myfilespopstats';`
- **Q7.** When you specify an engine for a library, what are you specifying? — a. the file format for files that are stored in the library · b. the name of a folder or directory where files are stored · c. credentials to access protected files · d. instructions for creating temporary SAS files
- **Q8.** Which option must be added to the PROC IMPORT statement to read a tab-delimited file? — a. TAB · b. DBMS=TAB · c. DLM=TAB · d. DLM=" " [contents of the quotes UNCLEAR]

```sas
proc import datafile="d:/mydata/tourism.tab"
            out=tourism replace;
run;
```
- **Q9.** Which statement about the CONTENTS procedure is false? (stray "display" under the stem) — a. PROC CONTENTS can be used to list all tables in a library. · b. The PROC CONTENTS report includes the engine used to read the data. · c. The PROC CONTENTS report displays all column attributes. · d. PROC CONTENTS lists a sample of the first five rows from the data.
- **Q10.** Which of the following statements lists the contents of the **orion** library in a report and suppresses the full detailed report for each individual table? — a. `proc contents data=orion;` · b. `proc contents data=orion._all_;` · c. `proc contents data=orion._all_ nods;` · d. `proc contents data=orion / _all_ nods;`

### Programming Question 1.03
Write a new program that reports the list of tables in the cr library (full descriptor portion not needed). Q: How many SAS tables are in the cr library?

### Programming Question 1.04
New program: read `payroll.csv` into a temporary table `payroll`, letting SAS scan all rows of the text file to determine column attributes; report the descriptor portion of payroll. Qs: (1) Value of Employee_Term_Date for row 23? (2) According to the report, what engine is used to read the payroll table?

### Programming Question 1.05
New program: read `employee.xlsx` directly, making column names follow recommended SAS naming rules; report the descriptor portion of every table read from the workbook. Qs: (1) Which column name was automatically changed to follow the rules? (give the original name) (2) What type is Employee_ID in both worksheets?

## 1.3 Exploring Data

### Overview (video 0:46)
- Explore/validate the orders CSV data and the Excel country lookup. Tools reviewed: PROC PRINT, FREQ, MEANS, UNIVARIATE to inspect values and find inconsistencies; WHERE to subset rows on one or more conditions; PROC SORT to reorder and remove duplicate rows.

### Using SAS Procedures to Explore and Validate Data (video 6:53)
- **Country lookup (ctryxl.countries):** PROC PRINT with `DATA=` and the data set option `OBS=30` to limit rows. 4 columns incl. Country_Key (2 letters) and Country_Name. Country_Key should be unique, but rows 4 and 5 look like exact duplicates.
- PROC FREQ with a TABLE statement for Country_Key and Country_Name, option `ORDER=FREQ` (descending frequency) to surface non-unique codes → 4 problem codes: AG, CF, GB, US; only "Antigua Barbuda" is duplicated in Country_Name.
- PROC PRINT + WHERE listing rows where Country_Key is AG, CF, GB or US: AG rows are exact duplicates; for the others the same code maps to two versions of the country name → keep the first one listed.
- PROC SORT: `DATA=` the worksheet, `OUT=` sorted copy `country_clean`, BY Country_Key; **NODUPKEY** keeps only the first row per BY value; **DUPOUT=** `dups` captures removed rows. Log: 237 rows in → 233 in country_clean; dups has the 4 removed rows.
- **Orders validation rules:**
  - Delivery_Date should be after Order_Date: PROC PRINT + WHERE Order_Date > Delivery_Date, VAR Order_ID Order_Date Delivery_Date → 5 suspicious rows; Delivery_Date miscoded as 0 (= January 1, 1960). Fix in Prepare phase.
  - Order_Type must be 1 (in-store), 2 (phone), 3 (internet); Customer_Country must be 2 uppercase letters; Customer_Continent one of 5 continents → PROC FREQ TABLE on the three columns: 3 orders have Order_Type 99 (to be set to missing); some lowercase Customer_Country values; Customer_Continent all fine.
  - PROC MEANS with VAR Quantity Retail_Price Cost_Price and `MAXDEC=0` (round to whole numbers) to check min/max → Quantity minimum is −1 (invalid; fix later).
  - Changing `means` to `univariate` (and removing MAXDEC=) → long output; the **Extreme Observations** table at the bottom for each column shows the 5 highest and 5 lowest values.

### Review Quiz: Exploring Data (read-only; all 10 read – Q1–Q2 text, Q3–Q10 screenshots)
- **Q1.** What does a PROC PRINT report display by default? — a. PROC PRINT does not create a default report; you must specify rows and columns. · b. All rows and columns; a row-number column can be requested. · c. Columns in this order: row numbers, all character columns, all numeric columns. · d. All rows and columns, a row-number column on the far left, and columns in the order they occur in the table.
- **Q2.** Which procedure produces a report that lists the number of rows for each distinct value in a selected column? — a. CONTENTS · b. MEANS · c. FREQ · d. PRINT
- **Q3.** Which FORMAT statement produces the following results? (Order_Date e.g. 29/08/2018, 17/08/2018, 24/07/2018, 08/07/2018, 22/06/2018, 09/01/2018; Cost_Price e.g. $1,266.00, $1,449.75, $1,583.60, $1,391.40; Quantity 5, 5, 5, 2, 5, 6; Retail_Price e.g. $2,596.50, $2,840.50, $3,191.00, $3,058.80)
  - a. `format Order_Date ddmmyyyy. Cost_Price Retail_Price dollar10.2;`
  - b. `format Order_Date ddmmyy10. Cost_Price Retail_Price dollar10.2;`
  - c. `format Order_Date date10. Cost_Price Retail_Price $10.2;`
  - d. `format Order_Date dmy10. Cost_Price Retail_Price dollar10.2;`
- **Q4.** Which statement in PROC MEANS specifies the numeric columns to summarize? — a. COL · b. VAR · c. MEANS · d. TABLES
- **Q5.** Which statement selects rows with BirthDate on or after January 1, 1980?
  - a. `where BirthDate ge 1/1/1980;`
  - b. `where BirthDate >= '1/1/1980'd;`
  - c. `where Birthdate >= "01JAN1980";`
  - d. `where BirthDate ge "01JAN1980"d;`
- **Q6.** Which statement selects **ProductID** values with *CX* as the second and third letters in the string?
  - a. `where ProductID like "_CX%";`
  - b. `where ProductID like "%CX%"` (no semicolon as shown)
  - c. `where ProductID like "*CX*";`
  - d. `where ProductID like "_CX*";`
- **Q7.** Which statement selects rows where **Country** is either *Argentina* or *Brazil*? (stray "display")
  - a. `where Country="Argentina" or Country="Brazil";`
  - b. `where Country in("Argentina", "Brazil");`
  - c. `where Country in("Argentina" "Brazil");`
  - d. all of the above
- **Q8.** True or False: This PROC PRINT step creates a report that lists only those rows where **Location** is *Maui*. — a. True · b. False

```sas
%let island=Maui;

proc print data=tourism;
    where Location='&island';
run;
```
- **Q9.** Which step creates a new, temporary sorted table named **calc**?
  - a. `proc sort data=work.calc out=finance.dividend; run;`
  - b. `proc sort dividend out=calc; by account; run;`
  - c. `proc sort data=finance.dividend out=work.calc; by account; run;`
  - d. `proc sort from finance.dividend to calc; by account; run;`
- **Q10.** Given the following program and data, how many rows will be in the **quizdups** table? — a. zero · b. one · c. three · d. four

```sas
proc sort data=quiz nodupkey dupout=quizdups;
    by Name;
run;
```
Table quiz (Name, Score): Scott 8 · Scott 8 · Charlotte 10 · Trevor 7 · Trevor 6 · Trevor 6 · Drew 9

### Programming Question 1.06
Open `p103q1.sas`, fix the syntax errors, run. Qs: (1) Name of the first player in the baseball_sort table? (2) How many rows are in the PROC PRINT result? (3) Which Position value has the most players? (4) Average of Salary?

### Programming Question 1.07
New program using procedures to check whether employee_raw meets: EmpID unique; Country is US or AU; 17 unique department names; if TermDate is known it is after HireDate. Qs: (1) Which EmpID occurs more than once? (2) How many rows violate the Country rule? (3) Department with the most employees? (4) How many rows have a known TermDate before HireDate?

### Programming Question 1.08
New program: read employee_raw, create sorted `emp_sort` sorted by all columns with entirely duplicated rows removed. Using procedures on emp_sort: (1) EmpID of observation 10? (2) List employees whose JobTitle includes "Logistics" – year of the most recent hire in that group? (3) Average salary for employees hired on or after January 1, 2010 with missing TermDate? (4) Third highest salary among all employees?

## 1.4 Preparing Data

### Overview (video 1:29)
- Preparing data = most complex phase: fix issues found in validation; create new columns/tables for analysis.
- Main tools: DATA step and PROC SQL; valuable to know both and when each is easier. **No exam questions specifically about PROC SQL**, but SQL may be used in programming questions.
- Plan: DATA step reading cr.orders → new table Profit; clean case issues and invalid values first.

### Using the DATA Step to Prepare Data (video 6:32)
- DATA statement names `Profit` (Work library); SET reads `cr.orders`; filter to rows where Delivery_Date is on or after Order_Date (drops the rows with Delivery_Date 0 = Jan 1, 1960).
- `UPCASE` overwrites Customer_Country with uppercase values.
- IF-THEN: if Quantity < 0 then set Quantity to missing (missing values are ignored in analysis/summaries).
- Assignment statement: Profit = (Retail_Price − Cost_Price) × Quantity; FORMAT Profit with DOLLAR, width 12 and 2 decimals (room for digits, decimal point, comma, dollar sign).
- ShipDays = Delivery_Date − Order_Date (days between). Several ShipDays are 0: these have Order_Type 1 (in-store purchase).
- Age_Range = first 5 characters of Customer_Age_Group (drops the word "years") using **SUBSTR**: arg1 column, arg2 start position (1), arg3 number of characters (5). Narrator: many more functions from the courses may be on the exam – check the Exam Content Guide.
- Order_Source via IF-THEN / ELSE IF chain for Order_Type 1, 2, 3, else "Unknown". ELSE is most efficient: once a condition is true, the remaining ELSE IF statements are skipped.
- **Truncation:** Order_Source length defaults to **6** (from the first assigned string "Retail"), so "Internet" and "Unknown" are truncated. Fix: LENGTH statement after SET, `$` for character, length **8** (fits "Internet") – define attributes explicitly.
- DROP statement removes Retail_Price, Cost_Price, Customer_Age_Group, Order_Type from Profit.

### Using PROC SQL to Join Tables (video 3:15)
- Not tested on the exam but valuable. Goal: add full country names (country_clean, already de-duplicated) to Profit. Could use DATA step MERGE or SQL join; SQL used here (MERGE reviewed later).
- By default SQL creates a report; to create a table start the query with `create table profit_country as` then SELECT. `profit.*` selects all Profit columns; then `Country_Name` (only in country_clean, so no table qualifier needed).
- FROM `profit` INNER JOIN `country_clean`; ON clause defines matching rows: Customer_Country (profit) = Country_Key (country_clean). Prefixes optional when a column exists in only one table.
- ORDER BY Order_Date descending. One semicolon ends the whole query; QUIT ends PROC SQL. Result: profit_country with Country_Name added.

### Review Quiz: Preparing Data (read-only; all 10 read from screenshots, never answered)
- **Q1.** In which phase does the DATA step read rows from the input table? — a. compilation · b. execution
- **Q2.** Which statement about the following program is true? — a. The program does not execute because of syntax errors. · b. The program reads a temporary table and creates a permanent table. · c. The program reads a permanent table and creates a temporary table

```sas
data australia;
    set orion.sales;
    where Country='AU';
run;
```
- **Q3.** In the assignment statement below, what is the value of **AvgQ** for the row that is shown? (row: Q1=3, Q2=. , Q3=4, Q4=5) — a. 3 · b. 4 · c. . (missing value) · d. The statement generates a syntax error.

```sas
AvgQ=mean(Q1, Q2, Q3, Q4);
```
- **Q4.** Which expression extracts the first five positions from **PostalCode**? (values 95602-6485, 84604-9134, 07090-5839, 91001-6733, 27513-4402)
  - a. `PostalCode5=substr(PostalCode, 5);`
  - b. `PostalCode5=substr(PostalCode, 1, '-');`
  - c. `PostalCode5=substr(PostalCode,1-5);`
  - d. `PostalCode5=substr(PostalCode, 1, 5);` (a stray "." follows on screen)
- **Q5.** Which statement about the following program is true? — a. **Age** is calculated as a precise number of years (including decimal values). · b. **Age** is calculated and rounded to the nearest whole number. · c. **Age** is not calculated because the DROP statement is before the assignment statement. · d. **Age** is not calculated because the TODAY function does not include any arguments.

```sas
data customer_age;
    set orion.customers;
    drop BirthDate;
    Age=yrdif(BirthDate, today(),"AGE");
run;
```
- **Q6.** Which of the following is a way that the length of a new variable can be set in the DATA step? — a. by the length of the variable the first time it is referenced in the DATA step · b. in an assignment statement · c. using a LENGTH statement · d. all of the above
- **Q7.** What is the length of the variable **Type** that is created in the DATA step below? — a. 5 · b. 8 · c. 10 · d. It depends on the first value of **Type** in the **cert.recrds** table [sic]. · e. answer [placeholder option as shown]

```sas
data work.newloan;
    set cert.records;
    if code='1' then Type='Fixed';
    else Type='Variable';
    length type $ 10;
run;
```
- **Q8.** In the program below, what is the value of **Region** if **Area** is *nw*? — a. West · b. East · c. Other · d. missing

```sas
data work.bonus;
    set orion.sales;
        length Region $ 5;
    if Area in('NW', 'SW') then Region='West';
    else if Area in('NE', 'SE') then Region='East';
    else Region='Other';
run;
```
- **Q9.** In the program below, what is the value of **Region** if **Area** is *SW*? — a. West · b. East · c. Other · d. missing

```sas
data work.bonus;
    set orion.sales;
        length Region $ 5;
    if Area in('NW', 'SW') then Region='West';
    if Area in('NE', 'SE') then Region='East';
    else Region='Other';
run;
```
- **Q10.** True or False: This program will successfully create two tables, **east** and **west**. — a. True · b. False

```sas
data west east;
    set orion.sales;
    if Area in('NW', 'SW') then do;
        Region='West';
        output west;
    if Area in('NE', 'SE') then do;
        Region='East'
        output east;
run;
```
(as shown: no END statements, and no semicolon after `Region='East'`)

### Programming Question 1.09
Open and examine `sashelp.holiday`. Open `p104q1.sas`, fix syntax errors; CountryCode should be the last two letters of Category. Qs: (1) How many holidays with CountryCode CA are in the output table? (2) What value should be the second argument of SUBSTR to create CountryCode correctly? (3) SAS date value for Boxing Day?

### Programming Question 1.10
New program: table `sales` from cr.employee, only Sales Department employees with no TermDate. New column SalesLevel from JobTitle: Sales Rep. I → Entry; Sales Rep. II or III → Middle; Sales Rep. IV → Senior. Report count per level. Qs: (1) Total Sales employees? (2) Total middle-level sales reps?

### Programming Question 1.11
New program: table `bonus` from cr.employee; exclude employees with a known TermDate; YearsEmp = years employed as of 01JAN2019; if YearsEmp ≥ 10: Bonus = 3% of Salary, Vacation = 20; otherwise Bonus = 2%, Vacation = 15. Count employees with 20 and 15 vacation days. Sort bonus by descending YearsEmp. Qs: (1) Rows in bonus? (2) Years employed for row 1 of the sorted table? (3) How many have 20 vacation days? (4) Bonus of the last employee in the sorted table?

## 1.5 Analyzing Data

### Using PROC FREQ (video 3:03)
- Input: profit_country (clean). Reviews PRINT, FREQ, MEANS options plus TITLE, FOOTNOTE, LABEL.
- Q: which months have the most/fewest orders? No month column → TABLES Order_Date with a FORMAT statement using **MONNAME** (month name): FREQ counts per formatted value. Default: months in chronological order with cumulative columns.
- `ORDER=FREQ` on the PROC statement (descending counts) and `/ NOCUM` on the TABLE statement (suppress cumulative columns).
- Crosstab: `Customer_Continent*Order_Source` (asterisk) on the TABLE statement; options **NOROW** and **NOCOL** suppress row and column percentages. TITLE statements added before the step.
- Findings: December is busiest; > 50% of orders are retail purchases in Europe.
- `ODS NOPROCTITLE;` removes "The FREQ Procedure" heading; stays off for all reports for the rest of the SAS session.

### Using PROC MEANS (video 6:43)
- PROC MEANS on profit_country: VAR ShipDays, CLASS Country_Name; WHERE excludes ShipDays = 0 (in-store purchases).
- Streamline: statistics **MIN MAX MEAN** listed on the PROC statement; `MAXDEC=0`. WHERE extended to phone orders only; titles added.
- Macro variable: `%LET os=Phone;` before TITLE; replace Phone in TITLE and WHERE with `&os`. Strings containing a macro variable reference must be in **double quotation marks** for SAS to substitute. Changing the value to Retail shows some retail orders took more than two weeks.
- Separate statistics per Order_Source, two ways: (1) drop the WHERE and put Order_Source first in CLASS – no sorting needed, one row per Order_Source × Country_Name combination; (2) sort by Order_Source and use a **BY** statement → separate report per value (useful e.g. for one Excel worksheet per report).
- Q: which age group has the highest median profit per order? PROC MEANS, VAR Profit, CLASS Age_Range; **OUTPUT** statement creates table `profit_summary`; **NOPRINT** suppresses the report.
- Default output table: first 5 rows are basic statistics for all rows, with one column for the statistic name and one for the value. Fix: name the statistics and output column names in the OUTPUT statement (median and sum of Profit); **WAYS** statement to keep only one row per unique value of the CLASS column.
- Custom report from the summary table: PROC PRINT `DATA=profit_summary NOOBS` (suppress Obs column); VAR three columns; LABEL statement – and the **LABEL option on PROC PRINT** is required for labels to show; FORMAT total and median profit as currency rounded to the nearest dollar.

### Review Quiz: Analyzing Data (read-only; all 10 read from screenshots, never answered)
- **Q1.** If you run this program, which title or titles appear in the final PROC PRINT results? — a. Inventory Report · b. <blank line> / Inventory Report · c. ABC Company / Sales Report · d. ABC Company / Inventory Report

```sas
title 'ABC Company';
title2 'Sales Report';
proc print data=sales;
run;

title2 'Inventory Report';
proc print data=inventory;
run;
```
- **Q2.** Which statement is true based on the given program? — a. The column **BP_Status** has a permanent label in the **data.health** table. · b. The label for **BP_Status** appears in the PRINT report. · c. The label for **BP_Status** appears in the FREQ report. · d. The label for **BP_Status** appears in both reports.

```sas
data pressure;
    set data.health;
    BP=cats(Systolic, "/", Diastolic);
    label BP_Status=
        "Blood Pressure Status";
run;

proc print data=pressure(obs=10);
    var BP BP_Status;
run;

proc freq data=pressure;
    tables BP_Status;
run;
```
- **Q3.** Which of the following statements about the BY statement in a reporting procedure is false? (stray "display") — a. The input data must be sorted by the BY variables. · b. The procedure results are grouped by the unique values of the BY variables. · c. The BY statement can be used in the PRINT, MEANS, FREQ, and UNIVARIATE procedures. · d. **First./Last.** variables are created for each BY variable.
- **Q4.** Which statements must be added to this program to create the following report? — a. `id Employee_ID;` · b. `sum Salary;` · c. `keep Employee_ID Job_Title Salary;` · d. a and b · e. b and c

```sas
proc print data=employee;
    where Department="Executives";
    var Job_Title Salary;
    format Salary dollar10.;
run;
```
Report shown: Employee_ID column in the leftmost (ID-style, highlighted) position; Job_Title; Salary — 120259 Chief Executive Officer $433,800 · 120260 Chief Marketing Officer $207,885 · 120261 Chief Sales Officer $243,190 · 120262 Chief Financial Officer $268,455 · total row $1,153,330 (no Obs column).
- **Q5.** By default, PROC FREQ creates a table of frequencies and percentages for which column types? — a. character columns · b. numeric columns · c. both character and numeric columns · d. None. Columns must always be specified.
- **Q6.** Which TABLES statement can be used to create the following output? (two-way "Table of Department by City" with only Frequency and Percent in each cell; Departments Administration, Engineering, Sales, Sales Management, Stock & Shipping; Cities Melbourne, Sydney; Totals e.g. 26/47/73)
  - a. `tables Department*City;`
  - b. `tables Department*City / norow nocol` (no semicolon as shown)
  - c. `tables Department City / crosslist;`
  - d. `tables Department City / freq percent;`
- **Q7.** Which option is ***not*** required in the PROC FREQ step to produce this output? (title "Employees by Department"; "Number of Variable Levels" table: Department 17; one-way table with Frequency and Percent only (no cumulative columns), rows in descending frequency: Sales 122, Administration 31, IS 20, … Strategy 1) — a. LIST · b. NLEVELS · c. NOCUM · d. ORDER=FREQ
- **Q8.** Which statement about the MEANS procedure is true? — a. The input table must be sorted by the column(s) in the CLASS statement. · b. Default statistics include N, SUM, MEAN, MIN, and MAX. · c. The default output is a table. · d. Without a VAR statement, PROC MEANS summarizes all numeric columns from the input table.
- **Q9.** Which WAYS statement creates the following report? (three tables for Analysis Variable Salary: overall (N Obs 308), by City (Melbourne, Miami-Dade, Philadelphia, San Diego, Sydney), by Country (AU, US); no Country×City table) — a. `ways 1, 2, 3;` · b. `ways _all_;` · c. `ways 2;` · d. `ways 0 1;`

```sas
proc means data=employee;
    var Salary;
    class Country City;
run;
```
- **Q10.** True or False: To create the **SumSalary** and **MedianSalary** columns in the **SalSum** table, you must add the SUM and MEDIAN options to the PROC MEANS statement. — a. True · b. False

```sas
proc means data=employee noprint;
    var Salary;
    class Country City;
    output out=SalSum;
    ways 2;
run;
```
Table shown: Country, City, _TYPE_ (3), _FREQ_, SumSalary, MedianSalary — AU Melbourne 26 $816,260.00 $27,462.50 · AU Sydney 47 $1572235.00 $27,365.00 · US Miami-Dade 85 $3989355.00 $32,650.00 · US Philadelphia 68 $3079915.00 $31,372.50 · US San Diego 82 $3009125.00 $30,215.00

### Programming Question 1.12
Open `p105q1.sas`, fix the errors; output should appear as shown [image not captured]. Qs: (1) Label of nHome in sashelp.baseball? (2) Which option must be added so the descriptive column headings appear in the report? (3) Total home runs for Baltimore? (4) Which statement must be added so the player's name replaces the default OBS column?

### Programming Question 1.13
New program analyzing the number of employees in the employee table by City, Department, JobTitle. Qs: (1) City with the most employees? (2) % of all employees in Sales? (3) Number of unique JobTitle values?

### Programming Question 1.14
New program on cr.profit: two-way frequency table with count and percent for Order_Date × Order_Source; Order_Date displayed with MONNAME (one row per month). Qs: (1) Retail orders in December? (2) % of all orders that were Retail?

### Programming Question 1.15
New program: summary statistics for cr.employee, Sales department only; sum, mean, min, max of Salary per JobTitle, rounded to whole numbers. Qs: (1) Total salary of all Sales employees? (2) Mean salary for Sales Rep. IV?

### Programming Question 1.16
PROC MEANS on cr.employee → summary table `salary_summary`, no report; statistics for Salary by Department and City; output columns TotalSalary (sum) and AvgSalary (mean); one row per unique Department × City combination. Qs: (1) Rows in salary_summary? (2) AvgSalary for Administration in Sydney?

## 1.6 Exporting Data

### Overview (video 0:48)
- Final phase: share data and reports. PROC EXPORT for a text file; a library to write data directly to a structured file such as Excel; ODS to write reports to Excel, RTF or PDF, with options to customize results.

### Using PROC EXPORT (video 3:22)
- Export profit_country (cleaned) to a new CSV. PROC EXPORT options: `DATA=` (SAS table), `OUTFILE=` (full path, file name, extension), `DBMS=` (file type: CSV here; also tab-delimited, generic delimited with any character, Excel, Access), `REPLACE` (overwrite existing file). Only RUN needed after. Log confirms orders_update.csv created.
- In the exported file dates use DATE9. and currency values are formatted; values containing a comma are enclosed in quotation marks to distinguish them from delimiters.
- Excel via PROC EXPORT: change the file extension and DBMS=.
- Or the **XLSX LIBNAME engine**: create library `outxl` pointing to orders_update.xlsx; any output table written with the outxl libref becomes a worksheet (3 steps → Orders_Update, Country_Lookup, profit_summary → 3 worksheets). **LIBNAME outxl CLEAR** after the final step that writes to the workbook.

### Using the Output Delivery System (video 5:38)
- PDF: `ODS PDF FILE=` "location and file name" before the three validation procedures (each with a title), `ODS PDF CLOSE` after. Other destinations: HTML, RTF, Excel, PowerPoint, etc.
- Bookmarks: `PDFTOC=1` option on the first ODS statement shows only the first bookmark level by default. Copy each TITLE statement before its step and change the keyword TITLE to ODS PROCLABEL [transcript shows "ODSPROCLABEL" – VERIFY spacing] → bookmarks use report titles instead of procedure names.
- Excel: `ODS EXCEL FILE=` before the first PROC FREQ, `ODS EXCEL CLOSE` after the last PROC PRINT → one worksheet per report, tabs named after procedures, titles not shown by default.
- `options(embedded_titles='yes')` prints titles in the worksheets – narrator says this option **will not be tested** on the exam. `STYLE=ANALYSIS` changes the look. Additional ODS EXCEL statements before each procedure with `options(sheet_name=…)` [option name inferred from "provide a sheet name" – VERIFY] set tab names: "Orders by Month", "Orders by Continent, Source", "Profit by Age".

### Review Quiz: Exporting Data (read-only; all 10 read from screenshots, never answered)
- **Q1.** Which statement is false concerning the options for the PROC EXPORT statement? — a. The INFILE= option identifies the input SAS table. · b. The REPLACE option specifies to overwrite an existing file. · c. The DBMS= option specifies the database identifier for the type of file being created. · d. The OUTFILE= option specifies the path and file name of the external data file being created.
- **Q2.** Which PROC EXPORT step contains valid syntax?

```sas
/* a */
proc export outfile="c:\temp\sales.txt" tab
            data=orion.sales replace;
run;
/* b */
proc export data=orion.sales dbms=csv
            outfile="c:\temp\cars.csv";
run;
/* c */
proc export data=orion.sales; dlm=',';
            outfile="c:\temp\cars.csv";
run;
/* d */
proc export dbms=tab data=orion.sales replace=yes
            outfile="c:\temp\cars.txt";
run;
```
- **Q3.** True or False: This LIBNAME statement creates the midyear.xlsx file if it does not exist. — a. True · b. False

```sas
libname sales xlsx 'c:\mydata\midyear.xlsx';
```
- **Q4.** What does the following program create? — a. two SAS tables: **hr.US_Emp** and **hr.AU_Emp** · b. two Excel workbooks: **hr.US_Emp** and **hr. AU_Emp** · c. two worksheets in the Excel workbook **employee**: **US_Emp** and **AU_Emp** · d. two worksheets in the Excel workbook **employee_master**: **US_Emp** and **AU_Emp**

```sas
libname hr xlsx 'c:\mydata\employee.xlsx';

data hr.US_Emp;
    set orion.employee_master;
    where Country='US';
run;
data hr.AU_Emp;
    set orion.employee_master;
    where Country='AU';
run;
```
- **Q5.** Which of the following is ***not*** a valid output format when using the Output Delivery System (ODS)? — a. CSVALL · b. EXCEL · c. POWERPOINT · d. WORD · e. HTML
- **Q6.** True or False: The following program creates a comma-delimited file that includes column headings and all rows from the **employee** SAS table. — a. True · b. False

```sas
ods csvall "c:/output/employee.csv";
proc print data=employee;
    var ID Name Job_Title Hire_Date;
    format Hire_Date ddmmyy8.;
run;
ods close;
```
- **Q7.** True or False: This program will write results to both the POWERPOINT and EXCEL destinations. — a. True · b. False

```sas
ods powerpoint file="c:/output/EmpCounts.pptx";
ods excel file="c:/output/EmpCounts.xlsx";

proc freq data=eg1.employee_master;
    tables Country*Department;
run;

proc means data=eg1.employee_master;
    var Salary;
    class Country City;
run;

ods powerpoint close;
ods excel close;
```
- **Q8.** Which option in an ODS statement changes the appearance of the output, including colors, fonts, and borders? — a. STYLE= · b. OPTIONS= · c. LAYOUT= · d. CSS=
- **Q9.** Which statement contains valid syntax for specifying a worksheet name?
  - a. `ods proctitle sheet_name='Sales';`
  - b. `ods excel sheet_name='Sales';`
  - c. `ods proctitle options(sheet_name='Sales');`
  - d. `ods excel options(sheet_name='Sales');`
- **Q10.** Suppose that you are creating an Excel file and a PDF file that include results from multiple SAS procedures. What determines the text of each worksheet name in the Excel file and the table of contents link in the PDF file? — a. assigned titles · b. procedure names · c. Sheet1, Sheet2, and so on · d. Output1, Output2, and so on

### Programming Question 1.17
Open `p106q1.sas`, fix the errors, run. Download heart.xlsx from the output folder and open it. Qs: (1) Are the TITLE statement titles included in the spreadsheets? (2) How many worksheets are in the Excel file?

### Programming Question 1.18
Open `p106q2.sas` and modify: create truck.pdf combining the two procedures' results without a page break between them; apply the Journal style. Qs: (1) Label of the first bookmark in the PDF table of contents? (2) Do both reports fit on a single page?

### Programming Question 1.19
New program using PROC EXPORT to export cr.employee_current to a comma-delimited file. Qs: (1) File size rounded to the nearest KB (Properties)? (2) Viewing the file as text, which fields are enclosed in quotation marks?

## Programming Question answers and solution code (revealed with "Show Answer"/"Show Solution Code"; read from screenshots)

### PQ 1.01 — answers: (1) **120** rows in CanadaSales · (2) Diff for row 5 = **215**
```sas
data CanadaSales;
    set sashelp.prdsale;
    Diff=Actual-Predict;
    where Country="CANADA" and Quarter=1;
run;
```

### PQ 1.02 — answers: (1) **55** countries in EUR · (2) average population for AFR = **16,045,289**
```sas
/*This program analyzes population estimates
in the SASHELP.DEMOGRAPHICS table.*/

proc freq data=sashelp.demographics;
    table Region;
run;

proc means data=sashelp.demographics sum mean maxdec=0;
    var Pop;
    class Region;
run;
```

### PQ 1.03 — answer: "There are **25** SAS tables in the library." (page note: more if you created other tables earlier; the important thing is the code)
```sas
libname cr "&path";

proc contents data=cr._all_ nods;
run;
```

### PQ 1.04 — answers: (1) Employee_Term_Date row 23 = **31JAN16** · (2) engine = **V9**
```sas
proc import datafile="&path/payroll.csv" out=payroll dbms=csv replace;
    guessingrows=max;
run;

proc contents data=payroll;
run;
```

### PQ 1.05 — answers: (1) original column name changed = **Phone Type** · (2) Employee_ID type = **Numeric**
```sas
options validvarname=v7;
libname xl xlsx "&path/employee.xlsx";

proc contents data=xl._all_;
run;
```

### PQ 1.06 — answers: (1) first player in baseball_sort = **Harper, Terry** · (2) PROC PRINT rows = **40** · (3) Position with most players = **C** · (4) average Salary = **536**
```sas
proc sort data=sashelp.baseball out=baseball_Sort;
    by Team Name;
run;

proc print data=baseball_Sort;
    where Team in ("San Francisco", "Los Angeles", "Oakland");
    var Name Team Salary Cr:;
run;

proc freq data=baseball_Sort order=freq;
    tables Position;
run;

proc means data=baseball_Sort maxdec=0 sum mean;
    var Salary;
run;
```

### PQ 1.07 — answers: (1) duplicated EmpID = **120107** · (2) Country rule violations = **8** · (3) department with most employees = **Sales** · (4) rows with known TermDate before HireDate = **1**
```sas
proc freq data=cr.employee_raw order=freq nlevels ;
    tables EmpID Country Department;
run;

proc print data=cr.employee_raw;
    where TermDate ne . and HireDate>TermDate;
    format salary dollar10. TermDate HireDate BirthDate date9.;
run;
```

### PQ 1.08 — answers: (1) EmpID of obs 10 = **120110** · (2) most recent hire year among Logistics titles = **2016** · (3) average salary, hired ≥ 01JAN2010 with missing TermDate = **$40,774.46** · (4) third highest salary = **$243,606**
```sas
proc sort data=cr.employee_raw out=emp_sort noduprecs;
    by _all_;
run;

proc print data=emp_sort;
    where JobTitle like '%Logistics%';
    format salary dollar10. TermDate HireDate BirthDate date9.;
run;

proc means data=emp_sort n mean;
    where HireDate >= "01JAN2010"d and TermDate is missing;
    var salary;
run;

proc univariate data=emp_sort;
    var Salary;
run;
```

### PQ 1.09 — answers: (1) holidays with CountryCode CA = **4** · (2) second argument of SUBSTR = **4** · (3) SAS date value for Boxing Day = **21909**
```sas
data holiday2019;
    set sashelp.holiday;
    where end=. and rule=0;
    CountryCode=substr(category,4,2);
    Date=mdy(month, day, 2019);
    keep Desc CountryCode Date;
run;
```

### PQ 1.10 — answers: (1) total Sales employees = **122** · (2) middle-level sales reps = **66**
```sas
data sales;
    set cr.employee;
    length SalesLevel $ 6;
    where Department="Sales" and TermDate is missing;
    Country=upcase(Country);
    if substr(JobTitle, 12)="I" then SalesLevel="Entry";
    else if substr(JobTitle, 12) in("II" "III") then SalesLevel="Middle";
    else if substr(JobTitle, 12)="IV" then SalesLevel="Senior";
run;

proc freq data=sales;
    tables SalesLevel;
run;
```

### PQ 1.11 — answers: (1) employees in bonus = **308** · (2) years employed, row 1 = **34** · (3) employees with 20 vacation days = **188** · (4) bonus of last employee = **681**
```sas
data bonus;
    set cr.employee;
    where TermDate is missing;
    YearsEmp=yrdif(HireDate, "01JAN2019"d, "age");
    if YearsEmp >= 10 then do;
        Bonus=Salary*.03;
        Vacation=20;
    end;
    else do;
        Bonus=Salary*.02;
        Vacation=15;
    end;
run;

proc freq data=bonus;
    tables Vacation;
run;

proc sort data=bonus;
    by descending YearsEmp;
run;
```

### PQ 1.12 — answers: (1) label for nHome = **Home Runs in 1986** · (2) option for descriptive headings = **LABEL** · (3) Baltimore total home runs = **164** · (4) statement to replace OBS with player name = **ID**
Target output shown: title "Baseball Team Statistics", BY line "Team at the End of 1986=Atlanta" (then Baltimore…), Player's Name as ID column, labeled headings (Position(s) in 1986, Years in the Major Leagues, Times at Bat in 1986, Hits in 1986, Home Runs in 1986), team sum row (e.g., Atlanta 4171 / 1055 / 116).
```sas
proc sort data=sashelp.baseball out=baseball_sort;
    by Team Name;
run;

title "Baseball Team Statistics";
proc print data=baseball_sort label;
    by Team;
    id Name;
    var Position YrMajor nAtBat nHits nHome;
    sum nAtBat nHits nHome;
run;
```

### PQ 1.13 — answers: (1) city with most employees = **San Diego** · (2) % in Sales = **47.41%** · (3) unique JobTitle values = **132**
```sas
proc freq data=cr.employee order=freq nlevels;
    tables City Department JobTitle / nocum;
run;
```

### PQ 1.14 — answers: (1) retail orders in December = **963** · (2) % of all orders Retail = **77.29%**
(Shown sample output: "Table of Order_Date by Order_Source", columns Internet, Phone, Retail, Unknown, Total; cells with Frequency and Percent only.)
```sas
proc freq data=cr.profit;
    format Order_Date monname.;
    tables Order_Date*Order_Source / nocol norow ;
run;
```

### PQ 1.15 — answers: (1) total salary of all Sales employees = **6910144** · (2) mean salary Sales Rep. IV = **39568**
```sas
proc means data=cr.employee sum mean min max maxdec=0;
    where Department="Sales";
    var Salary;
    class JobTitle;
    ways 0 1;
run;
```

### PQ 1.16 — answers: (1) rows in salary_summary = **55** · (2) AvgSalary Administration/Sydney = **$37,848.44**
```sas
proc means data=cr.employee noprint;
    var Salary;
    class Department City;
    output out=salary_summary mean=AvgSalary sum=TotalSalary;
    ways 2;
run;
```
(code beyond `ways 2;` not visible – presumably `run;`)

### PQ 1.17 — answers: (1) titles included in the spreadsheets? **No** · (2) worksheets in heart.xlsx = **7**
```sas
ods graphics on;
ods noproctitle;

ods excel file="&outpath/heart.xlsx";
title "Distribution of Patient Status";
proc freq data=sashelp.heart order=freq;
    tables DeathCause Chol_Status BP_Status / nocum plots=freqplot;
run;

title "Summary of Measures for Patients";
proc means data=sashelp.heart mean;
    var AgeAtDeath Cholesterol Weight Smoking;
    class Sex;
run;
ods excel close;
```

### PQ 1.18 — answers: (1) first bookmark label = **The Freq Procedure** · (2) both reports on a single page? **yes**
```sas
ods pdf file="&outpath/truck.pdf" style=journal startpage=no;
ods noproctitle;
title "Truck Summary";
title2 "SASHELP.CARS Table";

proc freq data=sashelp.cars;
    where Type="Truck";
    tables Make / nocum;
run;

proc print data=sashelp.cars;
    where Type="Truck";
    id Make;
    var Model MSRP MPG_City MPG_Highway;
run;
ods pdf close;
```

### PQ 1.19 — answers: (1) file size = **Approximately 29 KB** · (2) fields enclosed in quotation marks = **Name and Salary**
```sas
proc export data=cr.employee_current outfile="&outpath/emp_current.csv" dbms=csv replace;
run;
```

## Gaps
- Demo code visible only in video – not in transcripts.
- PQ program/data files (p101q1.sas etc.) not captured; PQ answers and solution code captured from screenshots (see section above).
