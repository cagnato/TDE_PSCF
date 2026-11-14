import threading
import time

count = 0
T = 8
M = 200000

#Sem sincronizção

def tarefa():
    global count
    for i in range(M):
        temp = count #ler
        time.sleep(0) #deixar outra thread entrar
        count = temp + 1 #somar e escrever

threads = [threading.Thread(target=tarefa) for _ in range(T)]

inicio = time.time()
for t in threads: t.start()
for t in threads: t.join()
fim = time.time()


print("esperado:", T * M)
print("obtido:  ", count)
print("tempo:   ", round(fim - inicio, 3), "segundos")