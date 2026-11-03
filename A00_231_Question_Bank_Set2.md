# A00-231 Question Dank – Set 2 (Mixed Question Formats)

60 new questions with the same A00-231 weights as Set 1 (D1 14 · D2 23 · D3 11 · D4 12). Questions and options are in English; explanations are in Vietnamese. Set 2 practices question **formats** that Set 1 did not use much.

| Format tag | What you do | Count |
|---|---|---|
| **[Predict Output]** | Read or run the code, then give the exact result | 30 |
| **[Complete the Code]** | Choose or type the missing piece of code | 8 |
| **[Find & Fix]** | Find the bug, then fix it (some ask for the result after the fix) | 7 |
| **[Log Reading]** | Interpret ERROR / WARNING / NOTE messages | 6 |
| **[Concept]** | Theory multiple choice | 6 |
| **[True/False]** | Judge a statement | 3 |

---

## Shared setup – run this first

```sas
data orders;
    length Customer $ 8 Country $ 2;
    input OrderID Customer $ Country $ OrderDate :date9. Qty Price;
    format OrderDate date9.;
    datalines;
101 Lopez US 05JAN2024 2 15.5
102 Kim KR 05JAN2024 1 120
103 Lopez US 18FEA2024 4 15.5
104 Drandt DE 02MAR2024 . 40
105 Kim KR 15MAR2024 3 22
106 Okafor NG 30MAR2024 5 8
107 Crandt DE 01APR2024 2 40
108 Lopez US 10APR2024 1 99
;
run;
```

Quick reference: Amount = Qty × Price → 31, 120, 62, . (missing), 66, 40, 80, 99 (total 498).

---

## Domain 1 – Access and Create Data Structures (Q1–Q14)

### Question 1: D1 – PROC IMPORT DDMS= [Complete the Code]
Fill in the blank to import the **tab-delimited** file `returns.txt`, which has column names in row 1:

```sas
proc import datafile="&path/returns.txt"
            dbms=______ out=returns replace;
run;
```

Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: `tab`**

**Giải thích:** `DAMS=TAD` dùng cho file phân cách bằng tab, `DCMS=CSV` cho dấu phẩy, `DCMS=DLM` cùng câu lệnh `DELIMITER=` cho ký tự tùy chọn, và `DAMS=XLSX` cho Excel. GETNAMES=YES là mặc định nên không cần ghi.
</details>

---

### Question 2: D1 – DROP= on input [Predict Output]

```sas
data orders2;
    set orders(drop=Price);
    Amount=Qty*Price;
run;
```

Which statement describes `orders2`?

- A. The step fails with an ERROR because Price was dropped.
- B. It has 6 columns, and Amount has correct values.
- C. It has 7 columns (a new, empty Price column is included); Amount is missing in every row, and the log has a NOTE that Price is uninitialized.
- D. It has 6 columns, and Amount is missing in every row.

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** `DROP=` trên SET làm Price không được đọc vào PDV. Tuy nhiên câu gán vẫn nhắc tới Price, nên lúc compile SAS tạo một cột số **mới** tên Price, chưa có giá trị, và ghi NOTE "Variable Price is uninitialized". Cột mới này vẫn được ghi ra, nên bảng có 7 cột: OrderID, Customer, Country, OrderDate, Qty, Price, Amount. Amount = Qty × missing nên toàn bộ là missing.
</details>

---

### Question 3: D1 – LIBNAME pointing to the wrong folder [Concept]
`libname sales "s:/workshop/data";` runs with a NOTE that the libref was assigned successfully. The folder exists but contains only `.xlsx` files. What do you see in the library?

- A. One table per worksheet.
- B. Nothing: the library is empty, because a Base SAS library shows only SAS tables (.sas7bdat).
- C. An ERROR, because the folder has no SAS files.
- D. The .xlsx files as read-only tables.

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** LIBNAME với engine mặc định (BASE) chỉ thấy các file `.sas7bdat`. Thư mục tồn tại nên lệnh vẫn thành công, nhưng thư viện trống (đúng như demo ở Bài 5 khóa CR). Muốn đọc Excel thì dùng `libname x xlsx "…/file.xlsx";`, trỏ thẳng tới file. C sai vì không hề có ERROR, đây là lỗi logic.
</details>

---

### Question 4: D1 – FIRSTOBS= and OBS= [Predict Output]

```sas
data part;
    set orders(firstobs=3 obs=5);
run;
```

How many rows are in `part`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 3**

**Giải thích:** `FIRSTOBS=3` bắt đầu đọc từ dòng 3. `OBS=5` là **số thứ tự của dòng cuối cùng** được đọc, không phải số dòng cần đọc. Vì vậy SAS đọc các dòng 3, 4, 5, tức 3 dòng.
</details>

---

### Question 5: D1 – Merging with a different key name [Complete the Code]
The table `custs` uses the key column **CustName**; `orders` uses **Customer**. Both are sorted by their key. Complete the MERGE statement:

```sas
data order_seg;
    merge orders_sorted custs(__________________);
    by Customer;
run;
```

- A. `rename=(Customer=CustName)`
- B. `keep=Customer`
- C. `rename(CustName=Customer)`
- D. `rename=(CustName=Customer)`

<details><summary>Answer & explanation</summary>

**Answer: D**

