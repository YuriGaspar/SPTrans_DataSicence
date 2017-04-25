# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 12:53:53 2017

@author: Yuri Gaspar
"""

#------ Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import calendar
import urllib3
from datetime import datetime

#------ Importing the datasets

# Years 2014 ~ 2017
dataset_d = {}
dataset_m = {}
month_list = ["janeiro", "fevereiro", "marco", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
month_list_abr = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
errors = []

current_year = 2017
for year in range(2014, current_year + 1):
    for month in range(1, 13):
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            year_str = str(year)
            month_str = str(month)
            day_str = str(day)
            
            month_str = month_str.zfill(2)
            day_str = day_str.zfill(2)
            date_str = year_str + month_str + day_str
            
            if year <= 2014 and month < 10: #Before this date, the links doesn't have /before acesso_a_informacao
                url = ("http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/transportes/SPTrans/{}/{}/passageiros/Passag-{}.xls".format(year_str, month_list[month - 1], date_str))
            else:
                url = ("http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/transportes/SPTrans/acesso_a_informacao/{}/{}/passageiros/Passag-{}.xls".format(year_str, month_list[month - 1], date_str))
            http = urllib3.PoolManager()
            r = http.request('GET', url)
            
            if r.status < 400:
                print ("url from {} exists. Saving...".format(month_list_abr[month - 1] + "/" + day_str + "/" + year_str))
                dataset_d[date_str] = pd.read_excel(url)
                last_day= day
            else:
                print ("Dia {} não encontrado".format(month_list_abr[month - 1] + "/" + day_str + "/" + year_str))
                print (url)
                errors.append(url)
                
                if year == current_year:
                    break

        if year == 2014 and month <= 12: #Before this date, the links doesn't have /before acesso_a_informacao
            if year == 2014 and month == 4:
                url_total = ("http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/transportes/SPTrans/{}/{}/passageiros/Pass_Transp_{}.xlsx".format(year_str, month_list[month - 1], month_list_abr[month - 1] + str(year % 100)))
            elif year == 2014 and month == 10 or month == 11:
                url_total = ("http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/transportes/SPTrans/acesso_a_informacao/{}/{}/passageiros/Pass_Transp_{}.xls".format(year_str, month_list[month - 1], month_list_abr[month - 1] + str(year % 100)))
            elif year == 2014 and month == 12:
                url_total = ("http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/transportes/SPTrans/acesso_a_informacao/{}/{}/passageiros/Pass_Transp_{}.xlsx".format(year_str, month_list[month - 1], month_list_abr[month - 1] + str(year % 100)))
            else:
                url_total = ("http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/transportes/SPTrans/{}/{}/passageiros/Pass_Transp_{}.xls".format(year_str, month_list[month - 1], month_list_abr[month - 1] + str(year % 100)))   
        else:
            url_total = ("http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/transportes/SPTrans/acesso_a_informacao/{}/{}/passageiros/Pass_Transp_{}.xls".format(year_str, month_list[month - 1], month_list_abr[month - 1] + str(year % 100)))
        
        http = urllib3.PoolManager()
        r = http.request('GET', url_total)
        
        if r.status < 400:
            print ("url from Total {} exists. Saving...".format(month_list_abr[month - 1] + "/" + year_str))
            dataset_m[year_str + month_str] = pd.read_excel(url_total)
            last_month = month
        else:
            print ("Mês Total {} não encontrado".format(month_list_abr[month - 1] + "/" + year_str))
            print (url_total)
            errors.append(url_total)
            if year == current_year:
                break

#------ Verifying Numbers
   
# Let's check if the sum of the days of month hits with the worksheet's total
import time
total = {}
total_paying = {}
total_integration = {}
total_free_passengers = {}
total_free_students = {}

xTicks = []

ytotal = []
ytotal_paying = []
ytotal_integration = []
ytotal_free_passengers = []
ytotal_free_students = []

for year in range(2014, current_year + 1):
    for month in range(1, 13):
        
        if year == 2017 and (month == last_month):
            break

        total_month = 0
        total_paying_month = 0
        total_integration_month = 0
        total_free_passengers_month = 0
        total_free_students_month = 0
        
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            year_str = str(year)
            month_str = str(month)
            day_str = str(day)
            month_str = month_str.zfill(2)
            day_str = day_str.zfill(2)
            date_str = year_str + month_str + day_str
            
            total_month = dataset_d[date_str].iloc[:,dataset_d[date_str].shape[1] -1 ].sum() + total_month
            
            if time.strptime(date_str, "%Y%m%d") >= time.strptime("20150409", "%Y%m%d"): 
                 total_paying_month = dataset_d[date_str].iloc[:,dataset_d[date_str].shape[1] -5 ].sum() + total_paying_month
                 total_integration_month = dataset_d[date_str].iloc[:,dataset_d[date_str].shape[1] -4 ].sum() + total_integration_month
                 total_free_passengers_month = dataset_d[date_str].iloc[:,dataset_d[date_str].shape[1] -3 ].sum() + total_free_passengers_month
                 total_free_students_month = dataset_d[date_str].iloc[:,dataset_d[date_str].shape[1] -2 ].sum() + total_free_students_month
            else:            
                 total_paying_month = dataset_d[date_str].iloc[:,dataset_d[date_str].shape[1] -4 ].sum() + total_paying_month
                 total_integration_month = dataset_d[date_str].iloc[:,dataset_d[date_str].shape[1] -3 ].sum() + total_integration_month
                 total_free_passengers_month = dataset_d[date_str].iloc[:,dataset_d[date_str].shape[1] -2 ].sum() + total_free_passengers_month
                
        total[year_str+month_str] = int(total_month)
        total_paying[year_str+month_str] = int(total_paying_month)
        total_integration[year_str+month_str] = int(total_integration_month)
        total_free_passengers[year_str+month_str] = int(total_free_passengers_month)
        total_free_students[year_str+month_str] = int(total_free_students_month)
        
        print ("Para o Mês de {} de {}, somando-se dia a dia chegamos em {} passageiros.".format(month_list[month - 1].title(), year, ('%f' % total[year_str+month_str]).rstrip('0').rstrip('.')))
        print ("Na planilha consolidada no Site da SPTrans o valor fornecido foi de {} passageiros".format(dataset_m[year_str + month_str].iloc[:,dataset_m[year_str + month_str].shape[1] -1].sum()))
        print ("Diferença de {} passageiros".format(total[year_str+month_str] - dataset_m[year_str + month_str].iloc[:,dataset_m[year_str + month_str].shape[1] -1 ].sum() ))
        print ("")
        
        xTicks.append(month_list_abr[month - 1].title() + " " + year_str) # for plot
        
        ytotal.append(total_month/10**6)
        ytotal_paying.append(total_paying_month/10**6)
        ytotal_integration.append(total_integration_month/10**6)
        ytotal_free_passengers.append(total_free_passengers_month/10**6)
        ytotal_free_students.append(total_free_students_month/10**6)

#------ Some Statitics

import statistics
statistics.mean(ytotal) # Arithmetic mean (average) of data.
statistics.median(ytotal) # Median (middle value) of data.
statistics.stdev(ytotal) # Sample standard deviation of data.

#------ Plotting Total Passengers  vs. Month

x = list(range(0, len(ytotal) ))
plt.xticks(x, xTicks)
plt.xticks(range(len(ytotal)), xTicks, rotation=60) #writes strings with 45 degree angle
colors = []
for i in range(0, len(ytotal)):
    if i < 12:
        colors.append('#F44336')
    elif i >= 12 and i < 24:
        colors.append('#FFC107')
    elif i >= 24 and i < 36:
        colors.append('#4A148C')
    else :
        colors.append('#48A51A')
plt.bar(x,ytotal, color=colors)
plt.tight_layout()
plt.xlabel("Data")
plt.ylabel('Quantidade de Passageiros Trasportados \n (em milhões de Pasageiros)')   
plt.show()

#------ Plotting Paying Passenger and Integration Passenger and Free Passengers and Free Pass Students 

raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
        'pre_score': [4, 24, 31, 2, 3],
        'mid_score': [25, 94, 57, 62, 70],
        'post_score': [5, 43, 23, 23, 51]}
df = pd.DataFrame(raw_data, columns = ['first_name', 'pre_score', 'mid_score', 'post_score'])
df

# Create the general blog and the "subplots" i.e. the bars
f, ax1 = plt.subplots(1, figsize=(10,5))

# Set the bar width
bar_width = 0.15

# positions of the left bar-boundaries
bar_l = [i+1 for i in range(len(df['pre_score']))]

# positions of the x-axis ticks (center of the bars as bar labels)
tick_pos = [1, 2, 3, 4, 5]

# Create a bar plot, in position bar_1
ax1.bar(bar_l,
        # using the pre_score data
        df['pre_score'],
        # set the width
        width=bar_width,
        # with the label pre score
        label='Pre Score',
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='#F4561D')

# Create a bar plot, in position bar_1
ax1.bar(bar_l,
        # using the mid_score data
        df['mid_score'],
        # set the width
        width=bar_width,
        # with pre_score on the bottom
        bottom=df['pre_score'],
        # with the label mid score
        label='Mid Score',
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='#F1911E')

# Create a bar plot, in position bar_1
ax1.bar(bar_l,
        # using the post_score data
        df['post_score'],
        # set the width
        width=bar_width,
        # with pre_score and mid_score on the bottom
        bottom=[i+j for i,j in zip(df['pre_score'],df['mid_score'])],
        # with the label post score
        label='Post Score',
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='#F1BD1A')
test = df['first_name']
# set the x ticks with names
plt.xticks(tick_pos, df['first_name'])

# Set the label and legends
ax1.set_ylabel("Total Passengers per Category")
ax1.set_xlabel("Date")
plt.legend(loc='upper left')

# Set a buffer around the edge
#plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])


# Verificar quais 100 linhas são mais utilizadas 

# Verificar quais 10 linhas são mais utilizadas por AREA

# Verificar quais 5 linhas são mais utilizadas por EMPRESA

# Verificar quais empresas transportam mais

# Verificar concessão vs. permissão

# verificar utilização por área (e entender o que significa)

# Verificar trajeto total e custo por passageiro e quilometragem e combustivel

