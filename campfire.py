import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

category_box = ["local"]
# category_box = ["community", "social-good", "local"]

# category_box = ["art", "music", "dance", "product", "technology", "game", "journalism",
# 			"community", "food", "photo", "fashion", "movie", "publishing",
# 			"anime", "performance", "sports", "business", "comedy", "social-good"]

pj_title_list = []
pj_detail_list = []
money_list = []
patron_list = []
remain_list = []
category_list = []

# with open('/Users/koji/Desktop/python/camp.html') as html_file:
#     soup = BeautifulSoup(html_file, 'html.parser')

for category in category_box:
	page = 1
	while True:
		url = "https://camp-fire.jp/projects/category/" + str(category) + "?page=" + str(page) + "project_status%5B%5D=closed"

		r = requests.get(url.format(page))

		soup = BeautifulSoup(r.content, "html.parser")
		if len(soup.select(".overview .total")) == 0:
			print("End of category.")
			break

		boxtitle_array = soup.select("div.box-title")
		overview_array = soup.select("div.overview")
		# success_array = soup.select("div.success-summary")

		j = 0
		for i in range(0, len(boxtitle_array)):
			pj_title = boxtitle_array[i].contents[0].contents[0].contents[0]

			if len(boxtitle_array[i].contents) == 1:
				pj_detail = "詳細説明なし"
			else:
				pj_detail = boxtitle_array[i].contents[1].contents[0].contents[0]

			print(pj_title) # title
			print(pj_detail) # detail
			pj_title_list.append(pj_title)
			pj_detail_list.append(pj_detail)

			# ※コミュニティ方式のときはoverviewが無い。　→　データから除外する
			if len(overview_array[i].contents) == 1:
				money = "コミュニティ方式(定額課金制)"
				patron = overview_array[j].contents[0].contents[2]
				remain = "毎月"
				j -= 1
			else:
				money = overview_array[j].contents[1].contents[2]
				patron = overview_array[j].contents[3].contents[2]
				remain = overview_array[j].contents[5].contents[2]

			print(money)
			print(patron)
			print(remain)
			money_list.append(money)
			patron_list.append(patron)
			remain_list.append(remain)
			category_list.append(category)


			print(category + ", " + str(page) + ", " + str(i))
			print("----------------")
		page += 1
		j += 1
		time.sleep(5)


df = pd.DataFrame({"category" : category_list,
					"pj_title" : pj_title_list,
					"pj_detail" : pj_detail_list,
					"money" : money_list,
					"patron" : patron_list,
					"remain" : remain_list}
					)

df.to_csv("campfire.csv", index=False)
