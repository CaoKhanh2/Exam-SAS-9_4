# CR – Lesson 2: Analyze TSA Claims Data – Case Study

Source: Certification Review player (id=238), text mode transcripts + text pages. Captured 2026-10-28. Paraphrased; short quotes in quotation marks.

## 2.0 Case Study Introduction and Requirements

### Case Study Overview (video 5:23)
- Scenario: ~6 months in a new job; manager assigns first SAS project: prepare and analyze **TSA** (Transportation Security Administration, US Dept. of Homeland Security) claims, filed when travelers are injured or property is lost/damaged during airport screening. Claims filed **2002–2017**. Must report on overall data and by any specified state.
- Data: CSV **TSAClaims2002_2017.csv**, built from public TSA claims data (concatenated, extra columns removed) joined with FAA airport facilities data. **14 columns, over 220,000 rows.**
- Columns: Claim_Number (duplicate claim numbers with different info are considered valid); Incident_Date, Date_Received; Claim_Type (**14** valid types); Claim_Site (**8** valid values); Disposition (final settlement); Close_Amount (settlement $); Item_Category (varies by year – not used); Airport_Code, Airport_Name; County, City, State (2-letter code), StateName (full name).
- Process: import CSV → explore and validate against requirements (real data has inconsistencies) → prepare (procedures, functions, conditional logic, WHERE, formats, labels; usually the longest stage) → analyze (reports, summary statistics, a visualization) → export results to a PDF for a meeting with the manager.

### Possible Approaches to Solving this Case Study (text)
- Try on your own with the "TSA Case Study Data and Report Requirements" document; or use the Assignment Guide (tasks per programming step); or Case Study Hints; or Case Study Solutions videos. Everyone needs the Requirements document.

### Essential Case Study Documents (text page with links)
- Case Study Data Information (data source); Case Study Requirements (all essential requirements – must be used); Case Study Assignment Guide (requirements broken into programming-process steps).
- [Documents not opened – likely PDF → Gaps]

## 2.1 Case Study Hints (text pages; hints revealed with "Show Answer")
- **Accessing:** Task: import TSAClaims2002_2017.csv. Hints: define the TSA library; set an option to enforce SAS naming conventions for column names; PROC IMPORT to create a SAS table; use the `GUESSINGROWS=MAX` statement in PROC IMPORT.
- **Exploring:** Preview the data; explore Claim_Site, Disposition, Claim_Type, Date_Received, Incident_Date and note required adjustments per the Requirements document. Hints: PROC PRINT and PROC CONTENTS to preview; PROC FREQ to explore and compare value lists to the valid values in the requirements.
- **Preparing:** Tasks: remove duplicate rows; sort by ascending Incident_Date; clean Claim_Site, Disposition, Claim_Type; State → uppercase, StateName → proper case; new column Date_Issues = "Needs Review" for rows with date issues as defined in the requirements; permanent labels and formats; exclude County and City. Hints: PROC SORT with **NODUPKEY** to remove duplicate rows – the page notes "NODUPRECS is no longer documented in SAS", still valid but NODUPKEY recommended; PROC SORT the duplicate-free table; IF-THEN for Claim_Site; IF-THEN/ELSE for Disposition and Claim_Type; functions for State/StateName; IF-THEN for Date_Issues testing Incident_Date and Date_Received; FORMAT and LABEL statements; a statement to exclude County and City.
- **Analyzing:** Overall: number of date issues; claims per year of Incident_Date; titles. State level (selected state): frequencies of Claim_Type, Claim_Site, Disposition; mean, min, max, sum of Close_Amount rounded to integer; titles. Hints: PROC FREQ for date issues and claims per year (format Incident_Date to analyze by year); macro variable for StateName, initial value California; PROC FREQ and PROC MEANS subset to the state and excluding rows with date issues.
- **Exporting:** single PDF named ClaimReports, any style; customize procedure labels. Hints: ODS statement to create the PDF; ODS statement to specify procedure labels.

