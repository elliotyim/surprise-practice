import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd

import uuid
import json

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

df = pd.read_csv("./dataset/artist_list.csv", sep=",")

URL = "https://www.daarts.or.kr/handle/11080/6034"
BASE_URL = "https://www.daarts.or.kr"


def get_category(txtbox):
    dl_tags = txtbox.find_all("dl")
    for dl in dl_tags:
        dt = dl.find("dt")
        if isinstance(dt, Tag) and dt.has_attr("class") and "ico02" in dt["class"][0]:
            return dl.contents[3].text
    return "no-category"


def get_img_data(url, author_id):
    payload = {"profile_img": None, "artworks": []}
    html = requests.get(url, verify=False).text
    soup = BeautifulSoup(html, "html.parser")

    try:
        profile_img = soup.find("div", class_="img")["style"].split("'")[1]
        payload["profile_img"] = BASE_URL + profile_img

        txtbox = soup.find_all("div", class_="txtbox")
        imgbox = soup.find_all("div", class_="imgbox")
        for i in range(min(len(imgbox) - 1, 10)):
            if imgbox[i + 1].contents[1]["data-image-url"]:
                img = dict()
                img["id"] = str(uuid.uuid4())
                img["author_id"] = author_id
                img["name"] = txtbox[i].contents[1].contents[0]
                img["category"] = get_category(txtbox[i])
                img["img_url"] = BASE_URL + imgbox[i + 1].contents[1]["data-image-url"]
                payload["artworks"].append(img)
    except Exception:
        pass
    return payload


count = 0
payload = []
art_categories = ["미술작가", "서양화", "회화", "한국화", "설치", "조각", "사진"]
for i, row in df.iterrows():
    if count == 100:
        break
    if row["ACT_RELM_CN"] not in art_categories:
        continue

    author_id = str(uuid.uuid4())

    img_data = get_img_data(url=row["URL"], author_id=author_id)
    author = {
        "id": author_id,
        "type": "artist",
        "name": row["NM"],
        "profile_img": img_data["profile_img"],
    }
    artworks = img_data["artworks"]
    if not artworks:
        continue
    print(f'{count+1}. {row["NM"]} ({i+1}/{len(df)})')
    payload.append({"author": author, "artworks": artworks})
    count += 1

with open("data.json", mode="w", encoding="utf8") as f:
    json.dump(payload, f, ensure_ascii=False)

print("Done.")

