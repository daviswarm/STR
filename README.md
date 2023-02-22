# STR-2022-2_AutonomousLogisticSystem

![](https://img.shields.io/badge/version-v0.1-blue)

Este repositório corresponde ao projeto final de programação da disciplina de Sistemas de Tempo Real da Universidade de Brasília e implementa um sistema logístico autônomo de transporte para movimentar items de um ponto a outro da fábrica em ambiente simulado por meio do [pyRTOS](https://github.com/Rybec/pyRTOS) e do [CoppeliaSim](https://www.coppeliarobotics.com/).

## Configuração

### Arquivos do CoppeliaSim

Arquivos padrão para utilização do Python com o CoppeliaSim.

- remoteApi.dll
- remoteApi.so
- sim.py
- simConst.py

Obs: Mais informações sobre a integração do CoppeliaSim com o Python estão disponíveis neste [vídeo](https://www.youtube.com/watch?v=cFe2opWCKLQ&list=PL1WrY7PmiW_iwesX41-rS6ddHlvbrpe0O&index=18).

### Arquivos do pyRTOS

Pasta com os arquivos para utilização da biblioteca pyRTOS.

- pyRTOS/

Obs: Mesma pasta disponível neste [link](https://github.com/Rybec/pyRTOS/tree/main/pyRTOS).

### Arquivos do projeto

Arquivos desenvolvidos durante o projeto para criação do cenário no CoppeliaSim e controle das tarefas por meio do Python via pyRTOS.

- str_scene.ttt
- main.py

## Como usar

1. Inicie a simulação do cenário no CoppeliaSim;
2. Execute o arquivo 'main.py'.
