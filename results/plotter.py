import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
from matplotlib.ticker import ScalarFormatter

if __name__ == "__main__":
    matplotlib.use("WebAgg")
    xfmt = ScalarFormatter()
    xfmt.set_scientific(True)
    xfmt.set_powerlimits((1, 2))
    names = ["potentials", "evaporator", "RUTH", "weather", "whales"]
    r"""
    # !!!K plots
    data = pd.read_csv("results/K_results.csv")
    # FInd the different values in the first column
    ds_values = data["Dataset"].unique()
    # Create a plot with ds_values subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 5), sharex=True, layout="constrained")
    for i, ds_val in enumerate(ds_values):
        # Get the data for the current value
        K_data = data[data["Dataset"] == ds_val]
        sns.lineplot(data=K_data, x="K", y="Time elapsed", color= "mediumseagreen", ax=axs[i // 2, i % 2], legend=False)
        axs[i // 2, i % 2].set_title(names[i])
        axs[i // 2, i % 2].set_xlabel('')
        axs[i // 2, i % 2].set_ylabel('')
    sns.despine(offset=10, trim=True)
    sns.set_context("paper")
    fig.supxlabel("Concatenations - K")
    fig.supylabel("Time elapsed (s)")
    plt.show()
    # !!!L plots
    data = pd.read_csv("results/L_results.csv")
    # FInd the different values in the first column
    ds_values = data["Dataset"].unique()
    data = data.groupby(["Dataset", "L"]).mean().reset_index()
    # Create a plot with ds_values subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 5), sharex=True, layout="constrained")
    for i, ds_val in enumerate(ds_values):
        # Get the data for the current value
        L_data = data[data["Dataset"] == ds_val]
        axs[i // 2, i % 2].stackplot(
            L_data["L"],
            L_data["Time int"],
            color="peachpuff",
            alpha=0.8,
            labels=["Hash time"],
        )
        axs[i // 2, i % 2].stackplot(
            L_data["L"],
            L_data["Time elapsed"],
            color="wheat",
            alpha=0.4,
            labels=["Search time"],
        )
        axs[i // 2, i % 2].set_title(names[i])
        axs[i // 2, i % 2].set_xlabel('')
        axs[i // 2, i % 2].set_ylabel('')

        if i == 3:
            axs[i // 2, i % 2].legend(loc="upper right")
    sns.despine(offset=10, trim=True)
    sns.set_context("paper")
    fig.supxlabel("Repetitions - L")
    fig.supylabel("Time elapsed (s)")
    plt.show()

    # !!!r plots
    data = pd.read_csv("results/R_results.csv")
    # FInd the different values in the first column
    ds_values = data["Dataset"].unique()
    r = [4, 8, 16, 32]
    r_dc = [6, 8, 15, 32]
    r_dist = [16, 312, 212, 38106]

    # Create a plot with ds_values subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 5), sharex=True, layout="constrained")
    for i, ds_val in enumerate(ds_values):
        # Get the data for the current value
        r_data = data[data["Dataset"] == ds_val]
        sns.lineplot(data=r_data, x="r", y="dist_computed", color= "coral", ax=axs[i // 2, i % 2])

        axs[i // 2, i % 2].vlines(
            r_dc[i], 0, r_dist[i], linestyle="dotted", color="crimson"
        )
        axs[i//2, i%2].scatter(r_dc[i], r_dist[i], color="crimson", zorder=5, s=50, label="Self-tuned r")
        axs[i // 2, i % 2].set_title(names[i])
        axs[i//2,i%2].yaxis.set_major_formatter(xfmt)
        axs[i // 2, i % 2].set_xlabel('')
        axs[i // 2, i % 2].set_ylabel('')    
    plt.legend()
    sns.despine(offset=1, trim=True)
    sns.set_context("paper")
    fig.supxlabel("Discretization parameter - r")
    fig.supylabel("Compared couples")
    plt.show()

    """
    # Multi subdimensional search plots
    data = pd.read_csv("results/multi_results.csv")
    fig, axs = plt.subplots(4, 1, figsize=(5, 6), sharex=True, layout="constrained")
    for i, row in data.iterrows():
        sns.lineplot(
            x=[0, data["mstumptime"][i]],
            y=[0, 0],
            ax=axs[i],
            linewidth=1.5,
            color="slategrey",
        )
        if i != 3:
            axs[i].annotate(
                f'MSTUMP: {data["mstumptime"][i]} s',
                (0.5, 0.01),
                xycoords=("axes fraction", "data"),
                color="slategray",
            )
        else:
            axs[i].annotate(
                f'MSTUMP: {data["mstumptime"][i]} s →',
                (0.65, 0.01),
                xycoords=("axes fraction", "data"),
                color="slategray",
            )

        plot = data.iloc[i]
        plot = plot.drop(["mstumptime"])
        hash_t = plot.values[-1]
        last_val = np.nanmax(plot.values)
        sns.scatterplot(
            x=plot.values[:-1],
            y=np.zeros(7),
            ax=axs[i],
            style=True,
            markers="|",
            legend=False,
            s=150.5,
            color="cornflowerblue",
        )
        sns.lineplot(
            x=[0, last_val], y=[0, 0], ax=axs[i], linewidth=4.5, color="mediumslateblue"
        )
        sns.lineplot(
            x=[0, hash_t], y=[0, 0], ax=axs[i], linewidth=5, color="darkslateblue"
        )

        sns.despine()
        axs[i].set_title(
            names[i], fontdict={"fontweight": "heavy", "fontsize": 10}, loc="left"
        )
        # Hide axes for all subplots except the last one
        if i < len(axs) - 1:  # For all but the last subplot
            axs[i].set_axis_off()
        else:  # For the last subplot
            axs[i].xaxis.set_visible(True)
            axs[i].spines["top"].set_visible(False)
            axs[i].spines["right"].set_visible(False)
            axs[i].spines["left"].set_visible(False)
            axs[i].yaxis.set_visible(False)  # Hide y-axis and its values
            axs[i].set_xlabel("time (s)")
    plt.show()

    # Noise plot

    data = pd.read_csv("results/noise.csv")
    # FInd the different values in the first column
    ds_values = data["Dataset"].unique()
    fig, axs = plt.subplots(1, 1, figsize=(10, 5), layout="constrained")
    colors = ["palevioletred", "skyblue"]
    names = ["potentials", "evaporator"]
    for val in ds_values:
        n_data = data[data["Dataset"] == val]
        sns.lineplot(
            data=n_data,
            x=" noise",
            y=" val",
            color=colors[val],
            alpha=0.7,
            label=names[val],
        )
    axs.set_ylabel("Recall")
    axs.set_xlabel("Injected dimensions")
    sns.despine(offset=10.2)
    plt.ylim((0, 1.1))
    plt.show()
