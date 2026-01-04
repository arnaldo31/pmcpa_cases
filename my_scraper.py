import requests
from bs4 import BeautifulSoup
import pandas
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload

import io
import re

# from keep_alive import keep_alive

# keep_alive()
save = []
pdf_names = []


def get_api_key():
    url = "https://vivinodatabase-default-rtdb.firebaseio.com/pmpc_key.json"
    auth_token = "e8SmAXVRomiHYq6C74Gjqk1W4mXcCzWfhlcwv4PO"
    params = {"auth": auth_token}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
        
    else:
        print("Error:", response.status_code, response.text)


def case():
    global ses
    ses = requests.session()

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'SiteKey MjU2MjoxMTcxMjpTZWFyY2hLZXk=',
        'Connection': 'keep-alive',
        'Content-type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.pmcpa.org.uk',
        'Referer': 'https://www.pmcpa.org.uk/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69',
        'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }


    for i in range(1,100000):

        json_data = {
            'ResponseType': 'JsonHtml',
            'Template': 'v3 cases',
            'facets': {
                'Category': [],
                'Case_ApplicableCodeyear': [],
                'Case_ReceivedYear': [],
                'Clause': [],
                'Year': [],
                'Code_Version': [],
                'Topic': [],
                'AdvertisedSanctions_Sanction': [],
            },
            'filters': {},
            'page': str(i),
            'query': '*',
            'text': '',
            'traits': [],
            'sort': {
                'Case_CompletedDate_date': 'desc',
            },
            'rangeFacets': {},
            'perPage': None,
            'enableRelatedSearches': False,
            'applyMultiLevelFacets': True,
        }

        response = ses.post('https://api.cludo.com/api/v3/2562/11712/search', headers=headers, json=json_data)

        data = response.json()['SearchResult']

        soup = BeautifulSoup(data,'html.parser')

        cards = soup.find_all(class_='search-results-item')
        if cards == []:
            print(cards)
            break
        for item in cards:
            url = item.a.get('href')
            #rint(url)
            #url = 'https://www.pmcpa.org.uk/cases/completed-cases/auth3731123-complainant-v-consilient-health/'
            try:
                parse(url)
            except Exception as e:
                print(e)
            
def get_pdf_names():
    credentials_info = get_api_key()
    # 🔑 IDs (IMPORTANT)
    SHARED_DRIVE_ID = "0AFAhcn0LL_J9Uk9PVA"      # Shared Drive ID
    FOLDER_ID = "1idWAaVq7DDoNc2nK9s7EPhv9hj88_wSq"  # Folder inside Shared Drive

    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES
    )

    service = build("drive", "v3", credentials=credentials)

    query = (
        f"'{FOLDER_ID}' in parents "
        "and mimeType='application/pdf' "
        "and trashed=false"
    )

    page_token = None

    while True:
        response = service.files().list(
            q=query,
            corpora="drive",                      # ✅ REQUIRED
            driveId=SHARED_DRIVE_ID,              # ✅ REQUIRED
            includeItemsFromAllDrives=True,       # ✅ REQUIRED
            supportsAllDrives=True,               # ✅ REQUIRED
            fields="nextPageToken, files(id, name)",
            pageToken=page_token
        ).execute()

        for f in response.get("files", []):
            pdf_names.append(f["name"])

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    print(len(pdf_names), ": total pdfs in Shared Drive folder")
    return pdf_names

def parse(url):

    headers2 = {
        'authority': 'www.pmcpa.org.uk',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76',
    }

    while True:
        try:
            res = ses.get(url,headers=headers2,timeout=10)
            break
        except Exception as e:
            print(e)

    soup = BeautifulSoup(res.text,'html.parser')
    dic = {}
    dic['Case Name'] = soup.h1.text.strip()
    try:
        des = soup.find(id='tab1').contents
        text_des = ''
        for d in des:
            if d.name == 'h2':
                continue
            if d.name == 'p':
                text_des += d.text + '\n'
            if d.name == 'table':
                for tb in d.find_all('tr'):
                    p1 = tb.find_all('td')[0].p.text.replace('\n','').strip()
                    p2 = tb.find_all('td')[1].p.text.replace('\n','').strip()
                    text_des += p1 + ' ' + p2

        if len(text_des) > 5000:
            dic['Description'] = text_des[:4999]
            dic['Description_2'] = text_des[4999:]
        else:
            dic['Description'] = text_des
    except:
        pass


    for info in soup.find(class_='info-holder').find_all('li'):
        key = info.find(class_='info-holder-name').text.strip()
        val = info.find(class_='info-holder-text').text.strip()
        try:
            a_cat = info.find(class_='info-holder-text').find_all('a')
            if a_cat != []:
                a = []
                for a_tag in a_cat:
                    a.append(a_tag.text)
                val = ' | '.join(a)
        except:
            pass
        dic[key] = val

    dic['url'] = url
    page_layout = soup.find(class_='page-layout-aside')
    if page_layout != None:
        a_pdfs = page_layout.find_all('a')
        if a_pdfs != []:
            c = 1
            for a_link in a_pdfs:
                link = a_link.get('href')
                if '/cases/completed-cases/' == a_link.get('href'):
                    continue
                if '.pdf' in link:
                    filename = a_link.find(class_='title').text.replace(' ','_').strip().lower()
                    filename = sanitize_filename(filename) + '.pdf'

                    dic[f'File{str(c)}_Name'] = filename
                    if 'https://www.pmcpa.org.ukhttps//www.pmcpa.org.uk' in link:
                        link = link.replace('https://www.pmcpa.org.ukhttps//www.pmcpa.org.uk','https://www.pmcpa.org.uk')
                    if 'https://www.pmcpa.org.uk' not in link:
                        link = 'https://www.pmcpa.org.uk' + link
                    dic[f'File{str(c)}_Link'] = link
                    download_pdf(link=link,filename=filename)

                else:
                    dic[f'File{str(c)}_Name'] = a_link.find(class_='title').text.strip()
                    if 'https://www.pmcpa.org.ukhttps//www.pmcpa.org.uk' in link:
                        link = link.replace('https://www.pmcpa.org.ukhttps//www.pmcpa.org.uk','https://www.pmcpa.org.uk')
                    if 'https://www.pmcpa.org.uk' not in link:
                        link = 'https://www.pmcpa.org.uk' + link
                    dic[f'File{str(c)}_Link'] = link
                    parse(link)
                c += 1

    
    save.append(dic)
    print(dic['Case Name'],len(save),sep=' | ')

