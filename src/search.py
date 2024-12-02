from fastapi import APIRouter, Query  # Імпортує APIRouter для створення маршрутизатора та Query для обробки параметрів запиту
import json  # Імпортує модуль для роботи з JSON-файлами.
from elasticsearch import Elasticsearch #імпортує еластік

router = APIRouter(tags=['Search by keyword'])  
@router.get('/get')  
def search_by_key(query: str = Query(description="Keyword to search for in vulnerabilities")):   #пошук за квері
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
    if response["hits"]["hits"]: # Перевірка, чи є документ у результаті
        document = response["hits"]["hits"][0]["_source"] # Отримання першого документа з результату і доступ до вмісту через сорс
    filtered_vulnerabilities = []  # порожній список для збереження знайдених вразливостей
    for vulnerability in document["vulnerabilities"]:  # Ітерує через кожну вразливість у списку
        if query.lower() in json.dumps(vulnerability).lower():  # Перевіряє, чи ключове слово query є у вразливості (case-insensitive)
            filtered_vulnerabilities.append(vulnerability)  # Додає знайдену вразливість до списку filtered_vulnerabilities
    
    for cve in filtered_vulnerabilities:
        client.index(
            index="filtered_search_by_word_cves",  # Ім'я нового індексу
            document=cve  # Збереження кожного CVE як окремий документ
        )    
    
    return {"result": filtered_vulnerabilities}  # Повертає словник з ключем result, що містить знайдені вразливості

    
