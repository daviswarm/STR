# Laboratorio 2 da materia de Sistemas de Tempo Real: Sistema Logistico Autonomo de Transporte
# Integrantes:
# Davi Salomão Soares Corrêa        - 18/0118820
# Francisco Henrique da Silva Costa - 18/0120174
# Matheus Teixeira de Sousa         - 18/0107101




# Avisos do CoppeliaSim
# Make sure to have the server side running in CoppeliaSim: 
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!



# import do CoppeliaSim
try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

# --------------------------------------------------

# Bibliotecas importadas
import time
import pyRTOS
import numpy as np
import math
import time
import pandas as pd
# --------------------------------------------------

# Path dos objetos no modelo
youBot = '/youBot'
targets = ['/Box','/pad1','/pad2','/pad3','/pad4','/pad5','/pad6','/pad7']
w1 = '/rollingJoint_fl'
w2 = '/rollingJoint_rl'
w3 = '/rollingJoint_rr'
w4 = '/rollingJoint_fr'
S1 = '/sensorFrontal'
S2 = '/sensorEsquerda'
S3 = '/sensorDireita'

# --------------------------------------------------
# Mensagens da Aplicacao
speeds_of_wheels = 128
map_target = 129
armmovement = 130
read = 131
#---------------------------------------------------

print ('Inicio')
sim.simxFinish(-1) # just in case, close all opened connections
client=sim.simxStart('127.0.0.1', 8000, True, True, 5000, 5) # Connect to CoppeliaSim


