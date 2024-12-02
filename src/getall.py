from fastapi import APIRouter  # Імпортує APIRouter для створення маршрутизатора в FastAPI
from elasticsearch import Elasticsearch #імпортує еластік

router = APIRouter(tags=['Last CVEs in 5 days'])  # Створює об'єкт маршрутизатора з тегом для  маршрутів у документації FastAPI

@router.get("/get/all")  
def get_recent_cves():  
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
    recent_cves = [] #потім для заповнення
    max_cves = 40  # Визначає максимальну кількість CVE, які потрібно повернути
    recent_dates = ["2024-11-21", "2024-11-20", "2024-11-19", "2024-11-18", "2024-11-17"]  #для фільтрації
    if response["hits"]["hits"]: # Перевірка, чи є документ у результаті
        document = response["hits"]["hits"][0]["_source"] # Отримання першого документа з результату і доступ до вмісту через сорс
    for vulnerability in document['vulnerabilities']:  # Ітерує через список вразливостей у JSON-даних.
        if vulnerability['dateAdded'] in recent_dates:  # Перевіряє, чи дата додавання вразливості є в списку нещодавніх дат
            recent_cves.append(vulnerability)  # Додає вразливість до списку recent_cves
        if len(recent_cves) == max_cves:  # Перевіряє, чи досягнуто максимальну кількість CVE
            break
    for cve in recent_cves:
        client.index(
            index="filtered_getall_cves",  # Ім'я нового індексу
            document=cve  # Збереження кожного CVE як окремий документ
        )  

    return recent_cves  # Повертає список нещодавніх CVE.
