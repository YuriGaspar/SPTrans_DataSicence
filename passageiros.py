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
import pylab as pl #needed yet?

#------ Importing the datasets

# Years 2014 ~ 2017
dataset_d = {}
dataset_m = {}
month_list = ["janeiro", "fevereiro", "marco", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
month_list_abr = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

for year in range(2014, 2018):
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
                print ("url from {} exists. Saving...".format(date_str))
                dataset_d[date_str] = pd.read_excel(url)
                last_day= day
            else:
                print ("Dia {} não encontrado".format(date_str))
                print (url)
                break

        if year == 2014 and month <= 12: #Before this date, the links doesn't have /before acesso_a_informacao
            if year == 2014 and month == 4:
                url_total = ("http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/transportes/SPTrans/{}/{}/passageiros/Pass_Transp_{}.xlsx".format(year_str, month_list[month - 1], month_list_abr[month - 1] + str(year % 100)))
            elif year == 2014 and month == 12:
                url_total = ("http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/transportes/SPTrans/acesso_a_informacao/{}/{}/passageiros/Pass_Transp_{}.xlsx".format(year_str, month_list[month - 1], month_list_abr[month - 1] + str(year % 100)))
            else:
                url_total = ("http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/transportes/SPTrans/{}/{}/passageiros/Pass_Transp_{}.xls".format(year_str, month_list[month - 1], month_list_abr[month - 1] + str(year % 100)))   
        else:
            url_total = ("http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/transportes/SPTrans/acesso_a_informacao/{}/{}/passageiros/Pass_Transp_{}.xls".format(year_str, month_list[month - 1], month_list_abr[month - 1] + str(year % 100)))
        
        http = urllib3.PoolManager()
        r = http.request('GET', url_total)
        
        if r.status < 400:
            print ("url from Total {} exists. Saving...".format(month_list_abr[month - 1] + year_str))
            dataset_m[year_str + month_str] = pd.read_excel(url_total)
            last_month = month
        else:
            print ("Mês Total {} não encontrado".format(date_str))
            print (url_total)
            break

#------ Verifying Numbers
   
# Let's check if the sum of the days of month hits with the worksheet's total

total = {}
xTicks = []
ytotal = []

for year in range(2014, 2018):
    for month in range(1, 13):
        
        if year == 2017 and month == last_month + 1:
            break

        total_month = 0
        
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            year_str = str(year)
            month_str = str(month)
            day_str = str(day)
            month_str = month_str.zfill(2)
            day_str = day_str.zfill(2)
            date_str = year_str + month_str + day_str
            
            total_month = dataset_d[date_str].iloc[:,dataset_d[date_str].shape[1] -1 ].sum() + total_month
        
        total[year_str+month_str] = int(total_month)
        print ("Para o Mês de {} de {}, somando-se dia a dia chegamos em {} passageiros.".format(month_list[month - 1].title(), year, ('%f' % total[year_str+month_str]).rstrip('0').rstrip('.')))
        print ("Na planilha consolidada no Site da SPTrans o valor fornecido foi de {} passageiros".format(dataset_m[year_str + month_str].iloc[:,dataset_m[year_str + month_str].shape[1] -1].sum()))
        print ("Diferença de {} passageiros".format(total[year_str+month_str] - dataset_m[year_str + month_str].iloc[:,dataset_m[year_str + month_str].shape[1] -1 ].sum() ))
        print ("")
        
        xTicks.append(month_list_abr[month - 1].title() + " " + year_str) # for plot
        ytotal.append(((total_month/10**6))) 

#------ Plotting Total Passengers  vs. Month

x = list(range(0, len(ytotal) ))
plt.xticks(x, xTicks)
plt.xticks(range(len(ytotal)), xTicks, rotation=60) #writes strings with 45 degree angle
plt.bar(x,ytotal)
plt.tight_layout()
plt.xlabel("Data")
plt.ylabel('Quantidade de Passageiros Trasportados \n (em milhões de Pasageiros)')   
plt.show()

# Verificar quais 100 linhas são mais utilizadas 

# Verificar quais 10 linhas são mais utilizadas por AREA

# Verificar quais 5 linhas são mais utilizadas por EMPRESA

# Verificar quais empresas transportam mais

# Verificar concessão vs. permissão

# verificar utilização por área (e entender o que significa)

# Verificar trajeto total e custo por passageiro e quilometragem e combustivel

