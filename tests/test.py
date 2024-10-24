import sys
sys.path.append('external_dependecies')
sys.path.append('source')
from RP_MH import pmotif_find2
from RP_DC import pmotif_find3
from RP_GRAPH import pmotif_findg
from RPG_CF import pmotif_findauto
import time, pandas as pd, numpy as np, queue
from data_loader import convert_tsf_to_dataframe
from base import z_normalized_euclidean_distance
from find_bin_width import find_width_discr
#from extra import relative_contrast
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

import tracemalloc
if __name__ == "__main__":
    
    # Get from command line arguments the number of the dataset to be used, the window size, dimensionality, K and L
    # 0: FOETAL_ECG.dat
    # 1: evaporator.dat
    # 2: oikolab_weather_dataset.tsf
    # 3: RUTH.csv
    if len(sys.argv) < 6:
        print("Usage: python test.py <dataset> <window_size> <dimensionality_motif> <K> <L> <device>")
        sys.exit(1)
    dataset = int(sys.argv[1])
    window_size = int(sys.argv[2])
    dimensionality = int(sys.argv[3])
    K = int(sys.argv[4])
    L = int(sys.argv[5])
    if len(sys.argv) == 7:
        device = int(sys.argv[6])
    else:
        device = 0

    paths = ["Datasets/FOETAL_ECG.dat", "Datasets/evaporator.dat", "Datasets/oikolab_weather_dataset.tsf", "Datasets/RUTH.csv", "Datasets/CLEAN_House1.csv",
                "Datasets/powerts.csv", "Datasets/earthquake.csv"]
    d = None

    # Load the dataset
    if dataset == 2:
        data, freq, fc_hor, mis_val, eq_len = convert_tsf_to_dataframe(paths[2], 0)
        d = np.array([data.loc[i,"series_value"].to_numpy() for i in range(data.shape[0])], order='C', dtype=np.float32).T
        # Apply a savgol filter to the data
        d = savgol_filter(d, 300, 2, axis=0)
    elif dataset == 4:
        data = pd.read_csv(paths[dataset])
        data = data.drop(['Time','Unix', 'Issues'],axis=1)
        d = np.ascontiguousarray(data.to_numpy(), dtype=np.float32)
        d = d[:100000,:]
    elif dataset == 3 or dataset == 5 or dataset == 6:
        data = pd.read_csv(paths[dataset])
        d = np.ascontiguousarray(data.to_numpy(), dtype=np.float32) if dataset == 3 else np.ascontiguousarray(data.to_numpy().T, dtype=np.float32)
    else:
        data = pd.read_csv(paths[dataset], sep=r'\s+')
        data = data.drop(data.columns[[0]], axis=1)
        d = np.ascontiguousarray(data.to_numpy(), dtype=np.float32)
    
    r = 32#find_width_discr(d, window_size, K)

    thresh = min(dimensionality/d.shape[1], 0.8)
    
    # Start the timer
    tracemalloc.start()
    start = time.process_time()
    # Find the motifs
    #for i in range(5):
    motifs, num_dist = pmotif_findg(d, window_size, 1, dimensionality, r, thresh, L, K)

    end = (time.process_time() - start)
    print("Time elapsed: ", end)
    print("Distance computations:", num_dist)
    size, peak = tracemalloc.get_traced_memory()

    print(f"Current memory usage is {size / 10**6}MB; Peak was {peak / 10**6}MB")


    # Plot
    #motifs = queue.PriorityQueue()
    print(motifs.queue)
    copy = motifs.queue
    motifs = copy
    #motifs = find_all_occur(extract, motifs, window_size)
    colors = ["red", "green", "pink", "pink", "cyan", "yellow", "orange", "gray", "purple"]
    fig, axs = plt.subplots(d.shape[1]-2, 1, sharex=True)
    X = pd.DataFrame(d)
    for i, dimension in enumerate(X.columns):
        if i == 0 or i == 1:
            continue
        i = i - 2
        axs[i].plot(X[dimension], label=dimension, linewidth= 1.2, color='#6263e0')
        axs[i].set_axis_off()
        #axs[i].set_xlabel("Time")
        #axs[i].set_ylabel("Dimension " + str(dimension))
        #axs[i].legend()
        for idx, motif in enumerate(motifs):
            # Highlight the motifs in all dimensions
            for m in motif[1][1]:
                if i+2 in motif[1][2][0]:
                    axs[i].plot(X[dimension].iloc[m:m+window_size], color=colors[idx], linewidth=1.8, alpha=0.7)
                    #axs[i].axvspan(m, m + window_size, color=colors[idx], alpha=0.3)
    #plt.axis('off')
    #plt.suptitle("MultiDimensional Timeseries with Motifs Highlighted")
    #plt.tight_layout(rect=[0, 0, 1, 0.96])
    if device == 1:
        plt.savefig("motifs.svg", format='svg')
    else:   
        plt.show()
        # Compute relative contrast 
        #rc1= relative_contrast(d, window_size, dimensionality)
        #print("RC1:", rc1)
