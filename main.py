# Autores:
#   Davi Salomão Soares Corrêa        - 18/0118820
#   Francisco Henrique da Silva Costa - 18/0120174
#   Matheus Teixeira de Sousa         - 18/0107101
#
# Implementa o código para o laboratório 2 da disciplina Sistemas de Tempo Real

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

# Dá o import do CoppeliaSim
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

# Mensagens da aplicação
speeds_of_wheels = 128
map_target = 129
armmovement = 130
read = 131

#---------------------------------------------------

print ('Início do programa')
sim.simxFinish(-1) # just in case, close all opened connections
client=sim.simxStart('127.0.0.1', 8000, True, True, 5000, 5) # Connect to CoppeliaSim

if client != -1:
    sim.simxStartSimulation(client, sim.simx_opmode_oneshot_wait)
    print ('Connected to remote API server')
    sim.simxAddStatusbarMessage(client, 'Iniciando...', sim.simx_opmode_oneshot_wait)
    time.sleep(0.02)

    # Pega a handle dos objetos do modelo para executar os comandos
    erro, handle_youBot = sim.simxGetObjectHandle(client, youBot, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do youBot")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
    
    erro, handle_S1 = sim.simxGetObjectHandle(client, S1, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do Sensor 1")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
    
    erro, handle_S2 = sim.simxGetObjectHandle(client, S2, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do Sensor 2")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()

    erro, handle_S3 = sim.simxGetObjectHandle(client, S3, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do Sensor 3")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
    
    erro, handle_w1 = sim.simxGetObjectHandle(client, w1, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do w1")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
    
    erro, handle_w2 = sim.simxGetObjectHandle(client, w2, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do w2")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
    
    erro, handle_w3= sim.simxGetObjectHandle(client, w3, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do w3")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
    
    erro, handle_w4 = sim.simxGetObjectHandle(client, w4, sim.simx_opmode_blocking)
    if erro != 0:
        print("Erro na handle do w4")
        sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
        sim.simxFinish(-1)
        exit()
    
    handle_targets = targets
    
    j = 0
    for i in targets:
        erro, handle_targets[j] = sim.simxGetObjectHandle(client, i, sim.simx_opmode_blocking)
        j = 1 + j
        if erro != 0:
            print("Erro na handle dos targets")
            sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
            sim.simxFinish(-1)
            exit()

    def task_adjust_speed(self):
        """
        Atualiza a velocidade de movimento do carro
        """

        # Valores iniciais
        stop = [0, 0, 0]
        speed = stop
        gain = 1
        counter = 0

        while True:
            # Atualiza as velocidades nas rodas do carrinho
            sim.c_SetJointTargetVelocity(client, handle_w1,
                                         (-speed[0] - speed[1] - speed[2])*gain,sim.simx_opmode_streaming)
            sim.c_SetJointTargetVelocity(client, handle_w2,
                                         (-speed[0] + speed[1] - speed[2])*gain,sim.simx_opmode_streaming)
            sim.c_SetJointTargetVelocity(client, handle_w3,
                                         (-speed[0] - speed[1] + speed[2])*gain,sim.simx_opmode_streaming)
            sim.c_SetJointTargetVelocity(client, handle_w4,
                                         (-speed[0] + speed[1] + speed[2])*gain,sim.simx_opmode_streaming)
            
            # Espera até chegar uma mensagem com a velocidade nova
            yield [pyRTOS.wait_for_message(self)]
            msgs = self.recv()
            
            for msg in msgs:
                if msg.type == speeds_of_wheels:
                    speed = msg.message
            
            # Verifica se é para ficar parado ou não
            if speed == stop:
                counter = 1 + counter
            else:
                counter = 0
            
            # Se ficar parado por 50 iterações, emite um aviso
            if counter > 50:
                print('[WARNING] - Emergência')

    def task_read_sensors(self):
        """
        Lê os valores dos diversos sensores do sistema
        """
        
        # Valores iniciais
        stop = [0, 0, 0]
        speed = stop 

        while True:
            # Lê os sensores de proximidade por ultrassom
            erro_s1, s1_read, _, _, _ = sim.simxReadProximitySensor(client, handle_S1, sim.simx_opmode_streaming)
            erro_s2, s2_read, _, _, _ = sim.simxReadProximitySensor(client, handle_S2, sim.simx_opmode_streaming)
            erro_s3, s3_read, _, _, _ = sim.simxReadProximitySensor(client, handle_S3, sim.simx_opmode_streaming)
            
            # Simula um sensor de posição no CoppeliaSim 
            erro, isonPosition, _, _, _ = sim.simxCallScriptFunction(client, youBot, sim.sim_scripttype_childscript,
                                                                     'isonPositionAndOrientation', [], [], [], bytearray(),
                                                                     sim.simx_opmode_blocking)
            
            # Se algo for detectado, para o carro
            if (s1_read > 0 or s2_read > 0 or s3_read > 0):
                self.send(
                    pyRTOS.Message(
                        speeds_of_wheels,
                        self,
                        "adjust_speed",
                        stop
                    )
                )
            # Se não, atualiza o valor de velocidade
            else:
                self.send(
                    pyRTOS.Message(
                        speeds_of_wheels,
                        self,
                        "adjust_speed",
                        speed
                    )
                )
            
            # Se alcançou o objetivo, para o carro e atualiza o mapa
            if erro == 0:
                if isonPosition[0] > 0:
                    self.send(
                        pyRTOS.Message(
                            speeds_of_wheels,
                            self,
                            "adjust_speed",
                            stop
                        )
                    )
                    self.send(
                        pyRTOS.Message(
                            map_target,
                            self,
                            "adjust_map",
                            1
                        )
                    )
            
            # Espera 0,2 segundos antes de enviar novamente
            yield [pyRTOS.timeout(0.2)]
            
            # Recebe a velocidade calculada para as rodas
            msgs = self.recv()
            for msg in msgs:
                if msg.type == read:
                    speed = msg.message

    def task_calculate_speed(self):
        """
        Calcula a velocidade de movimento do carro
        """
        
        while True:
            # Calcula a velocidade para as rodas
            _, _, speed, _, _ = sim.simxCallScriptFunction(client, youBot, sim.sim_scripttype_childscript,
                                                           'calculate_speed', [], [], [], bytearray(),
                                                           sim.simx_opmode_blocking)
            yield
            
            # Envia a velocidade calculada para as rodas
            self.send(
                pyRTOS.Message(
                    read,
                    self,
                    "read_sensors",
                    speed
                )
            )
            yield
            
    def task_adjust_map(self):
        """
        Determina o alvo a ser alcançado no mapa
        """
        
        # Valor inicial
        counter = 0
        
        while True:
            # Atualiza o alvo a ser alcançado pelo carro
            if counter < 8:
                _, _, _, _, _ = sim.simxCallScriptFunction(client, youBot, sim.sim_scripttype_childscript,
                                                           'New_target', [counter+1], [], [], bytearray(),
                                                           sim.simx_opmode_blocking)
            
            # Espera receber a notificação dos sensores
            yield [pyRTOS.wait_for_message(self)]
            
            msgs = self.recv()
            for msg in msgs:
                if msg.type == map_target:
                    counter = counter + msg.message

            # Se o alvo é uma posição de carga ou descarga, controla a garra
            if counter == 1 or counter == 4:
                self.send(
                    pyRTOS.Message(
                        armmovement,
                        self,
                        "arm_control",
                        counter
                    )
                )

            # Se chegou no final do mapa, volta para o começo
            if counter > 8:
                counter = 0
            
    def task_arm_control(self):
        """
        Controla o braço para carga e descarga
        """
        
        # Valores iniciais
        control = 0
        counter = 0

        while True:
            # Controla o braço
            _, _, _, _, _ = sim.simxCallScriptFunction(client, youBot, sim.sim_scripttype_childscript,
                                                       'arm_control', [control], [], [], bytearray(),
                                                       sim.simx_opmode_blocking)
            
            # Espera informação da chegada no ponto de carga ou descarga
            yield [pyRTOS.wait_for_message(self)]
            msgs = self.recv()
            
            for msg in msgs:
                if msg.type == armmovement:
                    counter = msg.message
            
            # Define o tipo de ação: carga ou descarga
            if counter == 1:
                control = 1
            elif counter == 4:
                control = -1

    # Define as tarefas e a ordem de prioridade
    # Controla garra
    pyRTOS.add_task(
        pyRTOS.Task(
            task_arm_control,
            priority=1,
            name="arm_control",
            notifications=None,
            mailbox=True,
        )
    )

    # Ajusta mapa
    pyRTOS.add_task(
        pyRTOS.Task(
            task_adjust_map,
            priority=2,
            name="adjust_map",
            notifications=None,
            mailbox=True,
        )
    )

    # Ajusta velocidade
    pyRTOS.add_task(
        pyRTOS.Task(
            task_adjust_speed,
            priority=3,
            name="adjust_speed",
            notifications=None,
            mailbox=True,
        )
    )

    # Lê sensores
    pyRTOS.add_task(
        pyRTOS.Task(
            task_read_sensors,
            priority=4,
            name="read_sensors",
            notifications=None,
            mailbox=True,
        )
    )

    # Calcula velocidade
    pyRTOS.add_task(
        pyRTOS.Task(
            task_calculate_speed,
            priority=5,
            name="calculate_speed",
            notifications=None,
        )
    )

    # Inicia o PyRTOS para gerir as tarefas
    pyRTOS.start()

    sim.simxStopSimulation(client, sim.simx_opmode_oneshot_wait)
    sim.simxAddStatusbarMessage(client, 'Finalizando...', sim.simx_opmode_blocking)
    sim.simxFinish(-1)

else:
    sim.simxFinish(-1)
    print ('Failed connecting to remote API server')

print ('Fim do programa')