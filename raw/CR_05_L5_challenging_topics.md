# CR – Lesson 5: Supplemental Material on Challenging Topics (Optional)

Source: Certification Review player (id=238), text mode. Captured 2026-10-28. In this lesson the "videos" have full written instructions; PQ pages have "Show Solution" (solutions → Visual Queue). Paraphrased; short quotes in quotation marks. All paths assume course files in `s:/workshop/ECRBM6`.

## Creating Libraries (demo 5:20)
- LIBNAME `crb` → `s:/workshop/ECRBM6/data`. Log NOTE: "Libref CRB was successfully assigned as follows." – shows what it connected to. Only **SAS7BDAT** files in that folder are accessible through the library.
- **Nonexistent folder** (typo `…/daat`, libref crb2): **no warning, no error** – only a NOTE "Library CRB2 does not exist." No error ≠ correct code.
- After fixing: NOTE "Libref CRB2 refers to the same physical library as CRB." Two librefs on one path is allowed but not recommended → clear crb2.
- **Existing but wrong folder** (crb3 → parent folder `s:/workshop/ECRBM6`, which has no SAS7BDAT files): library is created but **empty** – valid instructions, just not the intended ones; check the location.
- Excel: LIBNAME `emp` XLSX engine → `employee.xlsx` in the data folder; each data set in the library = one worksheet (tab).
- Typo in the workbook name (emp2 → nonexistent `employees.xlsx`): log says the library was assigned **successfully**, but emp2 is **empty**. Check the file exists and the path is typed correctly. After fixing, two libraries point to one workbook (allowed, not recommended) → clear emp2.

### Programming Question 5.01
Define library CRB (read/write SAS tables in the course data folder); create `crb.m7_sales_type1` with all rows of crb.m7_sales where Order_Type = 1. Qs: Why do these not connect to s:/workshop/data – `LIBNAME example "S:/WORKSHOP/";` and `LIBNAME example "s:/workhsop/data";`? Would either produce an error message in the log? Define library Country for country_lookup.xlsx in the data folder. Mean of Lat in country.Countries (3 decimals)? Most frequent Region value in country.Population?

## Comparing WHERE and IF Statements (demo 2:35)
- Goal: filter crb.employee_donations to Paid_By = "Payroll Deduction" and sum of Qtr1–Qtr4 > 50.
- DATA step copying to work.employee_donations with subsetting IF Paid_By = Payroll Deduction → **65 rows**, first EmpID **120267**. Same expression in a WHERE statement → same 65 rows / 120267. When the column exists in the input table, either works.
- New column TotalDonations = sum of Qtr1–Qtr4, then `WHERE TotalDonations > 50` → **ERROR: variable TotalDonations is not in file CRB.EMPLOYEE_DONATIONS** – a WHERE can't use a column that isn't in the input table.
- Changed to IF (placed **after** the assignment) → works. WHERE and IF both filter pre-existing columns; **only IF** filters new columns, because WHERE acts before any other DATA step processing.

### Programming Question 5.02
From crb.qtr_sales create work `qtr_metQuota` with all columns plus Total = sum of Qtr1–Qtr4; keep only rows with Qtr4 > 100 and Total > 500. Q: rows in work.qtr_metQuota?

## Using DROP and KEEP Statements (demo 4:48)
- DATA work.emp_US work.emp_AU from crb.employee; WHERE TermDate is not missing (applies to both outputs) [as written; VERIFY intent]; IF/THEN + OUTPUT send Country AU / US rows to their tables. WHERE filters rows as they come in; conditional OUTPUT filters while processing.
- **DROP=** data set option on an output table (`emp_AU(drop=State)`) applies only to that table. Data set options go in parentheses after the data set; the `=` right after DROP is required.
- **DROP statement** (Salary) → removed from **all** output tables.
- Since Salary isn't used, drop it on input: **DROP= on the input data set** → not read into the PDV, not available for processing; input data set options act before any other processing. Remove the now-redundant DROP statement.
- Dropping Country and TermDate on input fails – they're used (IF condition, WHERE) → **error and warnings** in the log. Use a DROP statement or DROP= on the output tables instead (takes effect after all processing). Result: emp_us **80 rows, 10 columns**; emp_au **34 rows, 9 columns**.
- KEEP works the same way: KEEP statement prevents output of non-kept columns; KEEP= on input prevents their use; timing same as DROP counterparts.

