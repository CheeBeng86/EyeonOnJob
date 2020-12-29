

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.generic import TemplateView

import os
from selenium import webdriver
from bs4 import BeautifulSoup
import chromedriver_binary
import pandas as pd
import time

# Create your views here.

def datascrap(request):
    return render(request,'datascrap.html')


def datascrap_run(request):
    #!/usr/bin/env python
# coding: utf-8
# Use Selenium 
    driver = webdriver.Chrome()
    position=[]
    company=[]
    state=[]
    for j in range(1): #loop the page click
        if j==0:
            url='https://www.jobstreet.com.my/en/job-search/job-vacancy.php?ojs=1'
        else:
            url='https://www.jobstreet.com.my/en/job-search/job-vacancy.php?ojs=1&pg='+ str(j+1)

        driver.get(url)
        # load data into bs4
        soup = BeautifulSoup(driver.page_source,'html.parser')


        for row in soup.find_all('div',attrs={'class':'FYwKg _31UWZ fB92N_6 _1pAdR_6 FLByR_6 _2QIfI_6 _2cWXo _1Swh0 HdpOi'}) :

            #position
            h1rows  = row.find_all('h1')  
            for h1row in h1rows:
                print("POSITION : " + h1row.get_text())
                position.append(h1row.get_text())



            #company
            spanrowcompanys = row.find_all('span', attrs={'class':'FYwKg _1GAuD C6ZIU_6 _6ufcS_6 _27Shq_6 _29m7__6'}) 
            for spanrowcompany in spanrowcompanys:
                print("COMPANY : " + spanrowcompany.get_text())
                company.append(spanrowcompany.get_text())



            spanrowstates = row.find_all('span', attrs={'class':'FYwKg sXF6i _1GAuD _29LNX'}) 
            for spanrowstate in spanrowstates:
                print("STATE : " + spanrowstate.get_text())    
                state.append(spanrowstate.get_text())

        time.sleep(3)   

    driver.close()    

    
    df = pd.DataFrame(list(zip(position,company,state)), columns=['Position', 'Company','State'])
    filename = "Job_new - Copy.csv"
    path= os.path.join(settings.DATA_ROOT,filename)
    #copy data frame from csv
    df_add = pd.read_csv(path)
    df_add.append(df)
    #store in dataframe
    df_add.to_csv(path)
    return render(request, 'daraframe.html')

def plot_csv(request):
    filename = "Job_new.csv"
    path= os.path.join(settings.DATA_ROOT,filename)
    read_df = pd.read_csv(path,index_col=0)
    splitposition=[]
    splitcompany=[]
    splitstate=[]

    #Always display Number of vacancy in Job screet.com
    x_data=read_df['State']
    y_data=read_df['State'].value_counts()
    plot_div_all = plot([go.Bar(
        x=x_data,
        y=y_data,
        name='Vacancy by Company',
    )], output_type='div')
    for i in range(len(read_df)) :
        if "," in read_df.loc[i,"State"]:
            #print(read_df.loc[i,"State"])
            splittext= read_df.loc[i,"State"].split(",")
            for text in splittext:
                splitposition.append(read_df.loc[i,"Position"])
                splitcompany.append(read_df.loc[i,"Company"])
                splitstate.append(text.strip())
            #print(read_df.iloc[i])
            read_df = read_df.drop([i], axis=0)
    dfadd = pd.DataFrame(list(zip(splitposition,splitcompany,splitstate)), columns=['Position', 'Company','State'])
    read_df = read_df.append(dfadd, ignore_index = True)


    if request.method == 'POST'and request.POST["filterPosition"] != "":
        positionfilter = request.POST["filterPosition"] # token form text box
        #read_df = pd.read_csv(os.path.join(BASE, "Job_new.csv"),index_col=0)
        conditions = (read_df.Position.str.contains(positionfilter))
        position_df = read_df[conditions]
 
        x_data=position_df['Company']
        y_data=position_df['Company'].value_counts()
        plot_div_position = plot([go.Bar(
            x=x_data,
            y=y_data,
            name='Vacancy by Company',
        )], output_type='div')
    else:
        return render(request, "daraframe.html")

    #Filter state and Plot number of interested POSITION    
    if request.POST["statefilter"] != "":
        statefilter = request.POST["statefilter"] # token form text box
        #read_df = pd.read_csv(os.path.join(BASE, "Job_new.csv"),index_col=0)
        conditions = (read_df['State']==statefilter)
        state_df = read_df[conditions]
 
        x_data=y=state_df['State']
        y_data=y=state_df['State'].value_counts()
        plot_div_State = plot([go.Bar(
            x=x_data,
            y=y_data,
            name='Number of Vacancy in State',
        )], output_type='div')
    else:
        return render(request, "daraframe.html")

    return render(request, 'plotly.html', context ={'plot_div_position': plot_div_position,"read_df":read_df,"x_data":x_data,"y_data":y_data,
    "position_df":position_df,"positionfilter":positionfilter,"plot_div_all":plot_div_all,"plot_div_State":plot_div_State})



from plotly.offline import plot
import plotly.graph_objs as go

class PlotlyChartView(TemplateView):
    def get(self, request, *args, **kwargs):
        x_data=[0,1,2,3]
        y_data=[x**2 for x in x_data]
        plot_div = plot([go.Scatter(
            x=x_data,
            y=y_data,
            mode='lines',
            name='My Plotly Chart',
            opacity=0.8,
            marker_color='green'
        )], output_type='div')

        return render(request, 'plotly.html', context={'plot_div':plot_div})

