import json
import pandas as pd
from collections import defaultdict

CATEGORIES = ["드로잉", "오브제", "사진", "판화", "서양화", "한국화", "공예", "서예", "조각", "뉴미디어"]
payload = defaultdict(int)

df = pd.read_csv("./dataset/gallery.csv", sep=",")
for i, row in df.iterrows():
    print(f"{i+1}/{len(df)}")
    payload[row["PRDCT_CL_NM"]] += row["RDCNT"]

df = pd.read_csv("./dataset/display.csv", sep=",")
df = df.dropna(subset=["PRDCT"])
for i, row in df.iterrows():
    print(f"{i+1}/{len(df)}")
    for c in CATEGORIES:
        if row["PRDCT"] and row["PRDCT"].find(c) > 0:
            payload[c] += row["RDCNT"]


with open("category.json", mode="w", encoding="utf8") as f:
    json.dump(payload, f, ensure_ascii=False)

print("Done.")
