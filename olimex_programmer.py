import time

import machine
from machine import Pin

miso = Pin(Pin.board.SDI, Pin.IN, Pin.PULL_DOWN)
mosi = Pin(Pin.board.SDO, Pin.OUT, value=0)
cs = Pin(Pin.board.CS0, Pin.OUT, value=1)
sck = Pin(Pin.board.SCK, Pin.OUT, value=0)

reset = Pin(Pin.board.SDA1, Pin.OUT, value=1)
done = Pin(Pin.board.SCL1, Pin.IN)


def pulse_clock():
    sck.value(1)  # Rising edge, FPGA captures the bit
    time.sleep_us(1)
    sck.value(0)  # Falling edge, we prepare the next bit
    time.sleep_us(1)


def send_dummy_clock_cycles(num_cycles):
    """
    Sends a specified number of clock pulses.
    Assumes CS/SS pin is already set to the correct state (HIGH for this step).
    """
    print(f"Sending {num_cycles} dummy clock cycles...")
    for _ in range(num_cycles):
        pulse_clock()


def send_spi_byte(byte_to_send):
    """
    Sends one byte (8 bits), MSB first, while CS is low.
    """
    # Assumes CS is already low
    for i in range(8):
        # Isolate the most significant bit (MSB)
        bit = (byte_to_send >> (7 - i)) & 1
        mosi.value(bit)
        pulse_clock()


def configure():
    # --- Step 1: Load the configuration file ---
    try:
        with open("example.bin", "rb") as f:
            config_image = f.read()
            print(f"Loaded example.bin: {len(config_image)} bytes.")
    except OSError:
        print(f"ERROR: File 'example.bin' not found on the board!")
        print("Please copy the file to the MicroPython device.")
        return

    print("--- Starting iCE40 Configuration ---")

    # --- Step 2: Reset the FPGA ---
    cs.value(0)
    sck.value(0)
    reset.value(0)
    time.sleep_us(200)  # Wait minimum 200 ns (it's okay if we exceed it)
    reset.value(1)

    # --- Step 3: Wait for memory clear ---
    print("Waiting 1200us for memory clear...")
    time.sleep_us(1200)  # Again it's okay to exceed the wait time

    # --- Step 4: Send 8 dummy clocks with chip select high ---
    cs.value(1)
    send_dummy_clock_cycles(8)
    cs.value(0)

    # --- Step 5: Send configuration image ---
    print(f"Sending {len(config_image)} bytes of configuration data...")
    for byte in config_image:
        send_spi_byte(byte)
    print("Configuration data sent.")

    # --- Step 6: Wait 100 dummy clocks for CDONE, keep chip select high ---
    cs.value(1)
    send_dummy_clock_cycles(100)

    # --- Step 7: Check CDONE ---
    if done.value() == 1:
        print("SUCCESS: CDONE pin is HIGH.")
        send_dummy_clock_cycles(49)
        print("FPGA configuration complete. I/O pins are now active.")
    else:
        print("ERROR: Configuration failed. CDONE pin is still LOW.")

    print("--- End of configuration ---")
