# P2 – Lesson 3: Manipulating Data with Functions

Source: SAS Programming 2 player (course id=235), text mode + screenshots. Captured 2026-10-28. Paraphrased; short quotes in quotation marks. Code copied from screenshots.

## 3.0 Lesson Overview
- New functions to manipulate numeric, date and character values; functions that change a column's data type.

## 3.1 Understanding SAS Functions and CALL Routines

### Review of Functions (0:44)
- Syntax forms: `function( );` `function(argument);` `function(argument1, argument2, ...);`
- A SAS function is a named, predefined process that produces a value; accepts none, one or several arguments, performs its computation and **returns a value**. Documentation groups functions and CALL routines by category; this lesson covers Descriptive Statistics, Date and Time, Truncation, Special, Random Number, and Character categories.

### Activity (p203a01.sas) – with answers (screenshot)
1. Why does the DATA step fail? "A function returns a value that must be used in an assignment statement or expression."
2. Fix by overwriting Name in uppercase: `data quiz_summary; set pg2.class_quiz; Name=upcase(Name); ... run;`
3. Mean1, Mean2, Mean3 use different ways to specify a column list as function arguments – same values.
4. Delete OF in Mean2 → "Without the OF keyword, Mean2 is the mean of the difference between Quiz1 and Quiz5": `Mean2=mean(Quiz1-Quiz5);`

### Specifying Column Lists (1:01) – from screenshot
- Column list forms: `col1-coln` (numbered range), `string:` (all columns starting with string), `col--col` (physical range left to right; any names), keywords `_NUMERIC_`, `_CHARACTER_`, `_ALL_`. Usage: `function(of column-list)`; `FORMAT column-list format;`
```sas
data quiz_summary;
    set pg2.class_quiz;
    Name=upcase(Name);
    AvgQuiz=mean(of Q:);
    format Quiz1--AvgQuiz 3.1;
    /*OR*/
    format _numeric_ 3.1;
run;
```
- The FORMAT statement uses a double-dash: all columns from Quiz1 to AvgQuiz get 3.1. **No OF keyword in the FORMAT statement**; OF is required when column lists are **arguments in a function or CALL routine**. `_NUMERIC_` formats all numeric columns; `_CHARACTER_` and `_ALL_` also available.

### Using a CALL Routine to Modify Data (1:25) – JS text + screenshots
- `CALL routine(argument-1 <, ...argument-n>);` – like functions, CALL routines perform a computation or system manipulation, but **do not return a value**; they alter column values or perform other system functions. To modify an argument, arguments **must be column names** – constants and expressions are not valid. Invoked with the CALL statement.
- Original quiz scores: Alfred 8 7 6 9 8; Alice 7 6 4 9 8; Barbara 9 8 7 . 7; Carol 6 5 5 8 8. Goal: drop each student's lowest 2 scores and average the top 3.
```sas
data quiz_report;
    set pg2.class_quiz;
    call sortn(of Quiz1-Quiz5);
    QuizAvg=mean(of Quiz3-Quiz5);
run;
```
- CALL SORTN reorders the numeric values of the argument columns for each row from low to high (values reordered in the existing columns, not new columns). Modified: Alfred 6 7 8 8 9; Alice 4 6 7 8 9; Barbara . 7 7 8 9 (missing sorted first); Carol 5 5 6 8 8. QuizAvg (Quiz3–Quiz5): Alfred 8.33, Alice 8.00, Barbara 8.00, Carol 8.00.

### Activity (p203a02.sas) – with answer
- Use SAS Help (support.sas.com/documentation) to read about CALL MISSING; simplify the step that sets two students' quiz scores to missing:
```sas
data quiz_report;
    set pg2.class_quiz;
    if Name in("Barbara", "James")
        then call missing(of Q:);
run;
```

## 3.2 Using Numeric and Date Functions

### Useful Numeric Functions (1:05)
- Familiar: `SUM(num1, num2, ...)`, `MEAN(num1, num2, ...)`, `YEAR(SAS-date)`, `MONTH(SAS-date)`, `TODAY( )`, `MDY(month, day, year)`.
- New: `RAND('distribution', parameter1, ...parameterk)`, `LARGEST(k, value-1 <, value-2 ...>)`, `ROUND(number <, rounding-unit>)`.
- Goal table: StudentID (random), top 3 quiz scores (Quiz1st, Quiz2nd, Quiz3rd) and Top3Avg (one decimal), e.g., 9860 9 8 8 8.3; 5835 10 10 9 9.7. RAND → random number; LARGEST → top 3 of 5; MEAN and ROUND → average with one decimal.