### Programming Question 5.03
(1) From crb.m7_sales: `crb.m7_sales_type1` = rows with Order_Type = 1, all columns except Order_Type and Delivery_Date; `crb.m7_sales_other` = Order_Type ≠ 1, all columns except Delivery_Date. Qs: rows in m7_sales_other? columns in m7_sales_type1? Customer_ID in row 3 of m7_sales_other? (2) From crb.country_info: work `country_info_SAM` = Continent 2, all columns; `country_info_NAM` = Continent 1, all columns except Continent. Qs: rows in country_info_SAM? columns in country_info_NAM? Country in row 33 of country_info_NAM?

## Using the LENGTH Statement (demo 4:14)
- work.orders from crb.orders; new character column Order_Source = "Known" when Order_Type is 1, 2 or 3, else "Unknown"; no LENGTH statement (best practice is to declare character lengths first).
- Log: no errors or warnings, notes fine – but Order_Source length is **5** ("Known" is first), so "Unknown" (7) is stored as **"Unkno"**. A column's length is set at its **first appearance** in the DATA step; later appearances are ignored.
- LENGTH Order_Source $ 7 placed right after SET (before the conditional statements) → length 7, no truncation.
- LENGTH placed **after** the conditional statements → **WARNING**: "Length of character variable Order_Source has already been set. Use the LENGTH statement as the very first statement in the DATA STEP to declare the length of a character variable." The real rule: LENGTH must come before any other appearance of the column. The late LENGTH has no effect – length stays 5, values truncated.

### Programming Question 5.04
(1) work.country_info from crb.country_info; new character column [stem says "Continent_Type" but the steps set "Continent_Name"]: Continent 5 → Asia; 3 → Europe; others → Other. Q: length of Continent_Name? (2) work.emp_don from crb.employee_donations; character column Type = "Recurring" if all of Qtr1–4 are nonmissing, "Occasional" if any are missing. Qs: length of Type? mean of Qtr2 for Type = Occasional?

## Converting Column Type (demo 3:09)
- work.qtr_sales from crb.qtr_sales with the `10.` format applied to BirthDate → shows it is numeric (days since January 1, 1960).
- Numeric → character: `BirthDate_char = put(BirthDate, mmddyy10.);` – **PUT**(value, **format**).
- Character → numeric: `BirthDate_again = input(BirthDate_char, anydtdte10.);` – **INPUT**(value, **informat**). Formats turn stored values into readable text; informats turn text into stored values – different concepts despite similar syntax. Values follow the MMDDYY10 pattern, so MMDDYY10. or the more generic **ANYDTDTE10.** informat works. BirthDate_again equals BirthDate.

### Programming Question 5.05
(1) From crb.qtr_sales make work.qtr_sales_id: character ID from Customer_ID in **Z5** format; numeric CustID = numeric interpretation of ID. Qs: ID in row 6? standard deviation of CustID (needs a step beyond the DATA step)? (2) From crb.tourism make crb.tourism_2008, reading only the _2008 column into the PDV; numeric `_2008_num` from _2008; optional conditional processing to avoid log warnings. Q: median of _2008_num? (Page notes a known issue: CRB.TOURISM does not exist on the lab image as of Feb 2024.)

## Creating an Accumulating Column (demo 2:35)
- Accumulating column = running total of another numeric column (current + all previous values); missing values ignored; rows in a logical order.
- PROC SORT sashelp.stocks BY Date OUT=work.stocks, subset Stock = "IBM" and year(Date) = 1999.
- DATA step overwriting work.stocks: `AccumulatedVolume = sum(AccumulatedVolume, Volume);` – alone it does **not** accumulate, because assignment-created columns reset to missing each iteration.
- Add `RETAIN AccumulatedVolume 0;` right after SET; FORMAT COMMA32. → accumulates as intended.

