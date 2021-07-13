import os
import shutil
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

BaseCompanyURL = "https://www.set.or.th"
BaseURL = "https://www.set.or.th/set/commonslookup.do?language=th&country=TH&prefix="
AllPrefixes = ["NUMBER", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
               "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


def CleanUpDirectory():
    if os.path.isdir('data'):
        shutil.rmtree("data")
    if os.path.isdir("extracted_data"):
        shutil.rmtree("extracted_data")


def InitDirectory():
    os.mkdir("data")
    os.mkdir("extracted_data")


def GetAllCompany():
    company = []
    for prefix in AllPrefixes:
        url = BaseURL + prefix
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        tdTags = soup.find_all("td")

        for tdTag in tdTags:
            aTags = tdTag.find_all("a")
            for aTag in aTags:
                DownloadZip(BaseCompanyURL + aTag['href'])
    return company


def DownloadZip(company: str):
    print(company)
    r = requests.get(company)
    soup = BeautifulSoup(r.content, "html.parser")

    company_name = soup.find_all(
        "div", {'class': 'col-xs-12 col-md-12 col-lg-8'})[0].text.split()[0]

    aTags = soup.find_all("a")

    downloadURL = False

    for aTag in aTags:
        if 'งบไตรมาส' in aTag.text or 'งบปี' in aTag.text:
            downloadURL = aTag["href"]

    if downloadURL:
        print(company_name + " : " + downloadURL)
        response = requests.get(downloadURL, stream=True)

        with open("data/"+company_name + ".zip", "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)
    else:
        raise Exception(company_name + " : " + "File Url Not Found")


def main():
    CleanUpDirectory()
    InitDirectory()
    GetAllCompany()


main()
