/*
 * Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
 * SPDX-License-Identifier: MIT
 */

#ifdef HOSTED
#include <stdio.h>
#else

typedef struct {
	volatile unsigned char pad0;
	volatile unsigned char to_usb; /* ready status on read, byte on write */
	volatile unsigned char from_usb_ready;
	volatile unsigned char from_usb_byte;
} usb_fifo_t;

static usb_fifo_t *usb_fifo = (void *)0x30000;

/* Output one character. */
static void putchar(char c)
{
	while (!usb_fifo->to_usb)
		;

	usb_fifo->to_usb = c;
}

#endif /* HOSTED */

/* Main loop. */
__attribute((noreturn))
int main(void)
{
	const char string[] = "Hello world!\r\n";

	while (1) {
		for (int i = 0; i < sizeof(string) - 1; i++)
			putchar(string[i]);

		for (int i = 0; i < 1 << 14; i++)
			__asm__ ("");
	}
}

#ifndef HOSTED
__asm__ (
"	.section .data._stack, \"aw\", @progbits\n"
"	.zero 1024\n"
"	.global stack_end\n"
"	.type stack, @object\n"
"_stack_end:"
"	.previous\n"
"\n"
"	.section .text._start, \"ax\", @progbits\n"
"	.global _start\n"
"	.type _start, @function\n"
"_start:\n"
"	la sp, _stack_end\n"
"	j main\n"
"	.size _start, .-_start\n"
"	.previous\n"
);
#endif /* HOSTED */
