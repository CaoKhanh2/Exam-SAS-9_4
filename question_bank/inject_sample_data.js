// Makes the course-data questions self-contained: injects a sample DATA step (datalines) into each question's `code`
// and recomputes the answer key from that same sample data. The course originals stay in `courseOriginal`.
// Safe to rerun: it always starts from courseOriginal. Usage: node question_bank/inject_sample_data.js
// ponytail: answers are computed by hand-written JS that mirrors each SAS step, not by running SAS; verify on SAS ODA if in doubt.
const fs = require('fs'), path = require('path'), assert = require('assert');
const file = path.join(__dirname, 'questions.json');
const bank = JSON.parse(fs.readFileSync(file, 'utf8'));

const BEGIN = '/* --- Bắt đầu: Dữ liệu mẫu tự động tạo --- */', END = '/* --- Kết thúc: Dữ liệu mẫu --- */';
const MON = { JAN: 0, FEB: 1, MAR: 2, APR: 3, MAY: 4, JUN: 5, JUL: 6, AUG: 7, SEP: 8, OCT: 9, NOV: 10, DEC: 11 };
const sasDate = s => s === '.' ? null : (Date.UTC(+s.slice(5), MON[s.slice(2, 5)], +s.slice(0, 2)) - Date.UTC(1960, 0, 1)) / 864e5;
const yearOf = d => new Date(Date.UTC(1960, 0, 1) + d * 864e5).getUTCFullYear();
const sum = a => a.reduce((x, y) => x + (y ?? 0), 0);
const mean = a => { const v = a.filter(x => x != null); return sum(v) / v.length; };
const round = (x, d = 0) => Math.round(x * 10 ** d + 1e-9) / 10 ** d;
const count = (a, f) => a.filter(f).length;
const sortBy = (a, ...keys) => [...a].sort((x, y) => { for (const k of keys) { const p = x[k] ?? -Infinity, q = y[k] ?? -Infinity; if (p < q) return -1; if (p > q) return 1; } return 0; });

// ---------- sample tables: columns "Name:type" (n = numeric, d = date9., $N = character length N) ----------
const T = {};
const table = (name, cols, lines, extra = {}) => {
  const c = cols.split(' ').map(s => { const [n, t] = s.split(':'); return { n, t }; });
  const rows = lines.trim().split('\n').map(l => l.split('|').map(v => v.trim()));
  rows.forEach(r => assert.strictEqual(r.length, c.length, `${name}: ${r}`));
  T[name] = { cols: c, raw: rows, ...extra,
    rows: rows.map(r => Object.fromEntries(c.map((col, i) => [col.n, col.t === 'd' ? sasDate(r[i]) : col.t === 'n' ? (r[i] === '.' ? null : +r[i]) : r[i]]))) };
};

table('employee', 'EmpID:n Name:$15 JobTitle:$22 Department:$16 Country:$2 City:$12 Salary:n HireDate:d TermDate:d Status:$1', `
120101|Abbott, Ray|Administration Manager|Administration|US|San Diego|58200|01JAN1990|.|M
120102|Baker, Lan|Office Assistant II|Administration|US|San Diego|31500|01JAN2006|.|S
120103|Chen, Mai|Office Assistant I|Administration|AU|Sydney|28650|01JAN2014|.|O
120104|Dang, Minh|Office Assistant III|Administration|AU|Sydney|34800|01JAN2009|20JUN2017|M
120105|Evans, Kate|Secretary I|Administration|us|Philadelphia|30150|01JAN2011|.|S
120106|Fischer, Tom|Engineer I|Engineering|US|San Diego|52350|01JAN2016|.|O
120107|Garcia, Luis|Engineer II|Engineering|AU|Melbourne|61500|01JAN2004|.|M
120108|Hoang, Thu|Engineering Manager|Engineering|US|Philadelphia|98400|01JAN1986|.|M
120109|Ito, Ken|Accountant I|Accounts|AU|Sydney|45900|01JAN2012|.|S
120110|Jones, Amy|Accountant II|Accounts|US|San Diego|52800|01JAN2000|03FEB2015|O
120111|Kim, Ha|Auditor II|Group Financials|US|San Diego|64200|01JAN2003|.|S
120112|Lopez, Ana|Auditor III|Group Financials|AU|Sydney|79650|01JAN1995|.|M
120113|Martin, Joe|Auditor I|Group Financials|au|Melbourne|48300|01JAN2017|.|O
120114|Nguyen, An|Sales Rep. I|Sales|AU|Sydney|26550|01JAN2018|.|S
120115|Owen, Sue|Sales Rep. II|Sales|US|San Diego|28200|01JAN2010|.|M
120116|Park, Jin|Sales Rep. III|Sales|US|San Diego|29700|01JAN2007|.|O
120117|Quinn, Liz|Sales Rep. IV|Sales|US|San Diego|33450|01JAN1988|.|M
120118|Reed, Sam|Sales Rep. IV|Sales|AU|Sydney|31950|01JAN1997|.|S
120119|Silva, Rui|Sales Rep. II|Sales|us|Philadelphia|27300|01JAN2013|10OCT2016|O
120120|Tran, Hoa|Sales Rep. I|Sales|AU|Melbourne|25800|01JAN2016|.|S`);

