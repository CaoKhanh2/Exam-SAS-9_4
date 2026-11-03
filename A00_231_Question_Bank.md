# A00-231 Question Bank – SAS 9.4 Base Programming (Performance-Based)

60 questions aligned to the A00-231 exam weights. Questions and options are in English; explanations are in Vietnamese.

| Domain | Questions | Share |
|---|---|---|
| 1. Access and Create Data Structures | Q1–Q14 (14) | ~23% |
| 2. Manage Data | Q15–Q37 (23) | ~38% |
| 3. Error Handling | Q38–Q48 (11) | ~18% |
| 4. Generate Reports and Output | Q49–Q60 (12) | ~20% |

**Question types:** MC = multiple choice (4 options, one correct) · PBQ = performance-based (run or edit code, type the result).

**Context:** the repository has no `.sas` or `.ipynb` files. The scenarios reuse the data themes from the course notes in `raw/` (storm, basin and weather tables from SAS Programming 2 and the Certification Review).

---

## Shared setup – run this first for every PBQ

```sas
data storms;
    length Name $ 10 Basin $ 2;
    input Name $ Basin $ Season MaxWind;
    datalines;
ANA NA 2021 45
BILL NA 2021 60
CLAUDETTE NA 2021 45
ANA NA 2022 40
DORA EP 2021 80
ENRIQUE EP 2021 95
FELICIA EP 2021 145
BLANCA EP 2022 60
;
run;

data basins;
    input Basin $ BasinName $;
    datalines;
EP Pacific
NA Atlantic
WP WPacific
;
run;
```

---

## Domain 1 – Access and Create Data Structures

### Question 1: D1 – Permanent tables and LIBNAME
The following statement has been submitted:

```sas
libname pg2 "s:/workshop/data";
```

Which DATA statement creates a **permanent** table?

- A. `data storm_new;`
- B. `data work.storm_new;`
- C. `data pg2.storm_new;`
- D. `data pg2-storm_new;`

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** Bảng lưu vĩnh viễn phải có tiền tố là libref trỏ tới một thư mục thật (`pg2.`). A và B đều ghi vào thư viện WORK, bị xóa khi kết thúc phiên SAS. D sai cú pháp vì phải dùng dấu chấm, không dùng gạch ngang.
</details>

---

### Question 2: D1 – PROC CONTENTS
What does the VARNUM option change in this report?

```sas
proc contents data=pg2.storm_summary varnum;
run;
```

- A. It lists only the numeric columns.
- B. It lists the columns in their logical position (creation order) instead of alphabetical order.
- C. It suppresses the descriptor portion of the table.
- D. It prints the first 10 rows of data.

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** Mặc định PROC CONTENTS liệt kê cột theo thứ tự chữ cái; VARNUM liệt kê theo đúng thứ tự cột trong bảng (case study TSA dùng cách này). A sai vì VARNUM không lọc theo kiểu dữ liệu. C là việc của NODS khi dùng với `_ALL_`. D sai vì PROC CONTENTS không in dữ liệu.
</details>

---

### Question 3: D1 – PROC IMPORT (CSV, GETNAMES)
Which statement, placed in the blank, tells PROC IMPORT to read the column names from the first row of the CSV file?

```sas
proc import datafile="&path/storm_damage.csv"
            dbms=csv out=storm_damage replace;
    __________;
run;
```

- A. `getnames=yes`
- B. `datarow=1`
- C. `header=yes`
- D. `namerow=0`

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** `GETNAMES=YES` lấy dòng đầu tiên làm tên cột (với CSV đây là giá trị mặc định). B: `DATAROW=1` nghĩa là đọc dữ liệu ngay từ dòng 1, tức coi dòng tiêu đề là dữ liệu. C và D không phải câu lệnh hợp lệ của PROC IMPORT.
</details>

---

### Question 4: D1 – PROC IMPORT (REPLACE, GUESSINGROWS)
The table `work.storm_damage` already exists. A programmer submits:

```sas
proc import datafile="&path/storm_damage.csv"
            dbms=csv out=storm_damage;
    guessingrows=max;
run;
```

What happens?

- A. The table is overwritten, and every row is used to determine column types.
- B. The import is cancelled, and the log says that the output data set already exists and that REPLACE must be specified.
- C. The new rows are appended to the existing table.
- D. An ERROR occurs because GUESSINGROWS= requires REPLACE.

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** Thiếu REPLACE thì PROC IMPORT không ghi đè bảng đã có: log ghi NOTE "Import cancelled… already exists. Specify REPLACE option to overwrite it." A chỉ đúng khi có REPLACE. C sai vì PROC IMPORT không bao giờ nối thêm dòng. D sai vì GUESSINGROWS=MAX (quét mọi dòng để xác định kiểu cột) không phụ thuộc REPLACE.
</details>

---

### Question 5: D1 – PROC IMPORT (XLSX)
Which step imports only the worksheet named **Parks** from `np_info.xlsx`?

- A.
```sas
proc import datafile="&path/np_info.xlsx" dbms=csv out=parks replace;
    sheet=Parks;
run;
```
- B.
```sas
proc import datafile="&path/np_info.xlsx" dbms=xlsx out=parks replace;
    getnames=Parks;
run;
```
- C.
```sas
proc import datafile="&path/np_info.xlsx" dbms=xlsx out=parks replace;
    sheet=Parks;
run;
```
- D.
```sas
proc import datafile="&path/np_info.xlsx" dbms=xlsx out=parks replace;
    datarow=Parks;
run;
```

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** Đọc file Excel cần `DBMS=XLSX`; câu lệnh `SHEET=` chọn sheet cần nhập. A dùng sai DBMS (CSV). B sai vì GETNAMES chỉ nhận YES hoặc NO. D sai vì DATAROW nhận số thứ tự dòng, không nhận tên sheet.
</details>

---

### Question 6: D1 – SAS/ACCESS XLSX engine
Consider:

