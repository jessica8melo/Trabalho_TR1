from camada.enlace import *
from camada.fisica import *

print(
    "\x1b[31;1m\
    ===========================\n\
       Simulação no terminal   \n\
    ===========================\n\x1b[0m\n\
    Digite uma entrada: "
)
strEntrda = input(">: ")
lstQuadros = contagem_caractere(strEntrda)
strBits = lista_para_string_bits(lstQuadros)
strBitsParaTransmitir = strBits + calcular_bit_paridade_par(strBits)

# Iria para camada física → modulação da onda ~ (camada física) → transmite

# Simula uma interferênica no meio da transmissão que mudou 1 bit
strBitsRecebidaComErro = simular_erro(strBits, 1)

# Reptor receberia → demodulação da onda ~ (camada física) → camada de enlace interpreta os bits

print(verificar_paridade_par(strBitsRecebidaComErro))