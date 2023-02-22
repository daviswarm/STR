# Autores:
#   Davi Salomão Soares Corrêa        - 18/0118820
#   Francisco Henrique da Silva Costa - 18/0120174
#   Matheus Teixeira de Sousa         - 18/0107101
#
# Lê os valores de tempo de resposta coletados e estima o WCRT

from numpy import std
import matplotlib.pyplot as plt

def read_file(file_name):
    with open(file_name, 'r') as file:
        line = file.readline()
    
    line = line[1:-1]
    line = line.split(', ')
    line = [float(k) for k in line]
    return line

def print_wcrt(data):
    print("\n--------------------------------")
    print(f"Tamanho: {len(data)}")
    print(f"Desvio padrão: {std(data)}")
    print(f"Valor máximo: {max(data)}")
    print(f"WCRT: {max(data) + std(data)}")
    print("--------------------------------\n")

def plot_frequency(data, name):
    plt.hist(data, 10, rwidth=1, color='tab:orange', zorder=2)
    plt.xlabel("Tempo de resposta (s)")
    plt.ylabel("Ocorrências")
    plt.tight_layout()
    plt.grid(True, zorder=1)
    plt.savefig(name)
    plt.show()

name = ['Resposta Ajusta mapa',
        'Resposta Ajusta velocidade',
        'Resposta Calcula velocidade',
        'Resposta Controla garra',
        'Resposta Lê sensores']

input = ['data/resposta_ajusta_mapa.txt',
         'data/resposta_ajusta_velocidade.txt',
         'data/resposta_calcula_velocidade.txt',
         'data/resposta_controla_garra.txt',
         'data/resposta_le_sensores.txt']

for i, j in zip(name, input):
    print(i)
    values = read_file(j)
    print_wcrt(values)
    output = j[0:-3] + 'pdf'
    plot_frequency(values, output)