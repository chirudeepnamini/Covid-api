from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup as bs
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

web_page= requests.get('https://www.mygov.in/covid-19/')
soup=bs(web_page.text,features="html.parser")
@app.on_event("startup")
async def retrieve():
    pass

@app.get("/vaccine-count")
def vaccine():
    yday_vcount=soup.find_all("div",class_="yday-vcount")
    total_vcount=soup.find_all("div",class_="total-vcount")
    return {"Yesterday's vaccine count":yday_vcount[0].strong.get_text(),"Total vaccination count":total_vcount[0].strong.get_text()}
@app.get("/testing-count")
def testing():
    testing_count=soup.find_all("strong",class_="testing_count")
    day=soup.find("div",class_="testing_sample")
    return {"date":day.find_all("span")[1].get_text(),"Testing count":testing_count[0].get_text(),"Total testing count":testing_count[1].get_text()}
@app.get("/num-cases")
def cases():
    count=soup.find_all("span",class_="icount")
    return {
        "Active cases":count[0].get_text(),
        "Total cases":count[1].get_text(),
        "Discharged":count[2].get_text(),
        "Deaths":count[3].get_text(),
    }
@app.get("/state-wise")
def statedata():
    info={}
    state_data=soup.find_all("div",class_="views-row")
    for i in range(0,len(state_data)-129):
        try:
            info[state_data[i].find("span",class_="st_name").get_text()] ={
                "Confirmed-cases":state_data[i].find("div",class_="tick-confirmed").small.get_text(),
                "Active-cases":state_data[i].find("div",class_="tick-active").small.get_text(),
                "Discharged":state_data[i].find("div",class_="tick-discharged").small.get_text(),
                "Deaths":state_data[i].find("div",class_="tick-death").small.get_text(),
                "Total-vaccinated":state_data[i].find("div",class_="tick-total-vaccine").small.get_text()
            }
            print(state_data[i].find("span",class_="st_name").get_text())
            print(state_data[i].find("span",class_="st_number").get_text())
            print(state_data[i].find("div",class_="tick-confirmed").small.get_text())
            print(state_data[i].find("div",class_="tick-active").small.get_text())
            print(state_data[i].find("div",class_="tick-discharged").small.get_text())
            print(state_data[i].find("div",class_="tick-death").small.get_text())
            print(state_data[i].find("div",class_="tick-total-vaccine").small.get_text())

        except:
            print("some error")
            print(len(state_data))
    return info
