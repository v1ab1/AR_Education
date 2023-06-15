import scrapy
import json

class GoogleScholarCitationSpider(scrapy.Spider):
    name = "citations"

    def start_requests(self):
        with open("organic.json", "r") as file:
            organic_results = json.load(file)

        for result in organic_results:
            url = result["link"]
            yield scrapy.Request(url=url, callback=self.parse, meta={'result': result})

    def parse(self, response):
        citation_count = response.css("#gs_cit0").css(".gs_ri::text").get()
        h_index = response.css("#gsc_rsb_st").css(".gsc_rsb_std::text").get()

        # Загрузка существующих данных из citations.json
        with open("citations.json", "r") as file:
            citations_data = json.load(file)

        # Добавление нового результата в список данных
        result = response.meta['result']
        result["citation_count"] = citation_count
        result["h_index"] = h_index
        citations_data.append(result)

        # Сохранение обновленных данных в citations.json
        with open("citations.json", "w") as file:
            json.dump(citations_data, file)

        # Возвращение результатов в виде словаря
        yield {
            "url": response.url,
            "citation_count": citation_count,
            "h_index": h_index
        }
