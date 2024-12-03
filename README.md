# Simulação do Algoritmo de Consenso Raft

## 📋 Descrição do Projeto  
Este projeto implementa uma simulação do **algoritmo Raft** em um ambiente distribuído, onde múltiplos nós (processos) tomam decisões e elegem um líder para alcançar consenso. A aplicação foi projetada para ilustrar o funcionamento de Raft, abordando as fases de eleição, troca de mensagens (*heartbeats*) e recuperação de nós após falhas simuladas.

### 📚 Algoritmo Implementado  
O **Raft** é um algoritmo de consenso utilizado em sistemas distribuídos para manter um log replicado consistente. Ele é projetado para ser mais simples e compreensível do que outros algoritmos, como Paxos, e inclui três fases principais:

- **Eleição de Líder:** Quando um nó detecta a falta de um líder, ele inicia uma eleição.
- **Replicação de Log (não implementada nesta versão):** O líder mantém logs consistentes em todos os nós.
- **Manutenção do Líder:** O líder envia *heartbeats* para os seguidores para evitar novas eleições.

---

## ⚙️ Configuração do Ambiente e Execução  

### Pré-requisitos  
- Python 3.x instalado.
- Biblioteca padrão `threading`, `queue` e `time` (já incluídas no Python).

### Passos para Executar  
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/simulacao-raft.git
   cd simulacao-raft
   ```
2. **Execute o script principal**:
  ```bash
    python raft_simulacao.py
  ```
3. **Observação**:
  O script irá iniciar 5 nós que se comunicarão, elegendo um líder e simulando falhas.

### 🛠 Explicação das Fases do Algoritmo

1. Início e Estado Inicial
Todos os nós começam como seguidores e aguardam mensagens ou timeouts para iniciar uma eleição.
2. Eleição de Líder
Quando o timeout expira, um nó se torna candidato, incrementa seu termo e solicita votos dos demais nós.
Os nós respondem com votos, desde que ainda não tenham votado para outro nó no mesmo termo.
Se o candidato receber a maioria dos votos, ele se torna líder.
3. Envio de Heartbeats
O líder envia mensagens de heartbeat periodicamente para os seguidores, informando que ainda está ativo e mantendo o estado de consenso.
4. Manutenção do Estado
Os nós continuam a ouvir mensagens e a responder adequadamente, atualizando seus estados conforme necessário.

### ⚠️ Falhas Simuladas e Respostas do Sistema
1. Falha de Nós
- Um nó pode ser programado para falhar usando o método falhar(). Durante a falha, ele para de enviar e receber mensagens.

Exemplo de log:
  ```bash
    Nó 2 falhou.
  ```

2. Recuperação de Nós
- Após 3 segundos, o nó falho é recuperado automaticamente com a função recuperar(), voltando ao estado de 
seguidor.

Exemplo de log:
```bash
  Nó 2 está se recuperando...
```

3. Novo Líder Após Falha
- Se o líder falhar, uma nova eleição é iniciada. O nó que atingir a maioria dos votos primeiro se tornará o novo líder.

4. Timeouts e Reeleições
- Se os seguidores não recebem heartbeats dentro do tempo limite, iniciam uma nova eleição.

### 📝 Exemplo de Logs Gerados

```bash
  Nó 1 iniciou eleição para o termo 1
  Nó 3 votou para o Nó 1 no termo 1
  Nó 1 tornou-se o líder no termo 1
  Nó 4 recebeu heartbeat do Nó 1
  Nó 2 falhou.
  Nó 2 está se recuperando...
  Nó 2 votou para o Nó 4 no termo 2
```

