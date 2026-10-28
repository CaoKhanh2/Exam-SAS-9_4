# P1 – Lesson 1: Essentials (+ Course Overview pages)

Course: SAS® Programming 1: Essentials (SAS9.4v2, English). Captured 2026-10-27 in all-text mode (Alt+W).

## Table of contents (from player)

Course Overview and Data Setup (4 pages; page 4 is in P1_L00_setup.md):
- CO-1 Welcome to the Course (1:50)
- CO-2 Demo: The SAS Programming Process (7:17)
- CO-3 Practicing in This Course (1:02)
- CO-4 Setting Up Your Practice Files (REQUIRED) → see P1_L00_setup.md

Lesson 1: Essentials – **13 pages**:
1. Lesson Overview (0:17)
2. SAS Programming Interfaces (1:35)
3. Demo: Programming with SAS Studio (4:25)
4. Demo: Programming with SAS Enterprise Guide (4:38)
5. Practice Using SAS Software
6. SAS Program Structure (2:40)
7. Activity
8. SAS Program Syntax (0:56)
9. Demo: Understanding SAS Program Syntax (2:12)
10. Demo: Finding and Resolving Syntax Errors (4:15)
11. Activity
12. Learning More
13. Lesson Review and Quiz

(Section headings in the TOC – "Using SAS Programming Tools", "Understanding SAS Syntax", "Lesson Summary" – are not pages.)

---

## Course Overview pages

### [Page CO-1/4] Welcome to the Course
**Type:** concept
**Content:**
- Instructor: Stacey Syphus. The course teaches writing SAS code for the most common data processing tasks.
- SAS programming language is at the core of SAS tools/solutions.
- Basic process steps used as the course framework:
  - access data or read it with a program
  - explore the data to see what's there and what you might need to add or change
  - prepare the data for analysis
  - analyze and report on the data
  - export results to various report and data formats
**Code:** none
**Capture status:** complete

### [Page CO-2/4] Demo: The SAS Programming Process
**Type:** demo
**Content:**
- Recommendation: view/read this demo; perform the steps only after completing data setup.
- Program analyzes real data for international storms (hurricanes, typhoons, cyclones) collected since 1980; data stored in an Excel workbook.
- Excel workbook **Storm.xlsx** worksheets:
  - **Storm_Summary** – one row per storm between 1980 and 2016. **Basin** represents a location. Wind speeds in miles per hour (MPH).
    - Note: refer to **Basin_Codes**, **SubBasin_Codes**, **Type_Codes** worksheets for full names of codes. Each basin code = an ocean and location (e.g., **NA** = **North Atlantic**). Each type code = a type of storm (e.g., **TS** = **Tropical Storm**).
  - **Storm_Detail** – one measurement for every six hours of a storm; wind speeds in knots.
  - **Storm_Damage** – description and damage estimates (adjusted for inflation) for US storms with damages greater than one billion dollars.
  - **Storm_Range** – one row per storm with a minimum of four wind measurements; top four in columns **Wind1** through **Wind4**.
  - **Storm_2017** – one row per storm for 2017.
  - **Basin_Codes**, **SubBasin_Codes**, **Type_Codes** – lookup tables with codes and descriptive values.
