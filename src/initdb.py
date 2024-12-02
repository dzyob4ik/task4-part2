from fastapi import APIRouter  # Імпортує APIRouter для створення маршрутизатора в FastAPI
from elasticsearch import Elasticsearch #імпортує еластік
import json

router = APIRouter(tags=['Last CVEs in 5 days']) 
@router.get('/init-db') #ініціалізуємо бд
def init_db():
    
    json_file = "/home/taras/Desktop/Python-final/task4-part1/src/known_exploited_vulnerabilities.json" # шлях до джсона
    URL = "https://1bb469e994bb4ab59fc129b1b8f6eb34.us-central1.gcp.cloud.es.io:443"
    API = "cjZqSWg1TUJBSG9VaG1uemhiZkE6aUZOQ3p0eFhTUnUzUXNWTWVJdTlwQQ=="


    client = Elasticsearch( 
    URL,
    api_key=API,
    )
    with open(json_file, "r") as file:  # Відкриває JSON-файл для читання
        data = json.load(file)  # Завантажує дані з JSON-файлу у змінну data
        

    response = client.create(index="test_1", id="test-doc", body=data) #створили індекс і залили інфу
    return response