# CR – Lesson 4: Preparing World Tourism Data – Case Study

Source: Certification Review player (id=238), text mode transcripts + text pages. Captured 2026-10-28. Paraphrased; short quotes in quotation marks.

## 4.0 Introduction and Requirements

### Case Study Overview: Preparing World Tourism Data (video 6:09)
- Role: prepare data for analysts (reports, visualizations, models). Two tables + requirements → prepare 2014 inbound/outbound tourism data for countries and continents.
- Deliverables (3 tables): **cleaned_tourism** (restructured tourism table), **final_tourism** (cleaned_tourism merged with country_info, matching rows only), **nocountryfound** (distinct list of countries with no match in country_info).
- **tourism** table: arrivals of non-resident visitors, departures, tourism expenditure (in the country and in other countries); raw data from the UN data website. **23 columns, over 2,400 rows.** Outbound tourism = residents traveling abroad (departures, expenditure in US$); inbound = visitors arriving (arrivals, expenditure in US$).
  - Column **A**: numeric ID when a country name appears in Country. **Country** mixes country names, tourism type (inbound/outbound) and category (arrivals, departures, expenditure…). **Series**: data collection method (e.g., IMF = International Monetary Fund). **_1995–_2014**: scaled numeric data stored as **text**. Expenditure values are US$ **millions**; arrivals/departures are in **thousands** (e.g., 21,719 thousand → 21,719,000).
- **country_info**: 2 columns, 250 rows – Continent (ID: 1 North America, 2 South America, …) and Country (name).
- Data preparation often takes ~80% of analysts' time. Program will: retain values across iterations, use functions, conditionally create columns, create and apply a custom format, remove and format columns, merge tables.

### View the Case Study Data (video 0:43)
- Read requirements and explore first. Country holds everything; when A has a value, Country has a country name (4 Afghanistan, 8 Albania, 12 Algeria, …). Many year columns are not needed.

### Possible Approaches / Essential Case Study Documents (text)
- Same approach options as Lesson 2 (requirements doc, Assignment Guide, Hints, Solutions). Documents: Data Information, Requirements, Assignment Guide (requirements sorted into steps for the 3 tables) [PDFs not opened].

## 4.1 Case Study Hints (revealed with "Show Answer")
- **Cleaned_Tourism Pt1:** redefine cr if needed (run the libname program); read cr.tourism → cr.cleaned_tourism; remove _1995–_2013 (DROP statement or DROP= option); create Country_Name and Tourism_Type ("Inbound tourism"/"Outbound tourism") from Country; remove rows that contain only the country name or tourism type. Hints: A has a value when Country is a country name → IF-THEN assigns Country to Country_Name; define Country_Name explicitly (length); value must appear on every row; IF-THEN for Tourism_Type, defined explicitly and written to every row; **subsetting IF** to drop rows where Country equals Country_Name or Tourism_Type.
- **Pt2:** Series → uppercase and ".." → missing character value; determine conversion type (Mn or Thousands) for the new Y2014 column (a helper column is easiest – last word of Country, extracted with functions, dropped later); in _2014 change ".." to a single period.
- **Pt3:** Y2014 = explicit character→numeric conversion of _2014 × conversion factor (1,000 or 1,000,000), only when there is a value (else missing) – IF-THEN-DO by conversion type; Category from Country with valid values: Arrivals; Departures; Passenger Transport - US$; Tourism expenditure in other countries - US$; Tourism expenditure in the country - US$; Travel - US$. Permanently format Y2014 with COMMA. Keep only Country_Name, Tourism_Type, Category, Series, Y2014.
- **Final_Tourism:** custom format for Continent: 1 North America, 2 South America, 3 Europe, 4 Africa, 5 Asia, 6 Oceania, 7 Antarctica. Merge cleaned_tourism with a sorted country_info, matches only; apply the format. Hints: PROC FORMAT; DATA step merge – both inputs sorted by the BY column and BY column names must be the same; IN= data set option + IF-THEN to output matches; FORMAT statement.
- **NoCountryFound:** one row per country in Cleaned_Tourism not found in country_info. Hint: in the same merge, output rows from cleaned_tourism with no match in country_sorted **and** the first time the country appears – BY statement + FIRST./LAST. variables.

## 4.2 Case Study Solutions

### Solution: Cleaned_Tourism Table, Pt1 (video 6:20)
- DATA cleaned_tourism; SET tourism with **DROP=** data set option for unneeded year columns (dropped from the PDV entirely since never needed).
- Country_Name: LENGTH statement **before SET** (so it becomes the first column); **RETAIN** Country_Name (initialized missing) so the value carries across iterations until changed; `if A ne . then Country_Name=Country;` [transcript says "RETURN statement" at one point – means RETAIN].
- Tourism_Type: LENGTH + RETAIN; `if lowcase(Country)="inbound tourism" then Tourism_Type="Inbound tourism"; else if lowcase(Country)="outbound tourism" then …` (LOWCASE guards against case issues).
- Rows where the original Country equals the new column values (header rows, e.g., row 1 Afghanistan, rows 2 and 7) removed with a **subsetting IF**: `if Country_Name ne Country and Country ne Tourism_Type;` – both true → continue; either false → return to the top of the DATA step (row not output).