```sas
libname np xlsx "&path/np_info.xlsx";

proc print data=np.parks;
run;

libname np clear;
```

Which statement is true?

- A. `np.parks` refers to the worksheet named Parks, and `LIBNAME np CLEAR` releases the connection to the workbook.
- B. `np.parks` is a SAS7BDAT file that the XLSX engine created in the same folder.
- C. `LIBNAME np CLEAR` deletes the workbook.
- D. The XLSX engine can read only the first worksheet.

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** Với engine XLSX, mỗi worksheet hiện ra như một bảng trong thư viện, và CLEAR gỡ libref để giải phóng workbook. B sai vì engine đọc thẳng file Excel, không tạo file SAS7BDAT. C sai vì CLEAR không xóa file. D sai vì mọi worksheet đều truy cập được.
</details>

---

### Question 7: D1 – Concatenation and column attributes (PBQ)
Run the code below.

```sas
data codes_a;
    length Code $ 3;
    input Code $ Rate;
    datalines;
NA1 1.5
EP2 2.0
;
run;

data codes_b;
    length Code $ 5;
    input Code $ Rate;
    datalines;
WP303 3.5
;
run;

data codes_all;
    set codes_a codes_b;
run;
```

What value of **Code** is stored in row 3 of `codes_all`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: WP3**

**Giải thích:** Khi ghép bảng bằng SET, thuộc tính cột lấy theo bảng đứng **đầu tiên** trong câu lệnh SET, nên Code có độ dài 3 và "WP303" bị cắt còn "WP3". Log có WARNING "Multiple lengths were specified…". Cách sửa: đặt `length Code $ 5;` **trước** câu lệnh SET.
</details>

---

### Question 8: D1 – One-to-many merge (PBQ)
Using `storms` and `basins` from the setup, sort as needed and merge the two tables by **Basin** without IN= variables or subsetting.

How many rows are in the output table? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 9**

```sas
proc sort data=storms out=storms_sort;
    by Basin;
run;

data storm_names;
    merge storms_sort basins;
    by Basin;
run;
```

**Giải thích:** Đây là merge một-nhiều. Mặc định DATA step merge ghi **cả dòng khớp lẫn không khớp**: EP có 4 dòng, NA có 4 dòng, và WP (chỉ có trong `basins`) thêm 1 dòng, tổng 9. Bảng `storms` phải được sort theo Basin trước khi merge; `basins` vốn đã theo thứ tự EP, NA, WP.
</details>

---

### Question 9: D1 – Merge with IN= (non-matches)

```sas
data unused_basins;
    merge storms_sort(in=inS) basins(in=inB);
    by Basin;
    __________;
run;
```

Which statement keeps only the basins that have **no** matching storm?

- A. `if inS=1 and inB=1;`
- B. `where inB=1 and inS=0;`
- C. `if inS=1 or inB=1;`
- D. `if inB=1 and inS=0;`

<details><summary>Answer & explanation</summary>

**Answer: D**

**Giải thích:** Biến IN= bằng 1 khi bảng tương ứng có giá trị BY của dòng đó, nên dòng chỉ có ở `basins` là `inB=1` và `inS=0`. B sai vì biến IN= chỉ tồn tại trong PDV lúc thực thi, mà WHERE chỉ dùng được cột của bảng đầu vào. A chỉ giữ các dòng khớp. C giữ mọi dòng.
</details>

---

### Question 10: D1 – SAS date values (PBQ)
What numeric value does SAS store for the date constant `'31DEC1959'd`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: -1**

**Giải thích:** Giá trị ngày của SAS là số ngày tính từ 01JAN1960 (bằng 0). Ngày trước mốc này có giá trị âm, nên 31DEC1959 bằng -1.
</details>

---

### Question 11: D1 – Informats vs formats
The character column `DateC` contains values such as `15/10/2018` (day/month/year). Which expression creates a numeric SAS date?

- A. `input(DateC, mmddyy10.)`
- B. `input(DateC, ddmmyy10.)`
- C. `put(DateC, ddmmyy10.)`
- D. `input(DateC, date9.)`

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** INPUT dùng **informat** để đọc chuỗi ký tự thành số, và DDMMYY10. khớp với dạng ngày/tháng/năm. A đọc theo tháng/ngày/năm, nên tháng 15 không hợp lệ và kết quả là missing. C sai vì PUT trả về ký tự. D sai vì DATE9. dành cho dạng 15OCT2018.
</details>

---

### Question 12: D1 – WHERE operators
Which WHERE statement selects storms whose Name **begins with** the letter B?

- A. `where Name like 'B_';`
- B. `where Name = 'B*';`
- C. `where Name like 'B%';`
- D. `where Name contains 'B%';`

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** Trong LIKE, `%` thay cho bất kỳ chuỗi ký tự nào (kể cả rỗng), còn `_` thay cho đúng một ký tự. A chỉ khớp tên dài đúng 2 ký tự. B so sánh với chuỗi "B*" theo nghĩa đen. D tìm chuỗi con "B%" theo nghĩa đen.
</details>

---

### Question 13: D1 – DROP= and KEEP= data set options (PBQ)
Run:

```sas
data ep_storms(drop=Basin) na_storms;
    set storms(keep=Name Basin MaxWind);
    if Basin="EP" then output ep_storms;
    else output na_storms;
run;
```

How many columns are in `ep_storms`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 2**

**Giải thích:** `KEEP=` trên SET chỉ đọc 3 cột vào PDV (Name, Basin, MaxWind); Season không được đọc vào. `DROP=Basin` trên bảng đầu ra chỉ áp dụng cho `ep_storms`, nên bảng này còn Name và MaxWind. `na_storms` có 3 cột. Basin vẫn dùng được trong câu IF vì DROP= trên bảng đầu ra chỉ có hiệu lực lúc ghi dòng.
</details>

---

### Question 14: D1 – Permanent vs temporary attributes
Which statement about the FORMAT statement is true?

