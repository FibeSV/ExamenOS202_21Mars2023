import numpy as np
import time
import matplotlib.pyplot as plt
import sys
from mpi4py import MPI
nombre_cas   : int = 256
nb_cellules  : int = 360  # Cellules fantomes
nb_iterations: int = 360

compute_time = 0.
display_time = 0.

def save_as_md(cells, symbols='⬜⬛'):
    res = np.empty(shape=cells.shape, dtype='<U')
    res[cells==0] = symbols[0]
    res[cells==1] = symbols[1]
    np.savetxt(f'resultat_{num_config:03d}.md', res, fmt='%s', delimiter='', header=f'Config #{num_config}', encoding='utf-8')

def save_as_png(cells):
    fig = plt.figure(figsize=(nb_iterations/10., nb_cellules/10.))
    ax = plt.axes()
    ax.set_axis_off()
    ax.imshow(cells[:, 1:-1], interpolation='none', cmap='RdPu')
    plt.savefig(f"resultat_{num_config:03d}.png", dpi=100, bbox_inches='tight')
    plt.close()

def Automate_cellulaire(num_config):
    t1 = time.time()
    cells = np.zeros((nb_iterations, nb_cellules+2), dtype=np.int16)
    cells[0, (nb_cellules+2)//2] = 1
    for iter in range(1, nb_iterations):
        vals = np.left_shift(1, 4*cells[iter-1, 0:-2]
                             + 2*cells[iter-1, 1:-1]
                             + cells[iter-1, 2:])
        cells[iter, 1:-1] = np.logical_and(np.bitwise_and(vals, num_config), 1)
    t2 = time.time()
    compute_time  = t2 - t1

    t1 = time.time()
    save_as_md(cells)
#    save_as_png(cells)
    t2 = time.time()
    display_time = t2 - t1

    return compute_time, display_time


global_com = MPI.COMM_WORLD.Dup()
rank       = global_com.rank
nbp        = global_com.size

nombre_cas_local = nombre_cas // nbp
remain = nombre_cas % nbp

start_nombre_cas,end_nombre_cas = rank*nombre_cas_local, rank*nombre_cas_local+nombre_cas_local
if rank!=(nbp-1):
    for num_config in range(start_nombre_cas,end_nombre_cas):
        ct, dt = Automate_cellulaire(num_config)
        compute_time +=ct
        display_time +=dt
    print(f"Temps calcul des generations de cellules : {compute_time:.6g}, rank={rank}")
    print(f"Temps d'affichage des resultats : {display_time:.6g}, rank={rank}")
else:
    for num_config in range(start_nombre_cas,end_nombre_cas+remain):
        ct, dt = Automate_cellulaire(num_config)
        compute_time +=ct
        display_time +=dt
    print(f"Temps calcul des generations de cellules : {compute_time:.6g}, rank={rank}")
    print(f"Temps d'affichage des resultats : {display_time:.6g}, rank={rank}")
