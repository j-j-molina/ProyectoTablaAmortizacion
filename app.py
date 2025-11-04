# app.py
from amort.rates import RateSpec, _ppya, tasa_periodica_normalizada
from amort.schedule import generar_tabla_frances, Abono
from amort.utils import export_csv, export_excel

FREQS = ["diaria","semanal","quincenal","mensual","bimestral","trimestral","semestral","anual"]
UNIDADES = ["dias","semanas","quincenas","meses","bimestres","trimestres","semestres","anios"]

def pick(msg, opciones):
    while True:
        v = input(f"{msg} {opciones}: ").strip().lower()
        if v in opciones:
            return v
        print(f"→ Elige una opción válida {opciones}")

def pfloat(msg):
    while True:
        try:
            raw = input(msg + ": ").strip().replace(",", ".")
            return float(raw)
        except:
            print("→ Ingresa un número válido (usa punto o coma para decimales)")

def pint(msg):
    while True:
        try:
            return int(input(msg + ": ").strip())
        except:
            print("→ Ingresa un entero válido")

def si_no(msg):
    return pick(msg, ["si","no"]) == "si"

def n_from_duracion(freq_pago: str, base_dias: int, duracion: float, unidad: str) -> int:
    per_year_pago = _ppya(freq_pago, base_dias)
    per_year_unidad = {
        "dias": float(base_dias),
        "semanas": 52.0,
        "quincenas": 24.0,
        "meses": 12.0,
        "bimestres": 6.0,
        "trimestres": 4.0,
        "semestres": 2.0,
        "anios": 1.0,
    }[unidad]
    n = int(round((duracion / per_year_unidad) * per_year_pago))
    return max(1, n)

def format_miles(df, use_miles: bool):
    if not use_miles:
        return df
    out = df.copy()
    for c in ["Cuota","Interés","Amortización","AbonoExtra","Saldo"]:
        out[c] = out[c].map(lambda x: f"{x:,.2f}")
    return out

def run_once():
    print("\n=== Tabla de Amortización (interactiva) ===\n")

    monto = pfloat("Monto del crédito")
    fecha_inicio = input("Fecha inicio (DD/MM/AAAA) [opcional]: ").strip() or None
    freq_pago = pick("Frecuencia de pago", FREQS)

    # Plazo: N cuotas o duración+unidad
    if si_no("¿Ingresar plazo como N cuotas? (si/no)"):
        n_periodos = pint("Número de cuotas (N)")
    else:
        duracion = pfloat("Duración (cantidad)")
        unidad = pick("Unidad de duración", UNIDADES)
        base_dias = 365 if (freq_pago == "diaria" and si_no("¿Base 365 para diaria? (si/no)")) else 360
        n_periodos = n_from_duracion(freq_pago, base_dias, duracion, unidad)

    # Tasa
    tasa_valor = pfloat("Valor de la tasa (ej. 24.33 para 24.33%)")
    tasa_tipo = pick("Tipo de tasa", ["nominal","efectiva"])
    tasa_cap = pick("Periodo de la tasa (si EA elige 'anual')", FREQS)
    tasa_venc = pick("Vencimiento de la tasa", ["vencida","anticipada"])
    base_dias_tasa = 365 if (tasa_cap == "diaria" and si_no("¿Base 365 para tasa diaria? (si/no)")) else 360

    rs = RateSpec(valor=tasa_valor, tipo=tasa_tipo, capitalizacion=tasa_cap,
                  vencimiento=tasa_venc, base_dias=base_dias_tasa)

    # Transparencia de tasa
    i_p = tasa_periodica_normalizada(rs, freq_pago)
    ppy = _ppya(freq_pago, base_dias_tasa)
    i_ea = (1 + i_p) ** ppy - 1
    print(f"\nTasa por periodo ({freq_pago}) = {i_p*100:.6f}% | EA equivalente = {i_ea*100:.6f}%")
    print(f"Plazo: {n_periodos} cuotas ({freq_pago})")

    # Abonos
    abonos = []
    while si_no("¿Agregar abono extraordinario? (si/no)"):
        per = pint("Periodo (N) en el que se aplica")
        mon = pfloat("Monto del abono")
        tip = pick("Tipo de recálculo", ["plazo","cuota"])
        abonos.append(Abono(periodo=per, monto=mon, tipo=tip))

    # Tabla
    df = generar_tabla_frances(
        principal=monto,
        tasa=rs,
        freq_pago=freq_pago,
        n_periodos=n_periodos,
        fecha_inicio=fecha_inicio,
        abonos=abonos,
    )

    # Formato y preview
    use_miles = si_no("¿Mostrar separador de miles? (si/no)")
    out = format_miles(df, use_miles)
    if si_no("¿Mostrar solo una vista previa de 12 filas? (si/no)"):
        print("\n--- Vista previa (12 filas) ---")
        print(out.head(12).to_string(index=False))
    else:
        print("\n--- Tabla completa ---")
        print(out.to_string(index=False, max_rows=None))

    # Resumen
    tot_interes = float(df["Interés"].sum())
    tot_abonos  = float(df["AbonoExtra"].sum())
    tot_cuotas  = float(df["Cuota"].sum())
    tot_pagado  = tot_cuotas + tot_abonos
    if use_miles:
        print(f"\nResumen → Intereses: {tot_interes:,.2f} | Abonos: {tot_abonos:,.2f} | Total pagado: {tot_pagado:,.2f}")
    else:
        print(f"\nResumen → Intereses: {tot_interes:.2f} | Abonos: {tot_abonos:.2f} | Total pagado: {tot_pagado:.2f}")

    # Export
    if si_no("¿Exportar CSV? (si/no)"):
        export_csv(df, "tabla.csv")
        print("CSV -> tabla.csv")
    if si_no("¿Exportar Excel? (si/no)"):
        export_excel(df, "tabla.xlsx")
        print("Excel -> tabla.xlsx")

def main():
    while True:
        run_once()
        if not si_no("\n¿Correr otro caso? (si/no)"):
            break
    print("\nListo. 👋")

if __name__ == "__main__":
    main()
