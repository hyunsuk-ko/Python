import pandas as pd
from flask import Flask, request, jsonify
import re
from IPython.display import display, HTML
import csv

# project: p4
# submitter: hko26
# partner: none

app = Flask(__name__)
df = pd.read_csv("main.csv")

count = 0
count_A = 0
count_B = 0
subscriber_list = []

@app.route('/')
def home():
    global count
    count += 1
    if count <= 10:
        if count % 2 == 0:
            global count_A
            count_A += 1
            with open("index_A.html") as f:
                html = f.read()
        else:
            global count_B
            count_B += 1
            with open("index_B.html") as f:
                html = f.read()
    else:
        if count_A > count_B:
            with open("index_A.html") as f:
                html = f.read()
        elif count_A < count_B:
            with open("index_B.html") as f:
                html = f.read()
            
    return html

@app.route('/browse.html')
def browse():
    return df._repr_html_()

@app.route('/hi.html')
def hi_handler():
    return "howdy!"

@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    global subscriber_list
    if re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email):
        with open("emails.txt", "a") as f: 
            f.write(email + "\n")
            f.close()
        with open("emails.txt") as g:
            for line in g:
                subscriber_list.append(line)
        return jsonify("thanks, you're subscriber number {}!".format(len(subscriber_list)))
    return jsonify("Please enter a valid email address.")

@app.route('/donate.html')
def donate():
    if request.args.get("from") == "A":
        global count_A
        count_A += 1
    else:
        global count_B
        count_B += 1
    with open('donate.html') as f:
        html = f.read()
    return html

@app.route('/api.html')
def api():
    with open("api.html") as f:
        html = f.read()
    return html
    
@app.route('/datacols.json')
def data_cols():
    with open("main.csv") as f:
        data = f.read()
        columns = data.split('\n')
    return jsonify(columns[0].split(","))

@app.route('/datarows.json')
def data_rows():
    data_list = []
    with open("main.csv") as f:
        rows = f.read().split("\n")[1:]
    #data_list.append(rows)
    print(len(rows))
    return jsonify(rows)

@app.route('/data.json')
def data():
    count = 0
    data_list = []
    
    state = request.args.get('state')
    urban_index = request.args.get('urban_index')
    lean = request.args.get('lean')
    poll_2020_D = request.args.get('poll_2020_D')
    poll_2020_R = request.args.get('poll_2020_R')
    
    with open("main.csv") as f:
        data = csv.DictReader(f)
        for row in data:
            if row["state"] == state:
                data_list.append([count, row])
                count += 1
            elif row["urban_index"] == urban_index:
                data_list.append([count, row])
                count += 1
            elif row["lean"] == lean:
                data_list.append([count, row])
                count += 1
            elif row["poll_2020_D"] == poll_2020_D:
                data_list.append([count, row])
                count += 1
            elif row["poll_2020_R"] == poll_2020_R:
                data_list.append([count, row])
                count += 1
    return jsonify(data_list)

@app.route('/datadicts.json')
def data_dict():
    data_list = []
    with open("main.csv") as f:
        data = csv.DictReader(f)
        for row in data:
            data_list.append(row)
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(host="0.0.0.0") # don't change this line!