## 2.2 Case Study Solutions

### Solution for Accessing Data (video 3:06)
- `%LET path=` folder of the CSV (location copied from the data folder's Properties in SAS Studio). LIBNAME `TSA` pointing to the data folder via the path macro variable. Narrator defines paths/permanent libraries at the top of programs.
- `OPTIONS VALIDVARNAME=V7` so imported column names follow SAS naming conventions.
- PROC IMPORT: `DATAFILE=` in quotes with `&path` then a slash and the file name; `DBMS=` CSV; `OUT=` the table in the TSA library named claims import [spoken; likely `tsa.claims_import`]; `REPLACE` (if the table already exists, overwrite it). (recovered from screenshot)
- **GUESSINGROWS=MAX** statement: use every row to determine column types, because the CSV has many missing values.
- Result: **220,855 rows, 14 columns**; all column names follow SAS naming rules; log clean.

### Solution for Exploring Data (video 5:42)
- PROC PRINT limited to the first 20 observations for a snapshot.
- PROC CONTENTS with **VARNUM** (columns in table order instead of alphabetical). Over 220,000 rows, 14 columns. Date_Received and Incident_Date have format BEST12. but should be dates; Close_Amount BEST12. should be DOLLAR – fix in prepare stage.
- PROC FREQ, TABLE on Claim_Site, Disposition, Claim_Type, Date_Received, Incident_Date with **NOCUM NOPERCENT**; FORMAT the date columns to show counts by year.
- Findings: Claim_Site – hyphen and missing values → "Unknown". Disposition – hyphen/missing; "Closed: Canceled" has an extra space; "losed: Contractor Claim" missing the C (73 rows). Claim_Type – hyphen/missing; combined categories with a slash: requirement says the claim type is the **first** type (fix "Passenger Property Loss/Personal Injury" and "Property Damage/Personal Injury"). Date_Received – starts 2002 but some dates after 2017, many missing. Incident_Date – a few before 2002 and after 2017, many missing.
- Date_Received should always be after Incident_Date: PROC PRINT with WHERE Date_Received < Incident_Date, dates formatted DATE9. First row: Incident_Date Dec 26, 2006 vs Date_Received Feb 8, 2006 → data issue.

### Solution for Preparing Data (video 7:33)
- Remove duplicates: PROC SORT with `OUT=` and **NODUPRECS** (removes *adjacent* rows that are entirely duplicated) and `BY _ALL_` (sort by all columns so full duplicates become adjacent). Log: **5** duplicate observations deleted. (Note: the Hints page recommends NODUPKEY instead – see above.)
- Second PROC SORT of the new table BY Incident_Date.
- DATA step: new table TSA Claims Cleaned [name as spoken], SET `tsa.claims_nodups`.
  - Claim_Site: IF Claim_Site IN (hyphen, missing) THEN "Unknown".
  - Disposition: hyphen/missing → Unknown; ELSE IF value missing the C → "Closed: Contractor Claim" (no space between colon and Contractor); ELSE IF "Closed: Canceled" with extra space → without the space.
  - Claim_Type: hyphen/missing → Unknown, then ELSE IFs for the combined categories.
  - `State=UPCASE(State)`; `StateName=PROPCASE(StateName)`.
  - Date_Issues = "Needs Review" (spoken as NEEDS REVIEW) IF any: Incident_Date after Date_Received; Date_Received missing; Incident_Date missing; YEAR(Incident_Date) < 2002 or > 2017; YEAR(Date_Received) < 2002 or > 2017. Conditions combined with OR inside parentheses.
  - FORMAT Incident_Date Date_Received DATE9.; Close_Amount DOLLAR20.2. LABEL each column with the underscore replaced by a space. DROP County City.
- Validate afterwards (recovered from screenshot): PROC FREQ on Claim_Site, Disposition, Claim_Type and Date_Issues, suppressing percent and cumulative frequency, with **ORDER=FREQ** (descending frequencies) – distinct values should follow the requirements; **4,241** Date_Issues.

### Validate Your Data (text) – use PROC FREQ on Claims_Cleaned and compare to the "Validation Results" document [document not opened].

### Solution for Analyzing Data (video 9:39)
- Analyses exclude rows with date issues.
- Overall date issues: PROC FREQ on Date_Issues with NOCUM NOPERCENT; title "Overall Date Issues in the Data", cleared after the step. **4,241** rows have a date issue; others missing (= no issue). Adding the **MISSING** option treats missing values as a valid category (shown as a row instead of "Frequency Missing" at the bottom).
- Claims per year: `ODS GRAPHICS` on; title "Overall Claims by Year"; PROC FREQ TABLE Incident_Date / NOCUM NOPERCENT **PLOTS=FREQPLOT**; FORMAT Incident_Date YEAR.; WHERE Date_Issues is null. **2004** has the most claims, mostly decreasing afterwards.
- State analysis (static first, California): PROC FREQ **ORDER=FREQ**, TABLE Claim_Type Claim_Site Disposition / NOCUM NOPERCENT; WHERE StateName = "California" and Date_Issues is null. California: mostly Passenger Property Loss; 2 "Complement" and 7 "Complaint" claim types; most claims at Checked Baggage; over 10,000 claims denied.
- PROC MEANS with statistics MEAN MIN MAX SUM and MAXDEC=0, VAR Close_Amount, same WHERE.
- `%LET statename=California;` at the top; every literal California replaced with `&statename` (recovered from screenshot). Narrator first forgot to initialize the macro variable – had to highlight and run the %LET statement – then reran: same results. Then changed to North Carolina and reran → all state-level results changed.

### Solution for Exporting Data (video 3:45)
- Requirements: one PDF named Claim Reports, any style, custom procedure labels. `%LET outpath=…` stores the output location (easy to reuse/change). `ODS PDF FILE=` with `&outpath` inside the quotes and file name **ClaimsReport** (recovered from screenshot).
- `ODS PDF FILE=…` with `STYLE=MEADOW` and `PDFTOC=1` (only first bookmark level expanded); all reports between ODS PDF FILE and `ODS PDF CLOSE`.
- `ODS NOPROCTITLE` removes procedure names above each output.
- `ODS PROCLABEL "…"` before each procedure: "Overall Date Issues", "Overall Claims by Year", "&StateName Claims Overview", "… Close Amount Statistics" – labels with &StateName change dynamically. PDF saved in the Reports folder; bookmarks show the PROC LABELs.

### Check Your Results (text) – compare to "Case Study Results" document [not opened].

## 2.3 Test your Solution
- "Quiz: Test your Case Study Code" (7 questions; read from screenshots, never answered):
  - **Q1.** How many date issues are there in the overall data? — a. 21660 · b. 4241 · c. 2539 · d. 3211
  - **Q2.** Looking at the frequency plot, are incidents generally increasing or decreasing from 2004 to 2017? — a. increasing · b. decreasing
  - **Q3.** Between 2004 and 2017, what is the first year that the incident frequency fell below 10,000? — a. 2006 · b. 2008 · c. 2010 · d. 2012 · e. 2016
  - **Q4.** Modify your code to analyze claims for the state of Hawaii. In Hawaii, how many claims were there for property damage? — a. 916 · b. 1258 · c. 1481 · d. 1802
  - **Q5.** In Hawaii, how many incidents occurred at the checkpoint? — a. 1099 · b. 989 · c. 1108
  - **Q6.** In Hawaii, how many claims were approved in full? — a. 107 · b. 1001 · c. 1017 · d. 987
  - **Q7.** What is the average Close Amount for claims in Hawaii? — a. 85 · b. 74 · c. 68

## Gaps
- Case study PDFs (Data Information, Requirements, Assignment Guide, Validation Results, Case Study Results) not opened.
- Demo code visible only in video.
