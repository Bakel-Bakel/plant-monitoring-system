# ⚡ Arduino Folder: `arduino/README.md`

## Arduino Code for Plant Monitoring System

This directory contains the firmware for the Arduino board. The code is responsible for collecting environmental sensor data and transmitting it to the Raspberry Pi via serial communication.

## 🔌 Connected Components

- **DHT22** – Temperature and Humidity
- **BH1750** – Light Intensity Sensor (I2C)
- **Analog pH Sensor**
- **Soil Moisture Sensor**
- **LCD (20x4)** – I2C Display
- **Relay + Fan** – Turns ON when temperature > 28°C

## 📤 Communication

The Arduino transmits data in this format over serial:

```

<temperature>,<humidity>,<pH>,<soil>,<lux>

```

Example:
```

24.7,56.2,6.8,410,238.5

```

This stream is read by the Raspberry Pi for dashboard display.

## ⚙️ Notes

- Make sure the I2C address of the LCD is correctly set (usually `0x27`).
- Ensure 5V power for sensors and proper analog-to-digital resolution.