### Programming Question 5.06
From crb.employee create work `dept_salary`, Department = Administration only; accumulating column **TotalDeptSalary** so row 1 = lowest-paid salary, row 2 = sum of the two lowest, etc. (i.e., sorted ascending by Salary); output only Salary and TotalDeptSalary; DOLLAR12. on TotalDeptSalary. Qs: Salary in row 5 (rounded)? TotalDeptSalary in row 15 (rounded)?

## Accumulating Columns Within Groups (demo 6:15)
- Grouped accumulation: the running total resets to zero at each new group value.
- PROC SORT sashelp.stocks OUT=work.stocks_sort, subset year(Date) = 1999, BY Stock Date.
- DATA stocks_total: `RETAIN YTDVolume 0;` `YTDVolume = sum(YTDVolume, Volume);` DROP Open Close High Low AdjClose; FORMAT YTDVolume COMMA20. → accumulates over the whole table (not yet by group).
- **BY Stock** makes **first.Stock** and **last.Stock** available – indicator columns, **not written to output** by default. Demo copies them to permanent columns FirstStock/LastStock to visualize: first.Stock = 1 on rows 1, 13, 25; last.Stock = 1 on rows 12, 24, 36 (three groups of 12).
- `if first.Stock=1 then YTDVolume=0;` before the accumulation → separate running totals per stock. Remove the helper copies; first./last. still exist because the BY statement creates them.

### Programming Question 5.07
(1) From crb.employee create work.dept_salary with Department, TotalDeptSalary (accumulation of Salary within Department, smallest to largest), HighSalaryJob (JobTitle of the highest-salary row); one row per Department; DOLLAR12. Qs: HighSalaryJob for Group Financials? TotalDeptSalary for Sales? (2) From crb.orders (multiple rows per Delivery_Date) make work.orders_accumulated: columns Delivery_Date, Daily_Profit, Accumulated_Profit; one row per Delivery_Date; Daily_Profit = accumulated profit for that day, with row profit given as "Retail_Price – Cost_Price * Quantity" [as written]; Accumulated_Profit = running total of Daily_Profit. Qs: Daily_Profit on row 50 (2 decimals)? Accumulated_Profit on row 60 (2 decimals)?

## Using Iterative DO Loops (demo 4:37)
- Forecast 5 years from crb.shoes_summary (one row per region with ProfitPerStore), 3% annual growth compounded monthly: `ProfitPerStore = ProfitPerStore * (1 + .03/12);` [the "+" was missing in the extracted text].
- Copy-pasting the statement 12 times is not recommended (a rate change means 12 edits) → `do Month=1 to 12; … end;`. Everything between DO and END runs on each iteration; the index increases by 1 at END. DROP TotalProfit TotalStores.
- After the loop **Month = 13** (starts at 1, incremented 12 times) → add Month to DROP.
- Outer loop `do Year=1 to 5; … end;` around the Month loop → one row per region with **Year = 6** (only implicit output at the end). Fix: **OUTPUT statement between the END of the Month loop and the END of the Year loop** → 5 rows per region, Year 1–5. The location of OUTPUT is essential.

### Programming Question 5.08 (read from screenshot)
Create `work.future_expenses_annual`: initial Wages = *12,874,000*, initial Medical = *649,000*; Wages increase 6% per year, Medical 9.5% per year, **compounded quarterly** – hint formulas per quarter: `Wages = Wages * (1 + .06/4);` and `Medical = Medical * (1 + .095/4);`; forecast Wages and Medical for the next 10 years; output one row per year. Qs: (1) Medical in row 9? (2) Wages in row 8?

