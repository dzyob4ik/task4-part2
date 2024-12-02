
from fastapi import APIRouter# Імпортує APIRouter для створення маршрутизатора в FastAPI
from elasticsearch import Elasticsearch


router = APIRouter(tags=['10NEW CVEs'])

@router.get("/get/new")
def getnew10():
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
    results = [] #  порожній список для збереження знайдених CVE 
    for i in range(10): # Ітерує через перші 10 найновіших вразливостей у списку
        results.append({ # Додає до списку results словник з даними про CVE
            "CVE": document["vulnerabilities"][i]["cveID"],  #ітерує по індексу
            "Name": document["vulnerabilities"][i]["vulnerabilityName"],
            "Date Added": document["vulnerabilities"][i]["dateAdded"]
        })
    
    return results #Повертає список з 10 нових CVE
