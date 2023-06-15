import json
import pandas as pd
from scrapy.crawler import CrawlerProcess
from organic import GoogleScholarSpider
from citations import GoogleScholarCitationSpider

# Создание пустого файла citations.json, если он не существует
with open("citations.json", "w") as file:
    json.dump([], file)

# Запуск пауков Scrapy
process = CrawlerProcess()
process.crawl(GoogleScholarSpider)
process.crawl(GoogleScholarCitationSpider)
process.start()

# Pandas
print("Ожидание сохранения результатов органического поиска...")
with open("organic.json", "r") as file:
    organic_data = json.load(file)
organic_df = pd.DataFrame(organic_data)
organic_df.to_csv("organic.csv", encoding="utf-8-sig", index=False)
print("Результаты органического поиска сохранены в файл organic.csv")

print("Ожидание сохранения результатов цитирования...")
with open("citations.json", "r") as file:
    citations_data = json.load(file)
citations_df = pd.DataFrame(citations_data)
citations_df.to_csv("citations.csv", encoding="utf-8-sig", index=False)
print("Результаты цитирования сохранены в файл citations.csv")
