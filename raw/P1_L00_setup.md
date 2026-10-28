# P1 – Course Overview: Setting Up Your Practice Files (REQUIRED)

Course: SAS® Programming 1: Essentials (SAS9.4v2, English). Captured 2026-10-27.
Scope: only the "Setting Up Your Practice Files (REQUIRED)" page and its 5 instruction pop-ups.

### [Page 1/1] Setting Up Your Practice Files (REQUIRED)
**Type:** concept (setup instructions)
**Content:**
- To complete the activities, demos, and practices you must **access SAS software** and **set up your practice files**.
- Three routes: Using the Hands-On Lab; Using SAS OnDemand for Academics; Using your own SAS software (SAS Studio, SAS Enterprise Guide, SAS Windowing Environment).
- Hands-On Lab already has the course files loaded; launch the lab and start using SAS Studio.

#### Pop-up 1 – Setup Instructions for the Lab
- Launch the Hands-On Lab and View the Course Files:
  1. Select the **Hands-On Lab** tab.
  2. First time in a course with the SAS Hands-On Lab for Terminal Servers you must read the documentation (Documentation icon opens it in a new browser tab).
  3. Select the checkbox certifying you read the documentation, then select **Submit**.
  4. To launch the lab, click **Launch**.
  5. Login page opens in a new tab with user name and password pre-filled; select **Log on**.
  6. On the Apps page, select **SAS Studio**.
  7. SAS Studio launches in the lab; you can maximize the window.
  8. In the Files and Folders panel expand **S:\ > workshop > EPG1V2**. The EPG1V2 folder contains all course files; activity/demo/practice steps give the file name to open.
  - Note: when asked to replace FILEPATH with the path to your **EPG1V2/data** folder, the virtual-lab path is **S:/workshop/EPG1V2/data** (view/copy via right-click data folder > Properties).
- Refreshing Your Practice Files (2 options):
  - Refresh all files in the course folder: select **Refresh Data** in the virtual lab block on the course page. This overwrites **all files in the course folder**, including SAS programs or other files you changed or saved.
  - Refresh **only** the SAS tables: open the EPG1V2 folder in the virtual lab and run the **refreshData.sas** program; it creates and saves a fresh copy of all SAS tables in your **data** folder.

#### Pop-up 2 – Setup Instructions for SAS OnDemand for Academics: SAS Studio
- Task 1 of 2: Access SAS OnDemand for Academics – sign in with your SAS profile email/password (same as for this training), then register for a SAS OnDemand for Academics account; same link used to sign in later.
- Task 2 of 2: Create your course files (assumes an active ODA account):
  1. Open the zip file and extract it; creates folder **EPG1V2** with one SAS program: **createdataPG1v2_oda.sas**.
  2. Sign in to the SAS OnDemand for Academics Dashboard and start SAS Studio.
  3. Server Files and Folders panel: click **New** and select **Folder**.
  4. In the Name box type **EPG1V2** in uppercase exactly as shown; click **Save**.
  5. If necessary expand **Files(Home)** and verify the EPG1V2 folder was created.
  6. Select the EPG1V2 folder and click **Upload**.
  7. Upload Files window: **Choose Files**, browse to EPG1V2 on your computer, select **createdataPG1v2_oda.sas**, **Open**, **Upload**. Program is added to the EPG1V2 folder on the server.
  8. Expand EPG1V2 and double-click **createdataPG1v2_oda.sas** to open it.
  9. Click **Run** or press **F3**. Creates all SAS files and data for the course; a list of SAS tables appears in the **Results** tab.
  10. Server Files and Folders panel should show 5 subfolders in the folder (screen text reads "EGP1V2"): **activities**, **data**, **demos**, **output**, **practices**.
- File path to data can be given as **~/EPG1V2/data** (full path: right-click data folder > Properties).
- Note: EPG1V2 is the location of your course files in ODA; instructions name the folder (activities, demos, or practices) and file name; files persist each time you sign in.

#### Pop-up 3 – Setup Instructions for SAS Studio (SAS installed on your PC)
- You must follow all steps in three tasks. Link: "Using Studio with SAS Viya?" (not followed).
- IMPORTANT: perform the tasks in the **same** SAS Studio session; don't close the browser until all three tasks are complete or you must start again.
- Task 1 of 3: Download the course files – open the ZIP file and extract; creates folder **EPG1V2** with two programs (**createdata.sas** and **setup.sas**) and five sub-folders: **activities**, **data**, **demos**, **output**, **practices**.
  - Note: if SAS Studio accesses SAS on a remote server, upload the course files to the server before Tasks 2 and 3 (link "Follow these instructions" – not followed).
