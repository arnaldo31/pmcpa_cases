# pmcpa.org.uk

This script scrapes [https://www.pmcpa.org.uk/cases/ongoing-cases/](https://www.pmcpa.org.uk/cases/ongoing-cases/) and saves the data to this [Google Sheet](https://docs.google.com/spreadsheets/d/1vZ0iYB58h7mwWSFuxN1BJZ5aaiAXmtd3CZXbF27vSLk/edit?gid=0#gid=0).  
It also downloads all new PDF files automatically to [Google Drive](https://drive.google.com/drive/folders/0AFAhcn0LL_J9Uk9PVA).

---

## Run Time of Script
- Every **Sunday at 11:00 PM GMT**


---

## Technologies Used
- Python  
- Google Sheets API  
- Google Drive API  
- Docker (Google Cloud)

---

## Installation

1. You will need to have [Python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) installed (on Mac they are already installed)
2. You will need to install the following packages with `pip`:
   go to `cmd` and type each of this line
   
    - Windows commands:
      ```
      python -m pip install requests
      python -m pip install beautifulsoup4
      python -m pip install lxml
      python -m pip install google-api-python-client
      python -m pip install google-auth
      python -m pip install pandas
      ```
3. download the code - https://github.com/arnaldo31/pmcpa_cases/archive/refs/heads/main.zip

4. run the `my_scraper.py`
   
## Workflow of Script
1. Access [PMC PA ongoing cases](https://www.pmcpa.org.uk/cases/ongoing-cases/)  
2. Scrape all new cases and store them in Google Sheets  
3. Download associated PDF files to Google Drive  

---

## Fields Stored in Google Sheets

| Column | Description |
|--------|-------------|
| Case Name | Name of the case |
| Completed | Status of completion |
| Date posted | Date the case was posted |
| Case number | Official case number |
| Description | Case description |
| Description_2 | Additional description/details |
| Applicable Code year | Code year applied in the case |
| No breach Clause(s) | Clauses found not in breach |
| Breach Clause(s) | Clauses found in breach |
| Sanctions applied | Sanctions applied |
| Additional sanctions | Any additional sanctions |
| Review | Review information |
| Sanction | Sanction type |
| Case number/s | Any other related case numbers |
| url | Link to the case page |
| File1_Name | Name of first PDF file |
| File1_Link | Link to first PDF file |
| File2_Name | Name of second PDF file |
| File2_Link | Link to second PDF file |
| File3_Name | Name of third PDF file |
| File3_Link | Link to third PDF file |
| File4_Name | Name of fourth PDF file |
| File4_Link | Link to fourth PDF file |
| File5_Name | Name of fifth PDF file |
| File5_Link | Link to fifth PDF file |
| File6_Name | Name of sixth PDF file |
| File6_Link | Link to sixth PDF file |
| File7_Name | Name of seventh PDF file |
| File7_Link | Link to seventh PDF file |