// 121005 is an exact duplicate row; us/au/NZ break the Country rule; 121009 has TermDate before HireDate
table('employee_raw', 'EmpID:n Name:$15 JobTitle:$22 Department:$15 Country:$2 Salary:n BirthDate:d HireDate:d TermDate:d', `
121001|Adams, Kim|Logistics Coordinator|Logistics|US|41250|12MAR1980|15JUN2008|.
121002|Bui, Lan|Sales Rep. I|Sales|AU|26900|05JUL1990|01FEB2012|.
121003|Cole, Ian|Logistics Manager|Logistics|US|72400|30JAN1975|10SEP2014|.
121004|Diaz, Eva|Sales Rep. II|Sales|us|28350|17OCT1985|20MAY2011|.
121005|Eng, Tao|Accountant I|Accounts|AU|46200|02DEC1988|03MAR2016|.
121005|Eng, Tao|Accountant I|Accounts|AU|46200|02DEC1988|03MAR2016|.
121006|Ford, Al|Sales Rep. III|Sales|au|30100|21APR1982|11NOV2009|30JUN2015
121007|Gray, Pat|Logistics Clerk|Logistics|AU|33600|08AUG1992|14FEB2016|.
121008|Ho, Vy|Sales Rep. I|Sales|NZ|25950|19JAN1993|01JUL2013|.
121009|Ives, Max|Engineer II|Engineering|US|64800|25MAY1979|18AUG2005|01MAR2003
121010|Joy, Rae|Sales Rep. IV|Sales|US|34500|03SEP1970|07JAN1999|.
121011|Khan, Ali|Director|Administration|US|151000|11NOV1965|01APR1996|.
121012|Lam, Bao|Engineering Manager|Engineering|AU|98700|14FEB1972|22OCT2001|.`);

table('employee_current', 'EmpID:n Name:$12 JobTitle:$22 Department:$20 Salary:n', `
120201|Abel, Tim|Accountant I|Accounts|42350
120202|Brook, Ann|Accountant III|Accounts|61800
120203|Cruz, Leo|Technician I|Engineering|39150
120204|Dunn, Mia|Engineer II|Engineering|58600
120205|Ellis, Bo|Engineering Manager|Engineering|87400
120206|Fox, Jay|Warehouse Assistant|Logistics Management|30700
120207|Gill, Ray|Logistics Coordinator|Logistics Management|45250
120208|Hart, Zoe|Director|Logistics Management|112500
120209|Ince, Uma|Strategy Analyst|Strategy|66300
120210|Juan, Pia|Strategy Manager|Strategy|94450`, { formats: 'Salary dollar10.' });

table('employee_new', 'EmpID:$9 Name:$12 HireDate:$10 AnnualSalary:$10', `
EMP120301|Ang, Lee|2009-03-14|$41,500
EMP120302|Bach, Mo|2011-01-16|$56,250
EMP120303|Cass, Di|2015-07-21|$38,900
EMP120304|Dorn, Al|2002-11-30|$72,100
EMP120305|Eadie, Jo|2018-05-27|$29,750`);

table('employee_addresses', 'Employee_ID:n Street_Number:n Street_Name:$15 City:$12', `
120108|1147|Elm St|Philadelphia
120101|46|Harbor Dr|San Diego
120116|305|Pine Ave|San Diego
120103|78|George St|Sydney
120120|12|Collins St|Melbourne
120107|920|Flinders Ln|Melbourne
120112|5|Pitt St|Sydney
120102|233|Bay Blvd|San Diego
120111|61|Ocean Ave|San Diego
120105|1802|Market St|Philadelphia
120118|44|Kent St|Sydney
120106|710|Mesa Rd|San Diego
120113|98|Swan St|Melbourne
120117|15|Coast Hwy|San Diego
120109|307|King St|Sydney
120114|21|Castle St|Sydney
120199|8|Lake Rd|San Diego`);

table('employee_donations', 'EmpID:n Qtr1:n Qtr2:n Qtr3:n Qtr4:n', `
120102|10|10|.|15
120105|20|20|20|20
120107|.|25|.|.
120111|5|5|5|5
120115|15|.|15|15
120117|25|25|25|25
120118|.|.|10|.
120130|10|10|10|10`);

table('employee_training', 'Name:$12 Compliance_Training:d Corporate_Security:d On_the_Job_Safety:d', `
Lee, Sun|12APR2018|.|03JUL2018
Abbott, Ray|07APR2018|02MAY2018|.
Nash, Ty|.|19APR2018|21AUG2018
Cho, Eun|07APR2018|07JUN2018|27APR2018
Bell, Ida|15JAN2018|.|.
Moss, Kai|28APR2018|11SEP2018|05APR2018
Diaz, Rob|.|.|14DEC2018
Park, Lia|02JUL2018|23APR2018|.`);

table('profit', 'Order_Date:d Order_Source:$8 Product_ID:n Profit:n', `
05JAN2018|Retail|210200100009|12.40
14FEB2018|Internet|210200300073|8.75
02MAR2018|Retail|220101400387|21.10
19APR2018|Catalog|230100500026|5.60
08MAY2018|Retail|210200100009|13.05
23JUN2018|Retail|210200300073|9.90
11JUL2018|Internet|220101400387|18.30
30AUG2018|Retail|230100500026|6.45
15SEP2018|Retail|210200100009|11.80
04OCT2018|Catalog|210200300073|7.25
21NOV2018|Retail|220101400387|20.40
03DEC2018|Retail|230100500026|6.10
17DEC2018|Retail|210200100009|12.95
28DEC2018|Internet|210200300073|9.15`, { formats: 'Product_ID 12.' });