### Demo: Using Numeric Functions (2:58) – p203d01.sas, from screenshots
```sas
data quiz_analysis;
    StudentID=rand('integer',1000,9999);
    set pg2.class_quiz;
    drop Quiz1-Quiz5 Name;
    Quiz1st=largest(1, of Quiz1-Quiz5);
    Quiz2nd=largest(2, of Quiz1-Quiz5);
    Quiz3rd=largest(3, of Quiz1-Quiz5);
    Top3Avg=round(mean(Quiz1st, Quiz2nd, Quiz3rd), .1);
run;
```
- LARGEST(1, of Quiz1-Quiz5) = largest score; OF references the range. Built step by step: Quiz2nd/Quiz3rd via k = 2, 3; Top3Avg = MEAN of the three; DROP Name for anonymity.
- RAND with `'integer'` as the first argument generates random integers between the 2nd and 3rd arguments (1000–9999 → four-digit ID). Because the assignment is **before SET**, StudentID is the first column added to the PDV and the leftmost column in the output. (Your random values may differ.)
- Top3Avg had a lot of precision → `round(mean(...))` rounds to the nearest integer; adding `.1` as the rounding unit rounds to the nearest tenth.

### Using Numeric Functions to Change Precision
- Truncation functions: **CEIL(number)** – smallest integer ≥ the argument; **FLOOR(number)** – largest integer ≤ the argument; **INT(number)** – the integer value.

### Activity (p203a03.sas) – with answers
- WindAvg1 and WindAvg2 have the same expression. Round WindAvg1 to the nearest tenth: `WindAvg1=round(mean(of Wind1-Wind4), .1);`
- `format WindAvg2 5.1;` – "The values appear the same, but the function changes the stored values, whereas the format affects only the displayed values."

### SAS Date, Datetime, and Time Values (0:53)
- Dates: number of days since January 1, 1960. **Time** value: number of **seconds from midnight**. **Datetime** value: number of **seconds from midnight on January 1, 1960**. Numeric storage enables calculating time between events and sorting.

### Extracting Data from a Datetime Value (0:30) – from screenshot
- `DATEPART(datetime-value)`, `TIMEPART(datetime-value)`
```sas
data storm_detail2;
    set pg2.storm_detail;
    WindDate=datepart(ISO_Time);
    WindTime=timepart(ISO_Time);
    format WindDate date9. WindTime time.;
run;
```
- Only required argument is a datetime value; they return raw SAS date / SAS time values – apply a format for display. Example ISO_Time 10DEC1999:10:00:00.00 → WindDate 10DEC1999, WindTime 10:00:00.

### Calculating Date Intervals (2:01)
- `INTCK('interval', start-date, end-date <, 'method'>)` returns the number of **interval boundaries** of a time period between two dates. Intervals e.g. year, month, week, weekday; optional 4th argument = method.
- Storm 21 July – 31 July 2017: standard week boundary = Sunday–Saturday → 2 end-of-week boundaries (between Jul 22/23 and Jul 29/30). This **discrete** method is the **default**.
- **Continuous** method counts from the start date: the only complete week ends between Jul 27/28. Specify `'C'` (letter C in quotes) as the 4th argument.

### Activity (p203a04.sas) – with answers
- Default discrete method counts weekly boundaries (ending each Saturday) between StartDate and EndDate. Rows 8 and 9: both storms two days, but Weeks differs: "MAARUTHA spans a Saturday/Sunday boundary, and ARLENE was in the middle of a week."
- `Weeks=intck('week', StartDate, EndDate, 'c');` → "Both storms were shorter than seven days, so the value of Weeks is 0."

### Question (03_2_q3) – with answer
- ServiceDate 10JUL2018, PayDate 05SEP2018. `Months2Pay=intck('month', ServiceDate, PayDate);` → **2** (two end-of-month boundaries: end of July and end of August). `intck('month', ServiceDate, PayDate, 'c')` → **1** (one boundary at August 10; the next would be September 10).

