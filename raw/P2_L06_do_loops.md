# P2 – Lesson 6: Processing Repetitive Code

Source: SAS Programming 2 player (course id=235), text mode + screenshots. Captured 2026-10-28. Paraphrased; short quotes in quotation marks. Code copied from screenshots.

## 6.0 Lesson Overview
- Save time with iterative processing: first the iterative DO loop, then conditional DO loops.

## 6.1 Using Iterative DO Loops

### Processing Repetitive Code (0:50)
- Earlier forecast program (sashelp.shoes, 5% growth for 3 years) had three Year assignments, three ProjectedSales assignments and three OUTPUT statements – repetitive.

### Iterative DO Loops (2:14) – from screenshots
```
DO index-column = start TO stop <BY increment>;
    . . . repetitive code . . .
END;
```
- Starts with DO, ends with END; statements between are processed repetitively during execution.
- **Index-column** controls the loop; its value is **incremented at the end of each pass**; it is **included in the output table unless you drop it** (Year kept here on purpose).
- **Start** = number/numeric expression giving the initial value; **stop** = value the index must **exceed** to stop the loop; keyword TO between them; loop continues while the index is within the start–stop range.
- `do year = 1 to 3;` = `do year = 1 to 3 by 1;` – optional **BY increment**, default **1**; increment added each pass until the index exceeds stop.
```sas
data forecast;
    set sashelp.shoes(rename=(Sales=ProjectedSales));
    do Year = 1 to 3;
        ProjectedSales=ProjectedSales*1.05;
        output;
    end;
    keep Region Product Subsidiary Year ProjectedSales;
    format ProjectedSales dollar10.;
run;
```
- For each DATA step iteration (each row of sashelp.shoes) the DO loop executes three times, updating Year and ProjectedSales and outputting a row.

### Demo: Executing an Iterative DO Loop (2:52) – p206d01a.sas (EG debugger) / p206d01b.sas (SAS Studio)
- Output: three rows (Year 1, 2, 3) per Region/Product/Subsidiary combination.
- Debugger: SET loads row 1, _N_ = 1; Year added to the PDV, initialized to missing; the DO statement sets Year to the start value 1; inside the loop ProjectedSales +5%, row output; at **END, Year increments to 2** and processing returns to the top of the loop; SAS checks whether Year is within the range; 2 → loop again; END → 3 → loop again → three rows written while still in the **first DATA step iteration**.
- After the third pass Year is incremented to **4**, outside the range → exit the loop. "Although the value of Year is 4, the loop executed three times." Explicit OUTPUT inside the loop → three rows per row read.
- SAS Studio alternative with PUTLOG:
```sas
data forecast;
    putlog 'Top of DATA Step ' Year= _N_=;
    set sashelp.shoes(obs=2 rename=(Sales=ProjectedSales));
    do Year = 1 to 3;
        ProjectedSales=ProjectedSales*1.05;
        output;
        putlog 'Value of Year written to table: ' Year=;
    end;
    putlog 'Outside of DO Loop: ' Year=;
    keep Region Product Subsidiary Year ProjectedSales;
    format ProjectedSales dollar10.;
run;
```
- Three rows (Year 1, 2, 3) for each of the first two input rows; review the PUTLOG text in the log.

### Activity (p206a01.sas) – with answers
```sas
data YearlySavings;
    Amount=200;
    do Month=1 to 12;
        Savings+Amount;
        output;
    end;
    format Savings 12.2;
run;
```
- No input data → only one DATA step iteration, but the loop with OUTPUT creates 12 rows (at month 12 savings = 2,400).
1. Add after the Savings sum statement: `Savings+(Savings*0.02/12);` (2% interest compounded monthly).
2. Savings at month 12 = **2426.16**.
3–4. Delete OUTPUT → rows created: **one row**.
5. Value of Month: **13**. 6. Value of Savings: **2426.16**.