table('products', 'Product_ID:n Product_Name:$20', `
240200100118|Tennis Racket
210200300073|Running Shoes
230100500026|Water Bottle
240100100434|Golf Gloves
210200100009|Soccer Ball
220101400387|Ski Jacket`, { formats: 'Product_ID 12.' });

table('qtr_sales', 'Customer_ID:n BirthDate:d Qtr1:n Qtr2:n Qtr3:n Qtr4:n', `
4|08FEB1984|120|95|150|110
5|21JUN1979|200|180|90|160
9|13NOV1990|80|60|70|50
10|02APR1986|150|140|130|120
11|30SEP1975|.|210|190|105
12|17JAN1988|90|110|100|101
16|05MAY1992|300|20|30|95
17|25DEC1981|130|120|140|.
19|11AUG1983|175|160|150|140
20|07MAR1977|60|70|.|250`);

const salesCols = id => `Order_ID:n Order_Type:n ${id}:n Customer_ID:n Order_Date:d Delivery_Date:d`;
table('m7_sales', salesCols('EmpID'), `
7001|1|120121|27|02JUL2019|06JUL2019
7002|2|120145|41|05JUL2019|12JUL2019
7003|1|120121|9|08JUL2019|10JUL2019
7004|3|120160|52|11JUL2019|20JUL2019
7005|1|120145|27|15JUL2019|18JUL2019
7006|2|120127|13|19JUL2019|27JUL2019
7007|1|120160|70|24JUL2019|26JUL2019
7008|3|120127|88|29JUL2019|07AUG2019`);
table('m8_sales', salesCols('Employee_ID'), `
8001|1|120121|31|01AUG2019|04AUG2019
8002|1|120127|45|06AUG2019|09AUG2019
8003|2|120145|27|12AUG2019|19AUG2019
8004|1|120160|9|17AUG2019|20AUG2019
8005|3|120121|66|22AUG2019|31AUG2019
8006|2|120127|18|28AUG2019|02SEP2019`);
table('m9_sales', salesCols('EmpID'), `
9001|2|120145|52|03SEP2019|10SEP2019
9002|1|120160|27|07SEP2019|09SEP2019
9003|1|120121|73|11SEP2019|14SEP2019
9004|3|120127|41|16SEP2019|25SEP2019
9005|1|120145|9|20SEP2019|23SEP2019
9006|2|120160|35|24SEP2019|01OCT2019
9007|1|120121|63|28SEP2019|30SEP2019`);

table('shoes_summary', 'Region:$15 TotalStores:n TotalProfit:n ProfitPerStore:n', `
Asia|14|96782|6913
Canada|37|263255|7115
Pacific|45|271800|6040
Western Europe|62|485460|7830`);

// Code = the Cont values of sashelp.demographics, so PQ 3.11 still sums the real sashelp data
table('continent_codes', 'Code:n Continent:$15', `
91|North America
92|South America
93|Europe
94|Africa
95|Asia
96|Oceania`);

table('country_info', 'Country:$12 Continent:n', `
Canada|1
Brazil|2
France|3
Kenya|4
Japan|5
Mexico|1
Peru|2
Germany|3
Vietnam|5
Chile|2
El Salvador|1
Australia|6`);

table('final_tourism', 'Country:$10 Continent:$15 Category:$40 y2014:n', `
France|Europe|Arrivals|86900000
Germany|Europe|Arrivals|33000000
Japan|Asia|Arrivals|13400000
Vietnam|Asia|Arrivals|7900000
Kenya|Africa|Arrivals|1260000
Canada|North America|Arrivals|16500000
Mexico|North America|Arrivals|29300000
France|Europe|Tourism expenditure in other countries|48000000000
Germany|Europe|Tourism expenditure in other countries|92400000000
Japan|Asia|Tourism expenditure in other countries|21600000000
Kenya|Africa|Tourism expenditure in other countries|1500000000`, { formats: 'y2014 comma18.' });

table('tourism', 'Country:$10 _2008:$10', `
France|1200
Germany|..
Japan|340
Kenya|525
Peru|88
Chile|..
Mexico|2750
Canada|610
Vietnam|430`);

table('orders', 'Delivery_Date:d Retail_Price:n Cost_Price:n Quantity:n', `
03JAN2019|45.60|10.20|2
01JAN2019|120.00|35.50|3
03JAN2019|18.90|6.10|1
02JAN2019|64.40|15.75|2
01JAN2019|33.20|9.80|2
05JAN2019|210.00|52.00|3
02JAN2019|27.50|8.40|1
04JAN2019|88.80|20.10|4
05JAN2019|15.00|4.25|2
04JAN2019|52.30|11.90|2`);

table('storm_summary', 'Season:n Name:$10 Basin:$2 MaxWindMPH:n MaxWindKM:n StartDate:d EndDate:d', `
1980|AGATHA|EP|115|185|09JUN1980|15JUN1980
1980|ALBINE|SI|80|129|27NOV1979|06DEC1979
1980|ALLEN|NA|190|306|31JUL1980|11AUG1980
2016|MATTHEW|NA|167|269|28SEP2016|09OCT2016
2016|MERANTI|WP|190|306|08SEP2016|17SEP2016
2016|WINSTON|SP|178|286|07FEB2016|03MAR2016
2017|MORA|NI|69|111|28MAY2017|31MAY2017
2017|HARVEY|na|132|212|17AUG2017|01SEP2017`);
table('storm_summary_small', T.storm_summary.cols.map(c => `${c.n}:${c.t}`).join(' '), T.storm_summary.raw.slice(0, 5).map(r => r.join('|')).join('\n'));

