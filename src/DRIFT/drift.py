import os
from pathlib import Path
import pandas as pd
from tqdm import tqdm

NAMES = ["vx", "evx", "vy", "evy", "az", "eaz", "vh", "evh", "vz", "evz"]


def load_export(infile: str) -> pd.DataFrame:
    """
    Lê arquivo de drift (DVL).
    Vz: vertical (positivo para cima)
    Vx: meridional (positivo para norte)
    Vy: zonal (positivo para leste)
    """
    df = pd.read_csv(
        infile,
        sep=r"\s+",
        header=None,
        engine="python",
    )

    # candidatos de colunas (data, hora) e quais colunas remover
    # (mantém seu comportamento original)
    candidates = [
        # caso 1: usa col 5 e 7, remove 0..7 e 18..22
        (5, 7, list(range(8)) + list(range(18, 23))),
        # caso 2: usa col 6 e 8, remove 0..8 e 19..23
        (6, 8, list(range(9)) + list(range(19, 24))),
    ]

    idx = None
    drop_cols = None

    for c_date, c_time, drops in candidates:
        if max(c_date, c_time) < df.shape[1]:
            dt_str = df[c_date].astype(str) + " " + df[c_time].astype(str)
            idx_try = pd.to_datetime(dt_str, errors="coerce")
            if idx_try.notna().any():
                idx = idx_try
                drop_cols = [c for c in drops if c < df.shape[1]]
                break

    if idx is None or drop_cols is None:
        raise ValueError(f"Não foi possível identificar colunas de data/hora em: {infile}")

    df = df.drop(columns=drop_cols).copy()
    df.index = idx
    df.index.name = "time"

    # garante que temos 10 colunas após o drop
    if df.shape[1] < len(NAMES):
        raise ValueError(f"Colunas insuficientes após limpeza em {infile}: {df.shape[1]}")

    df = df.iloc[:, :len(NAMES)]
    df.columns = NAMES

    # limpeza final
    df = df.sort_index()
    df = df[~df.index.isna()]
    df = df[~df.index.duplicated(keep="first")]

    return df


def process_day(folder: str, ext: str = "DVL") -> pd.DataFrame:
    folder = Path(folder)
    files = sorted(folder.glob(f"*.{ext}")) if not ext.startswith(".") else sorted(folder.glob(f"*{ext}"))

    if not tqdm(files):
        return pd.DataFrame(columns=NAMES)

    out = []
    for fn in files:
        out.append(load_export(str(fn)))

    df = pd.concat(out).sort_index()
    return df


def process_year(
        main_path: str, 
        ext: str = "DVL", 
        verbose: bool = True
        ) -> pd.DataFrame:
    main = Path(main_path)
    if not main.exists():
        raise FileNotFoundError(f"Pasta não existe: {main_path}")

    folders = sorted([p for p in main.iterdir() if p.is_dir()])

    out = []
    failed = []

    for folder in tqdm(folders, desc=f"Processing {main.name}"):
        try:
            df_day = process_day(str(folder), ext=ext)
            if not df_day.empty:
                out.append(df_day)
        except Exception as e:
            failed.append((folder.name, repr(e)))
            if verbose:
                print(f"[SKIP] {folder.name}: {e}")
            continue

    if not out:
        df = pd.DataFrame(columns=NAMES)
    else:
        df = pd.concat(out).sort_index()

    df.attrs["failed_days"] = failed
    return df

def process_drf():
    folder = 'F:\\database\\drift\\'
    
    files = os.listdir(folder)
    out = []
    for fn in tqdm(files):
        yy = fn.split('_')[1][:4]
        if yy == '2023':
            out.append(load_export(folder + fn))
    
    df = pd.concat(out)
    
    df.to_csv('2023') 