- A. A FORMAT statement in a PROC step permanently changes the stored values.
- B. A FORMAT statement in a DATA step changes the stored values.
- C. A FORMAT statement in a DATA step stores the format in the descriptor portion of the output table; a FORMAT statement in a PROC step affects only that report.
- D. Formats can be assigned only in PROC steps.

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** FORMAT trong DATA step là thuộc tính lâu dài, lưu trong descriptor portion của bảng; trong PROC step thì chỉ tạm thời cho báo cáo đó (Activity p204a01). A và B sai vì format không bao giờ thay đổi giá trị đã lưu, chỉ thay đổi cách hiển thị. D sai vì format gán được cả trong DATA step.
</details>

---

## Domain 2 – Manage Data

### Question 15: D2 – PROC SORT NODUPKEY (PBQ)
Run:

```sas
proc sort data=storms out=storms_nodup nodupkey dupout=storms_dups;
    by Name;
run;
```

How many rows are in `storms_nodup`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 7**

**Giải thích:** NODUPKEY giữ dòng đầu tiên cho mỗi giá trị BY. Tên ANA xuất hiện 2 lần (mùa 2021 và 2022), nên 1 dòng bị loại và chuyển sang `storms_dups` (DUPOUT=). Còn lại 8 − 1 = 7 dòng.
</details>

---

### Question 16: D2 – IF-THEN/ELSE with DO groups (PBQ)
Run:

```sas
data storm_cat;
    set storms;
    length Category $ 4;
    if MaxWind >= 74 then do;
        Category="Hurr";
        Points=2;
    end;
    else do;
        Category="Trop";
        Points=1;
    end;
run;
```

What is the **sum of Points** across all rows? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 11**

**Giải thích:** Có 3 cơn có MaxWind ≥ 74 (80, 95, 145), được 3 × 2 = 6 điểm. 5 cơn còn lại được 5 × 1 = 5 điểm. Tổng 11. Khối DO…END cho phép chạy nhiều câu lệnh khi điều kiện đúng.
</details>

---

### Question 17: D2 – Date constants
The numeric column `StartDate` holds SAS dates. Which WHERE statement selects dates from June 1 through November 30, 2021?

- A. `where StartDate between "01JUN2021"d and "30NOV2021"d;`
- B. `where StartDate between "01JUN2021" and "30NOV2021";`
- C. `where StartDate between '2021-06-01'd and '2021-11-30'd;`
- D. `where StartDate between 01JUN2021d and 30NOV2021d;`

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** Hằng ngày có dạng `"ddMONyyyy"d` (nháy đơn hay nháy kép đều được, theo sau là chữ d). B so sánh cột số với chuỗi ký tự. C sai vì hằng ngày không nhận dạng ISO. D thiếu dấu nháy.
</details>

---

### Question 18: D2 – RENAME= on an output table
Consider:

```sas
data storms2(rename=(MaxWind=WindMPH));
    set storms;
    Knots=MaxWind*0.869;
run;
```

Which statement is true?

- A. The step fails because the RENAME= option must be placed in the SET statement.
- B. The step runs, and Knots is calculated from MaxWind. The output table contains WindMPH instead of MaxWind.
- C. The step runs, but Knots is missing because MaxWind no longer exists.
- D. The assignment statement must refer to WindMPH.

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** RENAME= trên bảng đầu ra chỉ có hiệu lực khi dòng được ghi ra, nên trong DATA step tên cột vẫn là MaxWind. Ngược lại, RENAME= trên SET đổi tên ngay khi đọc vào PDV, và khi đó phải dùng tên mới. A, C và D đều sai vì nhầm thời điểm đổi tên.
</details>

---

### Question 19: D2 – LENGTH and truncation (PBQ)
Run:

```sas
data storm_region;
    set storms;
    if Basin="NA" then Region="Atlantic";
    else Region="East Pacific";
run;
```

What value of **Region** is stored for DORA? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: East Pac**

**Giải thích:** Độ dài cột ký tự được xác định khi SAS gặp cột lần đầu lúc compile. "Atlantic" dài 8, nên Region có độ dài 8 và "East Pacific" bị cắt còn "East Pac". Log không có NOTE, WARNING hay ERROR nào. Cách sửa: thêm `length Region $ 12;` trước câu IF.
</details>

---

### Question 20: D2 – RETAIN (PBQ)
Run:

```sas
data running_max;
    set storms;
    retain MaxSoFar 0;
    MaxSoFar=max(MaxSoFar, MaxWind);
run;
```

What is **MaxSoFar** in row 4? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 60**

**Giải thích:** RETAIN giữ giá trị qua các vòng lặp, giá trị ban đầu là 0. Lần lượt: max(0,45)=45, max(45,60)=60, max(60,45)=60, max(60,40)=60. Nếu không có RETAIN, MaxSoFar bị reset về missing ở mỗi vòng, và MAX bỏ qua missing, nên kết quả sẽ chỉ bằng MaxWind của từng dòng.
</details>

---

### Question 21: D2 – BY-group processing with the SUM statement (PBQ)
Create one row per **Basin** and **Season** with a column `StormCount` that counts the storms in each group. Use PROC SORT, BY, FIRST./LAST. and a sum statement.

What is **StormCount** for Basin = EP, Season = 2021? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 3**

```sas
proc sort data=storms out=storms_bs;
    by Basin Season;
run;

data storm_counts;
    set storms_bs;
    by Basin Season;
    if first.Season then StormCount=0;
    StormCount+1;
    if last.Season;
    keep Basin Season StormCount;
run;
```

**Giải thích:** Sum statement tự RETAIN, có giá trị ban đầu 0 và bỏ qua missing. Reset tại `first.Season` vì Season là biến BY cuối cùng: nhóm Season nằm bên trong từng Basin. EP 2021 gồm DORA, ENRIQUE, FELICIA, nên bằng 3. Bảng kết quả có 4 dòng.
</details>

---

### Question 22: D2 – FIRST./LAST. with two BY variables
`storms` is sorted by **Basin** and **Season** and read with `by Basin Season;`. What are the values for the row **BLANCA** (EP, 2022)?