table('storm_2017', 'Name:$10 Basin:$2 MaxWindMPH:n StartDate:d', `
HARVEY|NA|132|17AUG2017
IRMA|NA|178|30AUG2017
MARIA|NA|173|16SEP2017
HILARY|EP|138|21JUL2017
NORU|WP|109|19JUL2017
LAN|WP|161|15OCT2017`);

table('storm_damage', 'Event:$18 Date:d Cost:n Summary:$70', `
Hurricane Harvey|25AUG2017|125000000000|Made landfall as a Category 4 hurricane in Texas.
Hurricane Irma|10SEP2017|50000000000|Struck the Florida Keys as a category 4 storm.
Hurricane Katrina|29AUG2005|125000000000|Category 3 landfall in Louisiana.
Hurricane Sandy|29OCT2012|65000000000|Post-tropical at landfall, no category.`, { formats: 'Cost dollar18.' });

table('storm_subbasincodes', 'Sub_Basin:$2 SubBasin_Name:$17', `
AS|Arabian Sea
BB|Bay of Bengal
EA|Eastern Australia
WA|Western Australia
CP|Central Pacific
CS|Caribbean Sea
GM|Gulf of Mexico
NA|North Atlantic
MM|Missing`);

table('storm_top4_wide', 'Season:n Basin:$2 Name:$10 Wind1:n Wind2:n Wind3:n Wind4:n', `
2016|NA|MATTHEW|167|160|155|150
2016|WP|MERANTI|190|185|180|170
2017|NA|IRMA|178|175|170|165
2017|EP|HILARY|138|130|125|120`);

table('weather_zurich', 'Date:d Rain_mm:n', `
01JAN2017|0
02JAN2017|3.2
03JAN2017|.
04JAN2017|7.5
05JAN2017|0
06JAN2017|1.1
07JAN2017|.
08JAN2017|4.8`);

table('weather_houston', 'Date:d Month:n DailyRain:n', `
01JAN2017|1|0
02JAN2017|1|0.45
03JAN2017|1|1.20
01FEB2017|2|0
02FEB2017|2|0.30
03FEB2017|2|0
01MAR2017|3|2.15
02MAR2017|3|0
03MAR2017|3|0.60`);

table('class_quiz', 'Name:$8 Quiz1:n Quiz2:n Quiz3:n Quiz4:n Quiz5:n', `
Alfred|8|9|7|10|8
Barbara|9|8|9|7|10
James|6|7|8|7|6
Mary|10|9|10|9|8`);

table('class_new2', 'Student:$9 Sex:$1 Age:n', `
Elizabeth|F|12
Jonathan|M|13
Christina|F|14`);

table('class_test_narrow', 'Name:$8 TestSubject:$7 TestScore:n', `
Alfred|Math|82
Alfred|Reading|76
Barbara|Math|91
Barbara|Reading|88
Carol|Math|67
Carol|Reading|94`);

table('class_update', 'Name:$8 Sex:$1 Age:n Height:n Weight:n', `
Alfred|M|14|69|112.5
Alice|F|13|56.5|84
Barbara|F|13|65.3|98
David|M|13|62.1|101
Henry|M|14|63.5|102.5`);
table('class_teachers', 'Name:$8 Grade:n Teacher:$8', `
Alfred|9|Smith
Alice|8|Thomas
Barbara|8|Thomas
Carol|8|Thomas
Henry|9|Smith`);

table('savings', 'Name:$8 Amount:n', `
James|250
Linda|300
Mary|275
Robert|350`);

table('stocks2', 'Stock:$4 Date:$9 Volume:$12', `
IBM|03JAN2017|3,021,423
IBM|10JAN2017|4,118,276
MSFT|03JAN2017|20,694,101
MSFT|10JAN2017|18,593,004`);

table('cars', 'Make:$10 Model:$10 MPG:n', `
Toyota|Corolla|32
Ford|F-150|19
Honda|Civic|36`);
table('records', 'Code:$1 Amount:n', `
1|150000
2|98000
1|210000`);

// ---------- SAS text for one table ----------
function dataStep(lib, name) {
  const t = T[name], len = t.cols.map(c => c.t[0] === '$' ? `${c.n} $ ${c.t.slice(1)}` : `${c.n} 8`).join(' ');
  const dates = t.cols.filter(c => c.t === 'd').map(c => c.n);
  const fmt = [dates.length ? `${dates.join(' ')} date9.` : '', t.formats || ''].filter(Boolean).join(' ');
  const input = t.cols.map(c => c.t === 'd' ? `${c.n} :date9.` : c.t[0] === '$' ? `${c.n} $` : c.n).join(' ');
  return [`data ${lib}.${name};`, `    infile datalines dlm="|" dsd;`, `    length ${len};`, fmt && `    format ${fmt};`,
    `    input ${input};`, `    datalines;`, ...t.raw.map(r => r.join('|')), `;`, `run;`].filter(Boolean).join('\n');
}
const LIBDIR = { cr: 'cr', crb: 'cr', pg2: 'pg2', cert: 'cert' }; // cr and crb share one folder, like the course
function block(q, refs) {
  const libs = [...new Set(refs.map(r => r.lib))], dirs = [...new Set(libs.map(l => LIBDIR[l]))];
  const src = [q.code, q.solutionCode].join('\n');
  const lines = [BEGIN, 'options dlcreatedir;'];
  if (libs.some(l => l === 'cr' || l === 'crb')) lines.push('libname cr "%sysfunc(pathname(work))/cr";', 'libname crb "%sysfunc(pathname(work))/cr";');
  for (const l of libs) if (LIBDIR[l] === l && l !== 'cr') lines.push(`libname ${l} "%sysfunc(pathname(work))/${l}";`);
  if (/&path\b/.test(src)) lines.push('%let path=%sysfunc(pathname(work))/cr;');
  if (/&outpath\b/.test(src)) lines.push('%let outpath=%sysfunc(pathname(work));');
  assert(dirs.length);
  const seen = new Set();
  for (const r of refs) if (!seen.has(r.name)) { seen.add(r.name); lines.push('', dataStep(r.lib, r.name)); }
  if (q.extra) lines.push('', q.extra);
  lines.push(END);
  return lines.join('\n');
}