## Using Conditional DO Loops (demo 3:24)
- $1,000,000 reserve; +$25,000 each year; then 3% interest; then −$100,000 distribution. Model years with Reserve > 0 at the start of the year. Output columns: Year, Reserve.
- DATA work.model: Year=1; Reserve=1e6; `do while(Reserve > 0);` add 25000, ×1.03, −1e5, OUTPUT, Year+1; `end;` FORMAT Reserve COMMA20. – **DO WHILE checks the condition at the top** of the loop. Reserve > 0 at the start of **18** years; Reserve shows the end-of-year value.
- **DO UNTIL**: loops until the condition becomes true; condition reversed to `Reserve <= 0`; **checked at the bottom** (before END). Same results here – identical whenever the DO WHILE loop executes at least once (Reserve starts > 0).

### Programming Question 5.09 (read from screenshot)
Create `work.rewards` with two columns, Year and Reserve; Year starts at *1*; Reserve starts at *1e6*; each month 5000 is added to Reserve; 4% interest compounded monthly after the 5000 is added (hint: `Reserve = Reserve + (Reserve * .04 / 12);`); one row output per year; output continues until Reserve is greater than *1.5e6*; COMMA20 format on Reserve. Qs: (1) How many rows are written to output? (2) Value of Reserve in the last row?

## Combining Iterative and Conditional DO Loops (demo 3:18)
- $1,000,000 earning 4% per year; grows until it reaches $1,500,000 or 10 years pass.
- work.rewards_u: Reserve=1e6; `do Year=1 to 10 until(Reserve >= 1500000);` Reserve ×1.04; OUTPUT; `end;` – UNTIL condition checked at the bottom; iterator increases at END. FORMAT COMMA20. Loop has two stop conditions; here it stopped after 10 iterations (condition would stop it earlier if met).
- work.rewards_w: same with `while(Reserve < 1.5e6)` – condition checked right after DO (top). Both tables are identical for this cutoff; some other cutoffs would make them differ (bonus challenge).

### Programming Question 5.10 (read from screenshot)
Create `work.rewards` to hold a forecast for Reserve: initial Reserve *1,000,000*; 4% interest compounded monthly (hint: `Reserve = Reserve + Reserve * 0.04/12;` calculates one month of interest); write one row per forecast year; stop when either Reserve exceeds *2,000,000* or the forecast extends 30 years into the future. Qs: (1) Reserve on the last row, rounded to the nearest whole number? (2) How many rows are written to output?

## Finding Non-matches in a DATA Step Merge (demo 4:17)
- Merge crb.employee_addresses and crb.employee by employee ID, keeping only rows with information from employee_addresses.
- employee_addresses: ID column **Employee_ID**, **not sorted**; employee: **EmpId**, sorted. BY columns must have the **same name** in both tables.
- `PROC SORT DATA=crb.employee_addresses OUT=work.address_sort(rename=(Employee_ID=EmpId)); BY Employee_ID;` – RENAME= on the output table.
- `DATA work.emp_full; MERGE crb.employee work.address_sort(in=A); BY EmpId;` – by default all merged rows are written. **IN=A**: temporary indicator (1 if the row has data from address_sort, else 0) in the PDV. Demo copies A to A_indicator to see it, then subsetting `if A=1;` → every row has Street Number and Street Name; helper column removed.

### Programming Question 5.11
(1) Merge crb.employee and crb.employee_donations by EmpId; TotalDonation = sum of Qtr1–Qtr4; only rows with data from both → work.donation; keep EmpId, Name, Department, TotalDonation. Qs: rows in work.donation? TotalDonation in row 42? (2) Merge crb.profit and crb.products by Product_Id; rows from both → work.profit_detail; rows only from products → work.product_noSales. Qs: rows in work.profit_detail? Product_Id in row 13 of work.products_noSales?