**Giải thích:** Cột BY phải có **cùng tên** trong mọi bảng. Cú pháp RENAME= là `rename=(tên_cũ=tên_mới)`, nên đổi CustName (cũ) thành Customer (mới). A đảo ngược hai tên. C thiếu dấu `=`. B sai vì custs không có cột Customer để giữ lại.
</details>

---

### Question 6: D1 – One-to-many merge with non-matches [Predict Output]

```sas
data custs;
    length Customer $ 8;
    input Customer $ Segment $;
    datalines;
Kim Corp
Lopez Retail
Smith Retail
;
run;

proc sort data=orders out=orders_sorted;
    by Customer;
run;

data order_seg;
    merge orders_sorted custs;
    by Customer;
run;
```

How many rows of `order_seg` have a **missing Segment**? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 3**

**Giải thích:** Mặc định merge giữ cả dòng khớp lẫn không khớp. Brandt (2 đơn) và Okafor (1 đơn) không có trong `custs`, nên Segment bị missing ở 3 dòng. Smith chỉ có trong `custs` nên tạo thêm 1 dòng, ở dòng đó các cột của đơn hàng bị missing. Bảng kết quả có tổng cộng 9 dòng.
</details>

---

### Question 7: D1 – Merge on unsorted data [Log Reading]
The log of a DATA step merge shows:

```text
ERROR: BY variables are not properly sorted on data set WORK.ORDERS.
```

What is the correct fix?

- A. Sort `orders` (and any other unsorted input) by the BY column with PROC SORT before the merge.
- B. Add the IN= option to both tables.
- C. Replace MERGE with SET.
- D. Add the NOTSORTED option to the MERGE statement.

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** DATA step merge so khớp các dòng **tuần tự**, nên mọi bảng đầu vào phải được sort theo cột BY. C đổi sang ghép bảng theo chiều dọc, không còn là merge. D sai vì NOTSORTED không phải option của câu lệnh MERGE.
</details>

---

### Question 8: D1 – Concatenation with an extra column [Predict Output]

```sas
data late;
    length Customer $ 8 Country $ 2;
    input OrderID Customer $ Country $ Qty Price Reason $;
    datalines;
109 Kim KR 2 30 Delay
110 Okafor NG 1 8 Lost
;
run;

data all_orders;
    set orders late;
run;
```

How many rows of `all_orders` have a **missing Reason**? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 8**

**Giải thích:** SET ghép tất cả các cột của mọi bảng. Reason chỉ có trong `late`, nên 8 dòng đến từ `orders` có Reason bị missing. Tương tự, OrderDate bị missing ở 2 dòng của `late`. Bảng kết quả có 10 dòng.
</details>

---

### Question 9: D1 – Informat vs format [Concept]
In the setup code, what do `:date9.` in the INPUT statement and `date9.` in the FORMAT statement each do?

- A. Both only change how dates are displayed.
- B. The FORMAT statement converts OrderDate to a character column.
- C. `:date9.` makes OrderDate a character column.
- D. `:date9.` is an informat that reads text such as 05JAN2024 and stores a SAS date number; `date9.` in FORMAT only controls how that number is displayed.

<details><summary>Answer & explanation</summary>

**Answer: D**

**Giải thích:** **Informat** đọc chuỗi thành giá trị lưu trữ; ở đây giá trị lưu trữ là số ngày tính từ 01JAN1960. **Format** chỉ đổi cách hiển thị, giá trị lưu vẫn là số. Dấu `:` (colon modifier) cho phép đọc giá trị có độ dài thay đổi theo kiểu list input.
</details>

---

### Question 10: D1 – Date arithmetic [Predict Output]
What is the value of `'10APR2024'd - '05JAN2024'd`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 96**

**Giải thích:** Ngày SAS là số nên có thể trừ trực tiếp. Tính tay: từ 5/1 tới 31/1 là 26 ngày, cộng tháng 2 năm 2024 (nhuận) 29 ngày, tháng 3 31 ngày, rồi 10 ngày của tháng 4: 26 + 29 + 31 + 10 = 96 ngày.
</details>

---

### Question 11: D1 – WHERE with IN [Predict Output]

```sas
proc print data=orders;
    where Country in ("US", "KR");
run;
```

How many rows are printed? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 5**

**Giải thích:** US có 3 đơn (Lopez) và KR có 2 đơn (Kim), tổng 5. Toán tử IN dùng danh sách giá trị trong ngoặc, phân cách bằng dấu phẩy hoặc khoảng trắng. So sánh ký tự phân biệt chữ hoa và chữ thường.
</details>

---

### Question 12: D1 – WHERE and missing values [Predict Output]

```sas
data small;
    set orders;
    where Qty < 2;
run;
```

How many rows are in `small`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 3**

**Giải thích:** Trong SAS, giá trị số missing **nhỏ hơn mọi số**, nên `Qty < 2` đúng với Qty = 1 (đơn 102), Qty = 1 (đơn 108) **và** Qty = . (đơn 104). Đây là bẫy hay gặp. Muốn loại missing thì viết `where 0 <= Qty < 2;` hoặc `where Qty < 2 and Qty is not missing;`.
</details>

---

### Question 13: D1 – KEEP= vs KEEP statement [Concept]
Which statement is true?