// ---------- answers from the sample data ----------
const E = T.employee.rows, RAW = T.employee_raw.rows, CUR = T.employee_current.rows;
const dedupRaw = (() => { const s = sortBy(RAW, ...T.employee_raw.cols.map(c => c.n)); return s.filter((r, i) => i === 0 || JSON.stringify(r) !== JSON.stringify(s[i - 1])); })();
const active = E.filter(r => r.TermDate == null);
const yearsEmp = r => { const y = 2019 - yearOf(r.HireDate); assert.strictEqual(sasDate(`01JAN${2019 - y}`), r.HireDate, 'HireDate must be 01JAN for an exact YRDIF'); return y; };
const bonus = sortBy(active.map(r => ({ ...r, YearsEmp: yearsEmp(r) })), 'YearsEmp').reverse(); // descending, stable for unique values
const byGroup = (rows, k) => rows.reduce((m, r) => (m[r[k]] = m[r[k]] || []).push(r) && m, {});
const deptSalary = rows => Object.fromEntries(Object.entries(byGroup(rows, 'Department')).map(([d, rs]) => { const s = sortBy(rs, 'Salary'); return [d, { total: sum(s.map(r => r.Salary)), low: s[0].JobTitle, high: s.at(-1).JobTitle }]; }));
const addrSorted = sortBy(T.employee_addresses.rows.map(r => ({ ...r, EmpID: r.Employee_ID })), 'EmpID');
const empFull = E.map(e => ({ ...e, ...(addrSorted.find(a => a.EmpID === e.EmpID) || { Street_Number: null }) }));
const don = T.employee_donations.rows, empIds = new Set(E.map(r => r.EmpID));
const donation = don.filter(d => empIds.has(d.EmpID)).map(d => ({ ...d, Name: E.find(e => e.EmpID === d.EmpID).Name, TotalDonation: sum([d.Qtr1, d.Qtr2, d.Qtr3, d.Qtr4]) }));
const q3 = [...T.m7_sales.rows, ...T.m8_sales.rows, ...T.m9_sales.rows];
const m7other = T.m7_sales.rows.filter(r => r.Order_Type !== 1);
const trainSorted = sortBy(T.employee_training.rows, 'Name');
const narrow3 = trainSorted.flatMap(r => ['Compliance_Training', 'Corporate_Security', 'On_the_Job_Safety'].map(c => r[c]));
const narrow2 = trainSorted.flatMap(r => ['Compliance_Training', 'Corporate_Security'].map(c => r[c]));
const monthOf = d => new Date(Date.UTC(1960, 0, 1) + d * 864e5).getUTCMonth();
const ordersAcc = (() => { let acc = 0; return Object.entries(byGroup(sortBy(T.orders.rows, 'Delivery_Date'), 'Delivery_Date')).sort((a, b) => a[0] - b[0]).map(([, rs]) => { const day = sum(rs.map(r => r.Retail_Price - r.Cost_Price * r.Quantity)); acc += day; return { day, acc }; }); })();
const productsNoSales = sortBy(T.products.rows.filter(p => !T.profit.rows.some(r => r.Product_ID === p.Product_ID)), 'Product_ID');
const std = a => { const m = mean(a); return Math.sqrt(sum(a.map(x => (x - m) ** 2)) / (a.length - 1)); };
const median = a => { const s = [...a].sort((x, y) => x - y), n = s.length; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; };
const mode = a => { const c = {}; a.filter(x => x != null).forEach(x => c[x] = (c[x] || 0) + 1); const top = Math.max(...Object.values(c)), ks = Object.keys(c).filter(k => c[k] === top); assert.strictEqual(ks.length, 1, 'mode must be unique'); return +ks[0]; };
const csvBytes = (() => { // PROC EXPORT DBMS=CSV: header + formatted values, values with a comma quoted, LF line ends
  const dollar = n => '$' + n.toLocaleString('en-US'), q = v => /,/.test(v) ? `"${v}"` : v;
  const lines = ['EmpID,Name,JobTitle,Department,Salary', ...CUR.map(r => [r.EmpID, r.Name, r.JobTitle, r.Department, dollar(r.Salary)].map(String).map(q).join(','))];
  return Buffer.byteLength(lines.join('\n') + '\n');
})();
const unique = (a, f) => { const best = Math.max(...a.map(f)); assert.strictEqual(a.filter(x => f(x) === best).length, 1, 'tie'); return a.find(x => f(x) === best); };