- A. first.Basin=0, last.Basin=1, first.Season=1, last.Season=1
- B. first.Basin=1, last.Basin=1, first.Season=1, last.Season=1
- C. first.Basin=0, last.Basin=0, first.Season=1, last.Season=0
- D. first.Basin=0, last.Basin=1, first.Season=0, last.Season=1

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** Thứ tự sau khi sort: EP 2021 (DORA, ENRIQUE, FELICIA), **EP 2022 (BLANCA)**, NA 2021…, NA 2022. BLANCA không phải dòng đầu của EP nhưng là dòng cuối của EP, nên first.Basin=0 và last.Basin=1. BLANCA là dòng duy nhất của EP 2022, nên cả first.Season và last.Season đều bằng 1.
</details>

---

### Question 23: D2 – SUBSTR, UPCASE, SCAN, PROPCASE

```sas
data station;
    Station="us-tx-houston";
    StateCode=upcase(substr(Station, 4, 2));
    City=propcase(scan(Station, -1, '-'));
run;
```

What are the values of StateCode and City?

- A. `tx` and `houston`
- B. `TX` and `HOUSTON`
- C. `US` and `Houston`
- D. `TX` and `Houston`

<details><summary>Answer & explanation</summary>

**Answer: D**

**Giải thích:** `substr(Station,4,2)` lấy 2 ký tự bắt đầu từ vị trí 4, được "tx", rồi UPCASE thành "TX". `scan(...,-1,'-')` lấy từ **cuối cùng** (n âm thì đọc từ phải sang), được "houston", rồi PROPCASE thành "Houston".
</details>

---

### Question 24: D2 – Macro variables and the dot delimiter

```sas
%let basin=EP;
%let yr=2021;
```

Which DATA statement creates a table named **EP_2021**?

- A. `data &basin_&yr;`
- B. `data &basin._&yr;`
- C. `data &basin.._&yr;`
- D. `data "&basin"_&yr;`

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** Dấu chấm kết thúc tên macro variable, nên `&basin.` thành "EP" và nối với "_2021". A sai vì SAS tìm macro variable tên `basin_` (không tồn tại) và báo WARNING "Apparent symbolic reference BASIN_ not resolved". C cho ra "EP._2021" vì dấu chấm thứ hai được giữ lại trong text. D sai cú pháp tên bảng.
</details>

---

### Question 25: D2 – COMPRESS (PBQ)
What is the value of `Phone2`?

```sas
data phone;
    Phone="(713) 555-0142";
    Phone2=compress(Phone, "() -");
run;
```

Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 7135550142**

**Giải thích:** Đối số thứ hai của COMPRESS liệt kê **các ký tự cần xóa**, ở đây là ngoặc đơn, khoảng trắng và gạch ngang. Nếu không có đối số thứ hai, COMPRESS chỉ xóa khoảng trắng.
</details>

---

### Question 26: D2 – TRIM and concatenation
`First` has length 8 and the value `Ana`, so it is stored with trailing blanks. `Last` has the value `Lee`. Which expression returns exactly `Ana Lee`?

- A. `First || " " || Last`
- B. `trim(First || " " || Last)`
- C. `trim(First) || " " || Last`
- D. `compress(First) || Last`

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** TRIM bỏ khoảng trắng **ở cuối** First trước khi nối, nên ra "Ana Lee". A giữ 5 khoảng trắng thừa sau "Ana". B chỉ cắt khoảng trắng cuối của cả chuỗi, khoảng trắng ở giữa vẫn còn. D cho ra "AnaLee", thiếu khoảng trắng. Cách khác: `catx(" ", First, Last)`.
</details>

---

### Question 27: D2 – LARGEST / SMALLEST (PBQ)

```sas
data winds;
    Wind1=50; Wind2=.; Wind3=65; Wind4=40;
    Second=largest(2, of Wind1-Wind4);
    Low=smallest(1, of Wind1-Wind4);
run;
```

What is the value of **Second**? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 50**

**Giải thích:** LARGEST(k, …) trả về giá trị lớn thứ k trong các giá trị **không missing**: 65, 50, 40, nên giá trị thứ 2 là 50. Low = SMALLEST(1, …) = 40, vì giá trị missing bị bỏ qua.
</details>

---

### Question 28: D2 – ROUND and INT (PBQ)

```sas
data nums;
    X=round(18.456, .1) + int(-2.7);
run;
```

What is the value of X? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 16.5**

**Giải thích:** `round(18.456, .1)` làm tròn tới 0.1, được 18.5. INT bỏ phần thập phân **về phía 0**, nên int(-2.7) = -2 (khác FLOOR(-2.7) = -3). Tổng 18.5 + (-2) = 16.5.
</details>

---

### Question 29: D2 – Date functions MDY, MONTH, YEAR, QTR (PBQ)

```sas
data dates;
    D='15AUG2023'd;
    Q=qtr(D);
    Next=mdy(month(D), 1, year(D)+1);
    format Next date9.;
run;
```

What is the **formatted** value of Next? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 01AUG2024**

**Giải thích:** month(D)=8 và year(D)+1=2024, nên MDY(8,1,2024) là ngày 1/8/2024, hiển thị DATE9. là 01AUG2024. Ngoài ra Q = qtr(D) = 3, vì tháng 8 thuộc quý 3.
</details>

---

### Question 30: D2 – INTCK (discrete vs continuous)

```sas
data gap;
    A=intck('month', '31JAN2024'd, '01FEB2024'd);
    B=intck('month', '31JAN2024'd, '01FEB2024'd, 'c');
run;
```

What are the values of A and B?

- A. A=0, B=1
- B. A=1, B=1
- C. A=1, B=0
- D. A=0, B=0

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** Phương pháp mặc định (discrete) đếm **số ranh giới khoảng** đi qua. Từ 31/1 sang 1/2 vượt qua một ranh giới cuối tháng, nên A=1. Với `'c'` (continuous), SAS đếm số tháng đầy đủ tính từ ngày bắt đầu; chưa trọn một tháng nên B=0.
</details>

