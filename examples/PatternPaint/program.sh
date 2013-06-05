#!/bin/bash
# A script to automatically program the Blinkyboard8 firmware
# Simply resets the board using the baud rate hack, then programs it.

FIRMWARE_FILE=munged.hex
SERIAL_DEVICE=${1}

cat pov.hex PatternPlayer.hex > munged.hex


# First, set the baud rate to 1200 to trigger a firmware reset
stty -f ${SERIAL_DEVICE} 1200

sleep 1
# Next, program the board.
./avrdude-mac -cavr109 -pm32u4  -b57600 -P${SERIAL_DEVICE} -D -Uflash:w:${FIRMWARE_FILE}:i 