const num = (x, d = 0) => { const s = round(x, d).toFixed(d), c = Number(s).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }); return [...new Set([s, c])]; };
const pct = x => [round(x, 2).toFixed(2), round(x, 2).toFixed(2) + '%'];
const txt = (...a) => a;

// q.id -> { a: accepted answers computed from the sample data, stem: [[old, new]], extra: SAS appended to the data block }
// a omitted = the answer does not depend on the data values (syntax, log message, concept) and is kept.
const Q = {
  'mock2-q4': { tables: ['cr.continent_codes', 'cr.country_info'] },
  'mock2-q34': {}, 'mock2-q43': {}, 'set1-q2': {}, 'cr1-1.4-q7': {}, 'cr3-3.6-q10': {},
  'cr1-pq1.03-1': { tables: ['cr.continent_codes', 'cr.country_info', 'cr.profit'], a: txt('3'),
    note: 'Thư viện cr trỏ tới thư mục WORK/cr: nếu trong phiên SAS bạn đã chạy câu khác tạo thêm bảng cr.* thì số bảng sẽ lớn hơn.' },
  'cr1-pq1.07-1': { a: txt(String(unique(Object.entries(byGroup(RAW, 'EmpID')), ([, v]) => v.length)[0])) },
  'cr1-pq1.07-2': { a: txt(String(count(RAW, r => !['US', 'AU'].includes(r.Country)))) },
  'cr1-pq1.07-3': { a: txt(unique(Object.entries(byGroup(RAW, 'Department')), ([, v]) => v.length)[0]) },
  'cr1-pq1.07-4': { a: txt(String(count(RAW, r => r.TermDate != null && r.HireDate > r.TermDate))) },
  'cr1-pq1.08-1': { a: txt(String(dedupRaw[9].EmpID)) },
  'cr1-pq1.08-2': { a: txt(String(yearOf(Math.max(...dedupRaw.filter(r => /Logistics/.test(r.JobTitle)).map(r => r.HireDate))))) },
  'cr1-pq1.08-3': { a: num(mean(dedupRaw.filter(r => r.HireDate >= sasDate('01JAN2010') && r.TermDate == null).map(r => r.Salary)), 2) },
  'cr1-pq1.08-4': { a: num(dedupRaw.map(r => r.Salary).sort((x, y) => y - x)[2]) },
  'cr1-pq1.10-1': { a: txt(String(count(active, r => r.Department === 'Sales'))) },
  'cr1-pq1.10-2': { a: txt(String(count(active, r => r.Department === 'Sales' && ['II', 'III'].includes(r.JobTitle.slice(11))))) },
  'cr1-pq1.11-1': { a: txt(String(bonus.length)) },
  'cr1-pq1.11-2': { a: txt(String(bonus[0].YearsEmp)) },
  'cr1-pq1.11-3': { a: txt(String(count(bonus, r => r.YearsEmp >= 10))) },
  'cr1-pq1.11-4': { a: num(bonus.at(-1).Salary * (bonus.at(-1).YearsEmp >= 10 ? .03 : .02), 2) },
  'cr1-pq1.13-1': { a: txt(unique(Object.entries(byGroup(E, 'City')), ([, v]) => v.length)[0]) },
  'cr1-pq1.13-2': { a: pct(100 * count(E, r => r.Department === 'Sales') / E.length) },
  'cr1-pq1.13-3': { a: txt(String(new Set(E.map(r => r.JobTitle)).size)) },
  'cr1-pq1.14-1': { a: txt(String(count(T.profit.rows, r => r.Order_Source === 'Retail' && monthOf(r.Order_Date) === 11))) },
  'cr1-pq1.14-2': { a: pct(100 * count(T.profit.rows, r => r.Order_Source === 'Retail') / T.profit.rows.length) },
  'cr1-pq1.15-1': { a: num(sum(E.filter(r => r.Department === 'Sales').map(r => r.Salary))) },
  'cr1-pq1.15-2': { a: num(mean(E.filter(r => r.JobTitle === 'Sales Rep. IV').map(r => r.Salary))) },
  'cr1-pq1.16-1': { a: txt(String(new Set(E.map(r => r.Department + '|' + r.City)).size)) },
  'cr1-pq1.16-2': { a: num(mean(E.filter(r => r.Department === 'Administration' && r.City === 'Sydney').map(r => r.Salary)), 2) },
  'cr1-pq1.19-1': { a: txt(String(Math.max(1, Math.round(csvBytes / 1024))), '1 KB', '1KB'),
    note: `File mẫu khoảng ${csvBytes} byte, nên Properties hiển thị khoảng 1 KB.` },
  'cr1-pq1.19-2': {},
  'cr3-pq3.01-1': { a: txt(String(count(active, r => r.Country.toUpperCase() === 'US'))) },
  'cr3-pq3.01-2': { a: txt(String(count(active, r => r.Country.toUpperCase() !== 'US'))) },
  'cr3-pq3.03-1': { a: num(deptSalary(CUR).Strategy.total) },
  'cr3-pq3.03-2': { a: txt(String(3 * Object.keys(deptSalary(CUR)).length)) },
  'cr3-pq3.03-3': { a: num(deptSalary(CUR).Engineering.total * 1.03 ** 3) },
  'cr3-pq3.06-1': { a: num(deptSalary(CUR).Accounts.total) },
  'cr3-pq3.06-2': { a: txt(deptSalary(CUR).Engineering.low) },
  'cr3-pq3.06-3': { a: txt(deptSalary(CUR)['Logistics Management'].high) },
  'cr3-pq3.09-1': { a: txt(String(sasDate((([y, m, d]) => `${d}${Object.keys(MON)[m - 1]}${y}`)(T.employee_new.rows[1].HireDate.split('-'))))) },
  'cr3-pq3.09-2': {},
  'cr3-pq3.11-1': {}, 'cr3-pq3.11-2': {}, // labels for the real sashelp.demographics codes: the course answers still hold
  'cr3-pq3.12-1': { a: txt(String(count(E, r => r.Status === 'O'))) },
  'cr3-pq3.12-2': { a: txt(String(count(E, r => r.City === 'San Diego' && r.Salary >= 50000 && r.Salary <= 100000))) },
  'cr3-pq3.13-1': { a: txt(String(q3.length)) },
  'cr3-pq3.13-2': { a: txt('6') },
  'cr3-pq3.13-3': { a: txt(String(count(q3, r => r.Order_Type === 1))) },
  'cr3-pq3.14-1': { a: txt(String(empFull.length)) },
  'cr3-pq3.14-2': { a: txt(String(empFull[11].EmpID)), stem: [['row 27', 'row 12']] },
  'cr3-pq3.14-3': { a: txt(String(empFull[6].Street_Number)), stem: [['row 20', 'row 7']] },
  'cr3-pq3.15-1': { a: txt(String(donation.length)) },
  'cr3-pq3.15-2': { a: txt(String(donation.find(d => d.Name === 'Quinn, Liz').TotalDonation)), stem: [['Hill, Ronald', 'Quinn, Liz']] },
  'cr3-pq3.15-3': { a: txt(String(count(E, e => !don.some(d => d.EmpID === e.EmpID)))) },
  'cr3-pq3.16-1': { a: txt(String(5 * T.shoes_summary.rows.length)) },
  'cr3-pq3.16-2': { a: num(T.shoes_summary.rows.find(r => r.Region === 'Asia').ProfitPerStore * 1.03 ** 5) },
  'cr3-pq3.20-1': { a: txt(String(narrow3.length)) },
  'cr3-pq3.20-2': { a: txt(String(count(narrow3, d => d != null && monthOf(d) === 3))) },
  'cr3-pq3.20-3': { a: txt(String(count(narrow3, d => d == null))) },
  'crx-cr4-test-q1': { a: txt(unique(Object.entries(byGroup(T.final_tourism.rows.filter(r => r.Category === 'Arrivals'), 'Continent')), ([, v]) => mean(v.map(r => r.y2014)))[0].toLowerCase()) },
  'crx-cr4-test-q2': { a: num(mean(T.final_tourism.rows.filter(r => /tourism expenditure in other countries/.test(r.Category.toLowerCase())).map(r => r.y2014))) },
  'crx-pq5.02': { a: txt(String(count(T.qtr_sales.rows, r => r.Qtr4 > 100 && sum([r.Qtr1, r.Qtr2, r.Qtr3, r.Qtr4]) > 500))) },
  'crx-pq5.03-1-1': { a: txt(String(m7other.length)) },
  'crx-pq5.03-1-2': { a: txt(String(T.m7_sales.cols.length - 2)) },
  'crx-pq5.03-1-3': { a: txt(String(m7other[2].Customer_ID)) },
  'crx-pq5.03-2-1': { a: txt(String(count(T.country_info.rows, r => r.Continent === 2))) },
  'crx-pq5.03-2-2': {},
  'crx-pq5.03-2-3': { a: txt(T.country_info.rows.filter(r => r.Continent === 1)[2].Country.toLowerCase()), stem: [['row 33', 'row 3']] },
  'crx-pq5.04-1': {}, 'crx-pq5.04-2-1': {},
  'crx-pq5.04-2-2': { a: num(mean(don.filter(r => [r.Qtr1, r.Qtr2, r.Qtr3, r.Qtr4].includes(null)).map(r => r.Qtr2)), 1) },
  'crx-pq5.05-1-1': { a: txt(String(T.qtr_sales.rows[5].Customer_ID).padStart(5, '0')) },
  'crx-pq5.05-1-2': { a: num(std(T.qtr_sales.rows.map(r => r.Customer_ID)), 2) },
  'crx-pq5.05-2': { a: num(median(T.tourism.rows.filter(r => r._2008 !== '..').map(r => +r._2008))) },
  'crx-pq5.06-1': { a: num(sortBy(E.filter(r => r.Department === 'Administration'), 'Salary')[4].Salary) },
  'crx-pq5.06-2': { a: num(sum(sortBy(E.filter(r => r.Department === 'Administration'), 'Salary').slice(0, 4).map(r => r.Salary))), stem: [['row 15', 'row 4']] },
  'crx-pq5.07-1-1': { a: txt(deptSalary(E)['Group Financials'].high.toLowerCase()) },
  'crx-pq5.07-1-2': { a: num(deptSalary(E).Sales.total) },
  'crx-pq5.07-2-1': { a: num(ordersAcc[2].day, 2), stem: [['row 50', 'row 3']] },
  'crx-pq5.07-2-2': { a: num(ordersAcc[4].acc, 2), stem: [['row 60', 'row 5']] },
  'crx-pq5.11-1-1': { a: txt(String(donation.length)) },
  'crx-pq5.11-1-2': { a: txt(String(donation[4].TotalDonation)), stem: [['row 42', 'row 5']] },
  'crx-pq5.11-2-1': { a: txt(String(count(T.profit.rows, r => T.products.rows.some(p => p.Product_ID === r.Product_ID)))) },
  'crx-pq5.11-2-2': { a: txt(String(productsNoSales[1].Product_ID)), stem: [['row 13', 'row 2']] },
  'crx-pq5.12-2-1': { a: txt((d => { const t = new Date(Date.UTC(1960, 0, 1) + d * 864e5); return String(t.getUTCDate()).padStart(2, '0') + Object.keys(MON)[t.getUTCMonth()].toLowerCase() + t.getUTCFullYear(); })(narrow2[5])), stem: [['row 20', 'row 6']] },
  'crx-pq5.12-2-2': { a: txt(String(narrow2.length)) },
  'crx-pq5.12-2-3': { a: num(mode(narrow2)) },
  'p2l1-act-p201a04-1': { a: txt(String(T.storm_summary_small.rows[1].EndDate - T.storm_summary_small.rows[1].StartDate)) },
  'p2l1-act-01_2_q3': {}, 'p2l2-act-p202a01-3': {}, 'p2l2-act-02_1_q2': {}, 'p2l2-act-p202a03-1': {},
  'p2l2-act-p202a05-1': { a: txt(String(T.weather_houston.rows.length)), stem: [['daily data for 2017', 'the sample data in this question']] },
  'p2l3-act-p203a02': {}, 'p2l3-act-p203a08': {}, 'p2l3-act-p203a13': {},
  'p2l4-act-p204a03-1': { extra: 'proc format;\n    value $region "NA"="Atlantic"\n                  "WP","EP","SP"="Pacific"\n                  "NI","SI"="Indian"\n                  other="Unknown";\nrun;' },
  'p2l4-act-p204a04-2': { a: txt(String(Math.max(...T.storm_subbasincodes.rows.map(r => r.SubBasin_Name.length)))) },
  'p2b-p2l5-act-p205a01-1': {}, 'p2b-p2l5-act-p205a01-2': {},
  'p2b-p2l5-act-p205a01-3b': { a: txt(T.class_new2.cols.find(c => c.n === 'Student').t.slice(1)) },
  'p2b-p2l5-act-05_3_q1': {}, 'p2b-p2l6-quiz-q3': {},
  'p2b-p2l7-act-p207a02-2': {}, 'p2b-p2l7-act-p207a02-3': {}, 'p2b-p2l7-act-p207a05-1': {},
};
// Kept on purpose: PQ 5.01 asks about LIBNAME paths and an Excel file, not about table contents.
const SKIP = ['crx-pq5.01-2a', 'crx-pq5.01-2b', 'crx-pq5.01-2c', 'crx-pq5.01-3a', 'crx-pq5.01-3b'];

