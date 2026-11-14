import threading
import time


def Thread(thread_name):
    global var_A, var_B
    print(f'{thread_name} iniciando')

    print(f'{thread_name} tentando adquirir o lock_A')
    lock_A.acquire()
    print(f'{thread_name} iniciou o lock_A')

    var_A = f'{thread_name} alterou o valor de Var_A'
    print(var_A)

    time.sleep(1)

    print(f'{thread_name} tentando adquirir o lock_B')
    lock_B.acquire()
    print(f'{thread_name} iniciou o lock_B')

    var_B = f'{thread_name} alterou o valor de Var_B'
    print(var_B)

    lock_B.release()
    print(f'{thread_name} soltou o lock_B')

    lock_A.release()
    print(f'{thread_name} soltou o lock_A')

    print(f'{thread_name} concluiu')
    return 


# variáveis de lock

lock_A = threading.Lock()
lock_B = threading.Lock()
var_A = ""
var_B = ""

if __name__ == "__main__":
    print("=== PARTE 3: DeadLock (versão corrigida — hierarquia) ===")
    print("Pressione Ctrl+C para encerrar a simulação.\n")

    thread_1 = threading.Thread(target=Thread, args=("Thread_1",), daemon=True)
    thread_1.start()

    thread_2 = threading.Thread(target=Thread, args=("Thread_2",), daemon=True)
    thread_2.start()

    try:
        while True:
            time.sleep(1)
            if not thread_1.is_alive() and not thread_2.is_alive():
                print("\nExecução de todas as threads concluída.")
                break
    except KeyboardInterrupt:
        print("\nExecução encerrada.")