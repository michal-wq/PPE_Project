import glob
import os
import pandas as pd
import numpy as np

def unsplit(pfad):
    files = glob.glob(os.path.join(pfad, '*.csv'))
    df_liste = []

    for datei in files:
        temp_df = pd.read_csv(datei)
        df_liste.append(temp_df)

    ret_df = pd.concat(df_liste, ignore_index=True)
    return ret_df