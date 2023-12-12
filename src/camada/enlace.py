import numpy as np

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
    return lista

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
    
    return lista

def simular_erro(strDeBits: str, qtdErros: int):
    for j in range(0, qtdErros):
        # Gera um número inteiro aletório no intervalo [0, len(strDeBits)-1]
        i = np.random.randint(len(strDeBits)-1)

        lstDeBits = list(strDeBits)
        # Inverte o bit na posição "i"
        lstDeBits[i] = str(1 - int(lstDeBits[i]))

    return "".join(lstDeBits)

# Converte lista de char → string de bits
def lista_para_string_bits(listaDeCharacteres: list[str]):
    # ord(char) → inteiro que representa o caractere unicode
    # usa o versão curta da função format() – f"{:08b}"
    # para transformar em binário no formato "00000000"
    return "".join(f"{ord(x):08b}" for x in listaDeCharacteres)

def calcular_bit_paridade_par(strBits):
    # Conta nº de '1' na string e verifica se é par
    if strBits.count('1') % 2 == 0:
        return '0'
    else:
        return '1'

def verificar_paridade_par(strBitsRecebida):
    # Retira / salva o bit de paridade
    bitParidadeRecebido = strBitsRecebida[-1]
    # Recalcula o bit de partidade
    bitParidadeRecalculado = calcular_bit_paridade_par(strBitsRecebida[:-1])

    if bitParidadeRecebido == bitParidadeRecalculado:
        return("Sem erros, parça ;)")
    else:
        return("Errou, errou feio, errou rude")