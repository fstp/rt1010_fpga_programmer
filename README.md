# **Pyboard RT1010 iCE40HX1K FPGA Programmer**

## **Overview**

This project provides a MicroPython program to flash an Olimex iCE40HX1K-EVB FPGA using a RT1010 (MIMXRT1010) Pyboard.
It's a simple software SPI-based solution, using the hardware SPI was not possible due to some specific requirements of
the ICE (like sending dummy clock cycles while holding the chip select high, which is not possible with hardware SPI).

*The .bin file included is a dummy FPGA image that will light up the LEDs on the board, including the CDONE led to indicate success.*

## **Connections**
| RT1010 | Color | FPGA | FPGA Pin number |
| ----------- | ----------- | ----------- | ----------- |
| 3.3v | Red | 3.3v | 1 |
| GND | Black | GND | 2 |
| SCL1 (Done) | Orange | CDONE | 5 |
| SDA1 (Reset) | Blue | CRESET | 6 |
| SDO (MOSI) | Yellow | SDI | 7 |
| SDI (MISO) | Green | SDO | 8 |
| SCK | White | SCK (Clock) | 9 |
| CS0 (CSn) | Brown | SS_B (Chip Select) | 10 |

*For details on the PIN layout, check the block in bottom left of the schematics PDF "iCE40HX1K-EVB_Rev_B"*

## **Links**
  1. https://www.olimex.com/Products/FPGA/iCE40/iCE40HX1K-EVB/open-source-hardware  
  2. https://www.olimex.com/Products/MicroPython/RT1010-Py/open-source-hardware 
  3. https://www.cocoacrumbs.com/blog/2023-01-27-getting-started-with-the-olimex-ice40hx1k-evb/
  4. https://bitbucket.org/cocoacrumbselectronics/ice40hx1k-evb-demo/src/master/
  5. https://github.com/OLIMEX/iCE40HX1K-EVB
