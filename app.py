import threading
import random
import time
from queue import Queue

class Mensagem:
    def __init__(self, remetente, destinatario, termo, tipo_mensagem):
        self.remetente = remetente
        self.destinatario = destinatario
        self.termo = termo
        self.tipo_mensagem = tipo_mensagem 

class NoRaft(threading.Thread):
    def __init__(self, id_no, nos, fila_mensagens):
        super().__init__()
        self.id_no = id_no
        self.nos = nos
        self.fila_mensagens = fila_mensagens
        self.estado = 'seguidor'
        self.termo_atual = 0
        self.votou_para = None
        self.votos_recebidos = 0
        self.trava = threading.Lock()
        self.ativo = True

    def run(self):
        while True:
            if not self.ativo:
                time.sleep(3)
                self.recuperar()

            self.verificar_mensagens()

            if self.estado == 'seguidor':
                self.aguardar_timeout_eleicao()
            elif self.estado == 'candidato':
                self.iniciar_eleicao()
            elif self.estado == 'lider':
                self.enviar_heartbeat()

            time.sleep(1)

    def verificar_mensagens(self):
        while not self.fila_mensagens.empty():
            mensagem = self.fila_mensagens.get()
            if mensagem.destinatario == self.id_no and self.ativo:
                self.processar_mensagem(mensagem)

    def processar_mensagem(self, mensagem):
        with self.trava:
            if mensagem.termo > self.termo_atual:
                self.termo_atual = mensagem.termo
                self.estado = 'seguidor'
                self.votou_para = None

            if mensagem.tipo_mensagem == 'solicitar_voto':
                if self.votou_para is None or self.votou_para == mensagem.remetente:
                    self.votou_para = mensagem.remetente
                    print(f"Nó {self.id_no} votou para o Nó {mensagem.remetente} no termo {mensagem.termo}")
                    self.enviar_mensagem(mensagem.remetente, 'responder_voto')
            elif mensagem.tipo_mensagem == 'responder_voto':
                self.votos_recebidos += 1
                if self.votos_recebidos > len(self.nos) // 2:
                    self.tornar_lider()
            elif mensagem.tipo_mensagem == 'heartbeat':
                print(f"Nó {self.id_no} recebeu heartbeat do Nó {mensagem.remetente}")

    def iniciar_eleicao(self):
        with self.trava:
            self.termo_atual += 1
            self.votou_para = self.id_no
            self.votos_recebidos = 1
            print(f"Nó {self.id_no} iniciou eleição para o termo {self.termo_atual}")

        for no in self.nos:
            if no.id_no != self.id_no and no.ativo:
                self.enviar_mensagem(no.id_no, 'solicitar_voto')

    def tornar_lider(self):
        with self.trava:
            self.estado = 'lider'
        print(f"Nó {self.id_no} tornou-se o líder no termo {self.termo_atual}")

    def aguardar_timeout_eleicao(self):
        time.sleep(random.randint(3, 6))
        if self.estado == 'seguidor':
            self.estado = 'candidato'

    def enviar_mensagem(self, id_destinatario, tipo_mensagem):
        mensagem = Mensagem(self.id_no, id_destinatario, self.termo_atual, tipo_mensagem)
        self.fila_mensagens.put(mensagem)

    def enviar_heartbeat(self):
        for no in self.nos:
            if no.id_no != self.id_no and no.ativo:
                self.enviar_mensagem(no.id_no, 'heartbeat')
        time.sleep(2)

    def falhar(self):
        with self.trava:
            print(f"Nó {self.id_no} falhou.")
            self.ativo = False
            self.estado = 'seguidor'

    def recuperar(self):
        with self.trava:
            print(f"Nó {self.id_no} está se recuperando...")
            self.ativo = True
            self.votou_para = None
            self.estado = 'seguidor'

fila_mensagens = Queue()
nos = [NoRaft(i, [], fila_mensagens) for i in range(5)]
for no in nos:
    no.nos = nos

for no in nos:
    no.start()

time.sleep(10)
random.choice(nos).falhar()
time.sleep(15)
random.choice(nos).falhar()