## Restructuring Data with PROC TRANSPOSE (demo 5:32)
- Wide crb.employee_donations (EmpID, Qtr1–Qtr4) → narrow: one row per EmpId × quarter, one value per row (missing counts as a value). Equivalent to transposing each EmpId's row and stacking → **BY EmpId** (data must be sorted by EmpId; it already is).
- `PROC TRANSPOSE DATA=crb.employee_donations OUT=work.donations_narrow(rename=(_name_=Quarter col1=Amount)); BY EmpId;` – both sets of parentheses and all three equal signs are required [verified on screen: "We need to change _name_ to Quarter and Col1 to Amount. Add a RENAME= data set option to the output data set."]. No VAR statement needed: **all numeric columns not in BY are transposed by default**; use VAR to choose a subset.
- Narrow → wide: `PROC TRANSPOSE DATA=work.donations_narrow OUT=work.donations_wide; BY EmpId;` (sorted by EmpId) → columns COL1, COL2…; **ID Quarter** names the new columns from Quarter values; _NAME_ (source column name, here always Amount – redundant) removed with **DROP=** on the output table.

### Programming Question 5.12
(1) From sashelp.shoes create work.shoes_sales from Sales, excluding Subsidiary = Copenhagen, restructured to Region, Subsidiary, _Name_, then one column per product (Boot, Men's Casual, Men's Dress, Sandal, …) e.g., Africa/Addis Ababa/Sales/$29,761/$67,242/$76,793/$62,819… Qs: Slipper in row 13? rows in work.shoes_sales? median of Boot? (2) From crb.employee_training create work.training_narrow from Compliance_Training and Corporate_Security: Name, Course, Date (e.g., Abbott, Ray / Compliance_Training / 07APR2018; Abbott, Ray / Corporate_Security / 19JUL2018; Aisbitt, Sandy / Compliance_Training / .). Qs: Date in row 20 (DATE9.)? rows in work.shoes_sales [as written]? mode of Date as a SAS date value (days from 01Jan1960, e.g., 300)?

## Programming Question solutions ("Show Solution"; read from screenshots)

### PQ 5.01 solution
```sas
/* Your path may be different depending on your environment */

libname crb "s:/workshop/data";

data crb.m7_sales_type1;
   set crb.m7_sales;
   where order_type = 1;
run;
```
- 2a. `LIBNAME example "S:/WORKSHOP/";` → **Incorrect file path**
- 2b. `LIBNAME example "s:/workhsop/data";` → **Typo in workshop, resulting in an incorrect file path**
- 2c. Would either produce an error message in the log? → **No**
```sas
libname country xlsx "s:/workshop/ECRBM6/data/country_lookup.xlsx";
proc means data=country.countries;
        var Lat;
run;

proc freq data=country.population;
        table Region;
run;
libname country clear;
```
- 3a. Mean of Lat in country.Countries = **16.007** · 3b. Most frequent Region in country.Population = **EUR**

### PQ 5.02 solution — rows in work.qtr_metQuota = **39**
```sas
/* Option 1 */
data work.qtr_metQuota;
        set cr.qtr_sales;
        Total = sum(Qtr1, Qtr2, Qtr3, Qtr4);
        if Qtr4 > 100 and Total > 500;
run;

/* Option 2 */
data work.qtr_metQuota2;
        set cr.qtr_sales;
        where Qtr4 > 100;
        Total = sum(Qtr1, Qtr2, Qtr3, Qtr4);
        if Total > 500;
run;
```

### PQ 5.03 solution
```sas
data crb.m7_sales_type1(drop=order_type)
     crb.m7_sales_other;
        set crb.m7_sales;
        if Order_Type = 1 then output crb.m7_sales_type1;
        else output crb.m7_sales_other;
        drop Delivery_Date;
run;
```
- (1) rows in crb.m7_sales_other = **five** · (2) columns in crb.m7_sales_type1 = **three** · (3) Customer_ID row 3 of m7_sales_other = **27**
```sas
data country_info_sam country_info_nam(drop=Continent);
        set crb.country_info;
        if Continent = 2 then output country_info_sam;
        else if Continent = 1 then output country_info_nam;
run;
```
- (1) rows in country_info_SAM = **16** · (2) columns in country_info_NAM = **one** · (3) Country row 33 of country_info_NAM = **El Salvador**

