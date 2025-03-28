import matplotlib.pyplot as plt
import numpy as np
import random
import os
import time
import multiprocessing
from functools import wraps

# Configurações iniciais
import matplotli
matplotlib.use('Agg')  

# Defina seu nome de usuário Windows aqui
USERNAME = "pedro"  # Altere se necessário
DESKTOP_PATH = os.path.join("C:\\Users", USERNAME, "Downloads", "fractais_py")
os.makedirs(DESKTOP_PATH, exist_ok=True)

def salvar_figura(nome):
    """Salva a figura atual com tratamento de erros"""
    caminho = os.path.join(DESKTOP_PATH, f"{nome}.png")
    try:
        plt.savefig(caminho, bbox_inches='tight', dpi=300)
        print(f"{nome}.png salvo em: {caminho}")
    except Exception as e:
        print(f"ERRO ao salvar {nome}.png: {str(e)}")
    finally:
        plt.close()

def medir_tempo(funcao):
    """Decorador para medir tempo de execução"""
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = funcao(*args, **kwargs)
        fim = time.time()
        print(f"{funcao.__name__} executado em {fim - inicio:.2f} segundos")
        return resultado
    return wrapper

def gerar_fractal(transformacoes, probabilidades, iteracoes=100000):
    """Gera pontos para fractais IFS"""
    if not abs(sum(probabilidades) - 1.0) < 1e-6:
        raise ValueError("Probabilidades devem somar 1")
    
    x, y = 0.0, 0.0
    pontos = []
    for _ in range(iteracoes):
        r = random.random()
        acumulado = 0.0
        for i, prob in enumerate(probabilidades):
            acumulado += prob
            if r < acumulado:
                x, y = transformacoes[i](x, y)
                break
        pontos.append((x, y))
    return pontos

@medir_tempo
def sierpinski():
    transformacoes = [
        lambda x, y: (0.5 * x, 0.5 * y),
        lambda x, y: (0.5 * x + 0.5, 0.5 * y),
        lambda x, y: (0.5 * x + 0.25, 0.5 * y + 0.5)
    ]
    pontos = gerar_fractal(transformacoes, [1/3, 1/3, 1/3])
    plt.figure(figsize=(8, 8))
    plt.scatter(*zip(*pontos), s=0.1, color='black', marker='.')
    plt.title("Triângulo de Sierpinski")
    plt.axis('off')
    salvar_figura("sierpinski")

@medir_tempo
def samambaia_barnsley():
    transformacoes = [
        lambda x, y: (0.0, 0.16 * y),
        lambda x, y: (0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6),
        lambda x, y: (0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6),
        lambda x, y: (-0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44)
    ]
    pontos = gerar_fractal(transformacoes, [0.01, 0.85, 0.07, 0.07])
    plt.figure(figsize=(8, 8))
    plt.scatter(*zip(*pontos), s=0.1, color='green', marker='.')
    plt.title("Samambaia de Barnsley")
    plt.axis('off')
    salvar_figura("samambaia_barnsley")

@medir_tempo
def mandelbrot(width=800, height=800, max_iter=100):
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    image = np.zeros((height, width))

    for row in range(height):
        for col in range(width):
            c = complex(x_min + (x_max - x_min) * col / width,
                        y_min + (y_max - y_min) * row / height)
            z, n = 0.0j, 0
            while abs(z) <= 2 and n < max_iter:
                z = z * z + c
                n += 1
            image[row, col] = n

    plt.figure(figsize=(10, 10))
    plt.imshow(image, extent=(x_min, x_max, y_min, y_max), cmap='hot')
    plt.title("Conjunto de Mandelbrot")
    plt.axis('off')
    salvar_figura("mandelbrot")

@medir_tempo
def julia(c=-0.7 + 0.27015j, width=800, height=800, max_iter=100):
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    image = np.zeros((height, width))

    for row in range(height):
        for col in range(width):
            z = complex(x_min + (x_max - x_min) * col / width,
                        y_min + (y_max - y_min) * row / height)
            n = 0
            while abs(z) <= 2 and n < max_iter:
                z = z * z + c
                n += 1
            image[row, col] = n

    plt.figure(figsize=(10, 10))
    plt.imshow(image, extent=(x_min, x_max, y_min, y_max), cmap='twilight_shifted')
    plt.title("Conjunto de Julia")
    plt.axis('off')
    salvar_figura("julia")

