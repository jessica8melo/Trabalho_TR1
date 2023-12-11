import numpy as np

def nrz_polar(entrada): #Bit '1' é V e bit '0' é -V, sendo |V|=1
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
    return y

def bipolar(entrada): #Bit '0' é 0 e bit '1' varia entre +-V, sendo |V|=1
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
    return y

def manchester(entrada):
    x = np.arange(0,len(entrada),.01)
    aux_index1 = 1
    aux_index2 = 0.5 #Serve para trocar a saída quando chegamos na metade da representação do bit
    y = []
    for i in range(0,len(entrada)*100,1):
        if x[i]<aux_index1: 
            if x[i]>(aux_index2): #Verifica se a metade da representação do bit já chegou
                if entrada[aux_index1-1] == "1":
                    saida = -1
                else:
                    saida = 1
            else:
                if entrada[aux_index1-1] == "1":
                    saida = 1
                else:
                    saida = -1
            y.append(saida)
        else:
            if entrada[aux_index1] == "1":
                saida = 1
            else:
                saida = -1
            y.append(saida)
            aux_index1+=1
            aux_index2+=1
    return y

def ask(entrada): #Quando o bit é igual a '1', a amplitude é 1 e quando é igual a '0', a amplitude é 0
    y = [0]*100*len(entrada)

    for i in range(0,len(entrada)): #Cria a função senoidal de saída a partir da amplitude e da frequência de entrada
        if entrada[i] == "1":
            for j in range(1,100):
                y[(i)*100+j] = 1 * np.sin(2*np.pi*j/100)
        else:
            for j in range(1,100):
                y[(i)*100+j] = 0
    return y

def fsk(entrada): #Quando o bit é igual a '1', a frequência é 2, já quando o bit for '0', a frequência é 1
    y = [0]*100*len(entrada)

    for i in range(0,len(entrada)): #Cria a função senoidal de saída a partir da amplitude e das respectivas frequência
        if entrada[i] == "1":
            for j in range(1,100):
                y[(i)*100+j] = 1 * np.sin(2*np.pi*2*j/100)
        else:
            for j in range(1,100):
                y[(i)*100+j] = 1 * np.sin(2*np.pi*j/100)
    return y

def qam_8(entrada):
    # Converte a entrada num array
    arrayDados = np.frombuffer(entrada.encode("ASCII"), dtype=np.uint8) - ord("0")
    simbolo = 0
    amplitude = 0
    fase = 0
    y = []

    for x in range(0, len(entrada)):
        # Cada símbolo em 8-QAM representa 3 bits ∴ trocamos de símbolo de 3 em 3 bits
        if x % 3 == 0:
            simbolo = (arrayDados[x] << 2) + (arrayDados[x+1] << 1) + (arrayDados[x+2] << 0)
            match simbolo:
                case 0b000:
                    amplitude = 1
                    fase = 0            # 0*np.pi/2
                    print(f"S0 (0b000), fase: {fase:.3} - amplitude: {amplitude}")
                case 0b011:
                    amplitude = 1
                    fase = 0.5*np.pi    # 1*np.pi/2
                    print(f"S3 (0b011), fase: {fase:.3}, amplitude: {amplitude}")
                case 0b110:
                    amplitude = 1
                    fase = np.pi        # 2*np.pi/2
                    print(f"S6 (0b110), fase: {fase:.3}, amplitude: {amplitude}")
                case 0b101:
                    amplitude = 1
                    fase = -0.5*np.pi   # 3*np.pi/2
                    print(f"S5 (0b101), fase: {fase:.3}, amplitude: {amplitude}")
                case 0b001:
                    amplitude = 0.5
                    fase = 0.25*np.pi   # 1*np.pi/4
                    print(f"S1 (0b001), fase: {fase:.3}, amplitude: {amplitude}")
                case 0b010:
                    amplitude = 0.5
                    fase = 0.75*np.pi   # 3*np.pi/4
                    print(f"S2 (0b010), fase: {fase:.3}, amplitude: {amplitude}")
                case 0b111:
                    amplitude = 0.5
                    fase = -0.75*np.pi  # 5*np.pi/4
                    print(f"S7 (0b111), fase: {fase:.3}, amplitude: {amplitude}")
                case 0b100:
                    amplitude = 0.5
                    fase = 1.75*np.pi   # 7*np.pi/4
                    print(f"S4 (0b100), fase: {fase:.3}, amplitude: {amplitude}")
        # Calcula 100 amostras do sinal "y" para cada ponto discreto de "x"
        for j in range(0, 100):
            y.append(amplitude * np.cos(2*np.pi*(j*0.01) + fase))
    return y