### PQ 5.04 solution
```sas
data country_info;
        set cr.country_info;
        length Continent_Name $ 6;
        if continent = 5 then continent_name = "Asia";
        else if continent = 3 then continent_name = "Europe";
        else continent_name = "Other";
run;
```
- Length of Continent_Name: **6, or any number larger than 6 that you specified in the LENGTH statement**
```sas
data emp_don;
        set cr.employee_donations;
        length Type $ 10;
        if Qtr1 ^= . and Qtr2 ^= . and Qtr3 ^= . and Qtr4 ^= .
            then Type = "Recurring";
        else Type = "Occasional";
run;
proc means data=emp_don;
        where type="Occasional";
        var Qtr2;
run;
```
- (1) Length of Type: **10, or any value larger than 10 that you specified in the LENGTH statement** · (2) mean of Qtr2 for Occasional = **14**

### PQ 5.05 solution
```sas
data qtr_sales_id;
    set crb.qtr_sales;
    format BirthDate 10.;
    ID = put(Customer_ID, z5.);
    CustID = input(ID, z5.);
run;

proc means data=qtr_sales_id std;
        var CustID;
run;
```
- (1) ID in row 6 = **00012** · (2) standard deviation of CustID = **24538.09**
```sas
data crb.tourism_2008;
        set crb.tourism(keep=_2008);
        _2008_num = input(_2008, 20.);
run;

proc means data=crb.tourism_2008 median;
        var _2008_num;
run;

/* Solution for optional part */
data crb.tourism_2008;
        set crb.tourism(keep=_2008);
        if _2008 = ".." then _2008_num = .;
        else _2008_num = input(_2008, 20.);
run;

proc means data=crb.tourism_2008 median;
        var _2008_num;
run;
```
- Median of _2008_num = **525** (page note: "KNOWN ISSUE: CRB.TOURISM DOES NOT EXIST ON IBT IMAGE AS OF Feb2024")

### PQ 5.06 solution — (1) Salary row 5 = **32,681** · (2) TotalDeptSalary row 15 = **493,181**
```sas
proc sort data=crb.employee out=work.emp_sort;
        by Salary;
        where department = "Administration";
run;

data dept_salary;
    set emp_sort;
    TotalDeptSalary+Salary;
    keep Salary TotalDeptSalary;
    format TotalDeptSalary dollar20.2;
run;
```

### PQ 5.07 solution
```sas
proc sort data=crb.employee out=work.emp_sort;
        by department Salary;
run;

data dept_salary;
    set emp_sort;
    by Department;
    if first.Department then do;
        TotalDeptSalary=0;
    end;
    TotalDeptSalary+Salary;
    if last.department then do;
        HighSalaryJob=JobTitle;
        output;
    end;
    keep Department TotalDeptSalary HighSalaryJob;
    format TotalDeptSalary dollar12.;
run;

/* Note: PROC MEANS can get max Salary because it is a summary statistic. It cannot get information from specific rows of the data

proc means data=cr.employee;
        class department;
        var Salary;
run;
*/
```
- (1) HighSalaryJob for Group Financials = **Auditor III** · (2) TotalDeptSalary for Sales = **$6,910,144**
```sas
proc sort data=crb.orders out=work.orders;
        by delivery_date;
run;

data orders_accumulated;
        set orders;
        by delivery_date;
        Profit = retail_price - cost_price * quantity;

        retain Daily_Profit Accumulated_Profit 0;

        if first.delivery_date = 1 then daily_profit=0;

        daily_profit = sum(daily_profit, profit);
        accumulated_profit = sum(accumulated_profit, profit);

        if last.delivery_date = 1 then output;

        keep delivery_date daily_profit accumulated_profit;
        format daily_profit accumulated_profit comma20.2;
run;
```
- (1) Daily_Profit row 50 = **261.10** · (2) Accumulated_Profit row 60 = **9226.45**

