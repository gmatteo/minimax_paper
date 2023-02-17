#!/usr/bin/env python

import sys
from ruamel.yaml import YAML
import pandas as pd

def main():

    def get_doc():
        buf = []
        while lines:
            l = lines.pop(0)
            l = l.replace("!Tabular", "")
            if l.startswith( "..."): break
            buf.append(l)

        yaml = YAML(typ='safe')   # default, if not specfied, is 'rt' (round-trip)
        return yaml.load("".join(buf))

    lines = open(sys.argv[1], "rt").readlines()
    gwr_params = []
    se_docs = [None, None]

    dict_list = []
    count = -1
    while lines:
        line = lines.pop(0)
        if line.startswith("--- !GWR_params"):
            gwr_params = get_doc()
            #print(line)
            count = 0

        if line.startswith("--- !GWR_SelfEnergy_ee"):
            se_docs[count] = get_doc()
            count += 1

        if count == 2:
            count = 0
            #print(se_docs)
            keys = ["ntau",  "min_transition_energy_eV", "max_transition_energy_eV", "eratio",
                    "ft_max_err_t2w_cos", "ft_max_err_w2t_cos",
                    "ft_max_err_t2w_sin", "cosft_duality_error",]
            data = {k: gwr_params[k] for k in keys}
            data["Gamma_qp_gap"] = se_docs[0]["QP_gap"]
            data["Gamma_ks_gap"] = se_docs[0]["KS_gap"]
            data["X_qp_gap"] = se_docs[1]["QP_gap"]
            data["X_ks_gap"] = se_docs[1]["KS_gap"]
            dict_list.append(data)

    df = pd.DataFrame(dict_list)
    print(df[["ntau", "Gamma_qp_gap", "X_qp_gap",] + 
             [k for k in keys if "_err" in k]
            ])


if __name__ == "__main__":
    main()