### Shifting Date Values (0:50)
- Transactions example: SalesDate 10JUL2018 → BillingDate 01AUG2018; 17JUL2018 → 01AUG2018; 02AUG2018 → 01SEP2018 (shift to the first day of the following month).
- `INTNX('interval', start, increment <, 'alignment'>)` adjusts/shifts dates: interval (week, month, year, many others), start = SAS date column, increment = number of intervals to shift, optional alignment = position of the date within the interval.

### Demo: Shifting Date Values Based on an Interval (3:14) – p203d02.sas, from screenshots
```sas
data storm_damage2;
    set pg2.storm_damage;
    keep Event Date AssessmentDate;
    AssessmentDate=intnx('month', Date, 0);
    format Date AssessmentDate date9.;
run;
```
- Increment 0 → shifted to the **first of the same month** (default alignment = beginning).
- `intnx('month', Date, 2)` → forward two months, still the first of the month.
- `intnx('month', Date, -1, 'end')` → previous month, aligned to the end → last day of the previous month.
- `intnx('month', Date, -1, 'middle')` → all dates the 16th or 15th depending on days in the month (the wanted AssessmentDate).
- Final:
```sas
data storm_damage2;
    set pg2.storm_damage;
    keep Event Date AssessmentDate Anniversary;
    AssessmentDate=intnx('month', Date, -1, 'middle');
    Anniversary=intnx('year', Date, 10, 'same');
    format Date AssessmentDate Anniversary date9.;
run;
```
- Anniversary = same day and month as the storm date, 10 years later ('same' alignment).

### Practice (03_2_p) – Level 1: Using the LARGEST and ROUND Functions; Level 2: Working with Date/Time Values; Challenge: Creating Projected Date Values [pop-ups not opened – Gap]

## 3.3 Using Character Functions

### Useful Character Functions (0:53)
- Familiar: `UPCASE(char)`, `PROPCASE(char, <delimiters>)`, `SUBSTR(char, position <, length>)`. New: functions that remove, replace, find, or concatenate strings.
- Japan precipitation data: Station values inconsistent (JA000047663, JA-000047612, JA 0000 47909 …) → standardize with no spaces or symbols (JA000047612, JA000047909 …).

### Removing Characters from a String
| Function | What it does |
|---|---|
| COMPBL(string) | Converts all multiple blanks to single blanks |
| COMPRESS(string <, characters>) | Removes specified characters from the string |
| STRIP(string) | Removes leading and trailing blanks |

### Activity (p203a06.sas) – with answers (screenshots)
1. `NewLocation=compbl(Location);` – two or more consecutive blanks → single blank.
2. `NewStation=compress(Station);` with Station as the only argument → **blanks are removed**.
3. Second argument with the characters to remove, all in one set of quotes: `NewStation=compress(Station,"- ");`

### Extracting Words from a String (0:58)
- Location holds uppercase city, prefecture, country code ("OWASE, Mie, JA") → create City and Prefecture columns.
- `SCAN(string, n <, 'delimiters'>)` extracts the nth word; optional 3rd argument controls delimiters. `City=scan(Location,1);` → City gets **the same length as Location**.
- Default delimiters: blank ! $ % & ( ) * + , - . / ; < ^ |

### Demo: Using Character Functions to Extract Words from a String (3:16) – p203d03.sas, from screenshots
```sas
data weather_japan_clean;
    set pg2.weather_japan;
    Location=compbl(Location);
    City=scan(Location, 1);
    Prefecture=scan(Location, 2);
run;
```
- Row 8: MIYAKE-JIMA – hyphen is a default delimiter → City = MIYAKE, Prefecture = JIMA. Fix: third argument `','` (comma only) → City MIYAKE-JIMA, Prefecture Tokyo.
- `Country=scan(Location, -1);` – **negative values read from the right**; −1 = last word.
- `City=propcase(scan(Location, 1, ','));` → PROPCASE uses a default delimiter list → "Miyake-Jima" both capitalized; proper is "Miyake-jima". Second argument `' '` (space only):
```sas
data weather_japan_clean;
    set pg2.weather_japan;
    Location=compbl(Location);
    City=propcase(scan(Location, 1, ','), ' ');
    Prefecture=scan(Location, 2, ',');
    Country=scan(Location, -1);
run;
```