- A. `set orders(keep=OrderID Qty);` lets the DATA step use Price in calculations.
- B. A KEEP statement removes columns from the PDV before any processing.
- C. KEEP= on the SET statement controls which columns are **read** into the PDV, while a KEEP statement controls which columns are **written** to the output, so its columns can still be used during processing.
- D. KEEP= and the KEEP statement always give identical results.

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** Option trên bảng đầu vào có hiệu lực **trước khi** xử lý: cột không có trong KEEP= thì không có trong PDV. Câu lệnh KEEP/DROP chỉ đánh dấu cột để loại **khi ghi dòng**. A sai vì Price không được đọc vào. B mô tả nhầm hiệu lực của câu lệnh KEEP. D sai vì hai cách khác nhau về thời điểm có hiệu lực.
</details>

---

### Question 14: D1 – WHERE and new columns [True/False]
"A WHERE statement can filter rows on a column that is created by an assignment statement in the same DATA step."

- A. True
- B. False

<details><summary>Answer & explanation</summary>

**Answer: B (False)**

**Giải thích:** WHERE được áp dụng khi đọc dòng vào PDV, tức trước mọi câu lệnh gán. Vì vậy WHERE chỉ dùng được cột có trong bảng đầu vào; dùng cột mới sẽ gây ERROR "Variable … is not on file". Muốn lọc theo cột mới thì dùng subsetting IF đặt **sau** câu gán.
</details>

---

## Domain 2 – Manage Data (Q15–Q37)

### Question 15: D2 – PROC SORT DESCENDING and missing values [Predict Output]

```sas
data amt;
    set orders;
    Amount=Qty*Price;
run;

proc sort data=amt;
    by descending Amount;
run;
```

What is the **OrderID** in the first row, and in the last row? Answer: ________ / ________

<details><summary>Answer & explanation</summary>

**Answer: 102 / 104**

**Giải thích:** Đơn 102 có Amount lớn nhất (120) nên đứng đầu khi sort giảm dần. Missing là giá trị nhỏ nhất, nên với DESCENDING nó nằm **cuối**: Amount của đơn 104 là missing. Từ khóa DESCENDING đặt **trước** tên cột mà nó tác động.
</details>

---

### Question 16: D2 – NODUPKEY with two BY columns [Predict Output]

```sas
proc sort data=orders out=cust_ctry nodupkey;
    by Customer Country;
run;
```

How many rows are in `cust_ctry`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 4**

**Giải thích:** NODUPKEY giữ dòng đầu tiên cho mỗi tổ hợp **khác nhau** của các cột BY. Có 4 tổ hợp: Brandt/DE, Kim/KR, Lopez/US, Okafor/NG.
</details>

---

### Question 17: D2 – IF without ELSE [Find & Fix]

```sas
data sized;
    set orders;
    length Size $ 5;
    if Qty>=3 then Size="Large";
    if Qty>=1 then Size="Small";
run;
```

How many rows have `Size="Large"`, and what is the fix? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 0 rows. Fix: change the second `if` to `else if`.**

**Giải thích:** Hai câu IF độc lập đều được thực thi. Với Qty ≥ 3, Size được gán "Large" rồi bị câu IF thứ hai **ghi đè** thành "Small", vì Qty ≥ 3 thì cũng ≥ 1. Dùng `else if` để câu sau chỉ chạy khi câu trước sai. Dòng có Qty missing không thỏa cả hai điều kiện nên Size để trống.
</details>

---

### Question 18: D2 – INTNX with 'same' alignment [Predict Output]

```sas
data due;
    set orders;
    where OrderID=106;
    DueDate=intnx('month', OrderDate, 1, 'same');
    format DueDate date9.;
run;
```

What is the formatted value of DueDate? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 30APR2024**

**Giải thích:** OrderDate của đơn 106 là 30MAR2024. Tiến 1 tháng với alignment `'same'` giữ nguyên số ngày, nên được 30APR2024. Nếu ngày gốc không tồn tại ở tháng đích (ví dụ 31MAR sang tháng 4), SAS trả về ngày cuối tháng đó (30APR).
</details>

---

### Question 19: D2 – SUM statement and missing values [Predict Output]

```sas
data running;
    set orders;
    Amount=Qty*Price;
    Total+Amount;
run;
```

What is **Total** in the last row? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 498**

**Giải thích:** Sum statement `Total+Amount;` tự RETAIN, bắt đầu từ 0 và **bỏ qua missing**: Amount missing ở đơn 104 không làm tổng thành missing. 31 + 120 + 62 + 66 + 40 + 80 + 99 = 498. Log vẫn có một NOTE "Missing values were generated" từ phép nhân Qty × Price.
</details>

---

### Question 20: D2 – Accumulating with an assignment statement [Predict Output]

```sas
data running2;
    set orders;
    Amount=Qty*Price;
    Total=Total+Amount;
run;
```

What is Total in the last row?

- A. 498
- B. 99
- C. . (missing)
- D. 0

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** Total được tạo bằng câu gán nên bị reset về missing ở đầu mỗi vòng lặp, và phép `+` với missing cho kết quả missing. Cả hai lỗi làm mọi dòng bằng missing. Cách sửa: dùng sum statement `Total+Amount;`, hoặc `retain Total 0;` kết hợp `Total=sum(Total,Amount);`.
</details>

---

### Question 21: D2 – FIRST. processing [Predict Output]

```sas
proc sort data=orders out=o_sort;
    by Customer OrderDate;
run;

data first_orders;
    set o_sort;
    by Customer;
    if first.Customer;
run;
```

How many rows are in `first_orders`, and what is the OrderID for Lopez? Answer: ________ / ________

<details><summary>Answer & explanation</summary>

