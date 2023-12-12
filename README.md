# Simulador da camada física e de enlace do modelo OSI

Projeto proposto na disciplina de **Teleinformática e Redes** do [**Departamento de Ciência da Computação**](https://cic.unb.br/) da [**Universidade Federal de Brasília**](https://www.unb.br/).

## Camada física
Possui as modulações digitais:
- Non-return to Zero Polar (NRZ-Polar)
- Manchester
- Bipolar

E as modulações por portadora
- Amplitude Shift Keying (ASK)
- Frequency Shift Keying (FSK)
- 8-Quadrature Amplitude Modulation (8-QAM)

## Camada de enlace
Enquadramento por
- Contagem de caracteres
- Inserção de caracteres

Protocolos de detecção de erros [a ser implementado]
- Bit de paridade par
- CRC (polinômio CRC-32, IEEE 802)

Protocolo de correção de erros [a ser implementado]
- Hamming

## Requisitos para execução
- [Python v3.10+](https://www.python.org/)
- [Matplotlib v3.7+](https://matplotlib.org/) - gráficos
- [Numpy v1.20+](https://numpy.org/) - manipulação de número
- [PyGobject v3.40+](https://www.gtk.org/docs/language-bindings/python/)
- [Gtk v4.0+](https://www.gtk.org/) - interface gráfica

## Como iniciar?
Basta executar o arquivo "main.py"

## License
This project is licensed under the terms of the [MIT](https://choosealicense.com/licenses/mit/) license.