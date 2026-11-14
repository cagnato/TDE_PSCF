- **Grupo:** TDE2
- **Integrantes:** Davi Cagnato Pinto, Edgar Felipe Polswut, Luis Felipe Quintiliano, Nicolas Jacinto Grzebieniak
- **Linguagem escolhida:** Python (3.10+)
- **Link do video explicativo:** [Adicionar link do YouTube ao final]

# Parte 1 - Jantar dos Filósofos

## Sobre o Problema e o Surgimento do Deadlock

O Jantar dos Filósofos simula 5 filosofos (numerados de 0 a 4) sentados ao redor de uma mesa circular. Eles passam o tempo alternando entre três estados: pensando, com fome e comendo. Entre cada filosofo existe um garfo compartilhado (também numerados de 0 a 4), totalizando 5 garfos na mesa. Para conseguir comer, o filosofo precisa pegar os dois garfos ao seu lado: o da esquerda (indice p) e o da direita (indice (p + 1) % 5).

Na nossa primeira implementação (jantar_ingenuo.py), seguimos a abordagem ingênua onde todos os filósofos executam exatamente a mesma ação: quando ficam com fome, pegam primeiro o garfo da esquerda e logo em seguida tentam pegar o garfo da direita.

O problema acontece quando todos os 5 filósofos ficam com fome ao mesmo tempo e cada um pega o seu garfo da esquerda. Nesse momento, não sobra nenhum garfo livre na mesa. Quando eles tentam pegar o garfo da direita, todos ficam travados esperando o vizinho soltar o garfo. Como ninguém solta o primeiro garfo antes de terminar de comer, o programa entra em deadlock e nenhuma thread avança.

---

## Solução Proposta e Condição de Coffman Negada

Para que um deadlock aconteça, as quatro condições de Coffman precisam ocorrer juntas:
1. **Exclusão mutua**: um garfo não pode ser usado por dois filósofos ao mesmo tempo.
2. **Manter e esperar**: o filosofo segura um garfo enquanto espera o segundo ficar livre.
3. **Não preempção**: um filosofo não pode tomar o garfo da mão do vizinho a forca.
4. **Espera circular**: forma-se um ciclo fechado onde o filosofo 0 espera pelo 1, o 1 espera pelo 2, o 2 pelo 3, o 3 pelo 4 e o 4 espera pelo 0.

Na versão corrigida (jantar_corrigido.py), aplicamos a estratégia de Hierarquia de Recursos, que resolve o problema negando a condição de Espera Circular.

Em vez de pegar sempre esquerda e depois direita, criamos uma regra baseada no numero do garfo: todo filosofo deve pegar primeiro o garfo de menor índice (min) e depois o de maior índice (max).

Na pratica, isso muda o comportamento na mesa da seguinte forma:
- Os filósofos 0, 1, 2 e 3 continuam tentando pegar na ordem (0 -> 1), (1 -> 2), (2 -> 3) e (3 -> 4).
- O filosofo 4 (que senta entre os garfos 4 e 0) inverte a sua ordem e tenta pegar primeiro o garfo 0 e depois o garfo 4, já que 0 e menor que 4.

Com essa mudança, se os filósofos 0, 1, 2 e 3 pegarem os garfos 0, 1, 2 e 3, o filosofo 4 vai tentar pegar o garfo 0 primeiro. Como o garfo 0 ja esta ocupado com o filosofo 0, o filosofo 4 fica aguardando antes mesmo de encostar no garfo 4. Isso deixa o garfo 4 livre para o filosofo 3 pegar, comer e devolver os garfos 3 e 4 para a mesa, destravando todos os outros em sequencia.

---

## Progresso e Justiça (Ausência de Inanição)

Além de evitar o deadlock, também precisamos garantir que nenhum filosofo tenha starvation porque seus vizinhos não dão espaço.

No nosso código, todos os filósofos conseguem comer de forma justa por tres motivos:
1. **Refeicoes com tempo limitado**: assim que o filosofo consegue os dois garfos, ele come por um tempo curto e imediatamente executa liberar(right) e liberar(left).
2. **Pausa obrigatória para pensar**: logo após soltar os garfos, o filosofo volta para o estado "pensando" e passa por um time.sleep antes de sentir fome de novo. Enquanto ele esta pensando, os vizinhos que ja estavam na fila esperando por aqueles garfos conseguem adquiri-los, evitando que o mesmo filosofo pegue os garfos varias vezes seguidas.
3. **Tempos variados**: usamos random.uniform(0.5, 1.0) nos tempos de pensar e comer para evitar que dois vizinhos entrem em um ritmo sincronizado que prejudique o filosofo do meio.

