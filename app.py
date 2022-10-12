#!/usr/bin/env

import os
from twilio.rest import Client
import pandas as pd 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from flask import Flask, redirect, url_for, render_template, request

""" 
TODO 
- make twilio account and purchase phone number, set up API keys
- Make password more secure
- Host the website
"""

# Setup Twilio Client Connection Information
account_sid = "Enter Key"
auth_token = "Enter Key"

client = Client(account_sid, auth_token)


# Read Google Sheets and Parse Phone Numbers
def send_texts(sheet_url, numbers, message):
    url_1 = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
    rush_list = pd.read_csv(url_1)

    # Checks if phone number is already in DF Column
    has_phone = False
    for c in rush_list.columns:
        if "phone" in c.lower():
            has_phone = True
    
    # If there are NaN (aka not positioned in top left most point) filter out NaN
    if not has_phone:
        rush_list = rush_list.dropna(axis=0, how="all")
        rush_list = rush_list.dropna(axis=1, how="all")
        rush_list.columns = rush_list.iloc[0]
        rush_list = rush_list.iloc[1: , :]


    # Format phone numbers
    phones = []
    for col in rush_list.columns:
        if "phone" in col.lower():
            phones = rush_list[col].dropna().tolist()

    for i in range(len(phones)):
        phone = phones[i]
        phone = phone.replace('(', '')
        phone = phone.replace(')','')
        phone = phone.replace('-','')
        phone = phone.replace('_','')
        phone = phone.replace(',','')
        phone = phone.replace(' ', '')
        phone = phone.replace('+1', '')
        phone = "+1" + phone
        phones[i] = phone

    print(phones)
    # Send Twilio Messages
    for phone in phones:
        try:
            client.messages.create(
                to=phone,
                from_="+13802071428",
                body=message
            )
        except Exception as e:
            print(e)
            continue           

# Flask Portion
app = Flask(__name__)
input_url = ""
msg = ""


# Routes back to home page
@app.route("/")
def home():
    return render_template("goback.html")

# Login Page
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        global input_url
        global num
        global msg
        input_url = str(request.form["url"])
        num = str(request.form["number"])
        msg = str(request.form["text"])
        
        phones = send_texts(input_url, num, msg)
        return redirect(url_for("home", phone=phones))
    
    return render_template("index.html")

@app.route("/<phone>")
def phones(phone):
    return f"{phone}"

# Run app
if __name__ == "__main__":
    app.run(debug=True)