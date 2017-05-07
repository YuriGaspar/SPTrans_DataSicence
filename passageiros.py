# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 12:53:53 2017

@author: Yuri Gaspar
"""

#------ Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import calendar
import urllib3
from datetime import datetime
import locale
locale.setlocale(locale.LC_ALL, 'German')

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
            
            if year <= 2014 and month < 10: # Before this date, the links doesn't have /before acesso_a_informacao
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
        
        if year == current_year and month == last_month:
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
        
            empresa_today = dataset_d[date_str].groupby(by=["EMPRESA"])[dataset_d[date_str].columns.values[-1]].sum()
            tipo_today = dataset_d[date_str].groupby(by=["TIPO"])[dataset_d[date_str].columns.values[-1]].sum()
            area_today = dataset_d[date_str].groupby(by=["AREA"])[dataset_d[date_str].columns.values[-1]].sum()
            linha_today = dataset_d[date_str].iloc[:, [1, 2, 3, 4, -1]]
            
            if year == 2014 and month == 1 and day == 1: 
                empresa = empresa_today
                tipo = tipo_today
                area = area_today
                linha = linha_today
            else: 
                empresa = pd.concat([empresa_today, empresa], axis=1).fillna(0).sum(axis=1)
                tipo = pd.concat([tipo_today, tipo], axis=1).fillna(0).sum(axis=1)
                area = pd.concat([area_today, area], axis=1).fillna(0).sum(axis=1)
                linha_today.columns.values[-1] = "PASSAGEIROS"
                linha.columns.values[-1] = "PASSAGEIROS"
                linha = pd.concat([linha_today, linha], axis=0).fillna(0)
                linha = linha.groupby(by=["TIPO", "AREA", "EMPRESA", "LINHA"])[linha.columns.values[-1]].sum()
                linha = linha.reset_index()
                
                #20141203 começam a ter linhas sem nada mas com quantidade de passageiros
                
        total[year_str+month_str] = int(total_month)
        total_paying[year_str+month_str] = int(total_paying_month)
        total_integration[year_str+month_str] = int(total_integration_month)
        total_free_passengers[year_str+month_str] = int(total_free_passengers_month)
        total_free_students[year_str+month_str] = int(total_free_students_month)
        
        locale.format('%.2d', dataset_m[year_str + month_str].iloc[:,dataset_m[year_str + month_str].shape[1] -1].sum(), True)
        
        print ("Para o Mês de {} de {}, somando-se dia a dia chegamos em {} passageiros.".format(month_list[month - 1].title(), year, locale.format('%.2d', total[year_str+month_str], True) ))
        print ("Na planilha consolidada no Site da SPTrans o valor fornecido foi de {} passageiros".format(locale.format('%.2d', dataset_m[year_str + month_str].iloc[:,dataset_m[year_str + month_str].shape[1] -1].sum(), True)))
        print ("Diferença de {} passageiros".format( locale.format('%.2d', total[year_str+month_str] - dataset_m[year_str + month_str].iloc[:,dataset_m[year_str + month_str].shape[1] -1 ].sum(), True) ))
        print ("")
        
        xTicks.append(month_list_abr[month - 1].title() + " " + year_str) # for plot
        
        ytotal.append(total_month/10**6)
        ytotal_paying.append(total_paying_month/10**6)
        ytotal_integration.append(total_integration_month/10**6)
        ytotal_free_passengers.append(total_free_passengers_month/10**6)
        ytotal_free_students.append(total_free_students_month/10**6)
    

#------ Creating a Index Renaming the Columns and Sorting 
empresa = empresa.reset_index()
empresa.columns = ["EMPRESA", "PASSAGEIROS"]
empresa = empresa.sort_values("PASSAGEIROS", ascending=False)

tipo = tipo.reset_index()
tipo.columns = ["TIPO", "PASSAGEIROS"]
tipo = tipo.sort_values("PASSAGEIROS", ascending=False)

area = area.reset_index()
area.columns = ["AREA", "PASSAGEIROS"]
area = area.sort_values("PASSAGEIROS", ascending=False)

linha = linha.drop(linha.index[[0]]) #Deleting the first line with error values 
linha = linha.sort_values("PASSAGEIROS", ascending=False) #Sorting max => min
linha = linha.reset_index() # Creating a new index
linha = linha.drop(linha.columns[[0]], axis=1) #Deleting the the column create before (this way in can have a index in order =) )

linha_linha = linha.groupby(by=["LINHA"])[linha.columns.values[-1]].sum()
linha_linha = linha_linha.reset_index()

for index, row in linha_linha.iterrows():
    valor = row[0].split(' ')[0]
    linha_linha.set_value(index,'LINHANUM', valor) # Let's strip the LINHA COLUMN to get only the code of line and create a n ew column
    
    
    
#------ Some Statitics

import statistics
statistics.mean(ytotal) # Arithmetic mean (average) of data.
statistics.stdev(ytotal) # Sample standard deviation of data.

#------ Plotting Total Passengers vs. Month
def totalpassengersvsdate():
    plt.figure(figsize=(10,5))
    x = list(range(0, len(ytotal) ))
    plt.xticks(x, xTicks)
    plt.xticks(range(len(ytotal)), xTicks, rotation=60) # writes strings with 45 degree angle
    colors = []
    for i in range(0, len(ytotal)):
        if i < 12:
            colors.append('#F44336')
        elif i >= 12 and i < 24:
            colors.append('#FFC107')
        elif i >= 24 and i < 36:
            colors.append('#4A148C')
        else:
            colors.append('#48A51A')
    plt.bar(x,ytotal, color=colors)
    plt.xlabel("Data")
    plt.ylabel('Quantidade de Passageiros Trasportados \n (em milhões de Pasageiros)')
    plt.gcf().subplots_adjust(bottom=0.25, left=0.1)
   # plt.tight_layout()
    ano2014 = mpatches.Patch(color='#F44336', label='2014')
    ano2015 = mpatches.Patch(color='#FFC107', label='2015')
    ano2016 = mpatches.Patch(color='#4A148C', label='2016')
    ano2017 = mpatches.Patch(color='#48A51A', label='2017')
    plt.legend(handles=[ano2014,ano2015,ano2016,ano2017], 
               loc='upper center', 
               bbox_to_anchor=(0.5, -0.25),
               fancybox=False, 
               shadow=False, 
               ncol=4) 
    plt.show()

#------ Plotting Paying Passenger and Integration Passenger and Free Passengers and Free Pass Students vs Month
def typepassengervsdate():
    raw_data = {'Date': xTicks,
            'Passageiros Pagantes': ytotal_paying,
            'Passageiros com Integração': ytotal_integration,
            'Passageiros com Gratuidade': ytotal_free_passengers,
            'Passageiros Estudantes com Gratuidade': ytotal_free_students}
    df = pd.DataFrame(raw_data, columns = ['Date', 'Passageiros Pagantes','Passageiros com Integração', 'Passageiros com Gratuidade', 'Passageiros Estudantes com Gratuidade'])
    
    # Create the general and the "subplots" i.e. the bars
    f, ax1 = plt.subplots(1, figsize=(10,5))
    
    # Set the bar width
    bar_width = 0.8
    
    # positions of the left bar-boundaries
    bar_l = [i+1 for i in range(len(df['Passageiros Pagantes']))]
    
    # positions of the x-axis ticks (center of the bars as bar labels)
    tick_pos = list(range(1, len(xTicks) + 1))
    
    # Create a bar plot
    ax1.bar(bar_l,
            df['Passageiros Pagantes'],
            width=bar_width,
            label='Passageiros Pagantes',
            color='#F44336')
    
    # Create a bar plot
    ax1.bar(bar_l,
            df['Passageiros com Integração'],
            width=bar_width,
            bottom=df['Passageiros Pagantes'],
            label='Passageiros com Integração',
            color='#4A148C')
    
    # Create a bar plot
    ax1.bar(bar_l,
            df['Passageiros com Gratuidade'],
            width=bar_width,
            bottom=[i+j for i,j in zip(df['Passageiros Pagantes'],df['Passageiros com Integração'])],
            label='Passageiros com Gratuidade',
            color='#48A51A')
    
    # Create a bar plot
    ax1.bar(bar_l,
            df['Passageiros Estudantes com Gratuidade'],
            width=bar_width,
            bottom=[i+j+k for i,j,k in zip(df['Passageiros Pagantes'],df['Passageiros com Integração'], df['Passageiros com Gratuidade'])],
            label='Passageiros Estudantes com Gratuidade',
            color='#009688')
    
    # Set the x ticks with names
    plt.xticks(tick_pos, df['Date'], rotation = 60)
    
    # To label don't cut off 
    plt.gcf().subplots_adjust(bottom=0.25, left=0.1)
    
    # Set the label and legends
    ax1.set_ylabel("Total de Passageiros por Categoria \n (em milhões de Pasageiros)")
    ax1.set_xlabel("Data")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25),
              fancybox=True, shadow=False, ncol=4)   


#------ Check which companies carry the most

def mostusedcompanies(n_empresas):
    if n_empresas > len(empresa["EMPRESA"].tolist()):
        n_empresas = len(empresa["EMPRESA"].tolist())
    
    x = list(range(0, n_empresas))
    plt.figure(figsize=(10,5))
    plt.xticks(x, empresa["EMPRESA"].tolist())
    plt.xticks(range(0, n_empresas), empresa["EMPRESA"].tolist()[:n_empresas], rotation=90) # writes strings with 45 degree angle
    plt.bar(x, (empresa["PASSAGEIROS"]/10**6).tolist()[:n_empresas])
    plt.gcf().subplots_adjust(left=0.3)
    plt.tight_layout()
    plt.xlabel("Empresa")
    plt.ylabel('Quantidade de Passageiros Trasportados \n (em milhões de Pasageiros)')
    
    plt.show()
    
    print (empresa)

#------ Check concession vs. permission
def mostusedtype():
    x = list(range(0, len(tipo["TIPO"].tolist())))
    plt.figure(figsize=(10,5))
    plt.xticks(x, tipo["TIPO"].tolist())
    plt.xticks(range(len(tipo["TIPO"].tolist())), tipo["TIPO"].tolist()) # writes strings with 45 degree angle
    plt.bar(x, (tipo["PASSAGEIROS"]/10**6).tolist(), color="#009688")
    plt.gcf().subplots_adjust(left=0.3)
    plt.tight_layout()
    plt.xlabel("Tipo")
    plt.ylabel('Quantidade de Passageiros Trasportados \n (em milhões de Pasageiros)')
    plt.show()
    
    print (tipo)

#------ Verify usage by Area
def mostusedareas():
    x = list(range(0, len(area["AREA"].tolist())))
    plt.figure(figsize=(10,5))
    plt.xticks(x, area["AREA"].tolist())
    plt.xticks(range(len(area["AREA"].tolist())), area["AREA"].tolist()) # writes strings with 45 degree angle
    plt.bar(x, (area["PASSAGEIROS"]/10**6).tolist(), color="#009688")
    plt.gcf().subplots_adjust(left=0.3)
    plt.tight_layout()
    plt.xlabel("Área")
    plt.ylabel('Quantidade de Passageiros Trasportados \n (em milhões de Pasageiros)')
    plt.show()
    
    print (area)

#------ n most used Lines
def mostusedlines(n_linhas):
    if n_linhas > len(linha["LINHA"].tolist()):
        n_linhas = len(linha["LINHA"].tolist())
    
    plt.figure(figsize=(10,5))
    colors = []
    for i in range(0, n_linhas):
        if linha.ix[i,1] == "AREA 1":
            colors.append('#EC407A')
        elif linha.ix[i,1] == "AREA 2":
            colors.append('#9C27B0')
        elif linha.ix[i,1] == "AREA 3":
            colors.append('#2196F3')
        elif linha.ix[i,1] == "AREA 4":
            colors.append('#009688')
        elif linha.ix[i,1] == "AREA 5":
            colors.append('#8BC34A')
        elif linha.ix[i,1] == "AREA 6":
            colors.append('#FFC107')
        elif linha.ix[i,1] == "AREA 7":
            colors.append('#FF5722')
    plt.barh(range(0, n_linhas), (linha["PASSAGEIROS"]/10**6)[:n_linhas], align='center', color=colors)
    plt.yticks(range(0, n_linhas),linha["LINHA"][:n_linhas], rotation = 0)
    plt.gcf().subplots_adjust(left=0.3)
    plt.xlabel('Quantidade de Passageiros Trasportados \n (em milhões de Pasageiros)')
    plt.ylabel("Linha")
    AREA1 = mpatches.Patch(color='#EC407A', label='AREA 1')
    AREA2 = mpatches.Patch(color='#9C27B0', label='AREA 2')
    AREA3 = mpatches.Patch(color='#2196F3', label='AREA 3')
    AREA4 = mpatches.Patch(color='#009688', label='AREA 4')
    AREA5 = mpatches.Patch(color='#8BC34A', label='AREA 5')
    AREA6 = mpatches.Patch(color='#FFC107', label='AREA 6')
    AREA7 = mpatches.Patch(color='#FF5722', label='AREA 7')
    plt.legend(handles=[AREA1,AREA2,AREA3,AREA4,AREA5,AREA6,AREA7], loc=1)
    plt.show()
        
    print (linha.head(n_linhas))

#------ Check which n lines are most commonly used by AREA
def mostusedlinesperarea(n_linhas, area):
    if n_linhas > len(linha["LINHA"].tolist()):
        n_linhas = len(linha["LINHA"].tolist())
    
    linha_area = linha.loc[(linha["AREA"] == area)]
    
    plt.figure(figsize=(10,5))
    plt.barh(range(0, n_linhas), (linha_area["PASSAGEIROS"]/10**6)[:n_linhas], align='center', color="#009688")
    plt.yticks(range(0, n_linhas), linha_area["LINHA"][:n_linhas], rotation = 0)
    plt.gcf().subplots_adjust(left=0.3)
    plt.xlabel('Quantidade de Passageiros Trasportados \n (em milhões de Pasageiros)')
    plt.ylabel("Linha")
    plt.title("As {} linhas mais usadas na {}".format(n_linhas, area.title() ))
    plt.show()
        
    print (linha.head(n_linhas))
    
    
#------Check which n lines are most commonly used by COMPANY

def mostusedlinespercompanie(n_linhas, companie):
    if n_linhas > len(linha["LINHA"].tolist()):
        n_linhas = len(linha["LINHA"].tolist())
    
    linha_comp = linha.loc[(linha["EMPRESA"] == companie)]
    
    plt.figure(figsize=(10,5))
    plt.barh(range(0, n_linhas), (linha_comp["PASSAGEIROS"]/10**6)[:n_linhas], align='center', color="#009688")
    plt.yticks(range(0, n_linhas), linha_comp["LINHA"][:n_linhas], rotation = 0)
    plt.gcf().subplots_adjust(left=0.3)
    plt.xlabel('Quantidade de Passageiros Trasportados \n (em milhões de Pasageiros)')
    plt.ylabel("Linha")
    plt.title("As {} linhas mais usadas pela Empresa {}".format(n_linhas, companie.title() ))
    plt.show()
        
    print (linha.head(n_linhas))
    
#------ Calling the Plots :)
totalpassengersvsdate()
typepassengervsdate()
mostusedcompanies(35) # Number of companies to plot
mostusedtype()
mostusedareas()
mostusedlines(20) # Number of lines to plot
mostusedlinesperarea(20, "AREA 3") # Number of lines and the area to plot
mostusedlinespercompanie(20, "GATUSA")


#------ TO DO

# Arrumar as quantidades de passageiros de linhas pois mostra por empresa linhas iguais

# Deletar linhas com problemas NAN e/ou vazias (e descobir o que são)

# Verificar trajeto total e custo por passageiro e quilometragem e combustivel

shapes = pd.read_csv('gtfs/shapes.txt', sep=",")
routes = pd.read_csv('gtfs/routes.txt', sep=",")
trips = pd.read_csv('gtfs/trips.txt', sep=",")

i = 0
for index, row in shapes.iterrows():
    if row[3] == 1 and i == 1: # The last value with total distance made by the line 
         route_id = trips.loc[trips['shape_id'] == shape_id]['route_id'].values # Searching the Code of line in trips dataset 
         route_id = route_id[0] # Picking the value in the 
         route_id = list(route_id) #Spliting the Code Line in list
         del route_id[4] # Deleting the "-" because in linha_linha dataset there isn't
         route_id = "".join(route_id) # Reagrouping :)
         index_place = linha_linha.loc[linha_linha['LINHANUM'] == route_id].index.values # Picking the index value to that line
         linha_linha.set_value(index_place,'DISTTRAJETO', valor_dist) # Adding the total distance in the linha_linha dataset
         i = 1
    elif row[3] == 1 and i == 0:
         i = i + 1
    shape_id = row[0]
    valor_dist = row[4]

for index, row in linha_linha.iterrows():
    if np.isnan(row[3]) == False:
        print ("Na linha {} temos um uma relação de {} Passageiros por km ".format(row[0], locale.format('%2d', 1000*row[1]/row[3]) ))


positivos = linha_linha[linha_linha.DISTTRAJETO > 0].DISTTRAJETO
aleatorios = pd.Series(np.random.randn(100*len(positivos)), name='normal')
plt.hist(aleatorios, bins=75, width=0.1)

plt.hist(positivos, bins=85)

#plt.figure(figsize=(10,5))
#plt.hist(positivos, bins=75, width=1000, color="#009688")
#plt.yticks(range(0, n_linhas), linha_comp["LINHA"][:n_linhas], rotation = 0)
#plt.gcf().subplots_adjust(left=0.3)
#plt.xlabel('Quantidade de Passageiros Trasportados \n (em milhões de Pasageiros)')
#plt.ylabel("Linha")
#plt.title("As {} linhas mais usadas pela Empresa {}".format(n_linhas, companie.title() ))
#plt.show()