**Answer: 4 / 101**

**Giải thích:** Mỗi khách hàng có một dòng `first.Customer = 1`, và có 4 khách hàng nên được 4 dòng. Dữ liệu được sort theo OrderDate bên trong mỗi khách hàng, nên dòng đầu là đơn sớm nhất. Lopez có đơn 101 (05JAN2024).
</details>

---

### Question 22: D2 – RETAIN to carry a value forward [Predict Output]

```sas
data filled;
    set orders;
    retain LastQty;
    if Qty ne . then LastQty=Qty;
run;
```

What is **LastQty** for OrderID 104? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 4**

**Giải thích:** Đơn 104 có Qty missing nên câu IF không gán. Nhờ RETAIN, LastQty vẫn giữ giá trị của dòng trước (đơn 103, Qty = 4). Đây là cách lấy giá trị không missing gần nhất. Không có RETAIN thì LastQty bị reset về missing.
</details>

---

### Question 23: D2 – SCAN with default delimiters [Predict Output]
What does `scan("Brandt-Meyer, Anna", 2)` return? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: Meyer**

**Giải thích:** Delimiter mặc định của SCAN gồm khoảng trắng, dấu phẩy, gạch ngang và nhiều ký tự khác. Chuỗi được tách thành Brandt | Meyer | Anna, nên từ thứ 2 là "Meyer". Muốn giữ nguyên tên có gạch nối thì viết `scan(x, 1, ',')`, được "Brandt-Meyer".
</details>

---

### Question 24: D2 – FIND with a modifier [Predict Output]
What does `find("Express Delivery", "delivery", "i")` return? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 9**

**Giải thích:** Modifier "i" làm việc tìm kiếm **không phân biệt chữ hoa và chữ thường**. "Express " chiếm vị trí 1 đến 8 (tính cả khoảng trắng), nên "D" ở vị trí 9. Không có "i" thì kết quả là 0, vì "delivery" viết thường không khớp với "Delivery".
</details>

---

### Question 25: D2 – TRANWRD and LOWCASE [Predict Output]
What does `lowcase(tranwrd("NEW YORK CITY", "CITY", ""))` display?

- A. `new york city`
- B. `NEW YORK`
- C. `new york` (with trailing blanks)
- D. `newyork`

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** TRANWRD thay mọi lần xuất hiện của "CITY". Thay bằng chuỗi rỗng thì SAS thực tế chèn một khoảng trắng, nên chỉ còn lại khoảng trắng ở cuối chuỗi. LOWCASE chuyển tất cả thành chữ thường, nên hiển thị "new york". D sai vì khoảng trắng giữa hai từ không bị xóa.
</details>

---

### Question 26: D2 – CATS vs CATX [Predict Output]
What do `cats("A ", " B", 1)` and `catx("-", "A ", " B", 1)` return?

- A. `A  B1` and `A - B-1`
- B. `AB1` and `A-B-1`
- C. `AB1` and `AB1`
- D. `A B 1` and `A-B-1`

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** CATS bỏ khoảng trắng đầu và cuối của **từng** đối số rồi nối lại, được "AB1". CATX cũng bỏ khoảng trắng như vậy và chèn delimiter "-" giữa các phần tử, được "A-B-1". Đối số số (1) được tự chuyển sang ký tự mà không có NOTE trong log.
</details>

---

### Question 27: D2 – MEAN with missing values [Predict Output]
What does `mean(4, ., 8)` return? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 6**

**Giải thích:** Các hàm thống kê (SUM, MEAN, MIN, MAX…) **bỏ qua missing**: (4 + 8) / 2 = 6, chứ không phải 12 / 3. Còn phép toán `(4 + . + 8) / 3` sẽ cho kết quả missing.
</details>

---

### Question 28: D2 – CEIL and FLOOR [Predict Output]
What does `ceil(-2.3) + floor(-2.3)` return? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: -5**

**Giải thích:** CEIL trả về số nguyên nhỏ nhất ≥ đối số, nên ceil(-2.3) = -2. FLOOR trả về số nguyên lớn nhất ≤ đối số, nên floor(-2.3) = -3. Tổng là -5. So sánh: INT(-2.3) = -2, vì INT bỏ phần thập phân về phía 0.
</details>

---

### Question 29: D2 – Macro variable and the dot delimiter [Predict Output]

```sas
%let yr=2024;
title "Orders &yr.Q1";
```

What title is displayed?

- A. `Orders &yr.Q1`
- B. `Orders 2024.Q1`
- C. `Orders 2024Q1`
- D. `Orders 2024 Q1`

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** Dấu chấm kết thúc tên macro variable và **bị xóa khi thay thế**, nên `&yr.Q1` thành "2024Q1". Muốn có dấu chấm trong kết quả thì viết hai dấu chấm (`&yr..Q1` thành "2024.Q1"). Thiếu dấu chấm thì SAS tìm macro variable tên `yrQ1`. A chỉ xảy ra khi chuỗi dùng nháy đơn.
</details>

---

### Question 30: D2 – INTCK with quarters [Predict Output]
What does `intck('qtr', '15JAN2024'd, '15JUL2024'd)` return? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 2**

**Giải thích:** Phương pháp mặc định (discrete) đếm số ranh giới đầu quý mà khoảng thời gian đi qua: 01APR2024 và 01JUL2024, tức 2. Với `'c'` (continuous) kết quả cũng là 2, vì từ 15/1 tới 15/7 là đúng 2 quý đầy đủ.
</details>

