import threading
import time

Contador = 0
TempoTotal = 0
def incrementar():
    global Contador
    global TempoTotal
    t0 = time.time()
    for _ in range(1000000):
         Contador = Contador + 1
    tf = time.time()
    delta_t = tf - t0
    TempoTotal += delta_t
    print(f"tempo: {delta_t}")

threads = [threading.Thread(target= incrementar) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()

print(f"Contador: {Contador}")
print(f"TempoTotal: {TempoTotal}")