### Activity (p203a07.sas) – with answers
1. Subsetting IF keeps only rows where Prefecture is Tokyo → **the output table does not include any rows**.
2. Why is the condition always false (debugger or PUTLOG)? "When the SCAN function extracts Prefecture from Location, only a comma is specified as a delimiter. The leading space is included in the returned value."
3. Fix (four rows returned). Possible solutions: add a space as a delimiter (works if no spaces are embedded in City or Prefecture): `Prefecture=scan(Location, 2, ', ');` or STRIP ("removes leading and training [sic] blanks"): `Prefecture=strip(scan(Location, 2, ','));`

### Searching for Character Strings (0:51) – from screenshot
- `FIND(string, substring <, 'modifiers'>)` searches for a substring; optional modifiers: **"I"** = case-insensitive search, **"T"** = trims leading and trailing blanks. Returns the **start position** of the substring; **0 if not found**.
- `AirportLoc=find(Station, 'Airport');` – case-sensitive search. Raleigh Durham Airport → 16; Airport Road → 1; Cary Parkway → 0.

### Activity (p203a08.sas) – with answers
- CategoryLoc uses FIND to search for "category" in Summary. Why 0 in row 1? "Lowercase category is not found in row 1." Row 15? "The word category is not found in row 15 at all."
- Case-insensitive + uncomment IF-THEN:
```sas
data storm_damage2;
    set pg2.storm_damage;
    drop Date Cost;
    CategoryLoc=find(Summary, 'category', 'i');
    if CategoryLoc > 0 then
        Category=substr(Summary, CategoryLoc, 10);
run;
```
   "The SUBSTR function starts at the number stored in CategoryLoc and reads 10 characters, and returns the string to Category."

### Identifying Character Positions
| Function | What it does |
|---|---|
| LENGTH(string) | Length of a non-blank string, excluding trailing blanks; returns 1 for a completely blank string |
| ANYDIGIT(string) | First position at which a digit is found |
| ANYALPHA(string) | First position at which an alpha character is found |
| ANYPUNCT(string) | First position at which a punctuation character is found |

### Replacing Character Strings (0:27) – from screenshot
- `TRANWRD(source, target, replacement)` – find and replace: `Summary2=tranwrd(Summary, 'hurricane', 'storm');` replaces all instances of lowercase "hurricane" with "storm" ("Category 3 hurricane initially..." → "Category 3 storm initially...").

### Building Character Strings
| Function | What it does |
|---|---|
| CAT(string1, ... stringn) | Concatenates; does **not** remove leading or trailing blanks |
| CATS(string1, ... stringn) | Concatenates; removes leading/trailing blanks from each string |
| CATX('delimiter', string1, ... stringn) | Concatenates; removes leading/trailing blanks from each string and inserts the delimiter between strings |
- Arguments can be character or standard numeric values.

### Activity (p203a09.sas) – with answers
1. StormID1 (CAT) vs StormID2 (CATS): CAT keeps trailing blanks after Name in the concatenated string; CATS removes them.
2. `StormID3=catx("-", Name, Season, Day);`
3. Hyphen only between Name and Season: `StormID2=cats(Name, '-', Season, Day);`

### Practice (03_3_p) – Level 1: Using the SCAN and PROPCASE Functions; Level 2: Searching for Character Strings; Challenge: Determining the Maximum Length of a Column [pop-ups not opened – Gap]

## 3.4 Using Special Functions to Convert Column Type

### Handling Column Type (0:35)
- Columns are character or numeric; arithmetic needs numeric values, character functions (SUBSTR, SCAN) need character values. What if the column isn't the proper type?

### Activity (p203a10.sas) – with answers
1. PROC CONTENTS: **High and Volume are character, Low is numeric.**
2. Range (High − Low) is calculated accurately even though High is character. Log note: "NOTE: Character values have been converted to numeric values at the places given by: (Line):(Column). 75:10"
3. Uncomment DailyVol: created successfully? **No, DailyVol is missing for all rows.**

### Converting Column Type (1:18) – from screenshots
- `Range = High-Low;` – arithmetic on a character value → SAS **automatically attempts to convert** the values for evaluating the expression; works for High because it contains only standard numeric values (digits and decimal points). E.g., 89.92 − 81.56 = 8.36.
- `DailyVol = Volume/30;` – Volume values include **commas** (5,025,627) → cannot be interpreted as standard numeric → written as **missing** in the automatic conversion.
- Similarly a numeric column in a character expression → SAS attempts numeric→character conversion; might work or give unexpected results.
- `INPUT(source, informat)` converts character → numeric using an informat (how to read the string). `PUT(source, format)` converts numeric → character using a format (how to write the values).

