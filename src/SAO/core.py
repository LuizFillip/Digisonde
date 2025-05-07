import re
import pandas as pd 
import datetime as dt 



def dps_system_preface_parameters(line):
    # Define os campos com suas posições e descrições
    fields = [
        (1, 2, "Version Indicator"),
        (3, 6, "Year"),
        (7, 9, "Day of Year"),
        (10, 11, "Month"),
        (12, 13, "Day of Month"),
        (14, 15, "Hour (UT)"),
        (16, 17, "Minutes"),
        (18, 19, "Seconds"),
        (20, 22, "Receiver Station ID"),
        (23, 25, "Transmitter Station ID"),
        (26, 26, "DPS Schedule"),
        (27, 27, "DPS Program"),
        (28, 32, "Start Frequency (kHz)"),
        (33, 36, "Coarse Frequency Step"),
        (37, 41, "Stop Frequency (kHz)"),
        (42, 45, "Fine Frequency Step"),
        (46, 46, "Multiplexing"),
        (47, 47, "Number of DPS Small Steps"),
        (48, 49, "DPS Phase Code"),
        (50, 50, "Alternative Antenna Setup"),
        (51, 51, "Antenna Options"),
        (52, 52, "Total FFT Samples"),
        (53, 53, "Radio Silent Mode"),
        (54, 56, "Pulse Repetition Rate"),
        (57, 60, "Range Start"),
        (61, 61, "Range Increment"),
        (62, 65, "Number of Ranges"),
        (66, 69, "Scan Delay (hex)"),
        (70, 70, "Base Gain"),
        (71, 71, "Freq Search Enabled"),
        (72, 72, "Operating Mode"),
        (73, 73, "ARTIST Enabled"),
        (74, 74, "Data Format"),
        (75, 75, "Printer Selection"),
        (76, 77, "Ionogram FTP Threshold"),
        (78, 78, "High Interference Condition"),
    ]

    # Armazena os resultados
    parsed = {}

    for start, end, description in fields:
        # Corrige índice Python (começa do 0)
        value = line[start - 1:end]
        parsed[description] = value

    # Convertendo campo hexadecimal específico como exemplo
    if "Scan Delay (hex)" in parsed:
        hex_value = parsed["Scan Delay (hex)"]
        try:
            parsed["Scan Delay (decoded)"] = int(hex_value, 16)
        except ValueError:
            parsed["Scan Delay (decoded)"] = None

    return parsed

def extract_datetime(parsed):
    try:
        year = int(parsed["Year"])
        day_of_year = int(parsed["Day of Year"])
        hour = int(parsed["Hour (UT)"])
        minute = int(parsed["Minutes"])
        second = int(parsed["Seconds"])

        # Cria a data base a partir do dia do ano
        dn = dt.datetime(year, 1, 1) + dt.timedelta(days=day_of_year - 1)
        # Adiciona hora, minuto e segundo
        dn = dn.replace(hour=hour, minute=minute, second=second)

        return dn
    except Exception as e:
        print("Erro ao construir datetime:", e)
        return None

def scaled_characteristics(lines):
    
    col_names = [
       "foF2", "foF1", "M(D)", "MUF(D)", 
       "fmin", "foEs", "fminF", "fminE", 
       "foE", "fxI", "h'F", "h'F2", "h'E", 
       "h'Es", "zmE",
       "yE", "QF", "QE", "DownF", 
       "DownE", "DownEs",
       "FF", "FE", "D", "fMUF", "h'(fMUF)", 
       "delta_foF2", "foEp", "f(h'F)", "f(h'F2)",
       "foF1p", "hF2_peak", "hF1_peak", "zhalfNm", 
       "foF2p", "fminEs", "yF2", "yF1", "TEC",
       "ScaleHeightF2", "B0", "B1", "D1", "foEa",
       "h'Ea", "foP", "h'P", "fbEs", "TypeEs"
    ]


    table = ''.join(lines).replace('\n', '')
    
    out = []
    for ln in table.split():
    
        if '999' in ln:
            s = re.findall(r'\d+\.\d{3}', ln)
            out.extend(s)
        else:
            out.append(ln)

    return pd.DataFrame([out], columns=col_names)


def fn2dn(fn):
    date_str = fn.split('_')[-2]
    fmt = '%Y%m%d%H%M%S'
    return dt.datetime.strptime(date_str, fmt)


def SAO_data(infile):
    
    lines = open(infile).readlines()
    
    df = scaled_characteristics(lines[5:9])
    
    # parsed = dps_system_preface_parameters(lines[4])
    
    # df.index = [extract_datetime(parsed)]
    
    return df 


# for month_path in root.iterdir():
#     if month_path.is_dir():
#         for day_path in month_path.iterdir():
#             if day_path.is_dir():
#                 for file_path in day_path.iterdir():
#                     if file_path.is_file():
#                         print(file_path)
#                         # out.append(SAO_data(file_path))
                        

from tqdm import tqdm 

def run_in_root():
    
    root = 'E:\\database\\CAS_ionossonda\\2025\\2025\\'
    import os 
    out = []
    for month in os.listdir(root):
        
        month_path = f'{root}{month}'
        for day in tqdm(os.listdir(month_path), month):
            
            day_path = f'{root}{month}\\{day}'
            
            for file in os.listdir(day_path):
                
                infile  = f'{day_path}\\{file}'
                
                if file.endswith('SAO'):
                    try:
                        df = SAO_data(infile) 
                        df.index = [fn2dn(file)]
                        out.append(df)
                    except:
                        # print(file)
                        continue
                    
    
    ds = pd.concat(out)
    
    
    ds.to_csv('digisonde/src/SAO/test') 
    
# run_in_root()
