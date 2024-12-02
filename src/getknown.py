from fastapi import APIRouter  # Імпортує APIRouter для створення маршрутизатора в FastAPI
from elasticsearch import Elasticsearch


router = APIRouter(tags=['10 knownRansomwareCampaignUse CVEs'])  
@router.get("/get/known")  
def getcritical(): 
    client = Elasticsearch(
    "https://1bb469e994bb4ab59fc129b1b8f6eb34.us-central1.gcp.cloud.es.io:443",
    api_key="cjZqSWg1TUJBSG9VaG1uemhiZkE6aUZOQ3p0eFhTUnUzUXNWTWVJdTlwQQ==")
    # Визначає шлях до JSON-файлу з відомими вразливостями
    response = client.search(
        index="test_1",
        body={
            "query": {
                "match_all": {}
            },
            "size": 1  # Limit to the first document
        }
    ) 
    cves_found = [] #  порожній список для збереження знайдених CVE 
    if response["hits"]["hits"]:
        document = response["hits"]["hits"][0]["_source"]
    for i in range(len(document["vulnerabilities"])):  # Ітерує через індекси списку вразливостей у JSON-даних.
        if document["vulnerabilities"][i]["knownRansomwareCampaignUse"] == 'Known':  
            # Перевіряє, чи значення поля 'knownRansomwareCampaignUse' дорівнює Known
            cves_found.append(document["vulnerabilities"][i])  # Додає вразливість до списку cves_found
        if len(cves_found) == 10:  # Перериває цикл, якщо знайдено 10 CVE
            break
    return cves_found  # Повертає список знайдених CVE
    

        