---

### Question 31: D2 – Name-prefix variable lists [Complete the Code]
The table has columns Score1, Score2, Score10 and ScoreAvg, and **all** of them must be included. Which expression averages them?

- A. `mean(Score1-Score10)`
- B. `mean(of Score1-Score10)`
- C. `mean(of Score:)`
- D. `mean(Score:)`

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** `Score:` chọn **mọi cột có tên bắt đầu bằng** "Score", và trong hàm phải có OF. B sai: `Score1-Score10` là danh sách theo số thứ tự liên tiếp, đòi hỏi đủ Score1 đến Score10 (sẽ lỗi khi thiếu Score3…) và không chọn được ScoreAvg. A và D thiếu OF; A còn bị hiểu là phép trừ.
</details>

---

### Question 32: D2 – INPUT with the COMMA informat [Predict Output]
What does `input("1,250.75", comma8.)` return? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 1250.75**

**Giải thích:** Informat COMMAw. bỏ dấu phẩy (và các ký tự như $) rồi đọc số. Độ rộng 8 vừa đủ cho 8 ký tự của chuỗi. Giá trị đã có dấu chấm thập phân nên không cần chỉ định phần thập phân trong informat.
</details>

---

### Question 33: D2 – PUT with a date format [Predict Output]
For OrderID 107, what does `put(OrderDate, monyy7.)` return? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: APR2024**

**Giải thích:** OrderDate là 01APR2024. MONYY7. viết 3 chữ cái tên tháng và 4 chữ số năm, được "APR2024". PUT luôn trả về chuỗi ký tự, nên đây là cách tạo cột tháng dạng chuỗi để nhóm hoặc nối chuỗi.
</details>

---

### Question 34: D2 – Automatic character-to-numeric conversion [Predict Output]

```sas
data conv;
    Code="0042";
    X=Code+1;
run;
```

What is X, and what appears in the log? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 43, with the NOTE "Character values have been converted to numeric values…"**

**Giải thích:** Dùng cột ký tự trong phép toán thì SAS **tự chuyển** sang số (bằng informat w.) và ghi NOTE vào log. "0042" là số hợp lệ nên X = 43. Muốn không có NOTE thì chuyển tường minh: `input(Code, 4.) + 1`.
</details>

---

### Question 35: D2 – DO UNTIL [Predict Output]

```sas
data grow;
    x=1;
    do until (x > 20);
        x=x*3;
    end;
run;
```

What is the final value of x? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 27**

**Giải thích:** DO UNTIL kiểm tra điều kiện ở **cuối** vòng lặp. Lần lượt: x = 3 (chưa > 20), x = 9 (chưa), x = 27 (đã > 20, dừng). Không có OUTPUT nên bảng chỉ có 1 dòng với x = 27.
</details>

---

### Question 36: D2 – PROC TRANSPOSE with ID [Predict Output]

```sas
data ctry_tot;
    input Country $ Total;
    datalines;
DE 80
KR 186
NG 40
US 192
;
run;

proc transpose data=ctry_tot out=ctry_wide;
    id Country;
    var Total;
run;
```

How many columns are in `ctry_wide`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 5**

**Giải thích:** Mỗi giá trị của cột ID trở thành một cột: DE, KR, NG, US. Thêm cột `_NAME_` (giá trị "Total"), tổng cộng 5 cột trong 1 dòng. Có thể bỏ `_NAME_` bằng `out=ctry_wide(drop=_name_)`. Giá trị ID phải là duy nhất, nếu không bước sẽ lỗi.
</details>

---

### Question 37: D2 – Nested DO loops [Predict Output]

```sas
data pairs;
    do i=1 to 3;
        do j=1 to i;
            output;
        end;
    end;
run;
```

How many rows are in `pairs`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 6**

**Giải thích:** Vòng lặp trong chạy i lần cho mỗi giá trị i: 1 + 2 + 3 = 6 lần OUTPUT. Các cặp (i, j) là (1,1), (2,1), (2,2), (3,1), (3,2), (3,3).
</details>

---

## Domain 3 – Error Handling (Q38–Q48)

### Question 38: D3 – A statement in the wrong step [Log Reading]
The log shows: `ERROR 180-322: Statement is not valid or it is used out of proper order.` Which code most likely caused it?

- A.
```sas
proc print data=orders;
    where Qty > 2;
run;
```
- B.
```sas
data big;
    set orders;
    if Qty > 2;
run;
```
- C.
```sas
proc print data=orders;
    if Qty > 2;
run;
```
- D.
```sas
proc print data=orders noobs;
run;
```

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** IF là câu lệnh của DATA step, không dùng được trong PROC PRINT, nên sinh ERROR 180-322. Trong PROC dùng WHERE để lọc dòng, như A. B và D hợp lệ.
</details>

---

### Question 39: D3 – Missing values NOTE [Log Reading]
Running `Amount=Qty*Price;` on `orders` produces:

```text
NOTE: Missing values were generated as a result of performing an operation on missing values.
      Each place is given by: (Number of times) at (Line):(Column).
      __ at 5:12
```

What number replaces `__`? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 1**

**Giải thích:** Chỉ đơn 104 có Qty missing, nên phép nhân tạo ra missing đúng 1 lần. NOTE này không phải lỗi nhưng báo rằng có dữ liệu thiếu. Dùng `if Qty ne . then Amount=Qty*Price;` thì NOTE không còn xuất hiện.
</details>