### Output Inside and Outside the DO Loop (2:10) – from screenshots
- With OUTPUT between DO and END → a row for each loop iteration (12 rows: Month 1 Savings 200.33, 2 401.00, … 12 2426.16 [Amount 200]). The index is incremented at the bottom of the loop after each row is written; after 12 rows Month becomes 13, exceeds stop, loop ends.
- Without explicit OUTPUT → implicit output at the end of the DATA step, after the 12 iterations → one row: Amount 200, **Month 13**, Savings 2426.16 (the Savings statements don't run again when Month is 13).
- Reading input: `data YearSavings; set pg2.savings; do Month=1 to 12; … end; run;` – pg2.savings: James 250, Linda 300, Mary 275, Robert 350 → 4 DATA step iterations, 12 loop iterations each, implicit output → 4 rows (James 3,032.70; Linda 3,639.24; Mary 3,335.97; Robert 4,245.78 – value at the end of 12 months).
- Nested: `data FiveYearSavings; set pg2.savings; do Year=1 to 5; do Month=1 to 12; … end; end; run;` → outer loop 5 times, inner loop 12 times per year = 60 times; results James 15,788.11; Linda 18,945.73; Mary 17,366.92; Robert 22,103.35.

### Demo: Using Iterative DO Loops (5:38) – p206d02.sas, from screenshots
- Syntax: `DATA output-table; SET input-table; ... DO index-column = start TO stop <BY increment>; ... <OUTPUT;> END; ... <OUTPUT;> RUN;`
```sas
data YearSavings;
    set pg2.savings;
    *add an assignment statement;
    do Month=1 to 12;
        Savings+Amount;
        Savings+(Savings*0.02/12);
    end;
    format Savings comma12.2;
run;
```
- No explicit OUTPUT → implicit output at the end of each DATA step iteration. Output: 4 rows, Month 13; Savings James 3,032.70, Linda **6,733.15**, Mary **10,205.03**, Robert **14,656.79** – increasing because **Savings is automatically retained (sum statement)**, so each new person starts with the previous person's savings.
- Fix: reset before the loop: `Savings=0;` → James 3,032.70; Linda 3,639.24; Mary 3,335.97; Robert 4,245.78 (Month 13).
- Five years, nested loops:
```sas
data YearSavings;
    set pg2.savings;
    Savings=0;
    do Year=1 to 5;
        do Month=1 to 12;
            Savings+Amount;
            Savings+(Savings*0.02/12);
        end;
    end;
    format Savings comma12.2;
run;
```
- One row per person: Savings after five years; **Year = 6, Month = 13** (one increment beyond each stop value).
- OUTPUT at the bottom of the **outer** loop (after the inner END) → **5 rows per person, 20 rows**; Year only goes up to 5 in the output (Year incremented to 6 after the final row was output); Month still 13.
- OUTPUT at the bottom of the **inner** loop → **60 rows per person, 240 rows**; Month values 1–12 (output before Month incremented to 13). Flexibility: place the explicit OUTPUT inside or outside a DO loop.

### Practice (06_1_p) – Level 1: Using Nested Iterative DO Loops (DATA Step with No SET Statement); Level 2: Using an Iterative DO Loop (DATA Step with a SET Statement); Challenge: Using an Iterative DO Loop with a List of Values [pop-ups not opened – Gap]

## 6.2 Using Conditional DO Loops

### Conditional DO Loops (1:13) – from screenshots
```sas
data YearSavings;
    set pg2.savings;
    Savings=0;
    do Month=1 to 12;
        Savings+Amount;
        Savings+(Savings*0.02/12);
    end;
    drop Month;
    format Savings comma12.2;
run;
```
- Iterative loops run a specified number of times; when you don't know how many iterations are needed (e.g., stop when each person has saved more than 3000), use a **conditional DO loop**.
```
DO UNTIL (expression);
    . . . repetitive code . . .
END;

DO WHILE (expression);
    . . . repetitive code . . .
END;
```
```sas
do until (Savings>3000);
    Month+1;
    Savings+Amount;
    Savings+(Savings*0.02/12);
end;

do while (Savings<=3000);
    Month+1;
    Savings+Amount;
    Savings+(Savings*0.02/12);
end;
```
- **DO UNTIL** executes **until** a condition is true; **DO WHILE** executes **while** a condition is true. For both, the expression **must be enclosed in parentheses**. The WHILE version uses the opposite expression.

### Activity (p206a02.sas) – with answers
- Savings3K table: months until James exceeds 3000 = **12**; James's savings at that month = **3,032.70**.
- Equivalent DO WHILE: `do while (Savings<=3000);` – results for James identical? **Yes**.

### Checking the Condition (1:16) – from screenshots
- Many times DO UNTIL and DO WHILE give the same result, but the condition is checked at different times: **DO UNTIL – always checked at the bottom** of the loop (executes at least once); **DO WHILE – always checked at the top** (might not execute).
- pg2.savings2 (Name, Amount, Savings already earned): James 250 1250; **Linda 300 3600**; Mary 275 2200; Robert 350 1750.
- `do until (Savings>3000);` results: James 3026.36 Month 7; **Linda 3906.50 Month 1**; Mary 3038.77 Month 3; Robert 3167.54 Month 4.
- `do while (Savings<=3000);` results: James 3026.36 7; **Linda 3600.00, Month 1 [as displayed]**; Mary 3038.77 3; Robert 3167.54 4.
- Linda already exceeds 3000: DO UNTIL executes once (condition checked at the bottom); DO WHILE does not execute at all. "The statements in a DO UNTIL loop always execute at least one time, whereas the statements in a DO WHILE loop do not execute even once if the condition is false."

### Demo: Using Conditional DO Loops (4:38) – p206d03.sas, from screenshots
- Syntax: `DATA output-table; SET input-table; ... DO UNTIL | WHILE (expression); ... <OUTPUT;> END; RUN;`
```sas
data MonthSavings;
    set pg2.savings2;
    do until (Savings=3000);
        Savings+Amount;
        Savings+(Savings*0.02/12);
    end;
    format Savings comma12.2;
run;
```
- Savings is never exactly 3000 → **infinite loop**; stop it (EG: Stop toolbar button; SAS Studio: Cancel in the Running pop-up). Make sure the UNTIL condition will eventually be true → use `>` instead of `=`.
```sas
data MonthSavings;
    set pg2.savings2;
    Month=0;
    do until (Savings>3000);
        Month+1;
        Savings+Amount;
        Savings+(Savings*0.02/12);
    end;
    format Savings comma12.2;
run;
```
- Sum statement Month+1 counts iterations; Month is automatically retained (sum statement), so reset `Month=0;` before the loop for each new person (4 DATA step iterations).
- James, Mary, Robert exceed 3000 and Month shows how many months it took; Linda started at $3,600 but DO UNTIL ran once (+$300 and interest).
```sas
data MonthSavings;
    set pg2.savings2;
    Month=0;
    do while (Savings<3000);
        Month+1;
        Savings+Amount;
        Savings+(Savings*0.02/12);
    end;
    format Savings comma12.2;
run;
```
- DO WHILE with reversed logic → never executes for Linda; her Savings is still **3600**.

### Combining Iterative and Conditional DO Loops (1:18) – from screenshot
```
DO index-column = start TO stop <BY increment> UNTIL | WHILE (expression);
    . . . repetitive code . . .
END;
```
- Iterative syntax comes **before** the conditional syntax. The loop stops when the stop value is exceeded or the condition is met, **whichever is first** (e.g., reach 5,000 but don't go beyond 12 months).
```sas
do Month=1 to 12 until (Savings>5000);
    Savings+Amount;
    Savings+(Savings*0.02/12);
end;
```
- DO UNTIL: condition checked **before the index-column is incremented at the bottom** of the loop. If Savings > 5000 → stops and Month is **not incremented**; otherwise Month is incremented and checked against the stop value.
```sas
do Month=1 to 12 while (Savings<=5000);
    Savings+Amount;
    Savings+(Savings*0.02/12);
end;
```
- DO WHILE: condition checked at the **top**, index incremented at the bottom; if Savings ≤ 5000 the loop executes, index incremented and checked against stop; if stop not exceeded, condition checked again at the top.

### Demo: Combining Iterative and Conditional DO Loops (3:00) – p206d04.sas, from screenshots
```sas
data MonthSavingsW;
    set pg2.savings2;
    do Month=1 to 12 while (savings<=5000);
        Savings+Amount;
        Savings+(Savings*0.02/12);
    end;
    format Savings comma12.2;
run;

data MonthSavingsU;
    set pg2.savings2;
    do Month=1 to 12 until (savings>5000);
        Savings+Amount;
        Savings+(Savings*0.02/12);
    end;
    format Savings comma12.2;
run;

title "DO WHILE Results";
proc print data=MonthSavingsW;
run;

title "DO UNTIL Results";
proc print data=MonthSavingsU;
run;
```
- WHILE: up to 12 times while Savings ≤ 5000; condition evaluated at the top **after Month is incremented**. UNTIL: up to 12 times until Savings > 5000; evaluated at the bottom **before Month is incremented**.
- Savings values are the same in both reports (same number of executions). Row 1: Month = **13** in both – James never reached $5,000, so Month incremented one beyond the stop value, although the loop ran only 12 times.
- Other people: Savings match but **Month in the DO WHILE results is 1 greater** than in DO UNTIL, because in DO WHILE the index increments before the condition is checked → Month doesn't accurately count iterations. Best practice: create a counter inside the loop.
```sas
data MonthSavingsW;
    set pg2.savings2;
    Month=0;
    do i=1 to 12 while (savings<=5000);
        Month+1;
        Savings+Amount;
        Savings+(Savings*0.02/12);
    end;
    format Savings comma12.2;
    drop i;
run;
```
- Same changes in MonthSavingsU (`do i=1 to 12 until (savings>5000);`). Use a different (arbitrary) index variable i, Month as a sum-statement counter reset to 0 for each row, DROP i. Now Savings and Month match in both reports – Month = number of months to save $5,000 or reach 12 months, whichever comes first.

### Practice (06_2_p) – Level 1: Using a Conditional DO Loop; Level 2: Using an Iterative and Conditional DO Loop; Challenge: Controlling Execution of DO Loop Statements with CONTINUE and LEAVE [pop-ups not opened – Gap]

## 6.3 Lesson Review
- Learning More (links only): SAS documentation and examples for the DO statement; array processing in combination with DO loops.

### Summary of Lesson 6 (Lesson Review pop-up; screenshots)
- Iterative DO loop: `DATA output-table; ... DO index-column = start TO stop <BY increment>; ... repetitive code ... END; ... RUN;` – executes statements between DO and END repetitively based on an index column. The index column controls execution and **is included in the table being created unless you drop it**. Start = number/numeric expression for the initial value; stop = value the index must **exceed** to stop. The increment is **a positive or negative number**; BY and the increment are optional – if omitted the index increases by 1.
- With SET: the DO loop iterates for each iteration of the DATA step. **OUTPUT between DO and END** → one row per loop iteration. **OUTPUT after the DO loop** → a row based on the final iteration; the index column will be **an increment beyond the stop value**. DO loops can be nested.
- Conditional: `DO UNTIL | WHILE (expression); ... <OUTPUT;> END;` – executes based on a condition (iterative = set number of times). DO UNTIL executes until a condition is true, checked at the **bottom**, always executes at least once. DO WHILE executes while a condition is true, checked at the **top**, does not iterate even once if the condition is initially false. The expression must be in parentheses.
- Combined: `DO index-column = start TO stop <BY increment> UNTIL | WHILE (expression);` – index column listed before the UNTIL/WHILE condition. Iterative + UNTIL: condition checked **before** the index column is incremented at the bottom. Iterative + WHILE: condition checked at the **top**, index incremented at the **bottom**.

### Quiz: Lesson 6 (10 questions; read-only, NOT answered or submitted)
1. Which output table does this step produce?
```sas
data Earnings(keep=Qtr Earned);
    Amount=1000; Rate=.075/4;
    do Qtr=1 to 4;
        Earned+(Amount+Earned)*Rate;
    end;
run;
```
   a. Qtr 4, Earned 77.135865784 (one row) b. Qtr 5, Earned 77.135865784 (one row) c. Qtr 1–4: 18.75, 37.8515625, 57.311279297, 77.135865784 d. Qtr 1–5: 18.75, 37.8515625, 57.311279297, 77.135865784, 77.135865784
2. Which is true regarding the iterative DO loop (`DO index-column = start TO stop <BY increment>;`)? a. Start and stop values can be character or numeric. b. If no increment is specified, the default increment is 0. c. The index column is incremented at the bottom of each DO loop. d. The index column is not in the final table unless specifically kept.
3. Rows in work.savings? pg2.savings: James 250, Linda 300, Mary 275, Robert 350.
```sas
data work.savings;
    set pg2.savings;
    Savings=0;
    do Year=1 to 5;
        do qtr=1 to 4;
            Savings+Amount;
            Savings+(Savings*0.02/12);
        end;
    end;
run;
```
   a. 1 b. 4 c. 5 d. 20
4. Final value of Year? `data invest; do Year=2010 to 2019; Capital+5000; Capital+(Capital*.03); end; run;` a. . (missing) b. 2010 c. 2019 d. 2020
5. Which contains valid syntax? a. `do 1 to 10 by 2;` b. `do while (Year>2025);` c. `do until Earnings<=100000;` d. `do date='01JAN2019' to '31JAN2019';`
6. Rows in bikeinfo2? work.bikeinfo: Marco 12; Angela 10.
```sas
data bikeinfo2;
    set bikeinfo;
    do month=1 to 3;
        do week=1 to 4;
            bike=bike+2;
        end;
        output;
    end;
run;
```
   a. 2 b. 3 c. 6 d. 12 e. 24
7. Value of x at completion? `data test; x=15; do until(x>12); x+1; end; run;` a. . (missing) b. 13 c. 15 d. 16
8. Which statement is false? a. DO UNTIL executes until a condition is true. b. DO WHILE always executes at least one time. c. DO WHILE checks the condition at the top of the loop. d. DO UNTIL checks the condition at the bottom of the loop.
9. Which contains valid syntax? a. `do Age=10 to 14 and while (Weight<150);` b. `do week=1 to 52 do until (Mileage ge 2750);` c. `do Increase=5 to 10 while (temperature lt 102);` d. `do Year=2018 to 2028 or until (Earnings<=100000);`
10. Output table of `data test; bike=10; do day=1 to 7 while (bike lt 13); bike=bike+2; end; run;`? a. Bike 14, Day 2 b. Bike 14, Day 3 c. Bike 24, Day 7 d. Bike 24, Day 8

## Gaps
- Practices (06_1_p, 06_2_p) open in pop-ups – not opened.
- Quiz answers not available (quiz not submitted, by rule).
