import threading
import time

ContadorAP = 0
ContadorBP = 0

L = threading.Lock()

def thread_AP():
    global ContadorAP
    while True:
        with L:
            print("[Alta prioridade] Usando o recurso...")
            ContadorAP += 1
            time.sleep(0.9)

def thread_BP():
    global ContadorBP
    while True:
        with L:
            print("[Baixa prioridade] Usando o recurso...")
            ContadorBP += 1
            time.sleep()

TA = threading.Thread(target= thread_AP, daemon=True)
TB = threading.Thread(target= thread_BP, daemon=True)

TA.start()
TB.start()

time.sleep(10)

#Relatorio final

print("\nRelatorio")
print(f"Thread de baixa prioridade: {ContadorBP}")
print(f"Thread de alta prioridade: {ContadorAP}")