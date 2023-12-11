

# ---------- Protocolos de Enquadramento de Dados ----------

def contagem_caractere(entrada):
    lista = []
    for char in entrada:
        lista.append(char)
    if len(lista) <= 6:
        lista.insert(0, str(len(lista)))
    else:
        aux1 = len(entrada) % 6
        aux2 = len(entrada) // 6 - 1
        lista.insert(0, str(6))
        if aux1 != 0:
            lista.insert(-aux1, str(aux1))
        if aux2 > 1:
            while aux2 > 0:
                lista.insert(aux2*6 + 1, str(6))
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

def add_bit_paridade_par(bits):
    if bits.count('1')%2 == 0:
        bits = bits + '0'
    else:
        bits = bits + '1'
    return bits

def paridade_par(bits_entrada, bits_saida):
    mensagem_transmitida = add_bit_paridade_par(bits_entrada)
    recalculo_entrada = add_bit_paridade_par(mensagem_transmitida[:-1])
    mensagem_recebida = add_bit_paridade_par(bits_saida)
    recalculo_saida = add_bit_paridade_par(mensagem_recebida[:-1])

    if recalculo_saida == recalculo_entrada:
        return("Sem erros, parça ;)")
    else:
        return("Errou, errou feio, errou rude")