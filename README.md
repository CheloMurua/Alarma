# 🛡️ Detector de Movimiento con Alarma y Notificación

![ESP32](https://img.shields.io/badge/ESP32-32C0FF?style=for-the-badge&logo=esp32&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![IoT](https://img.shields.io/badge/IoT-FF6F61?style=for-the-badge&logo=iot&logoColor=white)

---

## 📌 Introducción

Este proyecto consiste en un **sistema de detección de movimiento** que utiliza:

- Microcontrolador **ESP32**
- Sensor **PIR**
- **Zumbador** para alertas sonoras

Su funcionamiento:

1. El sensor PIR detecta cambios en el entorno.
2. El ESP32 procesa la señal y activa un zumbador.
3. Se envía una **notificación vía Wi-Fi** a un servidor Flask.
4. Los eventos se registran temporalmente y se pueden consultar mediante un endpoint GET en formato JSON.

El objetivo final es evolucionar hacia una **plataforma IoT escalable**, con almacenamiento permanente en **MySQL** y soporte para múltiples dispositivos.

🔗 [Repositorio GitHub](https://github.com/CheloMurua/Alarma/tree/main/Alarma-Movimiento-ESP32)  
🔗 [Proyecto en Wokwi](https://wokwi.com/projects/442417296721929217)  
🔗 [Log de requests (Postman/Wokwi)](https://mchelom.pythonanywhere.com/records)  
🔗 [Video de prueba](#)  

---

## 🎯 Objetivo General

Diseñar e implementar un sistema de detección de movimiento basado en ESP32 y sensor PIR, incorporando:

- Capa de conectividad
- Transporte de datos confiable
- Backend con almacenamiento en MySQL

Para lograr una **solución IoT escalable, eficiente y confiable**.

---

## 📝 Objetivos Específicos

- Analizar las limitaciones del sistema actual centrado en la capa física.  
- Incorporar conectividad para transmitir datos desde los ESP32 hacia un servidor Flask.  
- Seleccionar tecnologías de transporte confiables (**Wi-Fi y HTTP**).  
- Desarrollar backend en Python con **Flask** y montar servidor + base de datos **MySQL** en PythonAnywhere.  
- Diseñar arquitectura modular para integrar nuevos sensores y nodos ESP32.  
- Optimizar consumo de recursos y garantizar escalabilidad.  
- Integrar el repositorio **Alarma-Movimiento-ESP32** como prueba de concepto.

---

## 🛠️ Hardware Utilizado

| Componente | Función |
|------------|--------|
| **ESP32** | Procesa señales y controla el zumbador |
| **Sensor PIR (Pin 13)** | Detecta movimiento mediante infrarrojos |
| **Zumbador (Pin 14)** | Emite alerta sonora |
| **Wi-Fi** | Envía notificaciones y datos al servidor |
| **Cables** | Interconexión de componentes |

### 🔌 Esquemas de conexión

- PIR → Pin digital 13 del ESP32  
- Zumbador → Pin digital 14  
- VCC → 3.3V  
- GND → tierra común  

---

## 💻 Funcionamiento del Código

1. **Inicialización**  
   - Configura pines de PIR y zumbador  
   - Conexión del ESP32 a Wi-Fi  

2. **Detección de movimiento**  
   - Evaluación periódica (cada 5 segundos simulada)  
   - Activación del zumbador durante 5 segundos al detectar movimiento  

3. **Notificación y registro**  
   - Envía HTTP POST al servidor Flask  
   - Registra evento en memoria con timestamp  
   - Notificación al usuario mediante endpoint de prueba  

4. **Loop continuo**  
   - Monitoreo constante del sensor y gestión de alertas  

---

## 📊 Resultados y Pruebas

- La alarma sonora y notificaciones funcionan correctamente.  
- Registro de eventos en servidor Flask confirmado.  
- Pruebas realizadas en **Wokwi** y con **Postman**.  

### 🔧 Mejoras futuras

- Integrar almacenamiento seguro en base de datos local o en la nube.  
- Añadir LEDs indicadores.  
- Incorporar sensores adicionales para reducir falsas alarmas.  
- Escalar a múltiples dispositivos y nodos ESP32.

---

## ✅ Conclusión

El proyecto demuestra cómo un ESP32 puede monitorear un área, activar alarmas y enviar notificaciones remotas vía HTTP.  
La integración hardware-software permite crear **sistemas de seguridad inteligentes, escalables y modulares**, sentando la base para futuros desarrollos domóticos con almacenamiento centralizado en MySQL y gestión de múltiples dispositivos.

---