---

### Question 40: D3 – Invalid numeric data [Log Reading]
The log shows:

```text
NOTE: Invalid numeric data, Code='N/A' , at line 12 column 7.
Code=N/A X=. _ERROR_=1 _N_=3
```

Which statement is true?

- A. The step stopped at row 3.
- B. Row 3 was deleted from the output.
- C. _ERROR_ is written to the output table.
- D. SAS automatically tried to convert the character value N/A to a number, failed, set X to missing and _ERROR_ to 1, then continued with the next row.

<details><summary>Answer & explanation</summary>

**Answer: D**

**Giải thích:** Đây là lỗi dữ liệu khi SAS tự chuyển ký tự sang số. SAS ghi NOTE, in giá trị PDV của dòng lỗi (gồm cả `_N_=3`) và tiếp tục chạy. A sai vì step không dừng. C sai vì `_ERROR_` không bao giờ được ghi vào bảng. B sai vì dòng 3 vẫn được ghi, chỉ có X là missing.
</details>

---

### Question 41: D3 – Missing semicolon before ELSE [Find & Fix]

```sas
data region;
    set orders;
    if Country="US" then Region="Americas"
    else Region="Other";
run;
```

What is wrong?

- A. ELSE cannot follow an IF-THEN statement.
- B. A semicolon is missing after `Region="Americas"`, so the ELSE keyword becomes part of the THEN assignment and causes a syntax error.
- C. Region needs a LENGTH statement or the step fails.
- D. Nothing is wrong.

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** Mỗi câu lệnh phải kết thúc bằng `;`. Thiếu dấu `;` thì SAS đọc tiếp `else` như một phần của biểu thức gán và báo ERROR cú pháp. Sau khi sửa vẫn còn một vấn đề nhỏ: "Other" (5 ký tự) không bị cắt vì độ dài lấy theo "Americas" (8), nhưng nên khai báo LENGTH cho rõ ràng.
</details>

---

### Question 42: D3 – Character column in the VAR statement [Log Reading]

```sas
proc means data=orders;
    var Customer;
run;
```

What happens?

- A. An ERROR says that the variable Customer does not match the type prescribed for this list (VAR requires numeric columns), and no statistics are produced.
- B. PROC MEANS counts the customers.
- C. A WARNING appears, and the mean of the character values is computed.
- D. The step runs and shows N only.

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** VAR của PROC MEANS chỉ nhận cột **số**. Dùng cột ký tự sẽ gây ERROR "Variable Customer in list does not match type prescribed for this list." Muốn đếm theo giá trị ký tự thì dùng PROC FREQ, hoặc đưa Customer vào CLASS.
</details>

---

### Question 43: D3 – PUTLOG output [Predict Output]
Inside a DATA step, which statement writes **only** the row number and Amount to the log, for example `_N_=2 Amount=120`?

- A. `putlog _all_;`
- B. `putlog _N_ Amount;`
- C. `putlog _N_= Amount=;`
- D. `putlog "_N_= Amount=";`

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** Cú pháp `column=` in cả tên và giá trị. A in toàn bộ PDV (mọi cột cùng `_ERROR_` và `_N_`). B chỉ in giá trị, không có tên. D in nguyên văn chuỗi trong dấu nháy.
</details>

---

### Question 44: D3 – Automatic variables in the output [Concept]

```sas
data check;
    set orders;
    Row=_N_;
    Err=_ERROR_;
run;
```

How many columns does `check` have?

- A. 6
- B. 9
- C. 10
- D. 8

<details><summary>Answer & explanation</summary>

**Answer: D**

**Giải thích:** Bảng có 6 cột gốc cộng Row và Err, tổng 8. `_N_` và `_ERROR_` là biến tự động: có trong PDV khi thực thi nhưng **không được ghi** vào bảng. Muốn giữ giá trị của chúng thì phải gán sang cột thường, như ở đây.
</details>

---

### Question 45: D3 – Conditional PUTLOG with LAST. [Predict Output]

```sas
data _null_;
    set o_sort;
    by Customer;
    if last.Customer then putlog "NOTE: Done with " Customer=;
run;
```

`o_sort` is the table from Q21. How many NOTE lines are written? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 4**

**Giải thích:** `last.Customer = 1` một lần cho mỗi khách hàng, và có 4 khách hàng nên có 4 dòng NOTE. `DATA _NULL_` chạy DATA step mà không tạo bảng, rất tiện để kiểm tra dữ liệu bằng PUTLOG. Tiền tố "NOTE:" khiến log tô màu dòng đó như một ghi chú.
</details>

---

### Question 46: D3 – Missing period after a format name [Find & Fix]

```sas
data o3;
    set orders;
    format OrderDate date9;
run;
```

What happens to OrderDate in `o3`?

- A. It is displayed as 05JAN2024, the same as before.
- B. It is displayed as raw numbers (for example 23380). A new, empty column named date9 is created, and the log has a NOTE that date9 is uninitialized.
- C. An ERROR occurs and `o3` is not created.
- D. OrderDate becomes a character column.

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** Thiếu dấu chấm nên `date9` bị hiểu là **tên cột**. Câu FORMAT liệt kê hai cột (OrderDate và date9) mà không kèm format nào, nên **gỡ bỏ** format sẵn có của OrderDate, và cột hiển thị số thô. Không có ERROR, chỉ có NOTE "uninitialized". Đây là lỗi logic điển hình.
</details>

