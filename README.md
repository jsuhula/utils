# 🦁 LogHunter - Analizador de Bitácoras Transaccionales

**LogHunter** es una aplicación de escritorio de alto rendimiento construida en **WPF (.NET 8)** diseñada para el análisis forense de bitácoras comprimidas.

Permite procesar cientos de archivos `.zip` simultáneamente sin necesidad de extraerlos al disco, buscando transacciones específicas (Query/Payment), calculando KPIs de rendimiento y detectando errores en formatos mixtos (**JSON, XML, Texto Plano**).

![Status](https://img.shields.io/badge/Status-Stable-green) ![.NET](https://img.shields.io/badge/.NET-8.0-purple) ![Platform](https://img.shields.io/badge/Platform-Windows-blue)

## 🚀 Características Principales

* **⚡ Procesamiento en Memoria (Zero-Extraction):** Lee archivos `.log` y `.txt` directamente desde los ZIPs usando `System.IO.Compression` y `Parallel.ForEach`, optimizando el uso de RAM y evitando la lentitud de escritura en disco.
* **🔍 Búsqueda Contextual:** Filtra transacciones basándose en un **Merchant ID** específico, ignorando ruido de otros comercios.
* **🧠 Detección Inteligente de Errores:**
    * **Anti Falsos Positivos:** Ignora etiquetas XML/JSON vacías (ej. `<errors></errors>`).
    * **Priorización:** Detecta etiquetas específicas como `<descripcion>` y `<code>` antes que errores genéricos.
    * **Soporte Híbrido:** Analiza tramas REST (JSON) y SOAP/JMS (XML) en el mismo flujo.
* **📊 Dashboard Operativo:** Visualización inmediata de:
    * Consultas vs. Pagos (Exitosos vs. Errores).
    * Tiempos de respuesta (Mínimo, Máximo, Promedio).
    * Rango horario del análisis.
    * **Top 10** de errores más frecuentes.
* **drill-down Interactivo:**
    * **Doble Clic** en tarjetas o en la lista de errores para ver el detalle de esas transacciones específicas.
    * Filtrado en tiempo real en la ventana de detalle (Ver Todos / Solo Errores / Solo Exitosos).
* **💾 Exportación:**
    * Copiar filas seleccionadas al portapapeles.
    * Exportar reportes filtrados a **CSV** (compatible con Excel).

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** C#
* **Framework:** .NET 8.0 (LTS)
* **UI:** WPF (Windows Presentation Foundation)
* **Librerías Clave:**
    * `System.Threading.Tasks.Parallel`: Para multi-hilo y concurrencia.
    * `System.Text.RegularExpressions`: Para parsing de patrones complejos compilados.
    * `System.IO.Compression`: Para lectura eficiente de ZIPs.

## 📋 Prerrequisitos

* Sistema Operativo: Windows 10/11.
* [.NET Desktop Runtime 8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0).
* (Para desarrollo) Visual Studio 2022 o superior con la carga de trabajo ".NET Desktop Development".

## 🚀 Guía de Uso

### 1. Iniciar Análisis
1.  Ejecuta `LogHunter.exe`.
2.  Haz clic en **Examinar** y selecciona la carpeta que contiene los archivos `.zip`.
3.  Ingresa el **Merchant ID** objetivo (ej. `10556655`).
4.  Haz clic en **Buscar Tramas**.
    * *Nota: La pantalla mostrará un overlay de carga mientras procesa los archivos.*

### 2. Interpretación del Dashboard
Una vez finalizado el escaneo, verás:
* **Tarjetas Superiores:** Conteo de transacciones Query/Payment y tiempos (ms).
* **Top Errores:** Lista de los mensajes de error más comunes agrupados por frecuencia.
    * *Tip:* Haz **Doble Clic** en un error de la lista para ver todas las tramas que causaron ese error específico.

### 3. Ver Detalle (Drill-Down)
Al hacer clic en cualquier tarjeta (ej. "PAGOS") o en un error del Top:
1.  Se abrirá una ventana de detalle con una tabla de datos.
2.  Usa los **Radio Buttons** superiores para filtrar la vista: "Ver Todos", "Solo Exitosos" o "Solo Errores".
3.  Selecciona filas y usa **"Copiar Selección"** para pegar en un correo o chat.
4.  Usa **"Exportar Todo (.csv)"** para generar un reporte completo.

## 🧪 Generación de Datos de Prueba (Testing)

El proyecto incluye un script de Python para generar logs "dummy" y probar la robustez de la lógica de detección.

1.  Asegúrate de tener Python instalado.
2.  Ejecuta el script incluido en la raíz:
    ```bash
    python generar_logs.py
    ```
3.  Esto creará una carpeta `logs_prueba` con 5 ZIPs conteniendo tramas XML y JSON mezcladas, con errores aleatorios y el Merchant ID `10556655`.

## 🧩 Lógica de Detección de Errores (Under the Hood)

El motor de análisis (`AnalizarLinea`) sigue una jerarquía estricta para determinar si una línea es un error real, evitando falsos positivos:

1.  **Filtro Rápido:** Verifica si existen palabras clave (`Error`, `Exception`, `Fault`, `Code`, `<error>`).
2.  **Nivel 1 (XML Específico):** Busca etiquetas `<descripcion>...</descripcion>` o `<code>...</code>`. Si encuentra contenido, lo toma como el error real.
3.  **Nivel 2 (XML Genérico):** Busca etiquetas `<fault>`, `<error>`, etc., pero **valida que el contenido no esté vacío** ni sea solo espacios en blanco.
4.  **Nivel 3 (JSON):** Busca `"error": "..."` validando contenido dentro de las comillas.
5.  **Nivel 4 (Texto Plano):** Fallback para errores de conexión o timeouts simples (ej. `Error: Connection timed out`).

## 📂 Estructura del Proyecto

```text
LOG_Scanner/
├── Models/
│   ├── LogEntry.cs          # Modelo de datos de una línea de log (Propiedades y Regex)
│   └── DashboardStats.cs    # Modelo para los contadores y KPIs
├── Ventanas/
│   ├── MainWindow.xaml      # Interfaz Principal, Dashboard y Lógica de Procesamiento
│   └── DetalleWindow.xaml   # Ventana de Grilla, Filtros y Exportación
├── App.xaml                 # Punto de entrada
└── README.md                # Documentación