### PQ 5.08 solution — (1) Medical row 9 = **1,510,865** · (2) Wages row 8 = **20,731,315**
```sas
data future_expenses_annual;
    Wages = 12874000;
    Medical = 649000;
    do Year = 1 to 10;
        do Qtr = 1 to 4;
                Wages = Wages * (1 + .06/4);
                Medical = Medical * (1 + .095/4);
                  output;
        end;

    end;
    drop Qtr;
    format Wages Medical comma20.;
run;
```
(As shown, the OUTPUT statement sits inside the inner Qtr loop, although the task says one row per year – recorded exactly as displayed.)

### PQ 5.09 solution — (1) rows written = **5** · (2) Reserve in last row = **1,553,596**
```sas
data rewards;
    Year = 1;
    Reserve = 1e6;
    do until (Reserve > 1.5e6);
       do month = 1 to 12;
          Reserve = Reserve + 5000;
          Reserve = Reserve + (Reserve * .04 / 12);
       end;
       output;
       Year = Year + 1;
    end;
    format Reserve comma20.;
    drop Month;
run;
```

### PQ 5.10 solution — (1) Reserve on last row = **2051975** · (2) rows written = **18**
```sas
/* Using DO UNTIL technique */
data rewards_u;
    Reserve = 1e6;
    do Year = 1 to 30 until (Reserve > 2e6);
       do month = 1 to 12;
          Reserve = Reserve + (Reserve * .04/12);
       end;
       output;
       /* condition check */
    end; /* Year = Year + 1 */
    format Reserve comma20.;
    drop Month;
run;

/* Using DO WHILE technique */
data rewards_w;
    Reserve = 1e6;
    do Year = 1 to 30 while (Reserve <= 2e6);
       /* condition check */
       do month = 1 to 12;
          Reserve = Reserve + (Reserve * .04/12);
       end;
       output;
    end; /* Year = Year + 1 */
    format Reserve comma20.;
    drop Month;
run;
```

### PQ 5.11 solution
```sas
/* Note: If the input tables are not already sorted by EmpID, need to be sorted by EmpId before this DATA step can execute. */
data donation(keep=EmpID Name Department TotalDonation);
    merge cr.employee(in=in_emp)
          cr.employee_donations(in=in_don);
    by EmpID;
    if in_don=1 and in_emp=1;
    TotalDonation=sum(of Qtr1-Qtr4);
run;
```
- (1) rows in work.donation = **124** · (2) TotalDonation row 42 = **60**
```sas
proc sort data=crb.profit out=work.profit;
        by Product_Id;
run;
proc sort data=crb.products out=work.products;
        by Product_Id;
run;

data work.profit_detail work.products_noSales;
        merge work.profit(in=fromF)
         work.products (in=fromD);
        by Product_ID;

        if fromF = 1 and fromD = 1 then output work.profit_detail;
        else if fromF = 0 and fromD = 1
then output work.products_noSales;
run;
```
- (1) rows in work.profit_detail = **10781** · (2) Product_Id row 13 of work.products_noSales = **210200300073**

### PQ 5.12 solution
```sas
proc transpose data=sashelp.shoes
    out=shoes_sales(drop=_label_);
    var Sales;
    by Region Subsidiary;
    id Product;
    where Subsidiary ^= 'Copenhagen';
run;
proc means data=work.shoes_sales median;
        var Boot;
run;
```
- (1) Slipper in row 13 = **$135,305** · (2) rows in work.shoes_sales = **52** · (3) median of Boot = **33291**
```sas
proc sort data=crb.employee_training out=training_sort;
        by Name;
run;

proc transpose data=training_sort
            out=training_narrow(rename=(col1=Date))
    name=Course;
    by Name;
    var Compliance_Training Corporate_Security;
run;
```
- (1) Date in row 20 = **02JUL2018** · (2) "How many rows are in work.shoes_sales?" [as written; refers to training_narrow] = **608** · (3) mode of Date as SAS date value = **21276**

## Gaps
- PQ solutions captured from screenshots (section above). PQ 5.08–5.10 question text recovered from screenshots.
