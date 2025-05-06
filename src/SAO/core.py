import re
import pandas as pd 


fn = "E:\\ionogram\\2015\\20151220CA\\CAJ2M_2015354101000.SAO"
fn = "E:\\database\\CAS_ionossonda\\2025\\2025\\01\\28\\OCGD_IDIS01_IOPA_L2_STP_20250128234500_V01.00.SAO"

lines = open(fn).readlines()


def scaled_characteristics(f):
    
    col_names = [
       "foF2", "foF1", "M(D)", "MUF(D)", 
       "fmin", "foEs", "fminF", "fminE", "foE",
       "fxI", "h'F", "h'F2", "h'E", "h'Es", "zmE",
       "yE", "QF", "QE", "DownF", "DownE", "DownEs",
       "FF", "FE", "D", "fMUF", "h'(fMUF)", 
       "delta_foF2", "foEp", "f(h'F)", "f(h'F2)",
       "foF1p", "hF2_peak", "hF1_peak", "zhalfNm", 
       "foF2p", "fminEs", "yF2", "yF1", "TEC",
       "ScaleHeightF2", "B0", "B1", "D1", "foEa",
       "h'Ea", "foP", "h'P", "fbEs", "TypeEs"
    ]


    table = ''.join(f[5:9]).replace('\n', '')
    
    out = []
    for ln in table.split():
    
        if '999' in ln:
            s = re.findall(r'\d+\.\d{3}', ln)
            out.extend(s)
        else:
            out.append(ln)
            
            
    return pd.DataFrame([out], columns=col_names)

# df = scaled_characteristics(f)

def parse_sao_line(line):
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



parsed_data = parse_sao_line(lines[4])

parsed_data

