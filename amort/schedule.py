# amort/schedule.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Literal, Optional, Dict
import pandas as pd
from amort.rates import RateSpec, tasa_periodica_normalizada, _ppya, Freq

Recalculo = Literal["cuota","plazo"]

@dataclass
class Abono:
    periodo: int
    monto: float
    tipo: Recalculo = "plazo"
    descripcion: str = ""

def cuota_frances(saldo: float, i: float, n: int) -> float:
    if n <= 0:
        raise ValueError("n (número de periodos) debe ser > 0")
    if i == 0:
        return saldo / n
    return saldo * (i * (1 + i) ** n) / ((1 + i) ** n - 1)

def generar_tabla_frances(
    principal: float,
    tasa: RateSpec,
    freq_pago: Freq,
    n_periodos: int,
    fecha_inicio: Optional[str] = None,   # "DD/MM/YYYY"
    abonos: Optional[List[Abono]] = None,
    redondeo: int = 2,
) -> pd.DataFrame:
    """
    Tabla método francés (vencida) con abonos.
    - Entrada de plazo SOLO como n_periodos (cuotas).
    """
    if n_periodos is None or n_periodos <= 0:
        raise ValueError("Debes proporcionar n_periodos > 0")

    abonos = abonos or []
    i_p = tasa_periodica_normalizada(tasa, freq_pago)
    saldo = float(principal)
    n_total = int(n_periodos)
    cuota = cuota_frances(saldo, i_p, n_total)

    def _fecha(k: int) -> Optional[str]:
        if not fecha_inicio:
            return None
        import datetime as dt
        d = dt.datetime.strptime(fecha_inicio, "%d/%m/%Y")
        mapa_meses = {"mensual":1,"bimestral":2,"trimestral":3,"semestral":6,"anual":12}
        if freq_pago in mapa_meses:
            m = mapa_meses[freq_pago]*k
            year = d.year + (d.month - 1 + m) // 12
            month = (d.month - 1 + m) % 12 + 1
            day = min(d.day, 28)
            return dt.datetime(year, month, day).strftime("%d/%m/%Y")
        dias = {"diaria":1,"semanal":7,"quincenal":15}.get(freq_pago, 30)
        return (d + dt.timedelta(days=dias*k)).strftime("%d/%m/%Y")

    abonos_idx: Dict[int, List[Abono]] = {}
    for a in abonos:
        abonos_idx.setdefault(a.periodo, []).append(a)

    filas = []
    k = 0
    while saldo > 1e-8 and k < n_total + 6000:
        k += 1
        interes = saldo * i_p
        amort = cuota - interes
        if amort <= 0:
            raise ValueError("La cuota no amortiza capital; revisa tasa o N.")
        nuevo_saldo = max(saldo - amort, 0.0)

        # Abonos en el periodo k
        abono_total = 0.0
        if k in abonos_idx and nuevo_saldo > 0:
            for a in abonos_idx[k]:
                monto = min(a.monto, nuevo_saldo)
                nuevo_saldo -= monto
                abono_total += monto
            if nuevo_saldo > 0:
                if any(a.tipo == "cuota" for a in abonos_idx[k]):
                    n_rem = max(n_total - k, 1)
                    cuota = cuota_frances(nuevo_saldo, i_p, n_rem)
                else:
                    # Mantener cuota, reducir plazo
                    saldo_tmp = nuevo_saldo
                    n_rem_estim = 0
                    while saldo_tmp > 1e-8 and n_rem_estim < 10000:
                        n_rem_estim += 1
                        interes_tmp = saldo_tmp * i_p
                        amort_tmp = cuota - interes_tmp
                        if amort_tmp <= 0:
                            n_rem = max(n_total - k, 1)
                            cuota = cuota_frances(nuevo_saldo, i_p, n_rem)
                            n_rem_estim = n_rem
                            break
                        saldo_tmp -= amort_tmp
                    n_total = k + n_rem_estim

        filas.append({
            "Periodo": k,
            "Fecha": _fecha(k) if fecha_inicio else None,
            "Cuota": round(cuota, redondeo),
            "Interés": round(interes, redondeo),
            "Amortización": round(cuota - interes, redondeo),
            "AbonoExtra": round(abono_total, redondeo),
            "Saldo": round(nuevo_saldo, redondeo),
        })
        saldo = nuevo_saldo

    df = pd.DataFrame(filas)
    if not df.empty and abs(df.iloc[-1]["Saldo"]) < 0.01:
        df.iloc[-1, df.columns.get_loc("Saldo")] = 0.0
    return df
