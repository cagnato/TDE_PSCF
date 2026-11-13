import threading
import time

# Dados:
N = 5  # 5 filósofos
garfos = [threading.Lock() for _ in range(N)]  # Garfos 0..N-1
estado = ["pensando"] * N


def garfo_esquerda(p):
    return p


def garfo_direita(p):
    return (p + 1) % N


def pensar(p):
    print(f"Filósofo {p}: {estado[p]}")
    time.sleep(0.5)


def adquirir(garfo):
    garfos[garfo].acquire()  # bloqueia até o garfo estar livre
    time.sleep(0.1)


def comer(p):
    print(f"Filósofo {p}: {estado[p]}")
    time.sleep(0.5)


def liberar(garfo):
    garfos[garfo].release()


# Para cada filósofo p:
def filosofo(p):
    # Protocolo ingênuo: pega sempre o da esquerda primeiro, depois o da direita
    left = garfo_esquerda(p)
    right = garfo_direita(p)

    # Loop:
    while True:
        pensar(p)
        estado[p] = "com fome"
        print(f"Filósofo {p}: {estado[p]} (tentando garfos {left} e {right})")
        adquirir(left)   # bloqueia até o garfo estar livre
        adquirir(right)  # bloqueia até o garfo estar livre
        estado[p] = "comendo"
        comer(p)
        liberar(right)
        liberar(left)
        estado[p] = "pensando"


if __name__ == "__main__":
    print("=== PARTE 1: JANTAR DOS FILÓSOFOS (VERSÃO INGÊNUA - COM DEADLOCK) ===")
    print("Pressione Ctrl+C para encerrar após observar o travamento.\n")

    for p in range(N):
        t = threading.Thread(target=filosofo, args=(p,), daemon=True)
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExecução encerrada.")