### Converting Character Values to Numeric Values (1:33) – from screenshots
- Stock Prices: Date character (01DEC2017 …) → `Date2=input(Date,date9.);` → 21154, 21124, 21094, 21063.
- INPUT has two arguments: source column, informat (tells SAS how the data is displayed so it can read it).

| Character value | Informat | Numeric value |
|---|---|---|
| 15OCT2018 | DATE9. | 21472 |
| 10/15/2018 | MMDDYY10. | 21472 |
| 15/10/2108 [as shown] | DDMMYY10. | 21472 |
| 123,456.78 | COMMA12. | 123456.78 |
| $123,456.78 | DOLLAR12. | 123456.78 |
| 123456 | 6. | 123456 |

- Width must accommodate all characters in the value. If the value has a decimal point, no decimal value is needed in the informat. If you use a decimal value in the informat when no decimal point is present, SAS **inserts a decimal point** at that position.
```sas
data work.stocks2;
    set pg2.stocks2;
    NewVolume1=input(Volume,comma12.);
    NewVolume2=input(Volume,comma12.2);
    keep volume newvolume:;
run;
```
- Volume 5,976,252 → NewVolume1 5976252, NewVolume2 59762.52. No NOTE/WARNING/ERROR (intended result of the decimal in the informat) but NewVolume2 is not an accurate conversion.

### Using a Generic Informat to Read Dates (1:33)
- **ANYDTDTEw.** reads many date layouts: 15OCT2018, 10/15/2018, 10152018, 20181015, Oct 15, 2018, October 15, 2018 → all 21472.
- Why not always use it? Takes a bit longer to process; you may prefer a specific informat to ensure dates follow a designated layout. Useful when the incoming date format is unknown or mixed.
- Ambiguous dates (6/1/2018): SAS uses the **DATESTYLE=** system option to decide month/day/year order. Default DATESTYLE = LOCALE (based on the LOCALE= option); LOCALE English → MDY → 6/1 = June 1st. An OPTIONS statement with DATESTYLE=DMY → 6/1 read as January 6th.

### Activity (p203a11.sas) – with answers (screenshots)
1. Date2 created as numeric; table has a character column Volume.
2. `Volume2=input(Volume,comma12.);` → numeric.
3. Change to `Volume=input(Volume,comma12.);` to update the existing column.
4. Volume is still character – why? "Volume cannot be in the PDV as both numeric and character. The character attribute of Volume from the SET statement is controlling the column type."

### Converting the Type of an Existing Column (1:46) – from screenshots
- PDV after SET: Stock $12, Date $9, Open N8, Close N8, High $6, Low N8, Volume $12, Date2 N8. The assignment cannot change Volume to numeric because it's already established (like LENGTH cannot change a length once set). Three steps:
```sas
data work.stocks2;
    set pg2.stocks2(rename=(Volume=CharVolume));
    Date2=input(Date,date9.);
    Volume=input(CharVolume,comma12.);
    drop CharVolume;
run;
```
1. RENAME= data set option on SET (current name on the left, new name on the right; outer parentheses surround all data set options, inner parentheses surround the columns being renamed) → CharVolume added to the PDV as character.
2. Assignment with INPUT using the renamed column; the original name on the left → Volume added to the PDV as numeric (PDV: … CharVolume $12, Date2 N8, Volume N8).
3. DROP the renamed column.

### Question (03_4_q3) – interactive "Check My Answer"; not clicked on the site
- Which statement renames the existing column Product in sashelp.shoes as Type? a. `set sashelp.shoes rename=(Type=Product);` b. `set sashelp.shoes(rename=(Type=Product));` c. `set sashelp.shoes(rename(Product=Type));` d. `set sashelp.shoes(rename=(Product=Type));`
- **Derived answer: d** [DERIVED – not confirmed on the site]. Basis: "Converting the Type of an Existing Column" above – RENAME= goes in parentheses after the table name, "current name on the left, new name on the right", outer parentheses around all data set options and inner parentheses around the renamed columns (`set pg2.stocks2(rename=(Volume=CharVolume));`). a: no parentheses around the option; b: names reversed; c: missing `=` after RENAME.

