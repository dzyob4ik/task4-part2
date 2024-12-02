from fastapi import APIRouter  # Імпортує APIRouter для створення маршрутизатора в FastAPI
from elasticsearch import Elasticsearch #імпортує еластік


router = APIRouter(tags=['10 knownRansomwareCampaignUse CVEs'])  
@router.get("/get/known")  
def getcritical(): 
    client = Elasticsearch(
    "https://1bb469e994bb4ab59fc129b1b8f6eb34.us-central1.gcp.cloud.es.io:443",
    api_key="cjZqSWg1TUJBSG9VaG1uemhiZkE6aUZOQ3p0eFhTUnUzUXNWTWVJdTlwQQ==")
    response = client.search(
        index="test_1", #Ім'я індексу в Elasticsearch
        body={
            "query": {
                "match_all": {} #повертає всі документи з індексу,для подальшої фільтрації
            }
        }
    ) 
    cves_found = [] #  порожній список для збереження знайдених CVE 
    if response["hits"]["hits"]: # Перевірка, чи є документ у результаті
        document = response["hits"]["hits"][0]["_source"] # Отримання першого документа з результату і доступ до вмісту через сорс
    for i in range(len(document["vulnerabilities"])):  # Ітерує через індекси списку вразливостей у JSON-даних
        if document["vulnerabilities"][i]["knownRansomwareCampaignUse"] == 'Known':  
            # Перевіряє, чи значення поля 'knownRansomwareCampaignUse' дорівнює Known
            cves_found.append(document["vulnerabilities"][i])  # Додає вразливість до списку cves_found
        if len(cves_found) == 10:  # Перериває цикл, якщо знайдено 10 CVE
            break
        
    
    for cve in cves_found:
        client.index(
            index="filtered_getknown_cves",  # Ім'я нового індексу 
            document=cve  # Збереження кожного CVE як окремий документ
        )    
    return cves_found  # Повертає список знайдених CVE
    

        