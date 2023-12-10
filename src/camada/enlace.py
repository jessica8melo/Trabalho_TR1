

# ---------- Protocolos de Enquadramento de Dados ----------

def contagem_caractere(entrada):
    quadros = []
    aux = 0 # posição do caractere referenciado
    erro = False # verifica se deu erro na transmissao
    cabecalhos = []
    while aux < len(entrada) - 1 and erro == False:
        if entrada[aux].isnumeric() == True:
            cabecalho = int(entrada[aux])
            cabecalhos.append(cabecalho)
            print(cabecalho)
            quadro = []
            aux += 1
            for i in range(cabecalho) :
                if aux < len(entrada):
                    quadro += entrada[aux]
                    aux += 1
                else:
                    erro = True
            quadros.append(quadro)
            print(quadro)
        else:
            erro = True
    
    return(quadros, cabecalhos, erro)


def insercao(entrada):
    quadros = []
    aux = 1 # posição do caractere referenciado
    erro = False # verifica se deu erro na transmissao
    flag = entrada[0]
    if entrada[-1] != flag:
            erro = True
    while aux < len(entrada) and erro == False:
        quadro = []
        while entrada[aux] != flag and aux < len(entrada):
            quadro.append(entrada[aux])
            aux += 1
        quadros.append(quadro)
        if aux != len(entrada) - 1 and entrada[aux+1] != flag:
            erro = True
        aux += 2
    
    return(quadros,flag,erro)