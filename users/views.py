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
    elif request.method == 'POST' and request.POST["scrapedata"]!="":
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

 