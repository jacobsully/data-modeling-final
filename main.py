from flask import Flask, jsonify, request
import pandas
import json
import numpy as np
import matplotlib.pyplot as plt  
import math
from db import get_salaries, get_batters, get_pitchers
from flask.templating import render_template

app = Flask(__name__)

class DataStore():
     BestValueBatter=None
     BestValuePitcher=None
     WorstValueBatter=None
     WorstValuePitcher=None
     BatterData=None
     PitcherData=None
     Year=None
data=DataStore()

def distance(m,b,x,y):
    return abs(m*x + y + b) / math.sqrt(m*m)

@app.route("/salary",methods=["GET","POST"])
def Salary():
    return get_salaries() 

@app.route("/get-batter-data",methods=["GET","POST"])
def returnBatterData():
    b=data.BatterData
    return b

@app.route("/get-best-value-batter",methods=["GET","POST"])
def returnBestValueBatter():
    b=data.BestValueBatter
    return b

@app.route("/get-worst-value-batter",methods=["GET","POST"])
def returnWorstValueBatter():
    b=data.WorstValueBatter
    return b

@app.route("/get-pitcher-data",methods=["GET","POST"])
def returnPitcherData():
    p=data.Pitcher
    return p

@app.route("/",methods=["GET","POST"])
def homepage():
    data.Year = request.form.get('Year_field',1985)
    Year = int(data.Year)

    salaryJson = str(get_salaries().get_json()).replace("'", '"')
    salary = pandas.read_json(salaryJson)
    batterJson = str(get_batters().get_json()).replace("'", '"')
    batter = pandas.read_json(batterJson)
    batter['TeamId'] = batter['TeamId'].str[:-1]
    pitcherJson = str(get_pitchers().get_json()).replace("'", '"')
    pitcher = pandas.read_json(pitcherJson)

    new_df = pandas.merge(batter, salary, how='left', left_on=["playerId","TeamId"], right_on = ["playerId","TeamId"])
    new_df = new_df.dropna()
    new_df = new_df[new_df['AB']>100]
    new_df['OBP'] = (new_df['H'] + new_df['BB'] + new_df['IBB'] + new_df['HBP']) / (new_df['AB'] + new_df['BB'] + new_df['IBB'] + new_df['HBP'])

    batterSalary = pandas.DataFrame()
    batterSalary['playerId'] = new_df['playerId']
    batterSalary['TeamId'] = new_df['TeamId']
    batterSalary['OBP'] = new_df['OBP']
    batterSalary['Salary'] = new_df['Salary']
    batterSalary['Year'] = new_df['Year']

    npFrame = batterSalary[batterSalary['Year']==Year]
    npFrameCut = npFrame[['OBP','Salary']]
    npFrameCut = npFrame.sort_values(by=['OBP'])
    X = npFrameCut.to_numpy()

    m, b = np.polyfit(npFrameCut['OBP'], npFrameCut['Salary'], 1)

    #npFrame.plot.scatter(x='OBP',y='Salary')
    #plt.plot(npFrameCut['OBP'], m*npFrameCut['OBP'] + b)

    bestValueBatter = npFrame.iloc[0]
    worstValueBatter = npFrame.iloc[0]
    for index, row in npFrame.iterrows():
        if distance(m,b,row['OBP'], row['Salary']) > distance(m,b,bestValueBatter['OBP'], bestValueBatter['Salary']) and (m*bestValueBatter['OBP'] + bestValueBatter['Salary'] + b)<0:
            bestValueBatter = row
        elif distance(m,b,row['OBP'], row['Salary']) > distance(m,b,worstValueBatter['OBP'], worstValueBatter['Salary']):
            worstValueBatter = row

    data.BestValueBatter = bestValueBatter.to_json()
    prodBestValueBatter = data.BestValueBatter
    data.WorstValueBatter = worstValueBatter.to_json()
    prodWorstValueBatter = data.WorstValueBatter

    npFrame.reset_index(drop=True, inplace=True)
    batterData = npFrame.transpose().to_json()
    data.BatterData = batterData
    prodBatterData = data.BatterData

    return render_template("index.html",BestValueBatter=prodBestValueBatter,WorstValueBatter=prodWorstValueBatter,BatterData=prodBatterData,Year=Year)

if __name__ == '__main__':
    app.run()