---

## Pseudocódigo do Protocolo

Abaixo esta o pseudocodigo utilizado como base para a versao corrigida com hierarquia de recursos:

Dados:
N = 5 filosofos
Garfos 0..N-1 (garfo i fica entre filosofos i e (i+1) mod N)

Para cada filosofo p:
  left = min(garfo_esquerda(p), garfo_direita(p))
  right = max(garfo_esquerda(p), garfo_direita(p))
  Loop:
    pensar()
    estado[p] <- "com fome"
    adquirir(left)  // bloqueia ate o garfo estar livre
    adquirir(right) // bloqueia ate o garfo estar livre
    estado[p] <- "comendo"
    comer()
    liberar(right)
    liberar(left)
    estado[p] <- "pensando"


**1. Testando a versão ingênua (com deadlock)**:

Saída obtida no console (mostrando o momento exato em que todos ficam com fome, pegam o primeiro garfo e o programa trava):

=== PARTE 1: JANTAR DOS FILOSOFOS (VERSAO INGENUA - COM DEADLOCK) ===
Pressione Ctrl+C para encerrar após observar o travamento.

Filosofo 0: pensando
Filosofo 1: pensando
Filosofo 2: pensando
Filosofo 3: pensando
Filosofo 4: pensando
Filosofo 0: com fome (tentando garfos 0 e 1)
Filosofo 1: com fome (tentando garfos 1 e 2)
Filosofo 2: com fome (tentando garfos 2 e 3)
Filosofo 3: com fome (tentando garfos 3 e 4)
Filosofo 4: com fome (tentando garfos 4 e 0)


**2. Testando a versão corrigida (sem deadlock)**:

Saída obtida no console (mostrando a ordem corrigida do Filosofo 4 tentando `0 -> 4` e a execução fluindo normalmente):

=== PARTE 1: JANTAR DOS FILOSOFOS (VERSAO CORRIGIDA - SEM DEADLOCK) ===
Pressione Ctrl+C para encerrar a simulação.

Filosofo 0: pensando
Filosofo 1: pensando
Filosofo 2: pensando
Filosofo 3: pensando
Filosofo 4: pensando
Filosofo 2: com fome (ordem de aquisicao: 2 -> 3)
Filosofo 2: comendo
Filosofo 4: com fome (ordem de aquisicao: 0 -> 4)
Filosofo 4: comendo
Filosofo 1: com fome (ordem de aquisicao: 1 -> 2)
Filosofo 0: com fome (ordem de aquisicao: 0 -> 1)
Filosofo 3: com fome (ordem de aquisicao: 3 -> 4)
Filosofo 2: pensando
Filosofo 1: comendo
Filosofo 4: pensando
Filosofo 3: comendo

# Parte 2 - Semáforo

## Como executar

```bash
python parte2-semaforo/semSincronizacao.py # termina sozinho
```

## Parâmetros

- **T** (número de threads): 8
- **M** (incrementos por thread): 200000
- **Valor esperado:** T × M = 8 × 200000 = 1600000

## Semáforo sem sincronização

| Execução | Valor esperado | Valor obtido | Tempo (s) |
|----------|----------------|--------------|-----------|
| 1        | 1.600.000      | 200.141      | 1,841     |
| 2        | 1.600.000      | 200.122      | 1,697     |
| 3        | 1.600.000      | 200.170      | 1,733     |

## Observação sobre o GIL

(1) O GIL é .

# Parte 3 — Deadlock

## Arquivos

| Arquivo | Descrição |
|---|---|
| `deadlock-travamento.py` | Versão que trava: Thread_1 adquire A → B e Thread_2 adquire B → A |
| `deadlock-hierarquia.py` | Versão corrigida: as duas threads adquirem sempre A → B (hierarquia de recursos) |

## Como executar

```bash
python parte3-deadlock/deadlock-travamento.py   # trava; encerre com Ctrl+C
python parte3-deadlock/deadlock-hierarquia.py   # termina sozinho
```

## 1. Reprodução do deadlock

Cada thread adquire um lock, dorme 1 segundo (para garantir que a outra também adquira o seu) e então tenta adquirir o lock que está com a outra.