---

### Question 31: D2 – INTNX alignment
What date does `intnx('month', '15FEB2024'd, 0, 'end')` return?

- A. 28FEB2024
- B. 29FEB2024
- C. 01FEB2024
- D. 15MAR2024

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** Increment 0 nghĩa là ở lại tháng hiện tại; alignment `'end'` trả về ngày cuối tháng. Năm 2024 là năm nhuận nên ngày cuối tháng 2 là 29FEB2024. C là kết quả của alignment mặc định ('beginning'). D đúng với `intnx('month',…,1,'same')`.
</details>

---

### Question 32: D2 – YRDIF (PBQ)

```sas
data age;
    Age=int(yrdif('15MAR2000'd, '14MAR2024'd, 'age'));
run;
```

What is the value of Age? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 23**

**Giải thích:** YRDIF với basis `'age'` tính số năm thực tế. Ngày 14/3/2024 còn một ngày nữa mới tới sinh nhật lần thứ 24, nên kết quả khoảng 23.997. INT cắt phần thập phân (không làm tròn), được 23.
</details>

---

### Question 33: D2 – Variable lists and the OF operator (PBQ)

```sas
data qtr;
    Q1=10; Q2=.; Q3=30; Q4=40;
    A=sum(of Q1-Q4);
    B=sum(Q1-Q4);
run;
```

What is the value of **B**? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: -30**

**Giải thích:** Thiếu từ khóa OF, `Q1-Q4` được hiểu là phép **trừ** Q1 − Q4 = 10 − 40 = −30. Còn A = sum(of Q1-Q4) = 10 + 30 + 40 = 80, vì SUM bỏ qua missing. Danh sách cột trong đối số của hàm bắt buộc phải có OF.
</details>

---

### Question 34: D2 – Type conversion with PUT
What does `put(1234.5, dollar10.2)` return?

- A. The character value `$1,234.50` (right-aligned in 10 positions)
- B. The numeric value 1234.50
- C. The character value `1234.50`
- D. The character value `$1,235`

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** PUT(giá trị, format) luôn trả về **ký tự**, viết theo format: DOLLAR10.2 thêm dấu $, dấu phẩy và 2 chữ số thập phân. B sai vì kết quả không phải số. C bỏ mất định dạng. D là kết quả của DOLLAR10. (không có chữ số thập phân).
</details>

---

### Question 35: D2 – Iterative DO loop with a negative increment (PBQ)

```sas
data countdown;
    do i=10 to 1 by -3;
        output;
    end;
run;
```

How many rows are in `countdown`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 4**

**Giải thích:** i nhận các giá trị 10, 7, 4, 1. Sau mỗi vòng, i giảm 3; khi i = −2 thì đã vượt giá trị stop, nên vòng lặp dừng. OUTPUT nằm trong vòng lặp nên có 4 dòng. Nếu không có OUTPUT, chỉ có 1 dòng với i = −2.
</details>

---

### Question 36: D2 – PROC TRANSPOSE wide to narrow (PBQ)

```sas
data wind_wide;
    input Name $ Wind1 Wind2 Wind3;
    datalines;
ANA 40 45 .
BILL 55 60 50
;
run;

proc transpose data=wind_wide
               out=wind_narrow(rename=(col1=WindMPH))
               name=Reading;
    by Name;
run;
```

How many rows are in `wind_narrow`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 6**

**Giải thích:** Không có câu lệnh VAR thì mọi cột số không nằm trong BY (Wind1–Wind3) đều được chuyển vị. Mỗi Name cho 3 dòng (giá trị missing vẫn thành một dòng), 2 Name cho 6 dòng. NAME= đổi tên `_NAME_` thành Reading; RENAME= đổi COL1 thành WindMPH. Dữ liệu đã được sort theo Name.
</details>

---

### Question 37: D2 – PROC TRANSPOSE narrow to wide (ID, PREFIX=)
`wind_rank` has the columns Name, Rank (values 1 and 2) and Wind, and is sorted by Name.

```sas
proc transpose data=wind_rank out=wind_w prefix=W;
    by Name;
    id Rank;
    var Wind;
run;
```

Which columns are in `wind_w`?

- A. Name, W1, W2
- B. Name, _NAME_, COL1, COL2
- C. Name, _NAME_, W1, W2
- D. Name, Rank, W1, W2

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** Giá trị của cột ID (1, 2) trở thành tên cột; PREFIX=W thêm tiền tố nên ra W1 và W2. Cột `_NAME_` (chứa "Wind") vẫn còn trừ khi bỏ bằng `out=wind_w(drop=_name_)`. B là kết quả khi không có ID và PREFIX=. Giá trị ID phải là duy nhất trong mỗi nhóm BY.
</details>

---

## Domain 3 – Error Handling

### Question 38: D3 – PUTLOG with a format
Which statement writes the value of `Total` to the log using the DOLLAR10.2 format?

- A. `putlog "Total" dollar10.2;`
- B. `putlog Total= format=dollar10.2;`
- C. `putlog dollar10.2 Total=;`
- D. `putlog Total= dollar10.2;`

<details><summary>Answer & explanation</summary>

**Answer: D**

**Giải thích:** Cú pháp là `PUTLOG column= format.;`: tên cột kèm dấu `=` (để in cả tên cột), rồi đến format. A in chuỗi "Total" chứ không in giá trị. B và C sai cú pháp.
</details>

---

### Question 39: D3 – Conditional PUTLOG

```sas
data check;
    set storms;
    if MaxWind > 140 then putlog "WARNING: Extreme wind for " Name=;
run;
```

What happens when this step runs?

