
# amort/rates.py
# Conversión de tasas: nominal ↔ efectiva, anticipada ↔ vencida, y equivalencias entre frecuencias.
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Dict

Freq = Literal["diaria","semanal","quincenal","mensual","bimestral","trimestral","semestral","anual"]
TasaTipo = Literal["nominal","efectiva"]
Vencimiento = Literal["vencida","anticipada"]
BaseDias = Literal[360,365]

PERIODOS_POR_ANO: Dict[Freq, float] = {
    "diaria": 360.0,      # por defecto 360; si base 365, se reescala
    "semanal": 52.0,
    "quincenal": 24.0,
    "mensual": 12.0,
    "bimestral": 6.0,
    "trimestral": 4.0,
    "semestral": 2.0,
    "anual": 1.0,
}

def _ppya(freq: Freq, base_dias: BaseDias) -> float:
    """Periodos por año efectivos considerando base de días para diaria."""
    if freq == "diaria":
        return float(base_dias)
    return PERIODOS_POR_ANO[freq]

@dataclass
class RateSpec:
    valor: float  # p.ej. 18.0 -> 18%
    tipo: TasaTipo  # "nominal" o "efectiva"
    capitalizacion: Freq  # frecuencia de capitalización si nominal; si efectiva, referencia del periodo de la tasa
    vencimiento: Vencimiento = "vencida"  # 'anticipada' descuenta al inicio
    base_dias: BaseDias = 360

    def as_decimal(self) -> float:
        return self.valor / 100.0

def nominal_to_effective_periodic(j: float, m_comp: float, p_target: float) -> float:
    """
    j: tasa nominal anual (decimal) con m_comp capitalizaciones por año.
    p_target: pagos por año deseados.
    Retorna i_p (efectiva por periodo de pago) como decimal.
    """
    i_eff_anual = (1.0 + j / m_comp) ** m_comp - 1.0
    return (1.0 + i_eff_anual) ** (1.0 / p_target) - 1.0

def effective_equivalent(i_eff_ref: float, p_ref: float, p_target: float) -> float:
    """Convierte i_eff_ref (efectiva por periodo ref) a i_eff_target (por periodo target)."""
    i_eff_anual = (1.0 + i_eff_ref) ** p_ref - 1.0
    return (1.0 + i_eff_anual) ** (1.0 / p_target) - 1.0

def anticipada_a_vencida(i: float) -> float:
    """Convierte tasa anticipada por periodo a vencida por el mismo periodo."""
    return i / (1.0 - i)

def vencida_a_anticipada(i: float) -> float:
    """Convierte tasa vencida por periodo a anticipada por el mismo periodo."""
    return i / (1.0 + i)

def tasa_periodica_normalizada(tasa: RateSpec, freq_pago: Freq) -> float:
    """
    Retorna la tasa efectiva por periodo de pago (vencida), equivalente a la especificación dada.
    Si el dato de entrada era anticipado, se convierte a vencida para el mismo periodo.
    """
    p_target = _ppya(freq_pago, tasa.base_dias)
    if tasa.tipo == "nominal":
        m_comp = _ppya(tasa.capitalizacion, tasa.base_dias)
        i_v = nominal_to_effective_periodic(tasa.as_decimal(), m_comp, p_target)
    else:
        p_ref = _ppya(tasa.capitalizacion, tasa.base_dias)
        i_v = effective_equivalent(tasa.as_decimal(), p_ref, p_target)

    if tasa.vencimiento == "anticipada":
        # construir la tasa anticipada equivalente del mismo periodo y normalizar a vencida
        i_a = vencida_a_anticipada(i_v)
        i_v = anticipada_a_vencida(i_a)
    return i_v
