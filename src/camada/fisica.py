import numpy as np

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