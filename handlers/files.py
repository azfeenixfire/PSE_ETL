import pandas as pd
import glob
import os



def import_files(folder_path):
    pse_files = glob.glob(folder_path)

    data = []  # pd.concat takes a list of dataframes as an agrument
    for csv in pse_files:
        #low mem set to false due to amount of columns, DT is unreliable, must convert later
        frame = pd.read_csv(csv, low_memory=False)
        frame['filename'] = os.path.basename(csv)
        data.append(frame)
    full_df = pd.concat(data, ignore_index=True)
    return full_df