@medir_tempo
def koch_curve(order=4, size=300):
    def koch_curve_recursive(points, order):
        if order == 0:
            return points
        new_points = []
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i + 1]
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            new_points.extend([
                p1,
                (p1[0] + dx / 3, p1[1] + dy / 3),
                (p1[0] + dx / 2 - dy * np.sqrt(3) / 6, p1[1] + dy / 2 + dx * np.sqrt(3) / 6),
                (p1[0] + 2 * dx / 3, p1[1] + 2 * dy / 3)
            ])
        new_points.append(points[-1])
        return koch_curve_recursive(new_points, order - 1)

    points = koch_curve_recursive([(0, 0), (size, 0)], order)
    plt.figure(figsize=(10, 5))
    plt.plot(*zip(*points), color='blue', linewidth=1)
    plt.title("Curva de Koch")
    plt.axis('equal')
    plt.axis('off')
    salvar_figura("koch_curve")

@medir_tempo
def fractal_tree():
    def draw_tree(ax, x, y, length, angle, depth):
        if depth == 0:
            return
        x_end = x + length * np.cos(np.radians(angle))
        y_end = y + length * np.sin(np.radians(angle))
        ax.plot([x, x_end], [y, y_end], color='brown', linewidth=1)
        draw_tree(ax, x_end, y_end, length * 0.7, angle - 30, depth - 1)
        draw_tree(ax, x_end, y_end, length * 0.7, angle + 30, depth - 1)

    fig, ax = plt.subplots(figsize=(8, 10))
    draw_tree(ax, 0, 0, 100, 90, 8)
    plt.title("Árvore Fractal")
    plt.axis('equal')
    plt.axis('off')
    salvar_figura("fractal_tree")

@medir_tempo
def sierpinski_carpet(size=3, iterations=4):
    carpet = np.ones((size**iterations, size**iterations))

    def recursive_remove(grid, x, y, size, iteration):
        if iteration == 0:
            return
        sub_size = size // 3
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    grid[x + sub_size:x + 2 * sub_size, y + sub_size:y + 2 * sub_size] = 0
                else:
                    recursive_remove(grid, x + i * sub_size, y + j * sub_size, sub_size, iteration - 1)

    recursive_remove(carpet, 0, 0, size**iterations, iterations)
    plt.figure(figsize=(8, 8))
    plt.imshow(carpet, cmap='gray_r')
    plt.title("Tapete de Sierpinski")
    plt.axis('off')
    salvar_figura("sierpinski_carpet")

@medir_tempo
def menger_sponge(iterations=2):
    def generate_sponge(grid, x, y, z, size, iteration):
        if iteration == 0:
            return
        sub_size = size // 3
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if sum([i == 1, j == 1, k == 1]) >= 2:
                        grid[
                            x + i * sub_size : x + (i + 1) * sub_size,
                            y + j * sub_size : y + (j + 1) * sub_size,
                            z + k * sub_size : z + (k + 1) * sub_size
                        ] = 0
                    else:
                        generate_sponge(grid, x + i * sub_size, y + j * sub_size, z + k * sub_size, sub_size, iteration - 1)

    grid_size = 3**iterations
    grid = np.ones((grid_size, grid_size, grid_size))
    generate_sponge(grid, 0, 0, 0, grid_size, iterations)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.voxels(grid, edgecolor='k')
    plt.title("Esponja de Menger")
    salvar_figura("menger_sponge")

def gerar_sequencial():
    print("\nEXECUCAO SEQUENCIAL (salvando em {})".format(DESKTOP_PATH))
    inicio = time.time()
    
    fractais = [
        sierpinski,
        samambaia_barnsley,
        mandelbrot,
        julia,
        koch_curve,
        fractal_tree,
        sierpinski_carpet,
        menger_sponge
    ]
    
    for fractal in fractais:
        fractal()
    
    print("\nTempo total sequencial: {:.2f} segundos".format(time.time() - inicio))

def gerar_paralelo():
    print("\nEXECUCAO PARALELA (salvando em {})".format(DESKTOP_PATH))
    inicio = time.time()
    
    processos = []
    for fractal in [
        sierpinski,
        samambaia_barnsley,
        mandelbrot,
        julia,
        koch_curve,
        fractal_tree,
        sierpinski_carpet,
        menger_sponge
    ]:
        p = multiprocessing.Process(target=fractal)
        p.start()
        processos.append(p)

    for p in processos:
        p.join()
    
    print("\nTempo total paralelo: {:.2f} segundos".format(time.time() - inicio))

def main():
    print("\nTodas as imagens serao salvas em: {}".format(DESKTOP_PATH))
    print("="*50)
    print("GERADOR DE FRACTAIS PARALELO")
    print("="*50)
    
    gerar_sequencial()
    gerar_paralelo()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()