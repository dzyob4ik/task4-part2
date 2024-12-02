from fastapi import APIRouter, Query  # Імпортує APIRouter для створення маршрутизатора та Query для обробки параметрів запиту
import json  # Імпортує модуль для роботи з JSON-файлами.
from elasticsearch import Elasticsearch

router = APIRouter(tags=['Search by keyword'])  
@router.get('/get')  
def search_by_key(query: str = Query(description="Keyword to search for in vulnerabilities")):  
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
    if response["hits"]["hits"]:
        document = response["hits"]["hits"][0]["_source"]
    filtered_vulnerabilities = []  # порожній список для збереження знайдених вразливостей
    for vulnerability in document["vulnerabilities"]:  # Ітерує через кожну вразливість у списку
        if query.lower() in json.dumps(vulnerability).lower():  # Перевіряє, чи ключове слово query є у вразливості (case-insensitive)
            filtered_vulnerabilities.append(vulnerability)  # Додає знайдену вразливість до списку filtered_vulnerabilities
    return {"result": filtered_vulnerabilities}  # Повертає словник з ключем result, що містить знайдені вразливості

    
