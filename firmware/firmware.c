/* Simple example for Teensy USB Development Board
 * http://www.pjrc.com/teensy/
 * Copyright (c) 2008 PJRC.COM, LLC
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include <avr/io.h>
#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include <stdint.h>
#include <math.h>
#include <util/delay.h>
#include "usb_serial.h"

#define LED_CONFIG	(DDRD |= (1<<6))
#define LED_ON		(PORTD |= (1<<6))
#define LED_OFF		(PORTD &= ~(1<<6))
#define CPU_PRESCALE(n) (CLKPR = 0x80, CLKPR = (n))

void send_str(const char *s);
uint8_t recv_str(char *buf, uint8_t size);
void parse_and_execute_command(const char *buf, uint8_t num);

// Serial to parallel SPI driver
static
void send_parallel_byte(
	const uint8_t c
)
{
	// D5 is clock, D4 is data
	PORTD = c & 0xDF;

	PORTD = c | 0x20;
}

static
void send_single_byte(
	const uint8_t c
)
{	
	// D5 is clock, D4 is data
	for(uint8_t i = 0; i < 8; i++) {
		PORTD = (((c >> (7 - i)) & 0x01) << 4);
		PORTD = (((c >> (7 - i)) & 0x01) << 4) | 0x20;
	}
}

int main(void)
{
	CPU_PRESCALE(0);
	usb_init();

	DDRB = 0xFF;
	DDRD = 0xFF;	

	// Send a canned routine, until we get some usb data
	while(usb_serial_available() <= 0) {
/*
		for (uint8_t j = 0; j < 128; j++) {
			for (uint8_t i = 0; i < 32; i++) {
				send_single_byte(0x80 | j);
				send_single_byte(0x80 | 0);
				send_single_byte(0x80 | 0);
			}	
			send_single_byte(0x00);
		}
		for (uint8_t j = 0; j < 128; j++) {
			for (uint8_t i = 0; i < 32; i++) {
				send_single_byte(0x80 | 0);
				send_single_byte(0x80 | j);
				send_single_byte(0x80 | 0);
			}	
			send_single_byte(0x00);
		}
		for (uint8_t j = 0; j < 128; j++) {
			for (uint8_t i = 0; i < 32; i++) {
				send_single_byte(0x80 | 0);
				send_single_byte(0x80 | 0);
				send_single_byte(0x80 | j);
			}	
			send_single_byte(0x00);
		}
*/
		for (uint8_t j = 0; j < 128; j++) {
			for (uint8_t i = 0; i < 32; i++) {
				uint8_t red =   64*(1+sin(i/2.0 + j/4.0));
				uint8_t green = 64*(1+sin(i/1.0 + j/9.0+2.1));
				uint8_t blue =  64*(1+sin(i/3.0 + j/14.0+4.2));

				send_single_byte(0x80 | red);
				send_single_byte(0x80 | green);
				send_single_byte(0x80 | blue);
			}	
			send_single_byte(0x00);
		}
	}


	while (1)
	{
		const int8_t n = usb_serial_available();
		if (n <= 0)
			continue;

		const uint8_t irq_flags = SREG;
		cli();

		int8_t i;
		for (i = 0 ; i < n ; i++)
		{
#define CDC_RX_ENDPOINT		3
			UENUM = CDC_RX_ENDPOINT;
			const uint8_t c = UEDATX;
			send_parallel_byte(c);
		}

		// Release the USB buffer
		UEINTX = 0x6B;

		// Re-enabled interrupts
		SREG = irq_flags;
	}
}

// Send a string to the USB serial port.  The string must be in
// flash memory, using PSTR
//
void send_str(const char *s)
{
	char c;
	while (1) {
		c = pgm_read_byte(s++);
		if (!c) break;
		usb_serial_putchar(c);
	}
}

// Receive a string from the USB serial port.  The string is stored
// in the buffer and this function will not exceed the buffer size.
// A carriage return or newline completes the string, and is not
// stored into the buffer.
// The return value is the number of characters received, or 255 if
// the virtual serial connection was closed while waiting.
//
uint8_t recv_str(char *buf, uint8_t size)
{
	int16_t r;
	uint8_t count=0;

	while (count < size) {
		r = usb_serial_getchar();
		if (r != -1) {
			if (r == '\r' || r == '\n') return count;
			if (r >= ' ' && r <= '~') {
				*buf++ = r;
				usb_serial_putchar(r);
				count++;
			}
		} else {
			if (!usb_configured() ||
			  !(usb_serial_get_control() & USB_SERIAL_DTR)) {
				// user no longer connected
				return 255;
			}
			// just a normal timeout, keep waiting
		}
	}
	return count;
}

// parse a user command and execute it, or print an error message
//
void parse_and_execute_command(const char *buf, uint8_t num)
{
	uint8_t port, pin, val;

	if (num < 3) {
		send_str(PSTR("unrecognized format, 3 chars min req'd\r\n"));
		return;
	}
	// first character is the port letter
	if (buf[0] >= 'A' && buf[0] <= 'F') {
		port = buf[0] - 'A';
	} else if (buf[0] >= 'a' && buf[0] <= 'f') {
		port = buf[0] - 'a';
	} else {
		send_str(PSTR("Unknown port \""));
		usb_serial_putchar(buf[0]);
		send_str(PSTR("\", must be A - F\r\n"));
		return;
	}
	// second character is the pin number
	if (buf[1] >= '0' && buf[1] <= '7') {
		pin = buf[1] - '0';
	} else {
		send_str(PSTR("Unknown pin \""));
		usb_serial_putchar(buf[0]);
		send_str(PSTR("\", must be 0 to 7\r\n"));
		return;
	}
	// if the third character is a question mark, read the pin
	if (buf[2] == '?') {
		// make the pin an input
		*(uint8_t *)(0x21 + port * 3) &= ~(1 << pin);
		// read the pin
		val = *(uint8_t *)(0x20 + port * 3) & (1 << pin);
		usb_serial_putchar(val ? '1' : '0');
		send_str(PSTR("\r\n"));
		return;
	}
	// if the third character is an equals sign, write the pin
	if (num >= 4 && buf[2] == '=') {
		if (buf[3] == '0') {
			// make the pin an output
			*(uint8_t *)(0x21 + port * 3) |= (1 << pin);
			// drive it low
			*(uint8_t *)(0x22 + port * 3) &= ~(1 << pin);
			return;
		} else if (buf[3] == '1') {
			// make the pin an output
			*(uint8_t *)(0x21 + port * 3) |= (1 << pin);
			// drive it high
			*(uint8_t *)(0x22 + port * 3) |= (1 << pin);
			return;
		} else {
			send_str(PSTR("Unknown value \""));
			usb_serial_putchar(buf[3]);
			send_str(PSTR("\", must be 0 or 1\r\n"));
			return;
		}
	}
	// otherwise, error message
	send_str(PSTR("Unknown command \""));
	usb_serial_putchar(buf[0]);
	send_str(PSTR("\", must be ? or =\r\n"));
}


