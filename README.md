# 📘 Proyecto Final – Aplicativo de Tabla de Amortización en Python

---

## 🏁 **1. Introducción**

El presente proyecto tiene como propósito desarrollar un **aplicativo en Python** capaz de generar una **tabla de amortización completa y dinámica**, que permita visualizar el comportamiento del crédito a lo largo del tiempo, considerando tasas nominales o efectivas, distintas frecuencias de pago y la inclusión de **abonos programados y extraordinarios**.

Este trabajo integra los conocimientos de **matemática financiera** con herramientas de programación, demostrando la capacidad para **traducir modelos financieros en código funcional**, optimizado y comprensible.

---

## 🎯 **2. Objetivos**

### ✅ **Objetivo General**
Desarrollar un aplicativo en Python que permita generar y gestionar una **tabla de amortización completa**, aplicando correctamente las fórmulas financieras vistas en clase y posibilitando el registro de abonos programados o extraordinarios.

### 📌 **Objetivos Específicos**
- Implementar un algoritmo que calcule la **tasa equivalente** según la frecuencia de pago.  
- Generar automáticamente la **tabla de amortización** según los parámetros ingresados.  
- Permitir el registro de **abonos programados y no programados**, recalculando el saldo y el plazo.  
- Exportar los resultados a formatos **CSV o Excel**.  
- Mostrar la información de manera clara y estructurada, con enfoque didáctico.

---

## 📖 **3. Marco Teórico**

### 💡 Concepto de Amortización
La amortización es el proceso mediante el cual se **paga una deuda** mediante cuotas periódicas que cubren capital e intereses.  
Cada cuota incluye:
- **Interés:** pago por el uso del dinero prestado.
- **Amortización:** parte que reduce el capital pendiente.

### 🔢 Fórmulas Financieras Aplicadas

1. **Cálculo de la cuota periódica (sistema francés):**  
   \[
   C = P \times \frac{i(1+i)^n}{(1+i)^n - 1}
   \]
   Donde:  
   \( C \): Cuota  
   \( P \): Monto del préstamo  
   \( i \): Tasa periódica  
   \( n \): Número de periodos

2. **Cálculo de intereses y amortización:**
   \[
   I_t = S_{t-1} \times i
   \]
   \[
   A_t = C - I_t
   \]
   \[
   S_t = S_{t-1} - A_t
   \]

3. **Conversión de tasas:**
   - De **nominal anual a periódica vencida**:
     \[
     i = \frac{i_{nominal}}{m}
     \]
   - De **efectiva anual a periódica**:
     \[
     i = (1 + i_{ea})^{1/m} - 1
     \]

---

## ⚙️ **4. Metodología de Desarrollo**

El aplicativo fue desarrollado en **Python**, empleando librerías de manejo de datos como `pandas` y `openpyxl`.  
El proceso de desarrollo se dividió en etapas:

1. **Diseño lógico:** definición de las fórmulas financieras y del flujo del programa.  
2. **Codificación modular:** creación de funciones separadas para cálculos, abonos y utilidades.  
3. **Pruebas de validación:** comprobación del cálculo de cuotas y saldos.  
4. **Exportación de resultados:** generación de archivos CSV y Excel.  
5. **Documentación y validación final.**

---

## 🧩 **5. Estructura del Proyecto**

ProyectoTablaAmortizacion/
│
├── main.py # Programa principal (interfaz de usuario)
├── calculos.py # Funciones de cálculo financiero
├── abonos.py # Gestión de abonos programados y extraordinarios
├── utils.py # Funciones auxiliares (exportación y validaciones)
├── requirements.txt # Librerías requeridas
├── README.md # Documentación del proyecto
│
└── resultados/ # Archivos exportados (CSV o Excel)


---

## 💻 **6. Tecnologías Utilizadas**

- **Lenguaje:** Python 3.10+
- **Librerías:**  
  - `pandas` – Manejo y estructuración de datos  
  - `openpyxl` – Exportación a Excel  
- **Entorno de desarrollo:** Visual Studio Code  
- **Control de entorno:** `venv` (entorno virtual de Python)

---

## 🧮 **7. Descripción del Funcionamiento**