- Steps:
  1. Do the course setup steps first; open your SAS software.
  2. Open **ep101d01.sas** from the **demos** folder (don't focus on syntax yet).
  3. **Section 1: Access Data** – connects to the Storm Excel workbook and imports data. The code: sets system options; establishes the location of course files and generated results; connects to Excel **Storm.xlsx**; creates a temporary copy of the **Storm_Damage** Excel spreadsheet as a SAS table.
  4. If using SAS Studio in the **SAS Virtual Lab**, see the comment in Section 1 for a change you need to make. With SAS OnDemand for Academics or your own software, don't change the code.
  5. Highlight Section 1, press F3 – data imported into a SAS table.
  6. **Section 2** (exploring): creates a frequency report of unique values of **Basin** and **Type**; calculates summary statistics for **MaxWindMPH** and **MinPressure**; prints the first five rows of the **storm_damage** table imported from Excel.
  7. Run Section 2. Two one-way frequency reports (Basin, Type); basin codes include a lowercase value for an **a**, [UNCLEAR – line clipped at right edge]. Summary Statistics table: average, minimum, maximum for MaxWindMPH and MinPressure; there are minimum pressure values of negative 9,999 – probably not correct, must be accounted for. Last table: first five rows of Storm Damage.
  8. **Section 3** (preparing): fixing case inconsistencies; creating new columns by extracting values from existing codes or concatenating values; computing storm length (days between start and end date); conditional processing to determine the ocean from the basin code; joining tables. Code: adds additional storm data from 2017; cleans data by correcting case differences and assigning descriptive values to coded values; creates new columns with numeric calculations and character manipulations; joins tables to combine columns from two tables.
  9. Run Section 3; examine Output Data – new tables are clean, validated, ready for the next phase.
  10. **Section 4** analyzes/reports and exports results [part of a sentence clipped: "…doing all sorts of interesting things. V…" – UNCLEAR]; analyzing storms for 2016 and Basin North Atlantic; computing summary statistics; creating a map of where storms occurred and their maximum wind speeds [UNCLEAR – clipped]. Code: designates values to subset data as **2016** and **NA** (North Atlantic basin); generates default reports and an Excel workbook with the reports; frequency report for **BasinName** for the selected year; summary statistics report and table for storms in the selected year; map of storms for the selected year and basin.
  11. Run Section 4; Results tab shows reports/graphics; the Excel workbook created as output has a tab summarizing 2016 storms by Basin with a bar chart [UNCLEAR – clipped], a tab for wind statistics, and a map of the most powerful storms in the North Atlantic Basin for the 2016 season [rest clipped].
  12. Open **Storm_Report2016.xlsx**: SAS Studio – Files and Folders > EPG1V2 > **output**; right-click > **Download File**. Enterprise Guide – Results tab link, or right-click > **Open**.
**Code:** program ep101d01.sas not displayed on page.
**Capture status:** partial (several long lines clipped at the right edge of the text pane in steps 7, 10, 11 – marked [UNCLEAR]; no code involved)

### [Page CO-3/4] Practicing in This Course
**Type:** concept
**Content:**
- Main data: storm data; also National Park Service data and SAS-provided sample tables.
- Demos: watch or follow along. Activities: short programming problem. Practices: more involved, often combine concepts; generally 3 levels – do any or all.
- Level 1: basic problems, step-by-step guidance. Level 2: intermediate, defined goals, less guidance. Challenge: complex problems, may require SAS Help and documentation. All practices have a complete solution you can check any time.
**Capture status:** complete

---

## Lesson 1 pages

### [Page 1/13] Lesson Overview
**Type:** concept
**Content:**
- Before writing SAS programs you need the essentials (foundation of the programming process): how to use SAS programming tools and the fundamentals of SAS program structure and syntax.
**Capture status:** complete

### [Page 2/13] SAS Programming Interfaces
**Type:** concept
**Content:**
- Several programming interfaces to interactively write and submit code.
- **SAS windowing environment** – interface that is part of SAS.
- **SAS Enterprise Guide** – client application on your PC; connects to SAS on a local or remote server.
- **SAS Studio** – web-based interface connecting to SAS on a server; runs in a web browser, no download, usable on any computer.
- This class uses SAS Studio and SAS Enterprise Guide (most modern programming tools). Code can also be written/submitted in applications such as Jupyter Notebook, but without access to some SAS programming tools.
- Programming basics: an editor to write/submit code; a way to read messages about submitted code (**the log**); a way to view reports and data your programs create. All SAS interfaces have these tools.
- SAS Studio and EG editors include code completion, formatting, and syntax coloring.
- You can use your preferred interface; course shows both SAS Studio and EG.
**Capture status:** complete

### [Page 3/13] Demo: Programming with SAS Studio
**Type:** demo
**Content:**
1. Open SAS Studio.
2. Browse data: navigation pane > **Libraries** > expand **My Libraries** > **SASHELP**. SASHELP has sample SAS tables used in demos/examples.
3. Double-click **CLASS** to open in the data grid. Left panel summarizes columns and attributes (left arrow minimizes it). **SASHELP.CLASS** has 19 rows (students: name, sex, age, height, weight). Close the SASHELP.CLASS tab.
4. An empty Program window opens by default; otherwise **New > SAS Program** or F4. Type the program in the **Code** tab (below). It reads SASHELP.CLASS, creates a copy called **myclass**, and prints MYCLASS.
5. **Run** or F3. The **Program 1** tab has tabs for Code, Log, Results, Output Data.
6. **Log** tab: program and messages returned from SAS; expand **Errors**, **Warnings**, **Notes** sections for a summary list; click a message to find it in the log. This program ran fine – only notes.
7. **Results** tab – report for MYCLASS.
8. **Output Data** tab – new table **Myclass**.
9. Highlighting a portion of code runs only the selection (used often in the course). Highlight PROC PRINT and RUN; Run/F3.
10. Log and results were replaced. Results shows the PROC PRINT report. Output data does not display because the code that created output data wasn't run.
11. View multiple tabs: drag a tab (Code, Log, Output Data, Results) to the side or bottom of the work area until a highlighted region appears; drag back to return to a single window.
**Code:**
```sas
data myclass;
    set sashelp.class;
run;

proc print data=myclass;
run;
```
**Capture status:** complete

### [Page 4/13] Demo: Programming with SAS Enterprise Guide
**Type:** demo
**Content:**
1. Open SAS Enterprise Guide.
2. Start page: **Create a New Program**.
3. Servers window (lower left): expand **Servers > Local > Libraries > SASHELP**. Note: the **Sashelp** library is a collection of sample data files provided by SAS; the course references various Sashelp files.
4. Double-click **class**: 19 students with name, sex, age, height, weight.
5. Select the **Program** tab.
6. Type/paste the program (below).
7. **Run** or F3; multiple tabs are created.
8. **Log** tab: program code and messages from SAS. **Log Summary** displayed by default at the bottom; click a message to find it in the log.
9. **Output Data** tab shows the new table **myclass**; **Results** tab shows the report.
10. Highlight PROC PRINT and RUN; **Run**/F3 submits only the highlighted portion.
11. Log and results were replaced.
12. Viewing multiple tabs: by default EG separates a program's tabs; right-click a tab > **Float**, **New vertical tab group**, or **New horizontal tab group**; or drag tabs outside EG.
  - Note: return a tab: right-click top bar > **Docked as tabbed document** (Float window) or **Move to previous tab group** (vertical/horizontal group). Defaults for program sub-tabs: **View > Program tab presets**.
**Code:**
```sas
data myclass;
    set sashelp.class;
run;

proc print data=myclass;
run;
```
**Capture status:** complete

### [Page 5/13] Practice Using SAS Software
**Type:** practice
**Content:**
- Practices help you get familiar with programming in SAS software. **You only have to do one** – for the software used when setting up practice files.
- Note: SAS provides access to SAS Studio only; the EG option is for students who already have their own SAS Enterprise Guide.

**Practice task + solution – Practice: Exploring SAS Studio**
1. Start SAS Studio. Main window: navigation pane (left) and work area (right).
2. Banner area options: **Search** (files and folders); **Open** (files from your files and shortcuts); **New Options** (new program, new import data, new query, close all tabs, maximize view); **SAS Programmer** (SAS Studio has SAS Programmer and Visual Programmer perspectives – a perspective is a predetermined set of features customized for a type of user; select SAS Programmer; more in *SAS® Studio: User's Guide*); **More application options** (edit autoexec file, view menu, preferences, tool options, background submission status, reset SAS session); **Help** (SAS Studio Help, SAS Product Documentation, About SAS Studio).
3. On the **Program 1** tab type/paste the DATA step. Note: if pasted, **Format Code** improves spacing.
4. **Run**/F3. Examine LOG and OUTPUT DATA. The RESULTS tab is empty because the program did not create a report.
5. On the CODE tab add summary statistics code: type **pr** – prompt with valid keywords and syntax help; Enter adds **proc**; space, type **me**, Enter adds **means**. Note: Autocomplete prompts include a window with syntax help and links to documentation and examples.
6. Space, select **data=** from the prompt, type **work.shoes**; space – prompt lists all valid options; complete `proc means data=work.shoes mean sum;`
7. Disable autocomplete: **More application options > Preferences > Code and Log**; clear **Enable autocomplete**; **Save**.
8. Space after SUM and before the semicolon – no prompt. Type **MAXDEC=2** to round to two decimals. Note: with autocomplete off, Ctrl+spacebar temporarily shows the prompt.
9. Add VAR, CLASS, RUN statements (code below).
10. Highlight PROC MEANS through RUN; Run/F3; confirm results.
11. Multiple tabs: drag **RESULTS** to the right side of the work area until a highlighted region appears; drag back to return.
12. RESULTS tab: **HTML**, **PDF**, or **Word** icon opens results in that format (prompt to open/save in browser). Note: more output options under **More application options > Preferences > Results**.
13. Save: CODE tab > **Save as**; navigate to the **output** folder; Name **shoesprogram**; Save – the .sas extension is added automatically.
```sas
data work.shoes;
    set sashelp.shoes;
    NetSales=Sales-Returns;
run;
```
```sas
proc means data=work.shoes mean sum;
    var NetSales;
    class region;
run;
```

**Practice task + solution – Practice: Exploring SAS Enterprise Guide**
1. Start EG and close the Start page. EG = navigation area on the left, work area on the right.
2. **File > New > Program** (or **Create a new item** tool > **Program**).
3. On the **Code** tab type/paste the DATA step (same code as above). Note: **Format Code** button improves spacing.
4. **Run**/F3. Examine Log and Output Data tabs.
5. **Log** tab: additional statements before and after the DATA step – *wrapper code* added by EG to set up the environment and results. Hide it: **Tools > Options > Results > General**, clear **Show generated wrapper code in SAS log**; **OK**.
6. Return to **Code** and rerun.
7. Add summary statistics code: type **pr** (prompt with valid keywords); Enter or spacebar adds **proc**; space, type **me**, Enter adds **means**.
8. Space; use prompts to select **data=work.shoes**; prompt lists all valid options; complete: `proc means data=work.shoes mean sum maxdec=2;` Note: autocomplete can be modified/disabled via **Program > Editor Options** > **Autocomplete** tab.
9. Add VAR, CLASS, RUN statements (after VAR and CLASS the prompt lists columns from **work.shoes**):
```sas
proc means data=work.shoes mean sum;
     var NetSales;
     class region;
run;
```
10. Highlight PROC MEANS through RUN; **Run**/F3. Note: the default output format in EG is HTML.
11. Default workspace layout for tabs is 1:1 Vertical split. Change via **View > Program tab presets**, or right-click a tab > **Float**, **New vertical tab group**, **New horizontal tab group**, or (if available) **Move to previous tab group**. Note: you can also drag a tab anywhere.
12. Single window for all program tabs: **View > Program tab presets > Standard**.
13. Other output types: **Code** tab > properties icon > **Results > Customize result formats, styles, and behavior**; clear selected boxes; select **PDF** and **Excel**; **OK**.
14. Run again – Excel and PDF files created on the **Results** tab. Note: PowerPoint, Excel, PDF, RTF results must be viewed outside EG.
15. Save: **Code** tab > **Save Program As**; navigate to **output**; File name **shoesprogram**; **Save** (.sas added automatically).
- Note on step 9 code: the practice page shows `proc means data=work.shoes mean sum;` (without MAXDEC=2) in the final block although step 8 adds maxdec=2 – captured as shown.
**Capture status:** complete

### [Page 6/13] SAS Program Structure
**Type:** concept
**Content:**
- A SAS program = a sequence of steps; each step performs a specific task.
- Two kinds of steps: **DATA** steps and **PROC** (procedure) steps; any combination allowed. Steps get their name from the keyword beginning the first statement (DATA or PROC).
- Most steps end with a **RUN** statement; a few PROC steps end with **QUIT**. Without RUN, the beginning of a new DATA or PROC step signals the end of the previous step.
- Example program: three steps – one DATA step and two PROC steps.
- DATA step: generally reads data from an input source, processes it, creates a SAS table; may also filter rows, compute new columns, join tables, other manipulations. Here: creates an output table and adds a new column.
- PROC step: processes a SAS table in a specific, predefined way (reports, graphs, data management, complex statistics). Here: PROC PRINT lists all rows and columns; PROC MEANS calculates basic summary statistics.
- Each step = a sequence of statements; most statements start with a keyword.
  - The DATA step has four statements: DATA, SET, an assignment statement, RUN. DATA, SET, RUN are keywords; the assignment statement creates a new column and doesn't start with a keyword.
  - First PROC step: 2 statements (PROC PRINT, RUN).
  - Last PROC step: three statements (PROC MEANS, VAR, RUN).
- **All statements must end with a semicolon.**
- Global statements (e.g., **TITLE**, **OPTIONS**, **LIBNAME**) can be outside DATA and PROC steps, typically define an option/setting for the SAS session, and do not need a RUN statement.
**Code:**
```sas
data myclass;
    set sashelp.class;
    heightcm=height*2.54;
run;

proc print data=myclass;
run;

proc means data=myclass;
    var age heightcm;
run;
```
**Capture status:** complete

### [Page 7/13] Activity
**Type:** activity
**Content:** Open **p101a03.sas** from the **activities** folder (program not shown on page).
1. How many steps are in the program? – Answer: three steps: one DATA step and two PROC steps.
2. How many statements are in the PROC PRINT step? – Answer: four statements.
3. How many global statements are in the program? – Answer: three TITLE statements.
4. Run the program and view the log. How many observations were read by the PROC PRINT step? – Answer: 11 observations.
**Capture status:** complete (program file itself not displayed)

### [Page 8/13] SAS Program Syntax
**Type:** concept
**Content:**
- The two programs below have exactly the same code: first DATA/PROC steps have no line breaks; second have line breaks and indentation. Spacing doesn't matter to SAS but matters to readers; program editors have code-formatting tools.
- Unquoted values (columns, table names, keywords) can be typed in any case.
- Comments are ignored when the program executes – document code or suppress code from executing.
  - Comment out a single statement ending in a semicolon: add an asterisk at the beginning of the statement.
  - Comment out multiple lines: `/*` at the beginning and `*/` at the end.
**Code:**
```sas
data myclass;set sashelp.class;run;
proc print data=myclass;run;

data myclass;
    set sashelp.class;
run;

proc print data=myclass;
run;
```
```sas
/* students under 13 years old */

data under13;
    set sashelp.class;
    where Age<13;
    *drop Height Weight;
run;
```
**Capture status:** complete

### [Page 9/13] Demo: Understanding SAS Program Syntax
**Type:** demo
**Content:**
1. Open **p101d02.sas** from **demos**. Not spaced well: multiple statements on a single line, inconsistent indentation.
2. Submit – runs without warnings or errors.
3. Click **Format Code** button or right-click > **Format Code**.
4. Add text before the DATA statement: *Program created by <your-name>*; highlight it and press Ctrl + forward slash (/) to surround it with `/*` and `*/`.
5. Comment out the first TITLE statement and the WHERE statement in PROC PRINT by putting an asterisk in front of each.
6. Run; verify there is no title in the report and **AvgMPG** has values less than 35.
**Code:**
Starting program:
```sas
data mycars; set sashelp.cars;
        AvgMPG=mean(mpg_city, mpg_highway);
run;
title "Cars with Average MPG Over 35";
proc print data=mycars;
var make model type avgmpg;
where AvgMPG > 35; run;
title "Average MPG by Car Type";
proc means data=mycars
mean min max maxdec=1;
var avgmpg;class type;
RUN;TITLE;
```
Solution code:
```sas
/*Program created by */
data mycars;
    set sashelp.cars;
    AvgMPG=mean(mpg_city, mpg_highway);
run;

*title "Cars with Average MPG Over 35";

proc print data=mycars;
    var make model type avgmpg;
    *where AvgMPG > 35;
run;

title "Average MPG by Car Type";

proc means data=mycars
     mean min max maxdec=1;
     var avgmpg;
     class type;
run;

title;
```
**Capture status:** complete

### [Page 10/13] Demo: Finding and Resolving Syntax Errors
**Type:** demo
**Content:**
- Examples of syntax errors: misspelled keywords, unmatched quotation marks, missing semicolons, invalid options.
- Some errors (e.g., unmatched quotation marks) can be caught by watching color-coded syntax. When SAS finds a syntax error, a warning or error message is written to the log.
1. Open **p101d03.sas** from **demos** (code below). Three syntax errors; color coding shows them: **DAAT** (misspelling of DATA) – other keywords are bold blue, DAAT is not; end of PROC PRINT statement missing a semicolon – coloring of following keywords VAR and WHERE differs; in PROC MEANS, **average** is an option and doesn't have the same blue coloring as other options.
2. Run; read the log top to bottom:
   - First message is a **warning**: Daat is underlined; SAS assumed DATA was simply misspelled and **successfully runs the DATA step**.
   - Next, **VAR** is underlined. VAR is valid, so when something underlined is accurate, look **immediately before** it. Message says syntax error, expecting one of the following – first suggestion is a semicolon. The missing semicolon at the end of PROC PRINT made SAS treat VAR as a continuation of the PROC PRINT statement; VAR is not a valid option. **The SAS system did not process the step** – PROC PRINT did not run.
   - Last error: **average** is underlined; the error message lists valid options for the PROC MEANS statement; average is not one of them. Correct to **MEAN**. This step also did not run because of the errors.
3. Fix the code and rerun.
**Code:**
Starting program (p101d03.sas):
```sas
daat mycars;
        set sashelp.cars;
        AvgMPG=mean(mpg_city, mpg_highway);
run;

title "Cars with Average MPG Over 35";
proc print data=mycars
        var make model type avgmpg;
        where AvgMPG > 35;
run;

title "Average MPG by Car Type";
proc means data=mycars average min max maxdec=1;
        var avgmpg;
        class type;
run;

title;
```
Solution code:
```sas
data mycars;
    set sashelp.cars;
    AvgMPG=mean(mpg_city, mpg_highway);
run;

title "Cars with Average MPG Over 35";
proc print data=mycars;
    var make model type avgmpg;
    where AvgMPG > 35;
run;

title "Average MPG by Car Type";
proc means data=mycars mean min max maxdec=1;
    var avgmpg;
    class type;
run;

title;
```
**Log messages shown:** described only (no verbatim text on page): a warning that SAS assumed DATA was misspelled; "syntax error, expecting one of the following" with semicolon first; the SAS System did not process the step; error listing valid PROC MEANS options.
**Capture status:** complete

### [Page 11/13] Activity
**Type:** activity
**Content:** Open **p101a04.sas** from **activities** (original program not shown on page).
1. Format the program. What syntax error is detected? – Answer: Formatting the code identifies the missing quotation mark.
2. Fix the error and run the program. – Answer code (quote fixed; other errors remain):
```sas
data canadashoes set sashelp.shoes;
        where region="Canada";
        Profit=Sales-Returns;
run;

prc print data=canadashoes;
run;
```
3. Read the log, identify additional syntax errors, correct, format again, add a comment describing the changes. – Answer:
```sas
/*Missing semicolon, unbalanced quote,
and misspelled PROC fixed.*/

data canadashoes;
    set sashelp.shoes;
    where region="Canada";
    Profit=Sales-Returns;
run;

proc print data=canadashoes;
run;
```
4. Run; how many rows are in **canadashoes**? – Answer: 37
**Capture status:** complete

### [Page 12/13] Learning More
**Type:** concept (links)
**Content:** "What If You Want to…"
- …use point-and-click SAS Studio tasks to generate code? – Watch the Getting Started with SAS Studio video; view free video tutorials on using SAS Studio tasks.
- …use the SAS windowing environment in this class? – Watch Getting Started with SAS Windowing Environment; complete the SAS windowing environment activity on the Extended Learning Page.
- …learn about using Enterprise Guide tasks to generate code? – In EG select **Help > Getting Started Tutorial**; take the SAS Enterprise Guide 1: Querying and Reporting course.
- …use Jupyter Notebook to submit code to SAS? – Blog post How to run SAS programs in Jupyter Notebook; Jupyter kernel for SAS on the SAS github page.
- …write code to take advantage of cloud-enabled SAS Viya? – Video An Introduction to SAS Viya Programming for SAS 9 Programmers; take Programming for SAS Viya (link to come) after SAS Programming 1.
- …integrate open source languages with SAS? – Free SAS Programming for R Users course; Getting Started with SAS Viya for R documentation.
**Capture status:** complete (external links not followed)

### [Page 13/13] Lesson Review and Quiz
**Type:** summary + quiz

**Summary of Lesson 1: Essentials** (Open Lesson Review)
- Running a SAS Program:
  - Submit with the **Run** icon or **F3**.
  - Run a subset: highlight statements first. SAS Studio: **Run** or F3. EG: arrow next to **Run** > **Run Selection** or F3.
  - A program can create a log, results, and output data.
  - Resubmitting in **Enterprise Guide or SAS Studio replaces** the log, output data, and results.
  - Resubmitting in the **SAS windowing environment appends** the log and results.
- Understanding SAS Syntax:
  - Programs consist of DATA and PROC steps; each step consists of statements. Forms: `DATA … ; other statements RUN;` and `PROC … ; other statements RUN;`
  - Global statements are outside steps: `TITLE … ;` `OPTIONS … ;` `LIBNAME … ;`
  - All statements end with a semicolon.
  - Spacing doesn't matter.
  - Unquoted values can be lowercase, uppercase, or mixed case.
  - Consistent spacing is good practice. Automatic spacing: SAS Studio – **Format Code** icon; EG – **Edit > Format Code** or Ctrl+I.
  - Comments prevent text from executing.
  - Common syntax errors: unmatched quotes, missing semicolons, misspelled keywords, invalid options.
  - Syntax errors might result in a warning or error in the log.
  - Refer to the log to diagnose and resolve syntax errors.

**Quiz questions** (Quiz: Lesson 1 – 10 questions; read only, nothing selected or submitted):
1. How many steps does this program contain? (options: one / two / four / eight) – tests distinguishing steps from statements.
```sas
data national;
    set sashelp.baseball;
    BatAvg=nHits/nAtBat;
run;

proc contents data=national;
run;

proc print data=national;
run;

proc means data=national;
    var BatAvg;
run;
```
2. Running a SAS program can create which of the following? (log / output data / results / all of the above) – tests the three program outputs.
3. Which of the following is a SAS syntax requirement? (column one; one statement per line; line space between steps; end each statement with a semicolon) – tests free-format rules.
4. Which steps are typically used to generate reports and graphs? (DATA / PROC / REPORT / RUN) – tests DATA vs PROC roles.
5. Does this comment contain syntax errors? (correctly specified / every comment line must end with semicolon / comment on more than one line / semicolon in the middle of the comment) – tests block-comment rules.
```sas
  /*
Report created for budget
presentation; revised October 15.
  */
proc print data=work.newloan;
run;
```
6. What result would you expect from submitting this step? (report / error message in the log / creation of table work.newsalesemps) – tests missing semicolon before RUN.
```sas
proc print data=work.newsalesemps
run;
```
7. What happens if you submit the following program? (SAS does not execute the step / SAS assumes PROC is misspelled and executes the step) – tests misspelled PROC keyword behaviour.
```sas
porc print data=work.newsalesemps;
run;
```
8. True/False: This program contains a syntax error because National is in different cases. – tests case-insensitivity of table names.
```sas
data national;
    set sashelp.baseball;
    BatAvg=nHits/nAtBat;
run;

proc means data=NATIONAL;
    var BatAvg;
run;
```
9. How many statements does this program contain? (five / six / seven / eight) – tests counting statements (comment, global TITLE/FOOTNOTE, multi-line statements).
```sas
*Create a cars report;

title "European Cars Priced Over 30K";
footnote "Internal Use Only";

proc print data=sashelp.cars;
    where Origin='Europe'
          and MSRP>30000;
    var Make Model Type
        Mpg_City Mpg_Highway;
run;
```
10. Which of the following is not a SAS programming interface? (SAS Enterprise Guide / SAS Manager / SAS Studio / SAS windowing environment) – tests interface names.
**Capture status:** complete

---

## Completeness check
- Lesson 1: **13/13 pages captured** (plus Course Overview CO-1..CO-3; CO-4 in P1_L00_setup.md).
- Partial items: CO-2 has clipped prose lines ([UNCLEAR]); no code affected.
