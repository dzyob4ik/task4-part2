from fastapi import FastAPI
import getnew, getall, getknown, search, initdb

app=FastAPI(
    title="NIST CVE API", #добавив заголовок і опис
    description="FastAPI додаток для отримання інформації про CVE з NIST"
)

@app.get('/') #тестив як працює фастапі
def text_hello():
    return{'text': 'hello'}

@app.get("/info") #вже сама функція гетінфо
def get_info():
   #виводить інфу про апку і про мене
    return {
        "app_name": "NIST CVE finder",
        "Creator": "Taras Dzoban",

    }
   #добавляємо роутера
app.include_router(initdb.router)
app.include_router(getnew.router)
app.include_router(getall.router)
app.include_router(getknown.router)
app.include_router(search.router)