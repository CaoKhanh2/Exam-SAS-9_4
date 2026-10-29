/* Fake (made-up) course data for the programming questions that use cr.* / crb.* / pg2.* tables.
   Same table and column names as the course data, random values (fixed seed), so the code runs
   but the numbers DIFFER from the course answers. Compare with the solution code run on this data.
   Libraries live in WORK: rerun this each new SAS session. Embedded into the simulator by build_practice_test.js. */
options dlcreatedir;
%let outpath=%sysfunc(pathname(work));
libname cr "&outpath/cr";
libname crb "&outpath/cr";
libname pg2 "&outpath/pg2";
%let path=&outpath/cr;

/* ---------------- cr ---------------- */
data cr.employee;
    call streaminit(231);
    length EmpID $ 6 Name $ 20 JobTitle $ 25 Department $ 15 Country $ 2 City $ 15 Status $ 1;
    format Salary dollar10. BirthDate HireDate TermDate date9.;
    do i=1 to 80;
        EmpID=put(120100+i, 6.);
        Name=catx(", ", scan("Smith Nguyen Tran Brown Lee Garcia Kim Patel", rand("integer", 1, 8)),
                        scan("Anna Minh John Mai Peter Lan David Hoa", rand("integer", 1, 8)));
        Department=scan("Sales|Accounts|Engineering|Logistics|Administration", rand("integer", 1, 5), "|");
        if Department="Sales" then JobTitle=catx(" ", "Sales Rep.", scan("I II III IV", rand("integer", 1, 4)));
        else JobTitle=catx(" ", Department, scan("Manager|Specialist|Assistant", rand("integer", 1, 3), "|"));
        if rand("uniform") < .6 then do;
            Country="US"; City=scan("Philadelphia|San Diego|Miami", rand("integer", 1, 3), "|");
        end;
        else do;
            Country="AU"; City=scan("Sydney|Melbourne", rand("integer", 1, 2), "|");
        end;
        if rand("uniform") < .1 then Country=lowcase(Country);
        Salary=round(25000 + 125000*rand("uniform"), 100);
        BirthDate="01JAN1960"d + rand("integer", 0, 14000);
        HireDate="01JAN2000"d + rand("integer", 0, 7000);
        if rand("uniform") < .2 then TermDate=HireDate + rand("integer", 100, 2000);
        else TermDate=.;
        Status=scan("M S O", rand("integer", 1, 3));
        output;
    end;
    drop i;
run;

/* duplicates, a bad Country and a HireDate after TermDate to find */
data cr.employee_raw;
    set cr.employee;
    Country=upcase(Country);
    if _n_=5 then Country="NZ";
    if _n_=7 then TermDate=HireDate-30;
    output;
    if _n_ in (3 10) then output;
run;

data cr.employee_current;
    set cr.employee;
    where TermDate is missing;
run;

data cr.employee_new;
    set cr.employee(obs=20 keep=EmpID Name HireDate Salary rename=(EmpID=ID HireDate=HD Salary=S));
    length EmpID $ 9 HireDate $ 10 AnnualSalary $ 12;
    EmpID=cats("EMP", ID);
    HireDate=put(HD, mmddyy10.);
    AnnualSalary=strip(put(S, dollar12.));
    drop ID HD S;
run;

data cr.employee_addresses;
    set cr.employee(keep=EmpID City rename=(EmpID=Employee_ID)) end=last;
    length Street $ 25;
    if mod(_n_, 4) ne 0 then do;
        Street=catx(" ", put(_n_*7, 3.), "Main St");
        output;
    end;
    if last then do;
        Employee_ID="130001"; City="Miami"; Street="1 Ocean Dr"; output;
    end;
run;

data cr.employee_donations;
    if _n_=1 then call streaminit(232);
    set cr.employee(keep=EmpID) end=last;
    array q{4} Qtr1-Qtr4;
    if mod(_n_, 3)=0 or last then do;
        do j=1 to 4;
            if rand("uniform") < .25 then q{j}=.;
            else q{j}=5*rand("integer", 1, 10);
        end;
        if last then EmpID="130002";
        output;
    end;
    drop j;
run;