- Task 2 of 3: Set the path to your course data folder:
  1. Start SAS Studio.
  2. Files and Folders panel: navigate to the EPG1V2 folder.
  3. Double-click **setup.sas**. Don't run it yet – edit the first line first.
  4. Expand EPG1V2; right-click **data** > **Properties**; copy the path shown in **Location**; close the window.
  5. In the Code window: (a) highlight FILEPATH and paste the copied path; (b) make no other changes.
  6. Click **Run** or press **F3**.
  7. Check the log for the note **Libref PG1 was successfully assigned**, followed by the engine and physical name specification. If it fails, make sure the referenced folder exists, review the program for errors, correct, resubmit.
  8. Code tab > **Save** to save the modified setup.sas.
  9. Close the setup.sas program tab.
- Task 3 of 3: Create the practice files – only once:
  1. Navigate to the EPG1V2 folder.
  2. Double-click **createdata.sas**.
  3. **Run**/**F3** – creates SAS data sets in the **data** folder.
  4. Check the log: no errors or warnings. There will be many notes (one per data set created). If it fails, verify all Task 2 steps.
  5. Close createdata.sas.
  6. Files and Folders panel: **New** > **SAS Program** to open a new program tab.
  - Note: unless you delete your practice files, you don't need to repeat this task.

#### Pop-up 4 – Setup Instructions for SAS Enterprise Guide 8
- Follow all steps in three tasks to set up data and create a project.
- Task 1 of 3: Download the course files – open the ZIP file and extract; creates folder **EPG1V2_EG** with five sub-folders: **activities**, **data**, **demos**, **output**, **practices**.
- Task 2 of 3: Open a new project and run code to create practice data.
  - Create the data for practices:
    1. Start SAS Enterprise Guide, create a new project (View > Project to open the Project window if needed).
    2. **Program > Open Program**; navigate to EPG1V2_EG > **data**; select **pg1v2_eg.sas**; Open. A shortcut is added to the Process Flow **Programs** folder.
    3. **Run**/**F3**. Creates all course data (may take time). Check the **Log** tab: no warnings or errors.
    4. **Results** tab lists created SAS tables. The Directory table shows the physical path to the files; this path is stored in a macro variable named **path**. EG notes in activities/practices tell you when to use **&path** in place of the file path.
  - Create the data for the case study:
    1. **Program > Open Program**; EPG1V2_EG > **data**; select **pg1v2_eg_casestudy.sas**; Open.
    2. **Run**/**F3** – creates data for the TSA Claims case study.
    - Note: if it errors, your environment likely doesn't allow SAS to download from a website; use the link to download the case study data locally. If SAS runs on a remote server, copy the .csv file to the remote server.
- Task 3 of 3: Save the project:
  1. Project window: right-click **Process Flow** > **Rename**; type **Autoexec**; Enter. A process flow named Autoexec makes EG prompt you to run it (with the data-creation program) when you open the project.
  2. **File > New > Process Flow** – an empty process flow for your work.
  3. **File > Save Project As** – suggested name: course code **EPG1V2**.
- Each time you open the project, EG prompts to run the Autoexec process flow; select **Yes** to recreate course data. Open starter programs from where you stored EPG1V2_EG.

#### Pop-up 5 – Setup Instructions for SAS Windowing Environment
- Follow all steps in three tasks to set up data and practice files for SAS on Windows.
- IMPORTANT: perform the tasks in the **same** SAS session; don't close SAS until all three are done.
- Task 1 of 3: Copy the course files – open the ZIP file and extract to a folder where you typically store SAS files; creates **EPG1V2** with **createdata.sas** and **setup.sas** and five sub-folders: **activities**, **data**, **demos**, **output**, **practices**.
- Task 2 of 3: Set the path to the data folder:
  1. Start SAS.
  2. **File > Open Program**; navigate to EPG1V2; select **setup.sas**; Open.
  3. Replace **FILEPATH** with the path to the **EPG1V2\data** folder. Note: if unknown, right-click EPG1V2\data in Windows Explorer > Properties; copy the path next to Location; paste over FILEPATH; add **\data** at the end of the path.
  4. Click **Submit** or press **F3**.
  5. Check the log for the note **Libref PG1 was successfully assigned**, followed by the engine and physical name specification. If not, check the folder exists and review/correct/resubmit.
  6. Click in the setup.sas window and click **Save**.
  7. Close setup.sas.
- Task 3 of 3: Create the practice files – only once:
  1. **File > Open Program**; EPG1V2; **createdata.sas**; Open.
  2. **Submit**/**F3** – creates SAS data sets in the **data** folder.
  3. Check the log: no errors or warnings; many notes (one per data set). If it fails, check Task 2.
  4. Close createdata.sas.
  5. **File > New Program** to open a new program editor window.
  - Note: unless you delete practice files, no need to repeat.

**Code:** none shown on these pages (setup.sas / createdata.sas contents not displayed).
**Log messages shown:** `Libref PG1 was successfully assigned` (followed by engine and physical name specification).
**Capture status:** complete (external links – ZIP downloads, Viya instructions, remote-server upload instructions, ODA sign-in – not followed; they are downloads/external sites).
