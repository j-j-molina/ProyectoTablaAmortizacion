# 📘 Aplicativo de Tabla de Amortización (método francés)

**Autores:** Valentina Rendón Claro · Juan José Molina Zapata  
**Curso/Proyecto:** Aplicativo de Tabla de Amortización en Python

Este proyecto genera una **tabla de amortización completa** (método francés, pagos vencidos) con:

- Conversión de tasas **nominal/efectiva** y **anticipada/vencida** en múltiples frecuencias: `diaria`, `semanal`, `quincenal`, `mensual`, `bimestral`, `trimestral`, `semestral`, `anual`.
- Cálculo correcto de la **tasa equivalente al periodo de pago** (normalizada a **vencida**).
- **Abonos extraordinarios** (programados o ad-hoc) con dos modalidades de recálculo:
  1) **Reducir plazo** (mantiene la cuota).  
  2) **Recalcular cuota** (mantiene el plazo restante).
- **Interfaz CLI** (flags) y **modo interactivo** tipo formulario en consola.
- **Exportación** a CSV/Excel.
- **Pruebas** que validan conversiones, cierre de tabla y abonos.

---

## ✅ Cobertura de la rúbrica

**1) Exactitud financiera (30%)**  
- Conversión explícita **nominal↔efectiva** y **anticipada↔vencida** para **todas las frecuencias**.  
- La tabla cierra con **saldo final = 0.00** (se fuerza a 0 si |saldo| < 0.01).  
- Validación de **cuota que amortiza** (error si amortización ≤ 0).  
- Impresión de **tasa por periodo** y **EA equivalente**.

**2) Funcionalidad: método y abonos (25%)**  
- Método **francés** operativo.  
- **Abonos** por periodo `N`, con recálculo de **plazo** o de **cuota**.

**3) Entradas y uso (UI/CLI) (15%)**  
- Entradas claras: **monto**, **tasa** (valor/tipo/capitalización/vencimiento/base), **frecuencia de pago**, **plazo por N cuotas** o **duración+unidad**, **fecha de inicio**, **abonos**.  
- CLI con flags útiles (`--miles`, `--preview`, `--export_*`).  
- **App interactiva** `app.py`.

**4) Código en Python (15%)**  
- Arquitectura modular: `amort/rates.py` (tasas), `amort/schedule.py` (tabla/abonos), `amort/utils.py` (export), `cli.py`, `app.py`.  
- Manejo de errores y validaciones.

**5) Pruebas y README (15%)**  
- `tests/test_core.py` cubre equivalencias de tasa, cierre de tabla y abonos (plazo/cuota).  
- Este README documenta uso, fórmulas y supuestos.

---

## 🛠️ Instalación

> Recomendado: Python **3.11/3.12** (3.13 funciona si hay wheels de `pandas` disponibles).

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# Windows: .venv\Scripts\activate

python -m pip install -U pip setuptools wheel
pip install -r requirements.txt
```

---

## 🚀 Uso rápido

### A) Modo interactivo (sin flags)

```bash
python app.py
```

- Pide todo como formulario: **N cuotas** o **duración+unidad**, tasa (tipo/capitalización/vencimiento), **abonos**, etc.  
- Muestra tabla completa o preview, **resumen** y permite exportar CSV/XLSX.

### B) CLI con flags

**Parámetros principales**

- **Tasa**:  
  `--tasa_valor` (porcentaje, p. ej. `24.33`) · `--tasa_tipo {nominal,efectiva}` ·  
  `--tasa_cap {diaria,semanal,quincenal,mensual,bimestral,trimestral,semestral,anual}` ·  
  `--tasa_venc {vencida,anticipada}` · `--base_dias {360,365}` (afecta **diaria**)

- **Plazo**:  
  `--n_periodos N` **o** `--duracion X --duracion_unidad {dias,semanas,quincenas,meses,bimestres,trimestres,semestres,anios}`  
  (la duración se convierte a **N** según la **frecuencia de pago**)

- **Frecuencia de pago**:  
  `--frecuencia {diaria,semanal,quincenal,mensual,bimestral,trimestral,semestral,anual}`

- **Fecha de inicio**:  
  `--fecha_inicio DD/MM/AAAA` (opcional; genera columna **Fecha**)

- **Abonos** (JSON):  
  `--abonos_json '[{"periodo":6,"monto":200000,"tipo":"plazo"},{"periodo":12,"monto":150000,"tipo":"cuota"}]'`

- **Salida/UX**:  
  `--miles` (separador de miles) · `--preview N` (0 = todas) · `--export_csv archivo.csv` · `--export_xlsx archivo.xlsx`

**Ejemplos**

```bash
# 1) EA 24.33%, pagos mensuales, 24 cuotas (con miles y fechas)
python cli.py --monto 7000000 --tasa_valor 24.33 --tasa_tipo efectiva --tasa_cap anual \
  --tasa_venc vencida --frecuencia mensual --n_periodos 24 \
  --fecha_inicio 01/01/2025 --miles

