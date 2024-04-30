# Plantronics_PTT
Small Python program to interface a Plantronics/Poly PTT USB headset to a serial port to control FlexRadio SmartSDR PTT

The program has been developed with Plantronics/Poly SHS2355-11 PTT headset but it can be easily adopted to any device with a HID interface.

<p align="center">
<img height="250" src="https://github.com/OH2LAK/Plantronics_PTT/blob/main/Plantronics_SHS2355-11.png">
</p>

## Why
Flexradio SmartSDR application PTT can be controlled either via CAT or via serial port signal RTS or DTR using the SmartSDR CAT program. In search of a handy PTT device to have possibility of controlling the PTT otherwise than mouse clicking the MOX button on the SmartSDR application, I started to investigate Plantronics SHS2355-11 PTT USB headsets which are used in public safety dispatch centers, etc. They provide a PTT pushbutton as seen in the picture, and also a high-quality USB sound device.

I thought of investigating how the PTT button of the PTT headset device can be read and to utilize the information to create a nice PTT interface for my Flexradio, amongst having then also a dedicated USB audio device for my headset.

## How
Information about the headset states that "The Push-to-Talk switch enumerates as button 1 of a single button game controller"

This lead to start investigating how to first get some data out of the USB device using a Python program reading the HID messages sent by the device. When the PTT button is pressed, the HID device sends message `[9, 1, 0]` , and when the PTT button is depressed, HID device sends message `[9, 0, 0]`.

The code loops around reading and evaluating the received HID message, and controlling the RTS/DTR signals of the configured serial port accordingly. The RTS/DTR signal then eventually control the PTT of the SmartSDR application, which then eventually controls the radio PTT.

With my very bad coding skills and the huge help of ChatGPT, this program was created in one night and I'm really proud of the outcome and it helped me to understand the coders world bit more again.

## Prerequisites
With Flexradio SmartSDR CAT, the PTT port needs to be configured as the program controls the PTT through this port. Regarding creating or configuring a PTT port within SmartSDR CAT, please refer to the SmartSDR CAT manual [SmartSDR CAT User Guide v3.x](https://www.flexradio.com/documentation/smartsdr-cat-user-guide-pdf/)

In my case, the PTT port is COM5, the signal is RTS and the active state is LOW

<p align="center">
<img height="400" src="https://github.com/OH2LAK/Plantronics_PTT/blob/main/SmartSDR_CAT.png">
<img height="400" src="https://github.com/OH2LAK/Plantronics_PTT/blob/main/SmartSDR_CAT-Edit_PTT_port.png">
</p>

## Usage

The Python code is compliled to a Windows executable using PyInstaller. It wraps the Python runtime and the code into a self-executing package without the need of installing Python separately.

The program has three mandatory parameters which need to be passed for the program to start.
* Port - the COM port to which the program will connect to (In my case, COM5)
* Signal - The RS232 signal which will be used to control PTT on the selected COM port (In my case, RTS)
* Polarity - Polarity of the RS232 signal, either active low or active high. (In my case, active LOW)

In addition, a QUIET parameter can be passed so that the program will not print out the PTT on/off events.

```
usage: Plantronics_PTT port signal polarity [quiet]

Plantronics/Poly PTT headset to serial port interface by Erik Finskas OH2LAK <erik@finskas.net>

positional arguments:
  port        Mandatory: Serial port name (e.g., COM1, /dev/ttyUSB0)
  signal      Mandatory: Signal to control (RTS or DTR)
  polarity    Mandatory: Polarity of the serial port signal (HIGH or LOW)
  quiet       Optional: Suppress PTT on/off messages
```

The program can be quit with a CTRL-C in the window, or just by killing the window running the program.


## Example output
```
C:\Users\superman\Documents\Ham Radio\Plantronics PTT headset\>Plantronics_PTT COM5 RTS LOW
Selected Serial port: COM5, Signal: RTS, Polarity: LOW
Plantronics/Poly PTT headset to serial port interface by Erik Finskas OH2LAK <erik@finskas.net>
PTT Button Control started. Serial port: COM5, Signal: RTS, Polarity: LOW
2024-04-30 23:07:28 - PTT on
2024-04-30 23:07:28 - PTT off (PTT on: 0 sec)
2024-04-30 23:07:47 - PTT on
2024-04-30 23:07:52 - PTT off (PTT on: 4 sec)
2024-04-30 23:07:54 - PTT on
2024-04-30 23:07:59 - PTT off (PTT on: 4 sec)

Program stopped.
```
## Disclaimer & License
I give no support or help if you struggle to get this program to work. I have not investigated or thought any security concerns of the program, thus it has some internal housekeeping so that the PTT state should clear out if the program hangs. Then of course the PTT can be switched off from the SmartSDR application. I selected the MIT license for the program as it gives everybody full freedom to do whatever they want with the code. Hope the program is useful for someone!
