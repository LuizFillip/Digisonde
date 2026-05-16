 
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple
import numpy as np
import pandas as pd

def find_header(
        infile: str, 
        header: str = 'yyyy.MM.dd'
        ) -> tuple:
    
    """Function for find the header
    and the data section"""
    
    with open(infile) as f:
        data = [line.strip() for line in f.readlines()]
    
    count = 0
    for num in range(len(data)):
        if (header) in data[num]:
            break
        else:
            count += 1
            
    return data[1].split(), data[count + 2:]



def structure_the_data(data: list) -> np.array:
    
    """
    Function for organize the data 
    (get from find_header function)
    in array format
    """
    out_second = []
    for first in range(len(data)):
        
        out_first = []
        out_second.append(out_first)
        
        for second in data[first].split():
            
            rules = [second != "/", 
                      second != '//',
                      second != '---']
            
            if all(rules):
                out_first.append(second)
            else:
                out_first.append(np.nan)
    
    return np.array(out_second)

MISSING_TOKENS = {"/", "//", "---"}
 


def freq_fixed(infile: str | Path) -> pd.DataFrame:
    """
    Read the frequency file and return a DataFrame with datetime index.

    Expected columns include:
    - yyyy.MM.dd
    - HH:mm:ss
    - (DDD)
    - frequency columns

    Parameters
    ----------
    infile : str or Path
        Path to input file.

    Returns
    -------
    pd.DataFrame
        DataFrame indexed by datetime, with numeric frequency columns.
    """
    columns, data = find_header(infile)
    arr = structure_the_data(data)

    df = pd.DataFrame(arr, columns=columns)

    df = df.rename(columns={
        "yyyy.MM.dd": "date",
        "HH:mm:ss": "time",
        "(DDD)": "doy",
    })

    df.index = pd.to_datetime(df["date"] + " " + df["time"], errors="coerce")

    # Identifica colunas de frequência (todas após as 3 primeiras)
    freq_cols = df.columns[3:]

    # Mapeia nomes tipo "1.0" -> 1
    rename_map = {}
    for col in freq_cols:
        try:
            rename_map[col] = int(float(col))
        except ValueError:
            rename_map[col] = col

    df = df.rename(columns=rename_map)

    # Converte apenas colunas de frequência para numérico
    converted_freq_cols = [rename_map[col] for col in freq_cols]
    df[converted_freq_cols] = df[converted_freq_cols].apply(pd.to_numeric, errors="coerce")

    # Remove colunas auxiliares, preservando "time" se você quiser inspecionar depois
    df = df.drop(columns=["date", "doy"])

    return df
 