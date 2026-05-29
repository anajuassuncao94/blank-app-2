from datetime import time


def texto_obrigatorio(valor: str) -> bool:
    return bool(valor and valor.strip())


def horario_valido(inicio: time, fim: time) -> bool:
    return fim > inicio
