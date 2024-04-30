# Plantronics / POLY PTT headset interface for Flexradio CAT
# Erik Finskas OH2LAK <erik@finskas.net>
# MIT license
#
# Developed using Plantronics / Poly USB PTT headset SHS 2355-11 
#
# Intended to control the virtual FlexVSP serial port RTS/DTR signal to control PTT on SmartSDR
# Active LOW state of signal is preferred.
#
# This code requires Python modules argparse, pyserial, hidapi

import argparse
import hid
import serial
import sys
from datetime import datetime

# Initialize selected HID device (0x047f:0xfaa9 = Plantronics / Poly USB PTT Headset SHS 2355-11)
PTTdevice = hid.device()
PTTdevice.open(0x047f, 0xfaa9)
PTTdevice.set_nonblocking(True)

# Print out the MIT license
def print_license():
    with open('LICENSE.md', 'r') as f:
        license_text = f.read()
        print(license_text)

# Main engine
def main(serial_port, signal, polarity, quiet):
    # Open the serial port
    ser = serial.Serial(serial_port, 9600)  # Adjust baud rate as necessary

    # Convert the signal parameter to uppercase for flexibility
    signal = signal.upper()

    # Convert the polarity parameter to uppercase for consistency
    polarity = polarity.upper()

    # Reset PTT state to off
    reset_PTT_state(ser, polarity)

    # Initialize timestamp for PTT on
    ptt_on_time = None

    # Display startup message with selected parameters
    print(f"Plantronics/Poly PTT headset to serial port interface by Erik Finskas OH2LAK <erik@finskas.net>")
    print(f"PTT Button Control started. Serial port: {serial_port}, Signal: {signal}, Polarity: {polarity}")

    try:
        while True:
            report = PTTdevice.read(64)
            if report:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if report == [9, 1, 0]:
                    if not quiet:
                        print(f"{timestamp} - PTT on")
                    ptt_on_time = datetime.now()  # Record PTT on time
                    if polarity == 'HIGH':
                        ser_signal = False  # Active high
                    elif polarity == 'LOW':
                        ser_signal = True   # Active low
                    else:
                        raise ValueError("Invalid polarity value. Use HIGH or LOW.")
                    if signal == 'RTS':
                        ser.setRTS(ser_signal)  # Set RTS signal
                    elif signal == 'DTR':
                        ser.setDTR(ser_signal)  # Set DTR signal
                elif report == [9, 0, 0]:
                    if not quiet:
                        ptt_off_time = datetime.now()  # Record PTT off time
                        if ptt_on_time is not None:
                            duration = ptt_off_time - ptt_on_time
                            print(f"{timestamp} - PTT off (PTT on: {duration.seconds} sec)")
                        else:
                            print(f"{timestamp} - PTT off")
                    if polarity == 'HIGH':
                        ser_signal = True   # Active high
                    elif polarity == 'LOW':
                        ser_signal = False  # Active low
                    else:
                        raise ValueError("Invalid polarity value. Use HIGH or LOW.")
                    if signal == 'RTS':
                        ser.setRTS(ser_signal)  # Set RTS signal
                    elif signal == 'DTR':
                        ser.setDTR(ser_signal)  # Set DTR signal

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt to gracefully exit the program
        print("\nProgram stopped.")
        reset_PTT_state(ser, polarity)
        ser.close()
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        # Perform cleanup
        reset_PTT_state(ser, polarity)
        ser.close()
        sys.exit(1)

def reset_PTT_state(ser, polarity):
    # Ensure PTT state is off based on polarity
    if polarity == 'HIGH':
        ser.setRTS(True)  # Set RTS signal to high (active)
        ser.setDTR(True)  # Set DTR signal to high (active)
    elif polarity == 'LOW':
        ser.setRTS(False)  # Set RTS signal to low (inactive)
        ser.setDTR(False)  # Set DTR signal to low (inactive)
    else:
        raise ValueError("Invalid polarity value. Use HIGH or LOW.")

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Plantronics/Poly PTT headset to serial port interface by Erik Finskas OH2LAK <erik@finskas.net>", 
                                     usage="%(prog)s port signal polarity [quiet]")

    # Add arguments
    parser.add_argument("port", nargs='?', help="Mandatory: Serial port name (e.g., COM1, /dev/ttyUSB0)")
    parser.add_argument("signal", nargs='?', help="Mandatory: Signal to control (RTS or DTR)")
    parser.add_argument("polarity", nargs='?', help="Mandatory: Polarity of the serial port signal (HIGH or LOW)")
    parser.add_argument("quiet", nargs='?', const=True, default=False, help="Optional: Suppress PTT on/off messages")
    parser.add_argument("--license", action="store_true", help="Display the MIT license")

    # Parse command-line arguments
    args = parser.parse_args()

    # If --license argument is provided, print the license and exit
    if args.license:
        print_license()
        sys.exit()

    # Check if all required arguments are provided
    if args.port is None or args.signal is None or args.polarity is None:
        parser.print_help()
        sys.exit()

    # Display confirmation message
    print(f"Selected Serial port: {args.port}, Signal: {args.signal}, Polarity: {args.polarity}")

    # Call main function with parsed arguments
    main(args.port, args.signal, args.polarity, args.quiet)