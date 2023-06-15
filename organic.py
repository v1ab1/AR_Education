import scrapy
import json

class GoogleScholarSpider(scrapy.Spider):
    name = "google_scholar"

    def start_requests(self):
        url = "https://scholar.google.com/scholar?hl=en"

        params = {
            "q": "ar in education",
            "hl": "ru",
            "as_ylo": "2018",
            "as_yhi": "2023",
            "start": "0",
            "as_sdt": "0"  # Добавлен параметр as_sdt
        }

        yield scrapy.FormRequest(url=url, formdata=params, callback=self.parse)

    def parse(self, response):
        organic_results = response.css("#gs_res_ccl_mid .gs_r")

        results = []
        for result in organic_results:
            title = result.css("h3 a::text").get()
            link = "https://scholar.google.com" + result.css("h3 a::attr(href)").get()
            publication_info_summary = result.css(".gs_a::text").get()
            snippet = result.css(".gs_rs::text").get()

            results.append({
                "title": title,
                "link": link,
                "publication_info_summary": publication_info_summary,
                "snippet": snippet
            })

        # Сохранение результатов в файл organic.json
        with open("organic.json", "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False)