- A. A line beginning with WARNING: is written to the log only for rows with MaxWind > 140, and the step completes normally.
- B. The step stops at the first row with MaxWind > 140.
- C. The message is written to the output table as a new column.
- D. The message is written for every row.

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** PUTLOG chỉ ghi ra log, không thay đổi dữ liệu và không dừng step. Đặt trong IF thì chỉ chạy khi điều kiện đúng, ở đây chỉ có FELICIA (145). Tiền tố "WARNING:" hoặc "NOTE:" khiến log tô màu dòng đó như cảnh báo hoặc ghi chú thật, giúp dễ tìm.
</details>

---

### Question 40: D3 – _N_ with a WHERE statement (PBQ)

```sas
data big;
    set storms;
    where MaxWind > 50;
    Row=_N_;
run;
```

What is the value of **Row** in the **last** row of `big`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 5**

**Giải thích:** WHERE lọc dòng **trước khi** đọc vào PDV, nên các dòng không thỏa điều kiện không tạo ra vòng lặp nào. Năm dòng thỏa điều kiện (BILL, DORA, ENRIQUE, FELICIA, BLANCA) ứng với 5 vòng lặp, nên _N_ của dòng cuối bằng 5. `_N_` đếm số vòng lặp DATA step, không đếm số dòng của bảng đầu vào.
</details>

---

### Question 41: D3 – _N_ with a subsetting IF (PBQ)

```sas
data big2;
    set storms;
    Row=_N_;
    if MaxWind > 50;
run;
```

What is the value of **Row** for FELICIA? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 7**

**Giải thích:** Với subsetting IF, mọi dòng đều được đọc vào PDV (mỗi dòng một vòng lặp), sau đó mới bị lọc. FELICIA là dòng thứ 7 của bảng đầu vào, nên _N_ = 7. So sánh với Q40: vị trí của câu lọc và loại câu lọc (WHERE hay IF) làm _N_ khác nhau.
</details>

---

### Question 42: D3 – _ERROR_ and invalid data
`WindC` is a character column. In one row its value is `N/A`.

```sas
data conv;
    set raw_winds;
    Wind=input(WindC, 3.);
run;
```

What happens for that row?

- A. The step stops with an ERROR.
- B. Wind is set to 0.
- C. Wind is missing, the log shows a NOTE about an invalid argument to the INPUT function together with the row's values, _ERROR_ is set to 1 for that row, and the step continues.
- D. Wind keeps the value from the previous row.

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** Lỗi dữ liệu (data error) không làm dừng step. SAS gán giá trị missing, ghi NOTE kèm giá trị PDV của dòng lỗi vào log, và đặt `_ERROR_=1`. `_ERROR_` và `_N_` là biến tự động, có trong PDV nhưng không được ghi vào bảng đầu ra. D sai vì cột tạo bằng câu gán bị reset về missing ở mỗi vòng lặp.
</details>

---

### Question 43: D3 – Misspelled procedure name

```sas
proc prnt data=storms;
run;
```

What appears in the log?

- A. A WARNING that SAS assumed PRINT, and the report is produced.
- B. An ERROR that procedure PRNT was not found; no report is produced.
- C. A NOTE only; the report is produced.
- D. Nothing; the step is silently ignored.

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** SAS không tìm được procedure tên PRNT, nên báo "ERROR: Procedure PRNT not found." và step không chạy. A sai: SAS chỉ tự sửa một số từ khóa bị gõ sai trong câu lệnh (có WARNING "Assuming the symbol … was misspelled"), không tự sửa tên procedure.
</details>

---

### Question 44: D3 – Missing semicolon on the DATA statement

```sas
data storms2
    set storms;
    Knots=MaxWind*0.869;
run;
```

What is the result?

- A. An ERROR occurs and no tables are created.
- B. The step runs normally and creates `storms2` with 8 rows.
- C. Only the Knots column is created in `storms2`.
- D. SAS reads `data storms2 set storms;` as one DATA statement naming three output tables (STORMS2, SET, STORMS). With no SET statement, each table has 1 row with Knots missing, the log has a NOTE that MaxWind is uninitialized, and `work.storms` is overwritten.

<details><summary>Answer & explanation</summary>

**Answer: D**

**Giải thích:** Khi thiếu dấu `;`, câu lệnh kéo dài tới dấu `;` kế tiếp, nên "set" và "storms" bị hiểu là tên bảng đầu ra. Step không đọc dữ liệu nào, chỉ chạy 1 vòng: MaxWind là cột chưa khởi tạo (NOTE uninitialized) nên Knots bằng missing. Nguy hiểm nhất là bảng `storms` gốc bị ghi đè. Bài học: luôn đọc cả các NOTE trong log.
</details>

---

### Question 45: D3 – Unbalanced quotation marks
A program begins with:

```sas
title "Storm Report;
proc print data=storms;
run;
```

What is the most likely result?

- A. An ERROR about the TITLE statement, and the report prints without a title.
- B. The report prints with the title "Storm Report".
- C. No report is produced: the rest of the code is treated as part of the quoted string, the program appears to keep running, and the log may show no ERROR.
- D. SAS adds the missing quotation mark automatically.

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** Thiếu dấu nháy đóng thì mọi code phía sau trở thành một phần của chuỗi, nên PROC PRINT không bao giờ chạy và chương trình có vẻ như vẫn đang chạy. Cách sửa: thêm dấu nháy đóng và submit lại; trong SAS Studio có thể cần hủy chương trình đang chạy trước.
</details>

---

### Question 46: D3 – Invalid option

```sas
proc print data=storms noob;
run;
```

What happens?

- A. The report prints without the Obs column.
- B. The log shows a syntax ERROR because NOOB is not a valid option, and the step does not run.
- C. A WARNING appears, and SAS uses NOOBS.
- D. The report prints with an Obs column and a NOTE.

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** Tên option sai khiến SAS báo ERROR cú pháp, liệt kê các option hợp lệ (gạch dưới chữ NOOB) và **không chạy** step, giống demo về option AVERAGE của PROC MEANS trong khóa học. Option đúng là `NOOBS`.
</details>

---

