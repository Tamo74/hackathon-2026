from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/part_time")
def part_time():
   return render_template("part_time.html")


@app.route("/subscriptions")
def subscriptions():
   return render_template("subscriptions.html")

@app.route("/finance")
def advice():
   return render_template("finance.html")

#410bb0b2fff24b4b9a7de9ec55d7d325
@app.route("/rent")
def rent():
   
   return render_template("rent.html")