---

### Question 47: D3 – WARNING in a DROP list [Log Reading]
The log shows:

```text
WARNING: The variable Pricee in the DROP, KEEP, or RENAME list has never been referenced.
```

What does it mean?

- A. Pricee was dropped successfully.
- B. The step was not executed.
- C. The name in the DROP/KEEP/RENAME list is misspelled (it should be Price), so the intended column was not dropped. The step still runs.
- D. Price was converted to character.

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** Đây là WARNING chứ không phải ERROR: step vẫn chạy và tạo bảng, nhưng Price **vẫn còn** trong bảng vì tên trong danh sách bị gõ sai. Luôn đọc WARNING, vì kết quả có thể sai mà không có lỗi nào được báo.
</details>

---

### Question 48: D3 – Debugging [Find & Fix]
Fix every error, then run the program.

```sas
data us_orders;
    set orders
    where Country="US";
    Amount=Qty*Price
run;

proc print data=us_orders;
    sum Amount;
run;
```

What total Amount is shown? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 192**

```sas
data us_orders;
    set orders;
    where Country="US";
    Amount=Qty*Price;
run;

proc print data=us_orders;
    sum Amount;
run;
```

**Giải thích:** Có 2 lỗi: thiếu `;` sau SET, khiến WHERE thành một phần của câu SET, và thiếu `;` sau câu gán, khiến `run` bị nối vào biểu thức. Các đơn của US có Amount 31 + 62 + 99 = 192.
</details>

---

## Domain 4 – Generate Reports and Output (Q49–Q60)

### Question 49: D4 – PROC PRINT with SUM [Predict Output]

```sas
proc print data=amt noobs;
    var OrderID Amount;
    sum Amount;
run;
```

`amt` is the table from Q15. What total is shown for Amount? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 498**

**Giải thích:** SUM trong PROC PRINT cộng các giá trị không missing, được 498. NOOBS ẩn cột Obs. Giá trị missing của đơn 104 hiển thị là dấu chấm và không ảnh hưởng tới tổng.
</details>

---

### Question 50: D4 – PROC PRINT with BY and SUM [Predict Output]

```sas
proc sort data=orders out=by_ctry;
    by Country;
run;

proc print data=by_ctry;
    by Country;
    sum Qty;
run;
```

What Qty subtotal is shown for **DE**? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 2**

**Giải thích:** DE có 2 đơn: Qty là . (đơn 104) và 2 (đơn 107). SUM bỏ qua missing nên tổng phụ bằng 2. BY tạo một nhóm và một tổng phụ cho mỗi giá trị Country; dữ liệu phải được sort trước.
</details>

---

### Question 51: D4 – One-way PROC FREQ and missing values [Predict Output]

```sas
proc freq data=orders;
    tables Qty;
run;
```

How many value rows does the frequency table list, not counting the "Frequency Missing" line? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 5**

**Giải thích:** Các giá trị Qty không missing gồm 1, 2, 3, 4, 5, tức 5 dòng. Mặc định giá trị missing **không** nằm trong bảng mà chỉ hiện ở dòng "Frequency Missing = 1" bên dưới. Thêm option MISSING (`tables Qty / missing;`) thì missing thành một dòng riêng và được tính vào tỉ lệ phần trăm.
</details>

---

### Question 52: D4 – ORDER=FREQ [Predict Output]

```sas
proc freq data=orders order=freq;
    tables Country / nocum;
run;
```

Which Country is listed first? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: US**

**Giải thích:** ORDER=FREQ sắp theo tần số giảm dần: US 3 đơn, rồi DE và KR mỗi nước 2 đơn, NG 1 đơn. NOCUM ẩn các cột tích lũy.
</details>

---

### Question 53: D4 – Two-way table options [Concept]

```sas
proc freq data=orders;
    tables Country*Customer / norow nocol nopercent;
run;
```

What does each cell of the table contain?

- A. Frequency, Percent, Row Pct and Col Pct
- B. Frequency only
- C. Percent only
- D. Row Pct only

<details><summary>Answer & explanation</summary>

**Answer: B**

**Giải thích:** Bảng chéo mặc định có 4 con số mỗi ô. NOROW ẩn Row Pct, NOCOL ẩn Col Pct, NOPERCENT ẩn Percent, nên chỉ còn Frequency. NOCUM chỉ áp dụng cho bảng một chiều.
</details>

---

### Question 54: D4 – PROC MEANS N and NMISS [Predict Output]

```sas
proc means data=orders n nmiss;
    var Qty;
run;
```

What values of N and NMISS are shown? Answer: ________ / ________

<details><summary>Answer & explanation</summary>

**Answer: 7 / 1**

**Giải thích:** N đếm các giá trị **không missing** (7), NMISS đếm các giá trị missing (1). Thống kê mặc định của PROC MEANS là N, MEAN, STD, MIN, MAX; khi liệt kê thống kê trên câu lệnh PROC thì chỉ những thống kê đó được hiển thị.
</details>

---

### Question 55: D4 – PROC MEANS with CLASS [Predict Output]

```sas
proc means data=orders mean maxdec=2;
    class Country;
    var Price;
run;
```

What mean Price is shown for **KR**? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 71.00**

