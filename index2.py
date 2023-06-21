import json
import pandas as pd
import time
from scholarly import scholarly

# Создание пустого файла citations.json, если он не существует
with open("citations.json", "w") as file:
    json.dump([], file)

# Органический поиск
print("Ожидание результатов органического поиска...")
search_query = scholarly.search_pubs("дополненная реальность образование")
organic_data = []
for i, result in enumerate(search_query, start=1):
    organic_data.append({
        "title": result['bib'].get("title", ""),
        "link": result['bib'].get("url", ""),
        "publication_info_summary": result['bib'].get("author", ""),
        "snippet": result['bib'].get("abstract", "")
    })
    print(f"Обработан результат органического поиска {i}")
    if i % 400 == 0:
        time.sleep(5)  # Задержка 5 секунд каждые 400 запросов
with open("organic.json", "w", encoding="utf-8") as file:
    json.dump(organic_data, file, ensure_ascii=False)
print("Результаты органического поиска сохранены в файл organic.json")

# Цитирование
print("Ожидание результатов цитирования...")
with open("organic.json", "r") as file:
    organic_data = json.load(file)

citations_data = []
for result in organic_data:
    publication = scholarly.fill(result["link"])
    citation_count = publication['citedby']
    h_index = publication['hindex']
    result["citation_count"] = citation_count
    result["h_index"] = h_index
    citations_data.append(result)
    print(f"Обработан результат цитирования {result['link']}")
    if len(citations_data) % 400 == 0:
        time.sleep(5)  # Задержка 5 секунд каждые 400 запросов
with open("citations.json", "w") as file:
    json.dump(citations_data, file)

# Преобразование в DataFrame и сохранение в CSV
organic_df = pd.DataFrame(organic_data)
organic_df.to_csv("organic.csv", encoding="utf-8-sig", index=False)
print("Результаты органического поиска сохранены в файл organic.csv")

citations_df = pd.DataFrame(citations_data)
citations_df.to_csv("citations.csv", encoding="utf-8-sig", index=False)
print("Результаты цитирования сохранены в файл citations.csv")
