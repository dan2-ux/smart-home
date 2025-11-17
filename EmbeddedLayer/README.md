# This directory contains the code for embedded layer for smart home

The main.ino file is built entirely on FreeRTOS, providing a stable and reliable embedded layer for recording, sending, and reading sensor data.

By leveraging FreeRTOS, I can customize tasks and assign priorities, ensuring smooth operation of the ESP32. Combined with MQTT communication, this setup allows the ESP32 to handle multiple tasks efficiently without delays or data loss.

If you want to use a different MCU for this layer, you may need to spend extra time on configuration, as unlike the ESP32, most other MCUs do not support FreeRTOS out of the box.