### Converting Numeric Values to Character Values (1:02) – from screenshots
- `PUT(source, format)` – first argument = numeric column to convert, second = format telling SAS how to display the new character value.
- `Day=put(Date,downame3.);` – numeric Date 21154 → "Fri" (21124 Wed, 21094 Mon, 21063 Fri): first three letters of the weekday via DOWNAME3.
- Formats in PUT work like display formats; specify format, width and decimals:

| Numeric value | Format | Character value |
|---|---|---|
| 21472 | DATE9. | 15OCT2018 |
| 21472 | DOWNAME3. | Mon |
| 21472 | YEAR4. | 2018 |
| 123456.78 | COMMA10.2 | 123,456.78 |
| 123456.78 | DOLLAR11.2 | $123,456.78 |
| 123.456 | 6.2 | 123.46 |

### Demo: Using the INPUT Function to Convert Column Types (7:09) – p203d04.sas, from screenshots
- Syntax pattern: `DATA output-table; SET input-table (RENAME=(current-column=new-column)); ... column1 = INPUT(source, informat); column2 = PUT(source, format); ... RUN;`
- weather_atlanta: Date and Precip stored as character; some Precip rows = **T** (trace value: very small precipitation, no measurable accumulation).
```sas
data atl_precip;
    set pg2.weather_atlanta;
    where AirportCode='ATL';
    drop AirportCode City Temp: ZipCode;
    TotalPrecip+Precip;
run;
```
- Log: "character values have been converted to numeric values at the places given by" (line 77). SAS converts character Precip with the **w. informat**; succeeds for legitimate numbers like .27, fails for T → missing. TotalPrecip is still correct (sum statement ignores missing).
- Better: explicit conversion:
```sas
data atl_precip;
    set pg2.weather_atlanta(rename=(Date=CharDate));
    where AirportCode='ATL';
    drop AirportCode City Temp: ZipCode Precip CharDate;
    if Precip ne 'T' then PrecipNum=input(Precip,6.);
    else PrecipNum=0;
    TotalPrecip+PrecipNum;
    Date=input(CharDate,mmddyy10.);
    format Date date9.;
run;
```
- With IF-THEN/ELSE + INPUT the log no longer has the conversion note nor notes about invalid numeric data for Precip='T'. Result: numeric precipitation column and numeric date column.

### Demo: Using the PUT Function to Convert Column Types (3:39) – from screenshots
```sas
data atl_precip;
    set pg2.weather_atlanta;
    CityStateZip=catx(' ',City,'GA',ZipCode);
run;
```
- ZipCode is numeric; CATX with ' ' concatenates, removes leading/trailing blanks, inserts a single space. "The CAT functions automatically convert numeric values to character values, and removes leading and trailing blanks in the converted value." **No note** in the log for CAT-function conversions.
- `ZipCodeLast2=substr(ZipCode, 4, 2);` → log note numeric→character conversion; ZipCodeLast2 is **missing**: automatic numeric→character conversion uses the **BEST12.** format, right-aligned → 30320 becomes seven leading spaces followed by 30320.
- Fix with PUT:
```sas
data work.weather_atlanta;
    set pg2.weather_atlanta;
    CityStateZip=catx(' ',City,'GA',ZipCode);
    ZipCodeLast2=substr(put(ZipCode,z5.), 4, 2);
run;
```
- The **Z format** writes a number as a character string with leading zeros if necessary to fill 5 positions → last two digits displayed correctly.

### Activity (p203a13.sas) – with answer
```sas
data work.stocks2;
    set pg2.stocks2(rename=(Volume=CharVolume Date=CharDate));
    Volume=input(CharVolume,comma12.);
    Date=input(CharDate,date9.);
    drop Char:;
run;
```
- Rename Date to CharDate (values like 01JAN2018), create numeric Date with INPUT/DATE9., drop all columns beginning with Char (`Char:`); Volume and Date are numeric.

## 3.5 Lesson Review
- Learning More (links only): questions to other SAS programmers; data cleaning techniques; Perl regular expressions; more function examples.