### Solution: Cleaned_Tourism Table, Pt2 (video 6:12)
- `Series=upcase(Series);` `if Series=".." then Series="";` (missing character).
- `Conversion_Type=scan(Country, -1, " ");` – **−1 = last word**; values "Thousands" or "Mn". Validate with PROC FREQ on Country_Name, Tourism_Type, Series, Conversion_Type: Tourism_Type only Inbound/Outbound; Series all uppercase with **318** missing; Conversion_Type only Thousands or Mn.
- `if _2014=".." then _2014=".";` (still character; converted in Pt3).

### Validate the Cleaned_Tourism Table (text) – PROC FREQ and compare to "Validation Results for Part 2" [PDF not opened].

### Solution: Cleaned_Tourism Table, Pt3 (video 9:36)
- `if Conversion_Type="Mn" then do;` – nested `if _2014 ne "." then Y2014=input(_2014, …)*1000000; else Y2014=.;` [informat not in transcript]. Assigning missing directly avoids the log note "Missing values were generated as a result of performing an operation on missing values" that converting a character period with INPUT would cause. Row 2: 91 → 91,000,000.
- Category (inside the DO): `scan(Country, 1, "-", "r")` – first word with hyphen as delimiter; the **"r" modifier removes leading and trailing blanks** (like STRIP); then **CAT** to append " - US$" per the requirements. `end;`
- `else if Conversion_Type="Thousands" then do;` – same, × 1,000, and Category is just the first part (Arrivals/Departures, no CAT).
- FORMAT Y2014 **COMMA25.**; DROP A, Conversion_Type, Country, _2014.
- Validation: PROC FREQ on Category (6 values), Tourism_Type (2), Series (7 distinct values, 318 missing); PROC MEANS on Y2014 with MIN MEAN MAX MAXDEC=0 (validation only – mixes people and dollars, so no dollar format).

### Validate the Final Cleaned_Tourism Table (text) – compare with "Validation Results" [PDF not opened].

### Solution: Final_Tourism Table (video 5:46)
- `PROC FORMAT; VALUE contIDs 1="North America" … 7="Antarctica"; RUN;` (log confirms the format).
- Merge prerequisites: sorted inputs and same BY column name. Cleaned_Tourism already sorted. PROC SORT country_info OUT=**Country_Sorted** with **RENAME=**(Country=Country_Name), BY Country_Name.
- `DATA Final_Tourism; MERGE Cleaned_Tourism(in=t) Country_Sorted(in=c); BY Country_Name; if t=1 and c=1 then output; FORMAT Continent contIDs.;` → log: **1,724 observations and 6 columns**.
- Validation: PROC FREQ with **NLEVELS** option (number of distinct levels, missing/non-missing levels) on Category, Series, Tourism_Type, Continent with NOCUM NOPERCENT; Continent shows formatted names (North America, South America, Europe, Africa, Asia, Oceania – no Antarctica). PROC MEANS MIN MEAN MAX MAXDEC=0 on Y2014.

### Validate the Final_Tourism Table (text) – compare with "Validation Results" [PDF not opened].

### Solution: NoCountryFound Table (video 3:11)
- Add `NoCountryFound(keep=Country_Name)` to the same DATA statement. `if t=1 and c=0 then output NoCountryFound;` → repeated countries; add `and first.Country_Name=1` → distinct list. Log: Final_Tourism 1,724 rows; NoCountryFound **9** countries.

## 4.3 Test Your Solution
- "Test Your Case Study Output Table" (text + questions; read-only): recreate final_tourism if needed; analyze 2014 arrivals per continent with mean, min, max rounded to whole numbers. Q: which continent has the highest average arrivals for 2014? Modify to give the overall mean (rounded) of tourism expenditure in other countries. Q: overall mean tourism expenditure in other countries for 2014? [answers revealed with "Show Answer"; read from screenshot]
  - Answer 1: **Europe** – "The mean number of arrivals in Europe was 10,540,377 in 2014."
```sas
proc means data=cr.final_tourism mean min max maxdec=0;
        var y2014;
        class Continent;
        where Category="Arrivals";
run;
```
  - Answer 2: **7,577,413,333**
```sas
proc means data=cr.final_tourism mean maxdec=0;
        var y2014;
        where lowcase(Category) contains "tourism expenditure in other countries";
run;
```

## Gaps
- Case study PDFs (Data Information, Requirements, Assignment Guide, three Validation Results) not opened.
- Demo code visible only in video (exact informat in Pt3 INPUT call not stated).