### Question 47: D3 – Reading the log (uninitialized variable)
After a DATA step runs, the log shows:

```text
NOTE: Variable MaxWnd is uninitialized.
```

What is the most likely cause?

- A. The column name MaxWind was misspelled in the code, so SAS created a new numeric column MaxWnd with missing values.
- B. The input table is empty.
- C. A LENGTH statement is missing.
- D. MaxWnd is a character column.

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** SAS gặp một cột chưa tồn tại và không được gán giá trị, nên tạo cột số toàn giá trị missing và ghi NOTE "uninitialized". Đây là lỗi logic: không có ERROR, kết quả vẫn ra nhưng sai. Lỗi thiếu dấu chấm sau tên format (ví dụ `dollar12`) cũng gây ra đúng NOTE này.
</details>

---

### Question 48: D3 – Debugging (PBQ)
The program below should compute the mean MaxWind for the EP basin, rounded to one decimal place. Fix every error and run it.

```sas
data ep_storms
    set storms;
    where Basin="EP';
run;

proc means data=ep_storms mean maxdec=1;
    var MaxWind
run;
```

What mean is displayed? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 95.0**

```sas
data ep_storms;
    set storms;
    where Basin="EP";
run;

proc means data=ep_storms mean maxdec=1;
    var MaxWind;
run;
```

**Giải thích:** Có 3 lỗi: thiếu `;` sau DATA, dấu nháy không khớp (`"EP'`), và thiếu `;` sau VAR. EP có 80, 95, 145, 60, tổng 380; 380 / 4 = 95.0.
</details>

---

## Domain 4 – Generate Reports and Output

### Question 49: D4 – PROC PRINT with ID and LABEL

```sas
proc print data=storms label;
    id Name;
    var Basin MaxWind;
    label MaxWind="Max Wind (MPH)";
run;
```

Which statement is true?

- A. The Obs column is replaced by Name, and the MaxWind heading shows "Max Wind (MPH)".
- B. The label is ignored unless NOOBS is also specified.
- C. Name appears twice, once as Obs and once as a column.
- D. The LABEL statement permanently changes the label stored in the table.

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** ID thay cột Obs bằng giá trị của Name. Muốn tiêu đề hiện label thì PROC PRINT cần option `LABEL` (đã có ở đây). B sai vì LABEL không cần NOOBS. D sai vì LABEL trong PROC chỉ tạm thời cho báo cáo đó.
</details>

---

### Question 50: D4 – PROC PRINT with BY and SUM (PBQ)
Sort `storms` by Basin, then print it grouped by Basin with a subtotal of MaxWind for each basin.

What subtotal is shown for **NA**? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 190**

```sas
proc sort data=storms out=storms_b;
    by Basin;
run;

proc print data=storms_b;
    by Basin;
    sum MaxWind;
run;
```

**Giải thích:** NA có 45 + 60 + 45 + 40 = 190. EP = 380, tổng chung = 570. Dùng BY trong PROC PRINT thì dữ liệu phải được sort trước, nếu không sẽ có ERROR báo dữ liệu chưa sắp xếp.
</details>

---

### Question 51: D4 – PROC PRINT with WHERE (PBQ)

```sas
proc print data=storms;
    where Season=2021 and MaxWind>=60;
run;
```

How many rows are printed? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 4**

**Giải thích:** Mùa 2021 có MaxWind ≥ 60 gồm BILL (60), DORA (80), ENRIQUE (95), FELICIA (145), tức 4 dòng. BLANCA (60) thuộc mùa 2022 nên bị loại.
</details>

---

### Question 52: D4 – PROC FREQ NLEVELS (PBQ)

```sas
proc freq data=storms nlevels;
    tables Name / nocum;
run;
```

How many levels does the "Number of Variable Levels" table show for Name? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 7**

**Giải thích:** NLEVELS đếm số giá trị **khác nhau**. Bảng có 8 dòng nhưng ANA xuất hiện 2 lần, nên chỉ có 7 giá trị khác nhau. NLEVELS rất tiện để kiểm tra một cột đáng lẽ phải là duy nhất (ID).
</details>

---

### Question 53: D4 – Two-way frequency table (PBQ)

```sas
proc freq data=storms;
    tables Basin*Season;
run;
```

What overall **Percent** is shown in the cell Basin = EP, Season = 2021? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 37.50**

**Giải thích:** Ô EP–2021 có tần số 3; tổng là 8 dòng, nên 3 / 8 = 37.50%. Bảng chéo (dấu `*`) mặc định hiện Frequency, Percent, Row Pct và Col Pct. Dùng NOROW và NOCOL để ẩn hai loại tỉ lệ sau.
</details>

---

### Question 54: D4 – PROC FREQ ORDER=
What does `ORDER=FREQ` in the PROC FREQ statement do?

- A. It sorts the input table permanently by frequency.
- B. It lists the values in ascending order of their raw values.
- C. It lists the values in descending order of frequency.
- D. It removes values that occur only once.

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** ORDER=FREQ sắp các giá trị theo tần số giảm dần, giúp nhanh chóng thấy giá trị phổ biến nhất hoặc giá trị trùng lặp. A sai vì PROC FREQ không thay đổi dữ liệu. B là thứ tự mặc định (ORDER=INTERNAL). D sai vì ORDER= không loại bỏ giá trị nào.
</details>

---

### Question 55: D4 – PROC MEANS with WAYS and OUTPUT (PBQ)

```sas
proc means data=storms noprint;
    class Basin Season;
    var MaxWind;
    ways 1 2;
    output out=wind_stats mean=AvgWind;
run;
```

How many rows are in `wind_stats`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 8**

**Giải thích:** `WAYS 1` cho 1 dòng mỗi giá trị Basin (2) và 1 dòng mỗi giá trị Season (2), tức 4 dòng. `WAYS 2` cho các tổ hợp Basin×Season có trong dữ liệu (EP2021, EP2022, NA2021, NA2022), thêm 4 dòng. Tổng 8. Không có WAYS thì có thêm dòng tổng chung (_TYPE_=0), thành 9.
</details>

