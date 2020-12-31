from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm


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
from plotly.offline import plot
import plotly.graph_objs as go

def dashboard(request):
    if request.method == 'POST' and request.POST["filterPosition"]!="":
        positionfilter = request.POST["filterPosition"] # token form text box
        #positionfilter = request.POST.get('filterPosition', False)
        filename = "Job_new.csv"
        path= os.path.join(settings.DATA_ROOT,filename)
        read_df = pd.read_csv(path,index_col=0)
        conditions = (read_df.Position.str.contains(positionfilter))
        position_df = read_df[conditions]
 
        x_data=position_df['Company']
        y_data=position_df['Company'].value_counts()
        plot_div_position = plot([go.Bar(
            x=x_data,
            y=y_data,
            name='Vacancy by Company',
        )], output_type='div')

        return render(request, 'users/dashboard.html', context ={'plot_div_position': plot_div_position,"read_df":read_df,"x_data":x_data,"y_data":y_data})
    elif request.method == 'POST' and request.POST["filterState"]!="":
        filterState = request.POST["filterState"] # token form text box
        #positionfilter = request.POST.get('filterPosition', False)
        filename = "Job_new.csv"
        path= os.path.join(settings.DATA_ROOT,filename)
        read_df = pd.read_csv(path,index_col=0)
        conditions = (read_df.State.str.contains(filterState))
        state_df = read_df[conditions]
 
        x_data=state_df['State']
        y_data=state_df['State'].value_counts()
        plot_div_position = plot([go.Bar(
            x=x_data,
            y=y_data,
            name='Vacancy by State',
        )], output_type='div')

        return render(request, 'users/dashboard.html', context ={'plot_div_state': plot_div_position,"read_df":read_df,"x_data":x_data,"y_data":y_data})
    elif request.method == 'POST' and request.POST.get("scrapedata","0")=="1":
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
        filename = "Job_new.csv"
        path= os.path.join(settings.DATA_ROOT,filename)
        #copy data frame from csv
        df_add = pd.read_csv(path)
        df_add.append(df)
        #store in dataframe
        df_add.to_csv(path)
        

        return render(request, "users/dashboard.html",context ={'plot_div_scrape': "Scape Done"})
    else:
        return render(request, "users/dashboard.html")
     


def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))

 