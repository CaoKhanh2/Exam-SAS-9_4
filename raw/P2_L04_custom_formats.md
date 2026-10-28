# P2 – Lesson 4: Creating and Using Custom Formats

Source: SAS Programming 2 player (course id=235), text mode + screenshots. Captured 2026-10-28. Paraphrased; short quotes in quotation marks. Code copied from screenshots.

## 4.0 Lesson Overview
- Create and use custom formats to enhance how data is displayed in a table or report.

## 4.1 Creating and Using Custom Formats

### Formatting Data Values (0:29) – from screenshot
- Unformatted pg2.class_birthdate: Name, Registration (C/I), Age, Height, Weight, BirthDate (16370 …).
```sas
proc print data=pg2.class_birthdate noobs;
    format Height Weight 3.0 Birthdate date9.;
run;
```
- Formats specify how values are displayed: Height/Weight width 3, no decimals (69, 57, 65, 63; 113, 84, 98, 103); BirthDate as two-digit day, three-letter month, four-digit year (26OCT2004 …). "When you use a format, the format name contains one period."

### Activity (p204a01.sas) – with answers
- FORMAT statement in the DATA step: Date with three-letter month and four-digit year, Volume with commas, CloseOpenDiff and HighLowDiff with dollar signs and two decimals:
  `format Date monyy7. Volume comma12. CloseOpenDiff HighLowDiff dollar8.2;`
- In PROC MEANS show only a four-digit year: `format Date year4.;`
- Advantage of FORMAT in the DATA step vs the PROC step: "Formats that you use in the DATA step are **permanent attributes** that are stored in the descriptor portion of the table. Formats that you use in a PROC step are **temporary attributes**."

### Creating and Applying a Custom Format (2:32) – from screenshots
- Goal: Registration C → Complete, I → Incomplete; Height low → Below Average, mid → Average, high → Above Average.
```
PROC FORMAT;
    VALUE format-name value-or-range-1 = 'formatted-value'
                      value-or-range-2 = 'formatted-value'
                      . . .;
RUN;
```
- PROC FORMAT creates custom formats; each **VALUE** statement creates one format. Format names are limited to **32 characters**. **Character format names must start with a dollar sign followed by a letter or underscore. Numeric format names must start with a letter or underscore.**
- Value-label pairs: left of = individual values or ranges; **character values need quotes, numeric values do not**; right of = formatted values, enclosed in quotation marks. Multiple VALUE statements allowed in one PROC FORMAT step.
```sas
proc format;
    value $regfmt 'C'='Complete'
                  'I'='Incomplete';
run;

proc print data=pg2.class_birthdate;
    format Registration $regfmt.;
run;
```
- **No period** after the format name in the VALUE statement; capital C / capital I mapped. No reference to a table or column in PROC FORMAT → the format can be applied to any column with those values. **Period after the format name when you use it.**

### Activity (p204a02.sas) – with answers
1. HRANGE: 50–57 Below Average, 58–60 Average, 61–70 Above Average:
```sas
value hrange 50-57='Below Average'
             58-60='Average'
             61-70='Above Average';
```
2. `format Registration $regfmt. Height hrange.;`
4. Why is Height not formatted in the first row? "A value of 57.3 does not fit into any of the ranges. Therefore, the actual value is displayed."

### Using Ranges (1:35) – from screenshot
```sas
value hrange 50-<58 = 'Below Average'
             58-60  = 'Average'
             60<-70 = 'Above Average';
```
- A dash next to a number **includes** the value (58-60 includes 58 through 60). A **less-than symbol before the ending value excludes the end** (50-<58 = 50 up to but not including 58). A **less-than symbol after the starting value excludes the start** (60<-70 = greater than 60 up to and including 70).
```sas
value hrange  low-<58 = 'Below Average'
              58-60   = 'Average'
             60<-high = 'Above Average';
```
- Keywords **LOW** (lowest possible value) and **HIGH** (highest possible value) in a range: low-<58 includes all numeric values less than 58 "including negative values and zero"; 60<-high includes all values greater than 60 (even 1 million).
```sas
value $regfmt 'C' = 'Complete'
              'I' = 'Incomplete'
          other = 'Miscoded';
```
- **OTHER** keyword as a single value: includes all values that don't match any other value or range (anything other than capital C or capital I → Miscoded).

### Demo: Creating and Using Custom Formats (3:28) – p204d01.sas, from screenshots
```sas
proc format;
    value stdate low - '31DEC1999'd = '1999 and before'
                 '01JAN2000'd - '31DEC2009'd = '2000 to 2009'
                 '01JAN2010'd - high = '2010 and later'
                 . = 'Not Supplied';
    value $region 'NA'='Atlantic'
                  'WP','EP','SP'='Pacific'
                  'NI','SI'='Indian'
                  ' '='Missing'
                  other='Unknown';
run;

proc freq data=pg2.storm_summary;
    tables Basin*StartDate;
    format StartDate stdate. Basin $region.;
run;
```
- STDATE = numeric format based on date values (date constants); LOW builds a range from the oldest date through 31DEC1999; a label for missing values (`.`). $REGION: several values separated by commas on the left; `' '` = blank (missing character). The log confirms the formats were output.
- The first version of the demo used `tables Basin*StartDate / norow nocol;` [as in the starting program].
- Crosstab shows formatted Basin values in rows and formatted StartDate ranges in columns: "Custom formats are not only a great way to just display values differently, but also group raw values."