if client!=-1:
    sim.simxStartSimulation(client, sim.simx_opmode_oneshot_wait)
    print ('Connected to remote API server')
    sim.simxAddStatusbarMessage(client, 'Iniciando...', sim.simx_opmode_oneshot_wait)
    time.sleep(0.02)

    # Pegar a handle dos objetos do modelo para executar os comandos
    erro, handle_youBot = sim.simxGetObjectHandle(client, youBot, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do youBot")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
        # Pegar a handle dos objetos do modelo para executar os comandos
    erro, handle_S1 = sim.simxGetObjectHandle(client, S1, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do Sensor 1")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
        # Pegar a handle dos objetos do modelo para executar os comandos
    erro, handle_S2 = sim.simxGetObjectHandle(client, S2, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do Sensor 2")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
        # Pegar a handle dos objetos do modelo para executar os comandos
    erro, handle_S3 = sim.simxGetObjectHandle(client, S3, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do Sensor 3")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
    # Pegar a handle dos objetos do modelo para executar os comandos
    erro, handle_w1 = sim.simxGetObjectHandle(client, w1, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do w1")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
    # Pegar a handle dos objetos do modelo para executar os comandos
    erro, handle_w2 = sim.simxGetObjectHandle(client, w2, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do w2")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
    # Pegar a handle dos objetos do modelo para executar os comandos
    erro, handle_w3= sim.simxGetObjectHandle(client, w3, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do w3")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
    # Pegar a handle dos objetos do modelo para executar os comandos
    erro, handle_w4 = sim.simxGetObjectHandle(client, w4, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do w4")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
    handle_targets=targets
    j=0
    for i in targets:
        erro, handle_targets[j] = sim.simxGetObjectHandle(client, i, sim.simx_opmode_blocking)
        j=1+j
        if erro != 0:
            print("Erro na handle dos targets")
            sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
            sim.simxFinish(-1)
            exit()

    def task_update_wheels(self): # atualiza velocidade de movimento do carro sempre que recebe uma velocidade nova
        # valores iniciais 
        stop=[0,0,0]
        speed=stop
        gain=1
        counter=0
        while True:
            # atualiza as velocidades nas rodas do carrinho
            sim.c_SetJointTargetVelocity(client,handle_w1, (-speed[0] - speed[1] - speed[2])*gain,sim.simx_opmode_streaming)
            sim.c_SetJointTargetVelocity(client,handle_w2, (-speed[0] + speed[1] - speed[2])*gain,sim.simx_opmode_streaming)
            sim.c_SetJointTargetVelocity(client,handle_w3, (-speed[0] - speed[1] + speed[2])*gain,sim.simx_opmode_streaming)
            sim.c_SetJointTargetVelocity(client,handle_w4, (-speed[0] + speed[1] + speed[2])*gain,sim.simx_opmode_streaming)
            # espera ate chegar uma mensagem com a velocidade novaa
            yield [pyRTOS.wait_for_message(self)]
            msgs = self.recv()
            for msg in msgs:
                if msg.type == speeds_of_wheels:
                    speed = msg.message
            # verifica se a velocidade recebida é de ficar parado ou seja tem alguma coisa impedindo o carrinho a continuar
            # se o carrinho fica parado por 50 interacoes seguidas ~ cerca de 30 segundos, envia o alerta de emergencia
            if speed == stop:
                counter=1+counter
            else:
                counter=0
            if counter>50:
                print('emergencia')
            
           


    def task_read_sensors(self): # le os valores de diversos sensores do sistema
        
        stop=[0,0,0]
        speed = stop 

        while True:
            # le os sensores de proximidade por ultrasson do modelo
            (
                erro,
                s1_read,
                distancePoint,
                detectedObjectHandle,
                detectedSurface,
            ) = sim.simxReadProximitySensor(client, handle_S1, sim.simx_opmode_streaming)
            (
                erro,
                s2_read,
                distancePoint,
                detectedObjectHandle,
                detectedSurface,
            ) = sim.simxReadProximitySensor(client, handle_S2, sim.simx_opmode_streaming)
            (
                erro,
                s3_read,
                distancePoint,
                detectedObjectHandle,
                detectedSurface,
            ) = sim.simxReadProximitySensor(client, handle_S3, sim.simx_opmode_streaming)
            
            # chama o script que simula um sensor de posicao no CoppeliaSim 

            (
                erro,
                isonPosition,
                outFloats,
                outStrings,
                outBuffer,
            ) = sim.simxCallScriptFunction(client, youBot,sim.sim_scripttype_childscript,'isonPositionAndOrientation', [], [] , [],bytearray(), sim.simx_opmode_blocking)
            # Caso os sensores de proximidade detectam algo eles emviam pra update weels o valor de parada das rodas caso contrario atualiza o ultimo valor de velocidade calculado

            if(s1_read>0 or s2_read>0 or s3_read>0):
                self.send(
                    pyRTOS.Message(
                        speeds_of_wheels,
                        self,
                        "update_wheels",
                        stop
                    )
                )
            else:
                self.send(
                    pyRTOS.Message(
                        speeds_of_wheels,
                        self,
                        "update_wheels",
                        speed
                    )
                )
            
            # Caso o sensor de posicao detecta que o objetivo foi alcancado emviam pra update weels o valor de parada das rodas
            # alem de enviar a mensagem de atualiacao pra task de atualizar o mapa 

            if erro==0:
                
                if isonPosition[0]>0:
                    self.send(
                    pyRTOS.Message(
                        speeds_of_wheels,
                        self,
                        "update_wheels",
                        stop
                    )
                    )
                    self.send(
                        pyRTOS.Message(
                            map_target,
                            self,
                            "map",
                            1
                        )
                    )
            # espera 0.2 segundos antes de ser enviada a task novamente
            yield [pyRTOS.timeout(0.2)]
            # recebe a velocidade calculada para colocar nas rodas e atingir o target definido
            msgs = self.recv()
            for msg in msgs:
                if msg.type == read:
                    speed = msg.message

            

    def task_calculate_speeds(self): # calcula a velocidade de movimento do carro
        
        while True:
            # chama o script no coppelia sim que cacula velocidade das rodas nescessarias para atingir o target definido
            (
                erro,
                outInts,
                speed,
                outStrings,
                outBuffer,
            ) = sim.simxCallScriptFunction(client, youBot,sim.sim_scripttype_childscript,'calculate_speeds', [], [] , [],bytearray(), sim.simx_opmode_blocking)
            yield
            # envia a velocidade calculada para colocar nas rodas e atingir o target definido
            self.send(
                pyRTOS.Message(
                    read,
                    self,
                    "sensors",
                    speed
                )
            )
            yield
            

    def task_map(self): # determina o alvo no mapa a ser alcancado
        counter =0
        
        while True:
            # chama o script que atualiza o target a ser atingido pelo carrinho, vale notar que counter+1 por causa da diferenca de notacao existente no CoppeliaSim e python
            if counter < 8:
                (
                    erro,
                    outInts,
                    outFloats,
                    outStrings,
                    outBuffer,
                ) = sim.simxCallScriptFunction(client, youBot,sim.sim_scripttype_childscript,'New_target', [counter+1], [] , [] ,bytearray(), sim.simx_opmode_blocking)
            # espera receber a notificacao dos sensores falando que esta na posicao desejada
            yield [pyRTOS.wait_for_message(self)]
            
            msgs = self.recv()
            for msg in msgs:
                if msg.type == map_target:
                    counter =counter+ msg.message
            # se o target é uma posicao que demanda receber ou soltar um item chama a task de utilizar a garra
            if counter == 1 or counter == 4:
                self.send(
                    pyRTOS.Message(
                        armmovement,
                        self,
                        "arm_control",
                        counter
                )
            )    
            # caso chegue ao fim do mapa volta ao inicio
            # poderia ser declarado o fim do programa aqui mas foi escolhido voltar ao inicio por diversos motivos.
            if counter > 8:
                counter=0
            
    def task_arm_control(self): # controla o braco do carrinho para pegar o objeto apesar de nao conseguir devido a limitacoes de comunicacao do CoppeliaSim e o programa em python
        # condicoes nescesarias para a garra iniciar aberta
        control=0
        counter=0

        while True:
            # script para controlar o braco robotico
            (
                erro,
                outInts,
                outFloats,
                outStrings,
                outBuffer,
            ) = sim.simxCallScriptFunction(client, youBot,sim.sim_scripttype_childscript,'arm_control', [control] , [] , [] ,bytearray(), sim.simx_opmode_blocking)
            # espera o mapa falar que ja chegamos no objetivo que tem o objeto a ser coletado ou ponto de deposito do objeto
            yield [pyRTOS.wait_for_message(self)]
            msgs = self.recv()
            for msg in msgs:
                if msg.type == armmovement:
                    counter = msg.message
            # define se deve ser coletado ou depositado o item 
            if counter == 1:
                control =1
            elif counter == 4:
                control = -1
    #definicao das tasks em ordem de prioridade
    pyRTOS.add_task(
        pyRTOS.Task(
            task_arm_control,
            priority=1,
            name="arm_control",
            notifications=None,
            mailbox=True,
        )
    )
    pyRTOS.add_task(
        pyRTOS.Task(
            task_map,
            priority=2,
            name="map",
            notifications=None,
            mailbox=True,
        )
    )
    pyRTOS.add_task(
        pyRTOS.Task(
            task_update_wheels,
            priority=3,
            name="update_wheels",
            notifications=None,
            mailbox=True,
        )
    )
    pyRTOS.add_task(
        pyRTOS.Task(
            task_read_sensors,
            priority=4,
            name="sensors",
            notifications=None,
            mailbox=True,
        )
    )
    pyRTOS.add_task(
        pyRTOS.Task(
            task_calculate_speeds,
            priority=5,
            name="calculate_speeds",
            notifications=None,
        )
    )

    # inicio do PyRTOS que ira gerir as tasks
    pyRTOS.start()


    sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
    sim.simxAddStatusbarMessage(client, 'Finalizando...', sim.simx_opmode_blocking)
    sim.simxFinish(-1)
else:
    sim.simxFinish(-1)
    print ('Failed connecting to remote API server')
print ('Program ended')