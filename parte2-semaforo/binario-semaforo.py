import threading
import time

count = 0
T = 8
M = 200000

# com semaforo binario
sem = threading.Semaphore(1)

def tarefa():
    global count
    for i in range(M):  

        sem.acquire()
        try:
            count = count + 1
        finally: 
            sem.release()
            
        time.sleep(0)

threads = [threading.Thread(target=tarefa) for _ in range(T)]

inicio = time.time()
for t in threads: t.start()
for t in threads: t.join()
fim = time.time()


print("esperado:", T * M)
print("obtido:  ", count)
print("tempo:   ", round(fim - inicio, 3), "segundos")