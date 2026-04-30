## 🛠️ Guía de Extensibilidad (Añadir un nuevo motor DB)

Gracias a la abstracción de la `DbConnectionFactory`, agregar soporte para un nuevo motor (ej. PostgreSQL) toma solo 3 pasos:

1.  **Instalar el Driver:** `dotnet add package Npgsql`
2.  **Actualizar la Factoría (`Core/DbConnectionFactory.cs`):**
    Añadir la condición: `else if (templateName.Contains("PostgreSQL")) return new NpgsqlConnection(connStr);`
3.  **Añadir Dialecto DDL (`Core/CredentialService.cs`):**
    Añadir¡Excelente elección! Actualizar la base a **.NET 10** te da acceso a las últimas mejoras de rendimiento, optimización de memoria (crítico para el manejo de strings seguros) y mejor empaquetado *Single-File*.

Para reflejar un nivel de ingeniería superior, he reestructurado el `README.md`. Ahora incluye secciones de postura de seguridad (ideal para auditorías), arquitectura del proyecto, y una guía de extensibilidad. 

Aquí tienes el README robusto y a nivel *Enterprise*:

***

# 🔐 DB Credential Pooler (Enterprise Edition)

**Herramienta de Mancomunación DDL (Split-Knowledge) para Bases de Datos**

![.NET](https://img.shields.io/badge/.NET-10.0-512BD4?style=for-the-badge&logo=dotnet)
![WPF](https://img.shields.io/badge/UI-WPF-0078D7?style=for-the-badge&logo=windows)
![Security](https://img.shields.io/badge/Security-Zero_Trust-red?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Architecture-Factory_Pattern-239120?style=for-the-badge)

## 📌 Resumen Ejecutivo

**DB Credential Pooler** es una utilidad de escritorio nativa diseñada para resolver el desafío criptográfico y operativo de la **mancomunación de credenciales**. Construida sobre **.NET 10**, proporciona una interfaz aislada para que equipos de Infraestructura, DBAs y Ciberseguridad puedan ejecutar alteraciones de contraseñas (`ALTER USER` / `ALTER LOGIN`) sin que ningún individuo posea la credencial completa.

## 🛡️ Postura de Seguridad (Threat Model)

Esta herramienta fue diseñada asumiendo un entorno *Zero-Trust*. Las mitigaciones implementadas incluyen:

*   **Ejecución Stateless y Efímera:** La aplicación carece de base de datos propia. No se almacena ningún log de credenciales, ni en disco ni en el registro de Windows.
*   **Aislamiento de Memoria RAM:** Las contraseñas (maestras y mancomunadas) existen en memoria únicamente durante el ciclo de vida del bloque `using` de la conexión, delegando la limpieza inmediata al *Garbage Collector* optimizado de .NET 10.
*   **Anti Shoulder-Surfing:** Enmascaramiento estricto a nivel de control UI (`PasswordBox`) que interactúa directamente con `SecureString` en bajo nivel.
*   **Sanitización de Vectores DDL:** Dado que los motores de DB no soportan parámetros tipificados para sentencias `ALTER`, el servicio implementa algoritmos de escape de caracteres específicos por motor para prevenir la inyección SQL de segundo orden.

## 🏗️ Arquitectura del Sistema

El proyecto sigue principios SOLID, separando la capa de presentación de la lógica de acceso a datos:
```text
📁 DbCredentialUI/
 ├── 📁 Core/
 │    ├── DbConnectionFactory.cs   # Factoría abstracta de conexiones (MySQL, SQL Server)
 │    ├── CredentialService.cs     # Lógica de negocio y sanitización DDL (Strategy Pattern)
 ├── 📁 Models/
 │    └── DbTemplate.cs            # Modelo de deserialización JSON
 ├── 📁 Resources/
 │    └── templates.json           # Diccionario dinámico de cadenas de conexión
 ├── MainWindow.xaml               # UI: Presentación y Binding
 └── MainWindow.xaml.cs            # Code-Behind: Orquestación de eventos
