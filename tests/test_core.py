
# tests/test_core.py
import math
from amort.rates import RateSpec, tasa_periodica_normalizada
from amort.schedule import generar_tabla_frances, Abono

def test_equivalencias_basicas():
    rs = RateSpec(24.0, "nominal", "mensual", "vencida")
    i_m = tasa_periodica_normalizada(rs, "mensual")
    assert abs(i_m - 0.02) < 1e-6

def test_efectiva_a_trimestral():
    rs = RateSpec(26.824, "efectiva", "anual", "vencida")
    i_t = tasa_periodica_normalizada(rs, "trimestral")
    assert abs(i_t - 0.06) < 1e-3

def test_anticipada_equivalente():
    rs = RateSpec(2.0, "efectiva", "mensual", "anticipada")
    i_m = tasa_periodica_normalizada(rs, "mensual")
    assert abs(i_m - (0.02/(1-0.02))) < 1e-9

def test_tabla_cierra_sin_abonos():
    rs = RateSpec(24.0, "nominal", "mensual", "vencida")
    df = generar_tabla_frances(1000000, rs, plazo_en_anios=1, freq_pago="mensual", fecha_inicio="01/01/2025")
    assert abs(float(df.iloc[-1]["Saldo"])) < 1.0

def test_abono_reduce_plazo():
    rs = RateSpec(24.0, "nominal", "mensual", "vencida")
    df = generar_tabla_frances(1000000, rs, 1, "mensual", abonos=[Abono(periodo=6, monto=200000, tipo="plazo")])
    assert len(df) < 12 + 1

def test_abono_recalcula_cuota():
    rs = RateSpec(24.0, "nominal", "mensual", "vencida")
    df = generar_tabla_frances(1000000, rs, 1, "mensual", abonos=[Abono(periodo=6, monto=200000, tipo="cuota")])
    c6 = float(df.loc[df["Periodo"]==6, "Cuota"].values[0])
    c7 = float(df.loc[df["Periodo"]==7, "Cuota"].values[0])
    assert c7 < c6
