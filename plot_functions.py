# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 16:52:00 2017

@author: Yuri Gaspar
"""

def mostusedlines(n_linhas):
    if n_linhas > len(linha["LINHA"].tolist()):
        n_linhas = len(linha["LINHA"].tolist())
    
    plt.figure()
    plt.barh(range(0, n_linhas), (linha["PASSAGEIROS"]/10**6)[:n_linhas], align='center', color='#009688')
    plt.yticks(range(0, n_linhas),linha["LINHA"][:n_linhas], rotation = 0)
    plt.gcf().subplots_adjust(left=0.3)
    plt.xlabel('Quantidade de Passageiros Trasportados \n (em milhões de Pasageiros)')
    plt.ylabel("Linha")
    plt.show()
    
    print (linha.head(n_linhas))