### Saída obtida

```
=== PARTE 3: DeadLock (versão que trava) ===
Pressione Ctrl+C para encerrar a simulação.

Thread_1 iniciando
Thread_1 tentando adquirir o lock_A
Thread_1 iniciou o lock_A
Thread_1 alterou o valor de Var_A
Thread_2 iniciando
Thread_2 tentando adquirir o lock_B
Thread_2 iniciou o lock_B
Thread_2 alterou o valor de Var_B
Thread_1 tentando adquirir o lock_B
Thread_2 tentando adquirir o lock_A

Execução encerrada.
```

As duas últimas linhas antes do Ctrl+C mostram o travamento:

- a Thread_1 segura o `lock_A` e espera o `lock_B`;
- a Thread_2 segura o `lock_B` e espera o `lock_A`.

Nenhuma das duas chega a imprimir "iniciou o lock_B" / "iniciou o lock_A" nem "concluiu". O programa fica parado indefinidamente até ser interrompido com Ctrl+C.

## 2. As quatro condições de Coffman

Todas as quatro condições aparecem ao mesmo tempo na versão que trava:

| Condição | Como aparece no código |
|---|---|
| **Exclusão mútua** | `threading.Lock()` só pode pertencer a uma thread por vez. Enquanto a Thread_1 tem o `lock_A`, nenhuma outra thread consegue adquiri-lo. |
| **Manter-e-esperar** | Cada thread continua segurando o primeiro lock enquanto chama `acquire()` no segundo. A Thread_1 não solta o `lock_A` enquanto espera o `lock_B`. |
| **Não preempção** | Um lock não pode ser tomado à força de quem o possui: só a própria thread dona pode chamar `release()`. Além disso, `acquire()` sem timeout espera para sempre, e a thread nunca desiste. |
| **Espera circular** | A Thread_1 espera o `lock_B`, que está com a Thread_2, e a Thread_2 espera o `lock_A`, que está com a Thread_1. Isso forma o ciclo T1 → T2 → T1. |

## 3. Correção: ordem global de aquisição (hierarquia de recursos)

Foi definida uma regra global: **toda thread adquire sempre o `lock_A` antes do `lock_B`**. Na implementação, as duas threads executam a mesma função, então seguem obrigatoriamente a mesma ordem. Os locks são liberados na ordem inversa (B e depois A).

### Condição quebrada: espera circular

As outras três condições continuam existindo: os locks ainda são exclusivos, a thread ainda segura o `lock_A` enquanto pede o `lock_B`, e os locks ainda não podem ser tomados. O que deixa de existir é a **espera circular**.

Com a ordem fixa, uma thread só pode estar segurando o `lock_B` se já segurar o `lock_A`. Então a thread que espera nunca segura um recurso de que a outra precisa: ela fica bloqueada já no `lock_A`, sem segurar nada. As esperas só podem seguir o sentido A → B, e nunca voltam. Sem ciclo, não há deadlock.

O `time.sleep(1)` foi mantido na versão corrigida de propósito: mesmo com a mesma pausa que causava o travamento, agora o programa termina.

### Saída obtida

```
=== PARTE 3: DeadLock (versão corrigida — hierarquia) ===
Pressione Ctrl+C para encerrar a simulação.

Thread_1 iniciando
Thread_1 tentando adquirir o lock_A
Thread_1 iniciou o lock_A
Thread_1 alterou o valor de Var_A
Thread_2 iniciando
Thread_2 tentando adquirir o lock_A
Thread_1 tentando adquirir o lock_B
Thread_1 iniciou o lock_B
Thread_1 alterou o valor de Var_B
Thread_1 soltou o lock_B
Thread_1 soltou o lock_A
Thread_1 concluiu
Thread_2 iniciou o lock_A
Thread_2 alterou o valor de Var_A
Thread_2 tentando adquirir o lock_B
Thread_2 iniciou o lock_B
Thread_2 alterou o valor de Var_B
Thread_2 soltou o lock_B
Thread_2 soltou o lock_A
Thread_2 concluiu

Execução de todas as threads concluída.
```

Nesse log, a Thread_2 tenta o `lock_A` e fica esperando sem segurar nenhum lock. A Thread_1 consegue pegar o `lock_B`, termina e solta os dois. Só então a Thread_2 continua. As duas threads concluem e o programa encerra sozinho.