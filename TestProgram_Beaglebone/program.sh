#!/bin/bash
# Call with one of the supported boards.

if [ -d $1 ]
then
  echo 'Specify a target board as the only command line option'
  exit 1
fi

if [ $1 = 'AnalogLEDFader' ]
then
  BOOTLOADER_FILE=Caterina-AnalogLEDFader.hex
elif [ $1 = 'USBDMX' ]
then
  BOOTLOADER_FILE=Caterina-USBDMX.hex
elif [ $1 = 'BlinkyTape' ]
then
  BOOTLOADER_FILE=Caterina-BlinkyTape.hex
elif [ $1 = 'Blinkyboard8' ]
then
  BOOTLOADER_FILE=Caterina-Blinkyboard8.hex
else
  echo 'Target' ${1} 'not recognized'
  exit 1
fi


# Lock bits (LOCK): 0x2F: User program can't overwrite bootloader, no memory locks enabled
# Extended fuse byte (EFUSE): 0xCB Hardware boot disabpeld, BOD disabled
# Fuse high byte (HFUSE): 0xD8 OCD, JTAG disabled, SPI program enabled, watchdog off, preserve eeprom, large bootloader, bootloader on reset
# Fuse low byte (LFUSE): 0xFF No divide by 9, no clock output, fast startup time, low power crystal oscillator

#First, program the fuses (in case the clock bits were set wrong initially?)
avrdude -c avrisp -pm32u4 -P/dev/tty.usbmodemfd1221 -B200 -Ulock:w:0x2F:m -Uefuse:w:0xcb:m -Uhfuse:w:0xd8:m -Ulfuse:w:0xff:m
#avrdude -c usbtiny -pm32u4 -Pusb -B200 -Ulock:w:0x2F:m -Uefuse:w:0xcb:m -Uhfuse:w:0xd8:m -Ulfuse:w:0xff:m
#avrdude -c dragon_isp -Pusb -pm32u4 -B200 -Ulock:w:0x2F:m -Uefuse:w:0xcb:m -Uhfuse:w:0xd8:m -Ulfuse:w:0xff:m

# Then program the bootloader (And applicaiton, too?)
avrdude -c avrisp -pm32u4 -P/dev/tty.usbmodemfd1221 -B1 -Uflash:w:${BOOTLOADER_FILE}:i
#avrdude -c usbtiny -pm32u4 -Pusb -B1 -Uflash:w:${BOOTLOADER_FILE}:i
#avrdude -c dragon_isp -Pusb -pm32u4 -B1 -Uflash:w:${BOOTLOADER_FILE}:i
