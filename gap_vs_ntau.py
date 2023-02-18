#!/usr/bin/env python

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ruamel.yaml import YAML
from abipy.tools.plotting import get_axarray_fig_plt

sns.set_theme(style="darkgrid")

def gaps_vs_ntau(filepath):

    def get_doc():
        buf = []
        while lines:
            l = lines.pop(0)
            l = l.replace("!Tabular", "")
            if l.startswith( "..."): break
            buf.append(l)

        yaml = YAML(typ='safe')   # default, if not specfied, is 'rt' (round-trip)
        return yaml.load("".join(buf))

    lines = open(filepath, "rt").readlines()
    gwr_params = []
    se_docs = [None, None]

    system = os.path.relpath(os.path.dirname(filepath)).split("_")[0]

    dict_list = []
    count = -1
    while lines:
        line = lines.pop(0)
        if line.startswith("--- !GWR_params"):
            gwr_params = get_doc()
            count = 0

        if line.startswith("--- !GWR_SelfEnergy_ee"):
            se_docs[count] = get_doc()
            count += 1

        if count == 2:
            count = 0
            keys = ["ntau",  "min_transition_energy_eV", "max_transition_energy_eV", "eratio",
                    "ft_max_err_t2w_cos", "ft_max_err_w2t_cos",
                    "ft_max_err_t2w_sin", "cosft_duality_error",]
            data = {k: gwr_params[k] for k in keys}
            data["system"] = system
            data["Gamma_qp_gap"] = se_docs[0]["QP_gap"]
            data["Gamma_ks_gap"] = se_docs[0]["KS_gap"]
            data["X_qp_gap"] = se_docs[1]["QP_gap"]
            data["X_ks_gap"] = se_docs[1]["KS_gap"]
            dict_list.append(data)

    df = pd.DataFrame(dict_list)
    eratio = df["eratio"][0]
    label = f"system: {system}, eratio: {eratio:.2f}"
    return df, label


def plot_tau_convergence(filepath):
    df, label = gaps_vs_ntau(filepath)

    print(df[["ntau", "Gamma_qp_gap", "X_qp_gap",] +
             [k for k in df if "_err" in k]
            ])

    system = df["system"][0]

    if True:
        ax_mat, fig, plt = get_axarray_fig_plt(None, nrows=1, ncols=2, sharex=True, sharey=False, squeeze=False)
        for irow, y in enumerate(("Gamma_qp_gap", "X_qp_gap")):
            ax = ax_mat[0, irow]
            kpt = y.split("_")[0]
            df.plot.scatter(x='ntau', y=y, c="cosft_duality_error",
                            colormap='viridis', title=f"kpt: {kpt}, {label}", ax=ax)
        plt.tight_layout()
        fig.savefig(f"{system}.png")
        plt.show()
        #sns.lineplot(x="ntau", y="Gamma_qp_gap", data=df)



if __name__ == "__main__":

    filepath = os.path.abspath(sys.argv[1])
    plot_tau_convergence(filepath)
    sys.exit(0)

    # Get all directories with output data.
    all_dirs = [p for p in os.listdir(".") if p.endswith("_888")]

    df_list, info_list = [], []
    for d in all_dirs:
        df, info = gaps_vs_ntau(os.path.join(d, "GWR", "run.abo"))
        df_list.append(df)
        info_list.append(info)
        #df.to_excel("foo.xlsx")

    #for d in all_dirs:
    #    df_list.append(gaps_gwr_ac_ppm_df(d))
    #    df = pd.concat(df_list)

    fontsize = 8
    ncols = 2
    ax_mat, fig, plt = get_axarray_fig_plt(None, nrows=len(df_list), ncols=ncols,
                                           sharex=True, sharey=False, squeeze=False)

    for irow, (df, info) in enumerate(zip(df_list, info_list)):
        for icol, y in enumerate(("Gamma_qp_gap", "X_qp_gap")):
            kpt = y.split("_")[0]
            if icol > 0 and ncols > 1: continue
            ax = ax_mat[irow, icol]
            #df.plot.scatter(x='ntau', y=y, c="cosft_duality_error", colormap='viridis', label=f"{info}", ax=ax)
            df.plot.scatter(x='ntau', y=y, colormap='viridis', label=f"{info}", ax=ax)
            ax.set_xlabel("ntau", fontsize=fontsize)
            ax.set_ylabel("", fontsize=fontsize)
            #set_visible(ax, False, "xlabel")

    #df = pd.concat(df_list)
    #sns.lineplot(x="ntau", y="Gamma_qp_gap", data=df, hue="system")
    plt.show()

