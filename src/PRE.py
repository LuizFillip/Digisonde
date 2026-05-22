import pandas as pd
import numpy as np
import datetime as dt
import digisonde as dg 
import GEO as gg 
import os 
from tqdm import tqdm 
import base as b 

def find_outliers_mean_std(
        data, col= 'vz_max', 
        threshold=2):
    """
    Encontra valores discrepantes 
    usando média e desvio-padrão.

    Critério:
        |x - média| >= threshold * std

    Parameters
    ----------
    data : pd.Series ou pd.DataFrame
    col : str, opcional
        Nome da coluna, caso data seja DataFrame.
    threshold : float
        Número de desvios-padrão. Ex: 3.

    Returns
    -------
    outliers : pd.DataFrame
        Dados discrepantes com valor, z-score, média e std.
    """
    
    if isinstance(data, pd.DataFrame):
        if col is None:
            raise ValueError("Informe 'col' quando data for DataFrame.")
        s = data[col].copy()
    else:
        s = data.copy()

    mean = s.mean(skipna=True)
    std = s.std(skipna=True)

    z = (s - mean) / std

    mask = np.abs(z) >= threshold

 
    return pd.DataFrame({
        'value': s[mask],
        'zscore': z[mask],
        'mean': mean,
        'std': std,
        'threshold_upper': mean + threshold * std,
        'threshold_lower': mean - threshold * std
    })
# 

def filter_timedusk(ds, dusk, window_min=30):
    

    t0 = dusk - pd.Timedelta(minutes = window_min)
    t1 = dusk + pd.Timedelta(minutes = window_min)

    return ds.loc[(ds.index >= t0) &  (ds.index <= t1)].copy()

def extract_vz_around_dusk(df, window_min=30):
    """
    Extrai, para cada dia:
    - dusk
    - vz máximo em ±window_min ao redor do dusk
    - horário do máximo
    - vz médio e mediano na janela
    """

    out = []

    for day in np.unique(df.index.date):
        dn = pd.Timestamp(day)

        ds = df.loc[df.index.date == dn.date()].copy()
        if ds.empty:
            continue

        # dusk do dia
        
        
        dusk = pd.Timestamp(gg.terminator(dn))
        dw = filter_timedusk(ds, dusk, window_min)
        
        if dw.empty or dw['vz'].dropna().empty:
            out.append({
                'date': dn,
                'dusk': dusk,
                'vz_max': np.nan,
                'time_vz_max': pd.NaT,
                'vz_mean': np.nan,
                
            })
            continue

        idxmax = dw['vz'].idxmax()

        out.append({
            'date': dn,
            'dusk': dusk,
            'vz_max': dw.loc[idxmax, 'vz'],
            'time_vz_max': idxmax,
            'vz_mean': dw['vz'].mean(), 
        })

    out = pd.DataFrame(out).set_index('date')
    return out

 
def remove_outliers_std(df, col, n_std=3):
    
    def filt(x):
        mu = x.mean()
        sigma = x.std()
        return x[(x >= mu - n_std*sigma) &
                 (x <= mu + n_std*sigma)]
    freq = df.index.to_period('M')
    return df.groupby(freq)[col].transform(filt).dropna()

def compute_vz_from_contour(
        infile, 
        low_freq = 2, 
        high_freq = 7                
        ):
    
    df = dg.freq_fixed(infile)
     
    df = df.between_time('20:00', '23:50').copy().interpolate()
 
    df['time'] = b.time2float(df.index)
 
    df['so'] = df[list(range(low_freq, high_freq + 1))].mean(axis=1)
    
    df['vz'] = (df['so'].diff() / df['time'].diff()) / 3.6
    df['vz'] = b.smooth2(df['vz'], 2)
    
    return df

def run_pre_all_years(
        window_min = 60, 
        low_freq = 4, 
        high_freq = 8
        ):
    
    
    out = []
    desc = 'Computing PRE from freqs'
    for year in tqdm(range(2013, 2025), desc):
        infile = f'SuppressionEPBs/data/freqs/{year}'
        df = compute_vz_from_contour(
            infile, 
            low_freq = low_freq, 
            high_freq = high_freq
            )
            
        out.append(
            extract_vz_around_dusk(
                df, 
                window_min = window_min
                )
            )
     
    df = pd.concat(out) 
    save_in = 'SuppressionEPBs/data/'
    filename = f'pre_sao_luis_{window_min}min_{low_freq}{high_freq - 1}'
    df.to_csv(save_in + filename)
    
    return df
 