import threading
import time


def Thread_1():
    global var_A, var_B
    print('Thread_1 iniciando')

    print("Thread_1 tentando adquirir o lock_A")
    lock_A.acquire()
    print("Thread_1 iniciou o lock_A")

    var_A = "Thread_1 alterou o valor de Var_A"
    print(var_A)

    time.sleep(1)

    print("Thread_1 tentando adquirir o lock_B")
    lock_B.acquire()
    print("Thread_1 iniciou o lock_B")

    var_B = "Thread_1 alterou o valor de Var_B"
    print(var_B)

    lock_B.release()
    print("Thread_1 soltou o lock_B")

    lock_A.release()
    print("Thread_1 soltou o lock_A")

    print("Thread_1 concluiu")
    return 


def Thread_2():
    global var_A, var_B
    print('Thread_2 iniciando')

    print("Thread_2 tentando adquirir o lock_B")
    lock_B.acquire()
    print("Thread_2 iniciou o lock_B")

    var_B = "Thread_2 alterou o valor de Var_B"
    print(var_B)

    time.sleep(1)

    print("Thread_2 tentando adquirir o lock_A")
    lock_A.acquire()
    print("Thread_2 iniciou o lock_A")

    var_A = "Thread_2 alterou o valor de Var_A"
    print(var_A)

    lock_A.release()
    print("Thread_2 soltou o lock_A")

    lock_B.release()
    print("Thread_2 soltou o lock_B")

    print("Thread_2 concluiu")
    return 


# variáveis de lock

lock_A = threading.Lock()
lock_B = threading.Lock()
var_A = ""
var_B = ""

if __name__ == "__main__":
    print("=== PARTE 3: DeadLock (versão que trava) ===")
    print("Pressione Ctrl+C para encerrar a simulação.\n")

    thread_1 = threading.Thread(target=Thread_1, args=(), daemon=True)
    thread_1.start()

    thread_2 = threading.Thread(target=Thread_2, args=(), daemon=True)
    thread_2.start()

    try:
        while True:
            time.sleep(1)
            if not thread_1.is_alive() and not thread_2.is_alive():
                print("\nExecução de todas as threads concluída.")
                break
    except KeyboardInterrupt:
        print("\nExecução encerrada.")