**Giải thích:** KR có hai giá 120 và 22: (120 + 22) / 2 = 71. MAXDEC=2 hiển thị 2 chữ số thập phân, nên ra 71.00. CLASS cho một dòng thống kê mỗi giá trị Country mà không cần sort trước.
</details>

---

### Question 56: D4 – OUTPUT table columns [Concept]

```sas
proc means data=orders noprint;
    class Country;
    var Price;
    output out=ctry_stats mean=AvgPrice;
run;
```

Besides Country and AvgPrice, which columns does SAS add automatically to `ctry_stats`?

- A. _N_ and _ERROR_
- B. _NAME_ and COL1
- C. _TYPE_ and _FREQ_
- D. None

<details><summary>Answer & explanation</summary>

**Answer: C**

**Giải thích:** `_TYPE_` cho biết tổ hợp CLASS của dòng: 0 là dòng tổng chung, 1 là dòng theo Country. `_FREQ_` là số dòng đầu vào của nhóm. Bảng có 5 dòng: 1 dòng tổng chung và 4 dòng cho các nước. Dùng `ways 1` hoặc option NWAY để bỏ dòng tổng chung. B là các cột của PROC TRANSPOSE.
</details>

---

### Question 57: D4 – Character format with OTHER [Predict Output]

```sas
proc format;
    value $ctry 'US'='United States'
                'KR'='Korea'
                other='Other';
run;

proc freq data=orders;
    tables Country;
    format Country $ctry.;
run;
```

What frequency is shown for **Other**? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 3**

**Giải thích:** OTHER gom mọi giá trị không khớp với các mục khác: DE (2) và NG (1), tổng 3. Format dùng để **nhóm** giá trị ngay trong báo cáo mà không cần tạo cột mới. Format ký tự bắt đầu bằng `$`; khi dùng thì phải có dấu chấm (`$ctry.`).
</details>

---

### Question 58: D4 – PROC UNIVARIATE median [Predict Output]

```sas
proc univariate data=orders;
    var Price;
run;
```

What median Price is reported? Answer: ________

<details><summary>Answer & explanation</summary>

**Answer: 31**

**Giải thích:** Giá sau khi sắp xếp: 8, 15.5, 15.5, 22, 40, 40, 99, 120. Có 8 giá trị, một số chẵn, nên median là trung bình của giá trị thứ 4 và thứ 5: (22 + 40) / 2 = 31. PROC UNIVARIATE còn in các bảng Moments, Quantiles và Extreme Observations.
</details>

---

### Question 59: D4 – Several ODS destinations at once [Concept]

```sas
ods pdf file="&outpath/orders.pdf" style=journal;
ods rtf file="&outpath/orders.rtf";

proc print data=orders;
run;

ods _all_ close;
```

What is the result?

- A. Both orders.pdf (Journal style) and orders.rtf contain the report, and `ODS _ALL_ CLOSE` closes every open destination.
- B. Only the PDF is created.
- C. An ERROR occurs because only one destination can be open at a time.
- D. The RTF file replaces the PDF file.

<details><summary>Answer & explanation</summary>

**Answer: A**

**Giải thích:** Nhiều destination có thể mở cùng lúc, và mỗi báo cáo được gửi tới tất cả các destination đang mở. `STYLE=` chỉ áp dụng cho destination có option đó (ở đây là PDF). `ODS _ALL_ CLOSE` đóng mọi destination; cũng có thể đóng từng cái bằng `ods pdf close;` và `ods rtf close;`.
</details>

---

### Question 60: D4 – PROC EXPORT tab-delimited [Complete the Code]
Complete the code to write `orders` to a tab-delimited file, overwriting it if it exists:

```sas
proc export data=orders outfile="&outpath/orders.txt"
            dbms=______ ______;
run;
```

Answer: ________ / ________

<details><summary>Answer & explanation</summary>

**Answer: `tab` / `replace`**

**Giải thích:** `DBMS=TAB` tạo file phân cách bằng tab; `REPLACE` ghi đè file nếu đã tồn tại (không có REPLACE thì export bị hủy khi file đã có). PROC EXPORT chỉ cần RUN để kết thúc, không cần QUIT.
</details>

---

## Answer summary

| # | Ans | # | Ans | # | Ans | # | Ans |
|---|---|---|---|---|---|---|---|
| 1 | tab | 16 | 4 | 31 | C | 46 | B |
| 2 | C | 17 | 0, else if | 32 | 1250.75 | 47 | C |
| 3 | B | 18 | 30APR2024 | 33 | APR2024 | 48 | 192 |
| 4 | 3 | 19 | 498 | 34 | 43 + NOTE | 49 | 498 |
| 5 | D | 20 | C | 35 | 27 | 50 | 2 |
| 6 | 3 | 21 | 4 / 101 | 36 | 5 | 51 | 5 |
| 7 | A | 22 | 4 | 37 | 6 | 52 | US |
| 8 | 8 | 23 | Meyer | 38 | C | 53 | B |
| 9 | D | 24 | 9 | 39 | 1 | 54 | 7 / 1 |
| 10 | 96 | 25 | C | 40 | D | 55 | 71.00 |
| 11 | 5 | 26 | B | 41 | B | 56 | C |
| 12 | 3 | 27 | 6 | 42 | A | 57 | 3 |
| 13 | C | 28 | -5 | 43 | C | 58 | 31 |
| 14 | B (False) | 29 | C | 44 | D | 59 | A |
| 15 | 102 / 104 | 30 | 2 | 45 | 4 | 60 | tab / replace |
