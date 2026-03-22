from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
import os
import json
import requests

app = Flask(__name__)
load_dotenv()
ADZUNA_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_KEY = os.getenv("ADZUNA_APP_KEY")
LETTING_KEY= os.getenv("LETTINGKEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/job", methods=["GET", "POST"])
def job():
   #id adzuna jobs 83164e22
   # api key 0593f89966311970b9e99491fe5a2d1b
   if request.method == "POST":
        jobs = []
        job_title = request.form.get("what")
        location = request.form.get("where")
        contract = request.form.get("contract_type")

        url = f"https://api.adzuna.com/v1/api/jobs/us/search/1"

        params = {
            "app_id": ADZUNA_ID,
            "app_key": ADZUNA_KEY,
            "what": job_title,
            "where": location
        }

        # contract filtering
        if contract == "part_time":
            params["part_time"] = 1
        elif contract == "full_time":
            params["full_time"] = 1

        response = requests.get(url, params=params)
        data = response.json()

        jobs = data.get("results", [])

        print(jobs)

   return render_template("job.html", jobs=jobs)




@app.route("/finance")
def advice():
   return render_template("finance.html")


#410bb0b2fff24b4b9a7de9ec55d7d325
@app.route("/rent", methods=["GET", "POST"] )
def rent():
     properties =[]
     city_form = request.form.get("city")
     if request.method == "POST":
        url = "https://api.rentcast.io/v1/listings/rental/long-term"

        headers = {
           "X-Api-Key": LETTING_KEY
    }
    
        params = {
           "city": city_form,
           "limit": 15
    }
        print(LETTING_KEY)
        response = requests.get(url, headers=headers, params=params)
        properties = response.json()
        print(json.dumps(properties, indent=4))
        
        print(properties)
        
     return render_template("rent.html", properties=properties)