def download_pdf(link:str,filename:str):
    
    #filename = filename + 'sss'
    if filename in pdf_names:
        #print('found ! ',filename)
        return
    
    print('filename {} not found!'.format(filename))
    xx = 0
    while True:
        if xx == 10:
            return
        try:
            response = requests.get(link,timeout=10)
            break
        except Exception as e:
            print(e)
            xx += 1

    upload_pdf_from_memory(pdf_bytes=response.content,filename=filename)
    
    # with open('.\\pdf_files\\'+filename+'.pdf',mode='wb+') as file:
    #     file.write(response.content)
    #     file.close()

def upload_pdf_from_memory(pdf_bytes, filename):

    credentials_info = get_api_key()

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]


    credentials = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES
    )


    service = build("drive", "v3", credentials=credentials)

    file_metadata = {
        "name": filename,
        "parents": ['0AFAhcn0LL_J9Uk9PVA']
    }

    media = MediaIoBaseUpload(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        resumable=True
    )

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink",
        supportsAllDrives=True

    ).execute()

    print(file['webViewLink'])

def sanitize_filename(name: str, replacement: str = "") -> str:
    # Remove invalid characters
    name = re.sub(r'[\\/:*?"<>|]', replacement, name)

    # Remove control characters
    name = re.sub(r'[\x00-\x1f]', '', name)

    # Strip trailing spaces and dots
    name = name.strip().rstrip('.')

    return name

def saving():
    
    credentials_info = get_api_key()

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]

    credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
    spreadsheet = build('sheets','v4',credentials=credentials)


    sheet_id = '1vZ0iYB58h7mwWSFuxN1BJZ5aaiAXmtd3CZXbF27vSLk'
    range_name = 'Sheet1!A1:AZ5000'

    keys = ['Case Name', 'Received','Completed','Date posted','Case number','Description','Description_2','Applicable Code year', 'Completed', 'No breach Clause(s)', 'Breach Clause(s)', 'Sanctions applied', 'Additional sanctions', 'Appeal', 'Review','Sanction', 'Case number/s', 'url', 'File1_Name', 'File1_Link', 'File1_FileName', 'File2_Name', 'File2_Link', 'File2_FileName', 'File3_Name', 'File3_Link', 'File3_FileName', 'File4_Name', 'File4_Link', 'File4_FileName', 'File5_Name', 'File5_Link', 'File5_FileName', 'File6_Name', 'File6_Link', 'File6_FileName', 'File7_Name', 'File7_Link', 'File7_FileName']
    df2 = pandas.DataFrame()
    df = pandas.DataFrame(save)

    for keys_item in keys:
        try:
            df2[keys_item] = df[keys_item]
        except:
            pass

    df2 = df2.fillna('')
    column_names = df2.columns.tolist()
    data_values = df2.values.tolist()
    two_d_list = [column_names] + data_values

    request_body = {
            'values': two_d_list
        }
    
    
    # 1️⃣ Clear existing data

    trial = 0
    while True:
        if trial ==10:
            break
        try:
            spreadsheet.spreadsheets().values().clear(
                spreadsheetId=sheet_id,
                range=range_name,
                body={}
            ).execute()
                        
            spreadsheet.spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range=range_name,
                body=request_body,
                valueInputOption='RAW'
            ).execute()

            print('succefull save : ',len(two_d_list))
            break
        except Exception as e:
            print(e)
            trial += 1
    


if __name__ == '__main__':
    get_pdf_names()
    try:
        case()
    except Exception as e:
        print(e)
    saving()
