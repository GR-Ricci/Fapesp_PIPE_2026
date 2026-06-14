def _extrair_nomes(serie):
    return serie.str.replace(',', ';').str.split(';').explode().str.strip()