# 2) Efectiva mensual 1.74%, 24 meses (duración+unidad)
python cli.py --monto 7000000 --tasa_valor 1.74 --tasa_tipo efectiva --tasa_cap mensual \
  --tasa_venc vencida --frecuencia mensual --duracion 24 --duracion_unidad meses \
  --fecha_inicio 15/10/2025 --miles

# 3) Nominal 24% cap. mensual (~2%/mes), 2 trimestres = 6 cuotas
python cli.py --monto 7000000 --tasa_valor 24 --tasa_tipo nominal --tasa_cap mensual \
  --tasa_venc vencida --frecuencia mensual --duracion 2 --duracion_unidad trimestres \
  --fecha_inicio 01/01/2025 --miles
```

---

## 🧩 Estructura

```text
amort/
  rates.py       # Conversión de tasas y normalización a vencida (periodo de pago)
  schedule.py    # Tabla método francés + abonos (reducir plazo o cuota) — SOLO por n_periodos
  utils.py       # export_csv, export_excel
cli.py           # CLI completa (flags)
app.py           # Modo interactivo (formulario en consola)
tests/
  test_core.py   # Pruebas base (equivalencias, cierre, abonos)
requirements.txt
```

---

## 🧮 Fórmulas clave

```text
# Nominal j con m capitalizaciones/año → Efectiva Anual
i_EA = (1 + j/m)^m - 1

# Efectiva Anual (i_EA) → Efectiva por periodo (p pagos/año)
i_p  = (1 + i_EA)^(1/p) - 1

# Efectiva de ref. (i_ref, p_ref) → periodo objetivo p
i_p  = (1 + i_ref)^(p_ref/p) - 1

# Anticipada ↔ Vencida (mismo periodo)
i_v = i_a / (1 - i_a)
i_a = i_v / (1 + i_v)

# Cuota – método francés (vencida)
C = P * [ i * (1+i)^n / ((1+i)^n - 1) ]

# Nota: todas las tasas se normalizan a "vencida por el periodo de pago" antes del cálculo.
```

---

## 🧪 Pruebas

```bash
# instalar pytest (si no lo tienes)
pip install pytest

# ejecutar
pytest -q
```

**Cubre:** equivalencias de tasas, cierre de tabla (saldo ~ 0), abonos que reducen **plazo** y que recalculan **cuota**.

---

## 📌 Supuestos y decisiones

- El **plazo** se trabaja por **N cuotas**. Alternativamente, se acepta **duración+unidad** y se convierte a N según la **frecuencia de pago**.  
- **Fechas**: para frecuencias mensuales/bimestrales/… se avanza por meses (si el día no existe, se ajusta al fin de mes). Para diaria/semanal/quincenal, avance por días (base 360 por defecto; 365 opcional).  
- **Redondeo**: impresión a 2 decimales; si |saldo final| < 0.01 se presenta como 0.00.  
- Validación de **amortización positiva**; en caso contrario se notifica al usuario.

---

## 🧾 Licencia

Uso académico. Autores: **Valentina Rendón Claro** y **Juan José Molina Zapata**.
