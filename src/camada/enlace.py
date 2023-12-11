

# ---------- Protocolos de Enquadramento de Dados ----------

def contagem_caractere(entrada):
    lista = []
    for char in entrada:
        lista.append(char)
    if len(lista) <= 6:
        lista.insert(0,len(lista))
    else:
        aux1 = len(entrada) % 6
        aux2 = len(entrada) // 6 - 1
        lista.insert(0,6)
        if aux1 != 0:
            lista.insert(-aux1, aux1)
        if aux2 > 1:
            while aux2 > 0:
                lista.insert(aux2*6 + 1,6)
                aux2 -= 1
    
    return(lista)


def insercao_caractere(entrada):
    lista = []
    for char in entrada:
        lista.append(char)
    if len(lista) <= 6:
        lista.insert(0,'&')

    else:
        aux1 = len(entrada) % 6
        aux2 = len(entrada) // 6 - 1
        lista.insert(0,'&')
        if aux1 != 0:
            lista.insert(-aux1, '&')
            lista.insert(-aux1, '&')
        if aux2 > 1:
            while aux2 > 0:
                lista.insert(aux2*6 + 1,'&')
                lista.insert(aux2*6 + 1,'&')
                aux2 -= 1
    lista.append('&')
    
    return(lista)