### Activity (p204a03.sas) – with answers
- Replace IF-THEN/ELSE creating BasinGroup with PUT and the $REGION format:
```sas
data storm_summary;
    set pg2.storm_summary;
    Basin=upcase(Basin);
    BasinGroup=put(Basin, $region.);
run;
```
- BasinGroup values in the PROC MEANS summary report: **3 groups**.

### Practice (04_1_p) – Level 1: Creating Custom Formats Based on Single Values; Level 2: Based on a Range of Values; Challenge: Based on Nesting Formats [pop-ups not opened – Gap]

## 4.2 Creating Custom Formats from Tables

### Reading a Table of Values for a Format (2:23) – from screenshots
```sas
proc format;
    value $sbfmt
          'AS'='Arabian Sea'
          'BB'='Bay of Bengal'
          'EA'='Eastern Australia'
          'WA'='Western Australia'
          'CP'='Central Pacific'
          'CS'='Caribbean Sea'
          'GM'='Gulf of Mexico'
          'MM'='Missing';
run;
```
- Typing all values is tedious; if they are stored in a table (Sub_Basin = values, SubBasin_Name = labels), read them from the table.
- Input table for a format must have at least three specific columns: **FmtName** (format name; character format names begin with $), **Start** (values left of = in VALUE), **Label** (values right of =). For ranges you also need an **End** column.
- Build it with a DATA step:
```sas
data work.sbdata;
    retain FmtName '$sbfmt';
    set pg2.storm_subbasincodes(rename=(Sub_Basin=Start
                                        SubBasin_Name=Label));
    keep Start Label FmtName;
run;

proc format cntlin=work.sbdata;
run;
```
- RENAME Sub_Basin → Start and SubBasin_Name → Label; RETAIN creates FmtName with the value $sbfmt for every row. work.sbdata has FmtName, Start, Label, one row per Sub_Basin. Then use the **CNTLIN=** option on the PROC FORMAT statement instead of a VALUE statement.

### Demo: Creating Custom Formats from Tables (4:08) – p204d02.sas, from screenshots
- Syntax: `PROC FORMAT CNTLIN=input-table FMTLIB; SELECT format-names; RUN;`
```sas
data sbdata;
    retain FmtName '$sbfmt';
    set pg2.storm_subbasincodes(rename=(Sub_Basin=Start
                                        SubBasin_Name=Label));
    keep Start Label FmtName;
run;

proc format cntlin=sbdata;
run;
```
- Log confirms $SBFMT was created.
- Second format from pg2.storm_categories (Low, High, Category): 74–95 Category 1; 96–110 Category 2; 111–129 Category 3; 130–156 Category 4; 157–high Category 5 → labels based on **ranges**. Mapping: (none) → FmtName = catfmt; Low → **Start**; High → **End**; Category → **Label**.
```sas
data catdata;
    retain FmtName "catfmt";
    set pg2.storm_categories(rename=(Low=Start
                                     High=End
                                     Category=Label));
    keep FmtName Start End Label;
run;

proc format cntlin=catdata;
run;
```
- "This is a numeric format, so it doesn't need a dollar sign in front of the name." Log confirms CATFMT.
```sas
title "Frequency of Wind Measurements for Storm Categories by SubBasin";
title2 "2016 Storms";
proc freq data=pg2.storm_detail;
    /*include only Category 1-5 2016 storms with known subbasin*/
    where Wind>=74 and Season=2016 and
          Sub_basin not in('MM', 'NA');
    tables Sub_basin*Wind / nocol norow nopercent;
    format Sub_basin $sbfmt. Wind catfmt.;
run;
title;
```
- Without formats the crosstab would have a column per unique wind value; with CATFMT the columns are the formatted wind categories (Category 1 through 4 shown).

### Activity (p204a04.sas) – with answer
- Create $SBFMT and CATFMT; uncomment the final PROC FORMAT step (with FMTLIB) → a report for all formats in the WORK library; add `select $sbfmt catfmt;` to limit the report.
- Default length of $SBFMT: "The length of the format matches the length of the longest label. The length of $SBFMT is **17**."