---

### Question 56: D4 – PROC UNIVARIATE
Which part of the default PROC UNIVARIATE output is most useful for finding the five highest and five lowest values of a column, together with their row numbers?

- A. Moments
- B. Basic Statistical Measures
- C. Quantiles
- D. Extreme Observations

<details><summary>Answer & explanation</summary>

**Answer: D**

**Giải thích:** Bảng Extreme Observations liệt kê 5 giá trị thấp nhất và 5 giá trị cao nhất kèm số thứ tự dòng (Obs), rất hữu ích khi kiểm tra dữ liệu (ví dụ phát hiện Quantity âm). Moments và Basic Statistical Measures cho mean, std, v.v. Quantiles cho các phân vị.
</details>

---

### Question 57: D4 – PROC FORMAT with ranges (PBQ)

```sas
proc format;
    value windcat low-<39 ='Depression'
                  39-<74  ='Storm'
                  74-high ='Hurricane';
run;

proc freq data=storms;
    tables MaxWind;
    format MaxWind windcat.;
run;
```

What frequency is shown for **Storm**? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 5**

**Giải thích:** `39-<74` gồm các giá trị từ 39 tới **dưới** 74: 45, 60, 45, 40, 60, tức 5 giá trị. Hurricane có 3 (80, 95, 145); không có Depression nào. Khi tạo format không có dấu chấm sau tên; khi dùng thì phải có (`windcat.`).
</details>

---

### Question 58: D4 – PROC FORMAT with CNTLIN=
You want to build a character format `$basinfmt` from the `basins` table with `proc format cntlin=fmt_data; run;`. Which DATA step prepares `fmt_data` correctly?

- A.
```sas
data fmt_data;
    retain FmtName '$basinfmt';
    set basins(rename=(Basin=Start BasinName=Label));
    keep FmtName Start Label;
run;
```
- B.
```sas
data fmt_data;
    set basins(rename=(Basin=Label BasinName=Start));
    FmtName='basinfmt';
run;
```
- C.
```sas
data fmt_data;
    set basins;
    Format='$basinfmt';
run;
```
- D.
```sas
data fmt_data;
    retain FmtName '$basinfmt.';
    set basins(rename=(Basin=Value BasinName=Text));
run;
```

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** Bảng CNTLIN tối thiểu cần các cột **FmtName** (format ký tự thì bắt đầu bằng $), **Start** (giá trị gốc) và **Label** (nhãn hiển thị); với khoảng giá trị thì cần thêm **End**. B đảo ngược Start và Label và thiếu dấu $. C dùng sai tên cột. D sai tên cột và thừa dấu chấm trong tên format.
</details>

---

### Question 59: D4 – ODS destinations and STYLE=
Which pair of statements creates a PowerPoint file from the reports placed between them?

- A. `ods pptx file="&outpath/storms.pptx";` … `ods pptx close;`
- B. `ods powerpoint file="&outpath/storms.pptx" style=powerpointlight;` … `ods powerpoint close;`
- C. `ods excel file="&outpath/storms.pptx";` … `ods excel close;`
- D. `ods powerpoint file="&outpath/storms.pptx";` … `ods close powerpoint;`

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** Destination PowerPoint có tên `ODS POWERPOINT`, và `STYLE=` chọn giao diện. Mọi destination đều theo mẫu `ODS dest FILE=…;` rồi `ODS dest CLOSE;`; tương tự với ODS PDF, RTF, EXCEL (file .xlsx) và CSVALL. A sai vì không có destination tên PPTX. C tạo file Excel dù có đổi đuôi. D đặt CLOSE sai vị trí.
</details>

---

### Question 60: D4 – PROC EXPORT with a delimiter
Which step writes `storms` to a pipe-delimited text file?

- A.
```sas
proc export data=storms outfile="&outpath/storms.txt" dbms=dlm replace;
    delimiter='|';
run;
```
- B.
```sas
proc export data=storms outfile="&outpath/storms.txt" dbms=tab replace;
    delimiter='|';
run;
```
- C.
```sas
proc export data=storms outfile="&outpath/storms.txt" dlm='|' replace;
run;
```
- D.
```sas
proc export data=storms outfile="&outpath/storms.txt" dbms=csv replace;
run;
```

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** `DBMS=DLM` cùng câu lệnh `DELIMITER='|'` tạo file phân cách bằng ký tự tùy chọn; REPLACE ghi đè file nếu đã có. B sai vì DBMS=TAB luôn dùng ký tự tab. C sai vì DLM= không phải option của câu lệnh PROC EXPORT. D tạo file phân cách bằng dấu phẩy.
</details>

---

## Answer summary

| # | Ans | # | Ans | # | Ans | # | Ans |
|---|---|---|---|---|---|---|---|
| 1 | C | 16 | 11 | 31 | B | 46 | B |
| 2 | B | 17 | A | 32 | 23 | 47 | A |
| 3 | A | 18 | B | 33 | -30 | 48 | 95.0 |
| 4 | B | 19 | East Pac | 34 | A | 49 | A |
| 5 | C | 20 | 60 | 35 | 4 | 50 | 190 |
| 6 | A | 21 | 3 | 36 | 6 | 51 | 4 |
| 7 | WP3 | 22 | A | 37 | C | 52 | 7 |
| 8 | 9 | 23 | D | 38 | D | 53 | 37.50 |
| 9 | D | 24 | B | 39 | A | 54 | C |
| 10 | -1 | 25 | 7135550142 | 40 | 5 | 55 | 8 |
| 11 | B | 26 | C | 41 | 7 | 56 | D |
| 12 | C | 27 | 50 | 42 | C | 57 | 5 |
| 13 | 2 | 28 | 16.5 | 43 | B | 58 | A |
| 14 | C | 29 | 01AUG2024 | 44 | D | 59 | B |
| 15 | 7 | 30 | C | 45 | C | 60 | A |