const REF = /\b(cert|crb?|pg2)\.(\w+)/gi;
const norm = a => a.map(s => String(s).toLowerCase().replace(/[$,%\s]/g, ''));
let changed = 0, kept = 0;
for (const q of bank.questions) {
  const orig = q.courseOriginal || { stem: q.stem, code: q.code, answer: q.answer, accepted: q.accepted, explanation: q.explanation };
  const refsIn = s => [...String(s || '').matchAll(REF)].map(m => ({ lib: m[1].toLowerCase(), name: m[2].toLowerCase() }));
  const refs = [orig.stem, orig.code, q.solutionCode].flatMap(refsIn).filter(r => r.name !== '_all_')
    .filter(r => T[r.name] || !new RegExp(String.raw`\bdata\b[^;]*\b${r.lib}\.${r.name}\b`, 'i').test(q.solutionCode)); // tables the step itself creates
  const cfg = Q[q.id];
  if (!cfg) { assert(!refs.length || SKIP.includes(q.id) || /_all_/.test(orig.stem + q.solutionCode), `unhandled question ${q.id}`); continue; }
  const want = cfg.tables ? cfg.tables.map(s => { const [lib, name] = s.split('.'); return { lib, name }; }) : refs;
  want.forEach(r => assert(T[r.name], `${q.id}: no sample table ${r.name}`));
  q.courseOriginal = orig;
  q.stem = (cfg.stem || []).reduce((s, [a, b]) => { assert(s.includes(a), `${q.id}: stem has no "${a}"`); return s.replace(a, b); }, orig.stem);
  q.code = block({ ...q, code: orig.code, extra: cfg.extra }, want) + (orig.code ? '\n\n' + orig.code : '');
  const origKey = q.type === 'mc' ? null : orig.accepted;
  if (cfg.a && JSON.stringify(norm([cfg.a[0]])) !== JSON.stringify(norm([origKey[0]]))) {
    q.answer = cfg.a[0];
    q.accepted = cfg.a;
    q.explanation = `**Với dữ liệu mẫu trong câu: ${cfg.a[0]}.**${cfg.note ? ' ' + cfg.note : ''}\n\n`
      + `Giải thích gốc (theo dữ liệu khóa học, đáp án gốc: ${orig.answer}): ${orig.explanation}`;
    changed++;
  } else {
    q.answer = orig.answer; q.accepted = orig.accepted;
    q.explanation = cfg.note ? `${cfg.note}\n\n${orig.explanation}` : orig.explanation;
    kept++;
  }
}
const missing = Object.keys(Q).filter(id => !bank.questions.some(q => q.id === id));
assert(!missing.length, 'unknown ids: ' + missing);
fs.writeFileSync(file, JSON.stringify(bank, null, 2));
console.log(`Injected sample data into ${changed + kept} questions: ${changed} answer keys recomputed, ${kept} unchanged.`);