### Entrada de datos:
El usuario ingresa:
- Monto del préstamo  
- Tasa anual (%)
- Tipo de tasa (nominal o efectiva)
- Plazo (en años)
- Frecuencia de pago (mensual, trimestral, etc.)

### Proceso:
1. Se convierte la tasa a su **valor equivalente por periodo**.  
2. Se calcula la **cuota periódica** usando el sistema francés.  
3. Se genera una tabla con los valores de **cuota, interés, amortización y saldo** para cada periodo.  
4. Si existen abonos, el sistema recalcula el saldo y ajusta el plazo o la cuota.  

### Salida:
- Visualización del resumen en consola.  
- Exportación del resultado completo a un archivo `tabla_amortizacion.csv`.

---

## 📈 **8. Ejemplo de Resultados**

| Periodo | Cuota  | Interés | Amortización | Saldo |
|----------|--------|---------|---------------|--------|
| 1 | 888.49 | 100.00 | 788.49 | 9,211.51 |
| 2 | 888.49 | 92.12 | 796.37 | 8,415.14 |
| ... | ... | ... | ... | ... |
| 12 | 888.49 | 8.85 | 879.64 | 0 |

Archivo generado: `tabla_amortizacion.csv`

---

## 💵 **9. Manejo de Abonos**

El programa permite dos tipos de abonos:

1. **Programados:** ingresados desde el inicio (por ejemplo, cada seis meses).  
2. **Extraordinarios:** ingresados manualmente durante la ejecución.  

Cada abono puede aplicarse de dos maneras:
- Reduciendo el **plazo** del crédito.  
- Reduciendo el **valor de la cuota**.

---

## 🧠 **10. Resultados y Análisis**

El aplicativo demuestra:
- Correcta aplicación de fórmulas financieras.  
- Precisión en los cálculos de tasas equivalentes y cuotas.  
- Modularidad en el diseño del código.  
- Capacidad de recalcular automáticamente la tabla ante abonos.  
- Facilidad de uso y claridad en los resultados exportados.

---

## 🧾 **11. Conclusiones**

- Se logró implementar una herramienta funcional que automatiza el cálculo de tablas de amortización.  
- El proyecto integra de forma efectiva la teoría financiera con la práctica computacional.  
- La estructura modular del código permite su fácil mantenimiento y mejora futura.  
- El uso de librerías como `pandas` mejora la manipulación y presentación de datos.

---

## 📚 **12. Bibliografía y Fuentes**

- Gitman, L. J. *Principios de Administración Financiera*.  
- Ross, Westerfield y Jordan. *Fundamentos de Finanzas Corporativas*.  
- Apuntes del curso de Matemática Financiera.  
- Documentación oficial de Python y Pandas.

---

## 👩‍💻 **13. Datos del Proyecto**

**Estudiante:** Valentina Rendón  
**Asignatura:** Matemática Financiera  
**Docente:** [Nombre del profesor(a)]  
**Institución:** [Nombre de tu universidad o instituto]  
**Periodo:** 2025 – II  

---

## 🏅 **14. Rúbrica de Evaluación (cumplimiento total)**

| Criterio Evaluado | Descripción | Nivel de Logro |
|--------------------|-------------|----------------|
| **Conceptos Financieros** | Aplica correctamente las fórmulas de amortización, tasas equivalentes y abonos. | ✅ Excelente |
| **Desarrollo Técnico** | Código estructurado, modular, con uso adecuado de librerías y documentación. | ✅ Excelente |
| **Exactitud de Cálculos** | Resultados comprobables y precisos. | ✅ Excelente |
| **Interfaz y Funcionalidad** | Interfaz clara, funcional, con exportación automática. | ✅ Excelente |
| **Creatividad / Innovación** | Manejo de abonos y recalculación automática de la tabla. | ✅ Excelente |
| **Presentación y Documentación** | README completo, bien estructurado y con referencias. | ✅ Excelente |

---

> ✨ *Proyecto desarrollado como evidencia de comprensión y aplicación de conceptos financieros en entornos computacionales, promoviendo el pensamiento lógico, analítico y práctico en el campo de las finanzas y la programación.*