data cr.employee_training;
    if _n_=1 then call streaminit(233);
    set cr.employee(obs=25 keep=Name);
    format Compliance_Training Corporate_Security On_the_Job_Safety date9.;
    Compliance_Training="01JAN2018"d + rand("integer", 0, 364);
    Corporate_Security="01JAN2018"d + rand("integer", 0, 364);
    On_the_Job_Safety="01JAN2018"d + rand("integer", 0, 364);
run;

data cr.profit;
    call streaminit(234);
    length Order_Source $ 8;
    format Order_Date date9. Profit dollar10.2;
    do i=1 to 200;
        Order_Date="01JAN2018"d + rand("integer", 0, 364);
        Order_Source=scan("Internet Retail Catalog", rand("integer", 1, 3));
        Profit=round(500*rand("uniform"), .01);
        output;
    end;
    drop i;
run;

data cr.qtr_sales;
    if _n_=1 then call streaminit(235);
    set cr.employee(keep=EmpID Name Department);
    where Department="Sales";
    Qtr1=rand("integer", 0, 300); Qtr2=rand("integer", 0, 300);
    Qtr3=rand("integer", 0, 300); Qtr4=rand("integer", 0, 300);
run;

/* m8_sales names the employee column Employee_ID on purpose */
%macro msales(m, idcol);
data cr.m&m._sales;
    call streaminit(&m);
    length &idcol $ 6;
    format Order_Date date9. Total dollar10.2;
    do Order_ID=&m*1000+1 to &m*1000+30;
        &idcol=put(120100+rand("integer", 1, 80), 6.);
        Order_Type=rand("integer", 1, 3);
        Order_Date=mdy(&m, rand("integer", 1, 28), 2019);
        Total=round(300*rand("uniform"), .01);
        output;
    end;
run;
%mend;
%msales(7, EmpID)
%msales(8, Employee_ID)
%msales(9, EmpID)

proc sql;
create table cr.shoes_summary as
    select Region, Product, sum(Stores) as TotalStores, sum(Sales-Returns) as TotalProfit format=dollar12.,
           calculated TotalProfit / calculated TotalStores as ProfitPerStore format=dollar10.2
    from sashelp.shoes
    group by Region, Product;
quit;

/* Code = the Cont values used in sashelp.demographics (continent names made up) */
data cr.continent_codes;
    length Continent $ 15;
    input Code Continent &;
    datalines;
91 North America
92 South America
93 Europe
94 Africa
95 Asia
96 Oceania
;
run;

data cr.country_info;
    length Country $ 15;
    input Country Continent;
    datalines;
Vietnam 5
Japan 5
France 3
Germany 3
Brazil 2
Kenya 4
Canada 1
Australia 6
;
run;

data cr.final_tourism;
    if _n_=1 then call streaminit(236);
    length Country $ 15 Continent $ 15 Category $ 45;
    set cr.country_info(rename=(Continent=Code));
    Continent=scan("North America|South America|Europe|Africa|Asia|Oceania", Code, "|");
    Category="Arrivals";
    y2014=rand("integer", 1000, 90000);
    output;
    Category="Tourism expenditure in other countries";
    y2014=rand("integer", 500, 40000);
    output;
    drop Code;
run;

/* ---------------- pg2 ---------------- */
proc format;
    value $region "NA"="Atlantic"
                  "WP", "EP", "SP"="Pacific"
                  "NI", "SI"="Indian"
                  other="Unknown";
run;

data pg2.storm_summary;
    call streaminit(237);
    length Name $ 15 Basin $ 2 Ocean $ 8;
    format StartDate EndDate date9.;
    do i=1 to 60;
        Season=2010 + rand("integer", 0, 7);
        Name=scan("ANA BILL CINDY DORA ERIN FRED GERT HARVEY IRMA JOSE KATIA LEE", rand("integer", 1, 12));
        Basin=scan("NA EP WP SP NI SI", rand("integer", 1, 6));
        if rand("uniform") < .15 then Basin=lowcase(Basin);
        Ocean=put(upcase(Basin), $region.);
        MaxWindMPH=rand("integer", 30, 180);
        MaxWindKM=round(MaxWindMPH*1.60934);
        StartDate=mdy(rand("integer", 1, 12), rand("integer", 1, 28), Season);
        EndDate=StartDate + rand("integer", 1, 15);
        output;
    end;
    drop i;
