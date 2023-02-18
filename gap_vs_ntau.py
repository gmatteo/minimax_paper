#!/usr/bin/env python

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ruamel.yaml import YAML
from pymatgen.util.plotting import add_fig_kwargs, get_ax_fig_plt, get_ax3d_fig_plt, get_axarray_fig_plt

sns.set_theme(style="darkgrid")

GWR_KEYS = ["ntau",  "min_transition_energy_eV", "max_transition_energy_eV", "eratio",
        "ft_max_err_t2w_cos", "ft_max_err_w2t_cos",
        "ft_max_err_t2w_sin", "cosft_duality_error",]

def _get_doc(lines):
    buf = []
    while lines:
        l = lines.pop(0)
        l = l.replace("!Tabular", "")
        if l.startswith( "..."): break
        buf.append(l)

    # default, if not specfied, is 'rt' (round-trip)
    return YAML(typ='safe').load("".join(buf))


def gwr_gaps_vs_ntau(filepath):
    lines = open(filepath, "rt").readlines()
    system = os.path.relpath(os.path.dirname(filepath)).split("_")[0]

    gwr_params = []
    se_docs = [None, None]
    dict_list = []
    count = -1
    while lines:
        line = lines.pop(0)
        if line.startswith("--- !GWR_params"):
            gwr_params = _get_doc(lines)
            count = 0

        if line.startswith("--- !GWR_SelfEnergy_ee"):
            se_docs[count] = _get_doc(lines)
            count += 1

        if count == 2:
            count = 0
            data = {k: gwr_params[k] for k in GWR_KEYS}
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
    df, label = gwr_gaps_vs_ntau(filepath)

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
        #fig.savefig(os.path.join("DATA_GWR", f"{system}.png"))
        plt.show()
        #sns.lineplot(x="ntau", y="Gamma_qp_gap", data=df)


def rpa_vs_ntau(filepath):
    lines = open(filepath, "rt").readlines()
    system = os.path.relpath(os.path.dirname(filepath)).split("_")[0]

    gwr_params = []
    se_docs = [None, None]
    dict_list = []
    count = -1
    magic = "ecut_chi ecut_chi^(-3/2)"

    """
        ecut_chi ecut_chi^(-3/2)     RPA Ec (eV)     RPA Ec (Ha)
  9.60000000E+00  3.36196471E-02 -1.27695639E+01 -4.69272860E-01
  1.02000000E+01  3.06972692E-02 -1.28113087E+01 -4.70806953E-01
  1.08000000E+01  2.81750287E-02 -1.28474220E+01 -4.72134091E-01
  1.14000000E+01  2.59802139E-02 -1.28780283E+01 -4.73258851E-01
  1.20000000E+01  2.40562612E-02 -1.29058990E+01 -4.74283082E-01
              oo               0 -1.32482109E+01 -4.86862814E-01
    """

    while lines:
        line = lines.pop(0)
        if line.startswith("--- !GWR_params"):
            gwr_params = _get_doc(lines)
            count = 0

        if magic in line:
            while lines:
                line = lines.pop(0)
                print("line", line)
                tokens = line.split()
                start = tokens.pop(0)
                if start == "oo":
                    #print(tokens)
                    data = {k: gwr_params[k] for k in GWR_KEYS}
                    data["system"] = system
                    data["rpa_ec_ev"] = float(tokens[1])  # ecrpa
                    #print("ec:", data["rpa_ec_ev"])
                    dict_list.append(data)
                    break

    df = pd.DataFrame(dict_list)
    eratio = df["eratio"][0]
    label = f"system: {system}, eratio: {eratio:.2f}"

    print(df[["ntau", "rpa_ec_ev",] +
             [k for k in df if "_err" in k]
            ])

    return df, label


if __name__ == "__main__":
    fontsize = 8
    filepath = os.path.abspath(sys.argv[1])

    #rpa_vs_ntau(filepath)
    #plot_tau_convergence(filepath)
    #sys.exit(0)

    # Get all directories with output data.
    all_dirs = [p for p in os.listdir(".") if p.endswith("_888")]

    task = "GWR_ntau"
    task = "RPA_ntau"
    df_list, info_list = [], []

    if task ==  "RPA_ntau":
        for d in all_dirs:
            rpa_df, rpa_info = rpa_vs_ntau(os.path.join(d, "RPA", "run.abo"))
            df_list.append(rpa_df)
            info_list.append(rpa_info)
            system = rpa_df["system"][0]
            #rpa_df.to_excel(os.path.join("DATA_RPA", f"{system}.xlsx"))

            ax, fig, plt = get_ax_fig_plt(ax=None)
            rpa_df.plot.scatter(x='ntau', y="rpa_ec_ev", c="cosft_duality_error",
                               colormap='viridis', title=rpa_info, ax=ax)
            plt.tight_layout()
            plt.show()
            #fig.savefig(os.path.join("DATA_RPA", f"{system}.png"))



    if task == "GWR_ntau":
        for d in all_dirs:
            gwr_df, gwr_info = gwr_gaps_vs_ntau(os.path.join(d, "GWR", "run.abo"))
            df_list.append(gwr_df)
            info_list.append(gwr_info)
            system = gwr_df["system"][0]
            #gwr_df.to_excel(os.path.join("DATA_GWR", f"{system}.xlsx")

    sys.exit(0)
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

