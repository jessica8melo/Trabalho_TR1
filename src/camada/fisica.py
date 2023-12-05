import numpy as np
import matplotlib.pyplot as plt

entrada = input()

def NRZ_Polar(entrada): #Bit '1' é V e bit '0' é -V, sendo |V|=1
    x = np.arange(0,len(entrada),.01)   #Eixo X vai de 0 até
    aux_index = 1 #Serve para analisar se percorreu-se toda unidade do eixo X antes de ir para o próximo bit de entrada
    y = []
    for i in range(0,len(entrada)*100,1):
        if x[i]<aux_index: #Ainda não percorreu
            if entrada[aux_index-1] == "1":
                saida = 1
            else:
                saida = -1
            y.append(saida)
        else: #Já percorreu
            if entrada[aux_index] == "1":
                saida = 1
            else:
                saida = -1
            y.append(saida)
            aux_index+=1
    return(x,y)

def Bipolar(entrada): #Bit '0' é 0 e bit '1' varia entre +-V, sendo |V|=1
    x = np.arange(0,len(entrada),.01)   
    aux_index = 1
    y = []
    pulso = True #Define se o bit '1' será positivo ou negativo
    for i in range(0,len(entrada)*100,1):
        if x[i]<aux_index:
            if entrada[aux_index-1] == "1" and pulso:
                saida = 1
            elif entrada[aux_index-1] == "1" and not(pulso):
                saida = -1
            else:
                saida = 0
            y.append(saida)
        else:
            if entrada[aux_index] == "1" and not(pulso):
                saida = 1
                pulso = not pulso
            elif entrada[aux_index] == "1" and pulso:
                saida = -1
                pulso = not pulso
            else:
                saida = 0
            y.append(saida)
            aux_index+=1
    return(x,y)

def Manchester(entrada): 
    x = np.arange(0,len(entrada),.01) 
    aux_index1 = 1
    aux_index2 = 0.5 #Serve para trocar a saída quando chegamos na metade da representação do bit
    y = []
    for i in range(0,len(entrada)*100,1):
        if x[i]<aux_index1: 
            if x[i]>(aux_index2): #Verifica se a metade da representação do bit já chegou
                if entrada[aux_index1-1] == "1":
                    saida = 0
                else:
                    saida = 1
            else:
                if entrada[aux_index1-1] == "1":
                    saida = 1
                else:
                    saida = 0
            y.append(saida)
        else:
            if entrada[aux_index1] == "1":
                saida = 1
            else:
                saida = 0
            y.append(saida)
            aux_index1+=1
            aux_index2+=1
    return(x,y)

def ASK(entrada): #Quando o bit é igual a '1', a amplitude é 1 e quando é igual a '0', a amplitude é 0
    y = [0]*100*len(entrada)
    x = np.arange(0,len(entrada),.01) 

    for i in range(0,len(entrada)): #Cria a função senoidal de saída a partir da amplitude e da frequência de entrada
        if entrada[i] == "1":
            for j in range(1,100):
                y[(i)*100+j] = 1 * np.sin(2*np.pi*j/100) 
        else:
            for j in range(1,100):
                y[(i)*100+j] = 0
    ## matplot chart / graph
    fig, ax = plt.subplots()
    ax.plot(x,y, color='green')
    return(fig)

def FSK(entrada): #Quando o bit é igual a '1', a frequência é 2, já quando o bit for '0', a frequência é 1
    y = [0]*100*len(entrada)
    x = np.arange(0,len(entrada),.01) 

    for i in range(0,len(entrada)): #Cria a função senoidal de saída a partir da amplitude e das respectivas frequência
        if entrada[i] == "1":
            for j in range(1,100):
                y[(i)*100+j] = 1 * np.sin(2*np.pi*2*j/100)
        else:
            for j in range(1,100):
                y[(i)*100+j] = 1 * np.sin(2*np.pi*j/100)
    ## matplot chart / graph
    fig, ax = plt.subplots()
    ax.plot(x,y, color='green')
    return(fig)