### Storing Custom Formats (1:30) – from screenshot
- `PROC FORMAT LIBRARY=libref<.catalog>;` or `PROC FORMAT LIB=libref<.catalog>;` and `OPTIONS FMTSEARCH=(catalog-specification-1 <catalog-specification-2...>);`
- By default custom formats are stored in the temporary **Work** library in a catalog named **Formats** (a SAS catalog = special SAS file storing different types of information in smaller units called catalog entries).
- `proc format library=pg2.myfmts;` – permanent formats: LIBRARY= (or LIB=) gives a library and catalog name; if only the library is given, SAS uses the default catalog named Formats.
- When SAS encounters a format it looks up the definition; by default it searches the Formats catalog in **WORK** and then, if a library named **Library** exists, the Formats catalog there. If saved elsewhere, tell SAS where with the global OPTIONS statement FMTSEARCH=:
- `options fmtsearch=(pg2.myfmts sashelp);` → searches the Myfmts catalog in PG2 and the Formats catalog in sashelp **after** the default locations Work.Formats and Library.Formats.

### Activity (p204a05.sas) – with answers
1. `proc format library=pg2;` or `proc format library=pg2.formats;`
2. Log shows the two formats created in a permanent location.
3. Before PROC PRINT: `options fmtsearch=(pg2);` or `options fmtsearch=(pg2.formats);`
4. Registration and Height formatted? **Yes**.

### Practice (04_2_p) – Level 1 and Level 2: Creating a Custom Format from a Table; Challenge: Updating a Custom Format by Using the CNTLOUT= Option [pop-ups not opened – Gap]

## 4.3 Lesson Review
- Learning More (link only): create a template for displaying values with PROC FORMAT.

### Summary of Lesson 4 (Lesson Review pop-up; screenshots)
- PROC FORMAT creates custom formats; a VALUE statement specifies criteria for one format; multiple VALUE statements allowed.
- Format name up to **32 characters**; must begin with $ followed by a letter or underscore for character formats; letter or underscore for numeric formats.
- Left of =: individual values or ranges; character values in quotation marks, numeric values not quoted. Right of =: formatted values in quotation marks.
- Keywords **LOW, HIGH, OTHER** can be used in the VALUE statement.
- **No period** in the format name when you create it; **include the period** when you use it.
- Custom formats can be used in the FORMAT statement and the PUT function.
- Creating from tables: `PROC FORMAT CNTLIN=input-table FMTLIB; SELECT format-names; RUN;` – CNTLIN= specifies a table from which PROC FORMAT builds formats. The input table must contain at minimum three **character** columns [as stated]: **Start** (raw values), **Label** (formatted labels), **FmtName** (format name; character formats start with a dollar sign).
- [Remainder of the summary – storing formats – blocked by the filter; content captured above from the lesson pages.]

### Quiz: Lesson 4 (10 questions; read-only, NOT answered or submitted)
1. Which contains valid syntax? a. `value grades 'A'='Excellent' 'B'='Good';` b. `value qtrfmt 1,2,3='First' 4,5,6='Second';` c. `value $grades. 'A'='Excellent' 'B'='Good';` d. `value qtrfmt '1'-'3'='First' '4'-'6'='Second';`
2. Formatted value for 100 given:
```sas
proc format;
    value rates 1-<100='low'
                100<-<200='medium'
                200-300 ='high'
                other ='out of range';
run;
```
   a. low b. medium c. high d. out of range
3. In the FORMAT procedure, you specify the name of the format and the name of the column that will use the custom format. a. True b. False
4. Correct formatted output for Code values 1, 2, 3 given:
```sas
proc format;
    value $answer '1'='Yes'
                  '2'='No'
                  'other'='Not Answered';
run;
```
   a. Yes / No / (blank) b. Yes / No / Not c. Yes / No / 3 d. Yes / No / Not Answered
5. Which does **not** have proper syntax for specifying a range in the VALUE statement? a. `500>-700` b. `500-<700` c. `'A'-'C'` d. `'Horse'-'Mouse'`
6. Which is true concerning options for the FORMAT procedure? a. FMTLIB goes in the SELECT statement. b. CNTLIN= goes in the VALUE statement. c. FMTLIB specifies the library to store the format. d. CNTLIN= specifies a table from which formats are built.
7. Which columns are required in an input table to create a format based on numeric ranges? a. FMTNAME, START, and LABEL b. FORMAT, START, END, and NAME c. FMTNAME, START, END, and LABEL d. FORMAT, START, LAST, NAME, and TYPE
8. Which option in the PROC FORMAT statement specifies a library to store a custom format? a. CATALOG= b. FMTLIB= c. LIBRARY= d. STORE=
9. Default search order used to locate formats? a. LIBRARY.FORMATS > WORK.FORMATS b. SASHELP.FORMATS > LIBRARY.FORMATS c. SASHELP.FORMATS > WORK.FORMATS d. WORK.FORMATS > LIBRARY.FORMATS
10. Valid syntax for the FMTSEARCH= option? a. `options fmtsearch=sashelp;` b. `options fmtsearch=sashelp.formats;` c. `options fmtsearch=(sashelp sashelp.fmts);` d. `options fmtsearch=[sashelp.fmts sashelp];`

## Gaps
- Practices (04_1_p, 04_2_p) open in pop-ups – not opened.
- Part of the Lesson 4 summary blocked by the filter (covered by lesson pages).
- Quiz answers not available (quiz not submitted, by rule).