### Summary of Lesson 3 (Lesson Review pop-up; JS text, one chunk blocked)
- `function(argument1, argument2, ...);` `CALL routine(argument-1 <, ...argument-n>);`
- RAND generates random numbers from a selected distribution; 'INTEGER' as first argument → uniformly distributed random integer between the 2nd and 3rd arguments (lower/upper limits).
- LARGEST returns the **kth largest nonmissing** value (first argument = k). There is also a **SMALLEST** function (kth smallest nonmissing value).
- ROUND rounds the first argument to the nearest integer; optional second argument = rounding unit.
- CEIL / FLOOR / INT truncate decimal values (definitions as above). DATEPART / TIMEPART extract date/time from a datetime. INTCK counts intervals ('C' = continuous). INTNX shifts dates.
- COMPBL / COMPRESS / STRIP remove characters. SCAN returns the nth word; **negative n reads from the right**; default delimiters blank ! $ % & ( ) * + , - . / ; < ^ |; optional 3rd argument = delimiter list in a single set of quotation marks.
- **PROPCASE** converts all uppercase letters to lowercase, then uppercases the first character of each word; **default delimiters: blank / - ( . tab**; optional 2nd argument = delimiter list in one set of quotes.
- FIND; LENGTH / ANYDIGIT / ANYALPHA / ANYPUNCT; TRANWRD; CAT / CATS / CATX.
- "The INPUT function converts a character value to a numeric value using a specified informat. SAS automatically tries to convert character values to numeric values using the **w.** informat."
- "The PUT function converts a numeric or character value to a character value using a specified format. SAS automatically tries to convert numeric values to character values using the **BEST12.** format."
- If SAS converts automatically, a **note** is displayed in the log; if you explicitly convert with a function, **no note**.
- CAT functions automatically convert numeric→character and remove leading blanks on the converted data; no note in the log.

### Quiz: Lesson 3 (10 questions; read-only, NOT answered or submitted)
1. Functions and CALL routines both return a value that must be used in an assignment statement or expression. a. True b. False
2. Which function calculates the average of Week1, Week2, Week3, Week4? a. `mean(Week1, Week4)` b. `mean(Week1-Week4)` c. `mean(of Week1, Week4)` d. `mean(of Week1-Week4)`
3. Which expression rounds Sales to the nearest hundredth? a. `round(Sales)` b. `round(Sales, 2)` c. `round(Sales, .01)` d. `round(Sales, dollar10.2)`
4. Which function could remove the non-numeric symbols in Phone (202-555-0190, 202.555.0110, (202)555-0133, [202]555-0128)? a. COMPRESS b. COMPBL c. SCAN d. FIND
5. Which statement reads CityCountry and correctly assigns Country? (CityCountry "Athens, Greece" → Country "Greece"; "New Delhi, India" → "India"; "Auckland, New Zealand" → "New Zealand") a. `Country=scan(CityCountry, 2);` b. `Country=scan(CityCountry, -1);` c. `Country=scan(CityCountry, 2, ',');` d. `Country=scan(CityCountry, 2, ', ');`
6. Which expression creates CityCountry from City and Country (Athens + Greece → "Athens, Greece")? a. `cat(City, ", ", Country)` b. `cats(", ", City, Country)` c. `catx(City, ", ", Country)` d. `catx(", ", City, Country)`
7. How many rows are written by `if find(Location, "Oahu", "i") > 0 then output;` for Location = Honolulu, Oahu / Kaanapali, Maui / Hilo, Hawaii / kailua, oahu / LAIE, OAHU? a. 0 b. 1 c. 3 d. 5
8. Which function converts the numeric Level to character values? a. `put(Level, 3.)` b. `put(3., Level)` c. `input(3., Level)` d. `input(Level, 3.)`
9. Which converts the character values of Base to numeric? a. `put(comma10.2, Base)` b. `put(Base, comma10.2)` c. `input(Base, comma10.2)` d. `input(comma10.2, Base)`
10. Which step is **not required** when converting a character column Date to a numeric SAS date column with the same name? a. Rename Date to a new name, such as CharDate. b. Use INPUT to read CharDate and create numeric Date. c. Specify an appropriate informat in INPUT. d. Format the new numeric Date column.

## Gaps
- Practices (03_2_p, 03_3_p) open in pop-ups – not opened.
- Question 03_4_q3 is interactive ("Check My Answer") – not clicked; answer derived from lesson content (marked [DERIVED]).
- One chunk of the Lesson 3 summary (CATX row + syntax box) blocked by the filter; content duplicated in the lesson pages above.
- Quiz answers not available (quiz not submitted, by rule).
