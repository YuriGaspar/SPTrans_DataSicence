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

#------ Importing the datasets

# Years 2014 ~ 2017
datasets = {}
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
                datasets[date_str] = pd.read_excel(url)
                last_day= day
            else:
                print ("Dia {} não encontrado".format(date_str))
                print (url)
                break
        
        if year <= 2014 and month < 10: #Before this date, the links doesn't have /before acesso_a_informacao
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
            datasets[year_str + month_str] = pd.read_excel(url_total)
            last_month = month
        else:
            print ("Mês Total {} não encontrado".format(date_str))
            print (url_total)
            break
    
# Vamos veriicar se os totais batem com a planilha de Total

#total = [0]*1000
total = {}
for year in range(2014, 2018):
    for month in range(1, 13):
#        
        if year == 2017 and month == last_month + 1:
            break
#        if month == last_month:
#            final_day = last_day
#        else:
#            final_day = calendar.monthrange(year, month)[1]
        total_month = 0
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            year_str = str(year)
            month_str = str(month)
            day_str = str(day)
            month_str = month_str.zfill(2)
            day_str = day_str.zfill(2)
            date_str = year_str + month_str + day_str
            
            total_month = datasets[date_str].iloc[:,datasets[date_str].shape[1] -1 ].sum() + total_month
        total[year_str+month_str] = total_month
        print ("Para o Mês de {} de {}, somando-se dia a dia chegamos em {} passageiros.".format(month_list[month - 1].title(), year, ('%f' % total[year_str+month_str]).rstrip('0').rstrip('.')))
        print ("Na planilha consolidada no Site da SPTrans o valor fornecido foi de {} passageiros".format(datasets[year_str + month_str].iloc[:,datasets[year_str + month_str].shape[1] -1].sum()))
        print ("Diferença de {} passageiros".format(total[year_str+month_str] - datasets[year_str + month_str].iloc[:,datasets[year_str + month_str].shape[1] -1 ].sum() ))
        print ("")


# SAND BOX

datasets["20141002"].iloc[:,17].sum()


# Verificar evolução de passageiros pagantes, bilhete unico, integração, por categoria etc


# Verificar quais linhas são mais utilizadas

# Verificar quais empresas transportam mais

datasets["20170101"].groupby("EMPRESA").sum()
# Verificar concessão vs. permissão
# verificar utilização por área (e entender o que significa)
# Verificar trajeto total e custo por passageiro e quilometragem e combustivel

