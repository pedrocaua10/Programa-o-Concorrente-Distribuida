import random
import threading
import time

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]
    return quicksort(left) + [pivot] + quicksort(right)

def quicksort_parallel(arr, result, index):
    result[index] = quicksort(arr)

def gerar_numeros_aleatorios(n=100, min_val=1, max_val=200):
    return [random.randint(min_val, max_val) for _ in range(n)]

def testar_quicksort(n):
    numeros = gerar_numeros_aleatorios(n)
    
    print(f"\nTestando lista com {n} numeros:")
    print(f"Primeiros 10 numeros antes da ordenacao:", numeros[:10])
    
    start_time = time.time()
    numeros_ordenados = quicksort(numeros)
    end_time = time.time()
    print("Tempo de execucao sem threads:", end_time - start_time, "segundos")
    print(f"Primeiros 10 numeros apos a ordenacao (sem threads):", numeros_ordenados[:10])
    
    start_time = time.time()
    
    pivot = numeros[-1]
    left = [x for x in numeros[:-1] if x <= pivot]
    right = [x for x in numeros[:-1] if x > pivot]
    
    left_sorted = [None]
    right_sorted = [None]
    
    thread_left = threading.Thread(target=quicksort_parallel, args=(left, left_sorted, 0))
    thread_right = threading.Thread(target=quicksort_parallel, args=(right, right_sorted, 0))
    
    thread_left.start()
    thread_right.start()
    
    thread_left.join()
    thread_right.join()
    
    numeros_ordenados_parallel = left_sorted[0] + [pivot] + right_sorted[0]
    
    end_time = time.time()
    print("Tempo de execucao com threads:", end_time - start_time, "segundos")
    print(f"Primeiros 10 numeros apos a ordenacao (com threads):", numeros_ordenados_parallel[:10])

if __name__ == "__main__":
    # Testar com listas de 10, 100 e 1000 numeros
    testar_quicksort(10)
    testar_quicksort(100)
    testar_quicksort(1000)