run;

data pg2.storm_summary_small;
    set pg2.storm_summary(obs=5);
run;

data pg2.storm_2017;
    set pg2.storm_summary(drop=Season);
    Season=2017;
    StartDate=mdy(month(StartDate), day(StartDate), 2017);
    EndDate=StartDate + 5;
run;

data pg2.storm_damage;
    length Event $ 20 Summary $ 80;
    format Date date9. Cost dollar14.;
    input Event & Date :date9. Cost Summary & $80.;
    datalines;
Hurricane Harvey  25AUG2017 125000000000 Made landfall as a Category 4 hurricane in Texas.
Hurricane Irma  10SEP2017 50000000000 Struck Florida as a category 4 storm.
Hurricane Maria  20SEP2017 90000000000 Devastated Puerto Rico at CATEGORY 4.
Hurricane Sandy  29OCT2012 65000000000 Post-tropical cyclone with no category at landfall.
Hurricane Katrina  29AUG2005 125000000000 Category 3 landfall in Louisiana.
;
run;

data pg2.storm_subbasincodes;
    length Sub_Basin $ 2 SubBasin_Name $ 20;
    input Sub_Basin SubBasin_Name &;
    datalines;
NA North Atlantic
CS Caribbean Sea
GM Gulf of Mexico
BB Bay of Bengal
AS Arabian Sea
MM Missing
;
run;

data pg2.storm_top4_wide;
    call streaminit(238);
    length Basin $ 2;
    do Season=2014 to 2017;
        do Basin="NA", "EP", "WP";
            Wind1=rand("integer", 140, 180); Wind2=Wind1-rand("integer", 1, 15);
            Wind3=Wind2-rand("integer", 1, 15); Wind4=Wind3-rand("integer", 1, 15);
            output;
        end;
    end;
run;

data pg2.weather_zurich;
    call streaminit(239);
    format Date date9.;
    do Date="01JAN2017"d to "31DEC2017"d;
        TempC=round(10 - 12*cos(2*constant("pi")*(Date-"15JAN2017"d)/365) + 3*rand("normal"), .1);
        if rand("uniform") < .05 then Rain_mm=.;
        else if rand("uniform") < .6 then Rain_mm=0;
        else Rain_mm=round(20*rand("uniform"), .1);
        output;
    end;
run;

data pg2.weather_houston;
    call streaminit(240);
    format Date date9.;
    do Date="01JAN2017"d to "31DEC2017"d;
        Month=month(Date);
        DailyRain=ifn(rand("uniform") < .7, 0, round(2*rand("uniform"), .01));
        output;
    end;
run;

data pg2.class_quiz;
    if _n_=1 then call streaminit(241);
    set sashelp.class(keep=Name);
    array q{5} Quiz1-Quiz5;
    do j=1 to 5;
        q{j}=rand("integer", 5, 10);
    end;
    drop j;
run;

/* Student is longer than sashelp.class Name ($8), so renaming it to Name gives a length message */
data pg2.class_new2;
    length Student $ 12;
    input Student Age Height Weight;
    datalines;
Alexandria 13 60 95
Maximilian 14 65 110
Jo 12 55 80
;
run;

data pg2.class_test_narrow;
    if _n_=1 then call streaminit(242);
    set sashelp.class(keep=Name);
    length TestSubject $ 7;
    TestSubject="Math"; TestScore=rand("integer", 50, 100); output;
    TestSubject="Reading"; TestScore=rand("integer", 50, 100); output;
run;
proc sort data=pg2.class_test_narrow;
    by Name;
run;

data pg2.stocks2;
    call streaminit(243);
    length Stock $ 4 Date $ 9 Volume $ 12;
    do Stock="IBM", "MSFT";
        do d="03JAN2017"d to "31JAN2017"d by 7;
            Date=put(d, date9.);
            Volume=put(rand("integer", 1000000, 9000000), comma12.);
            Close=round(50 + 100*rand("uniform"), .01);
            output;
        end;
    end;
    drop d;
run;

title "Fake course data ready (values differ from the course answers)";
proc sql;
    select libname, memname, nobs from dictionary.tables
    where libname in ("CR" "PG2") order by libname, memname;
quit;
title;
