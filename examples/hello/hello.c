/*
 * Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
 * SPDX-License-Identifier: MIT
 */

#ifdef HOSTED
#include <stdio.h>
#else

typedef struct {
	volatile unsigned char to_usb_byte;
	volatile unsigned char to_usb_valid;
	volatile unsigned char from_usb_ready;
	volatile unsigned char from_usb_byte;
} usb_fifo_t;

static usb_fifo_t *usb_fifo = (void *)0x30000;

/* Output one character. */
static void putchar(char c)
{
	while (usb_fifo->to_usb_valid)
		;

	usb_fifo->to_usb_byte = c;
	usb_fifo->to_usb_valid = 1;
}

#endif /* HOSTED */

/* Main loop. */
__attribute((noreturn))
int main(void)
{
	while (1) {
		for (int i = 0; i < 3; i++) {
			putchar('A' + i);
			for (int j = 0; j < 2048; j++)
				__asm__ ("");
		}
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
