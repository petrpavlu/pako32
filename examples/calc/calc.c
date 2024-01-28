/*
 * Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
 * SPDX-License-Identifier: MIT
 */

#ifdef HOSTED
#include <stdio.h>
#else

typedef unsigned int size_t;

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

/* Output a string. */
static void printf(const char *s)
{
	while (*s != '\0')
		putchar(*s++);
}

/* Read one character. */
static char getchar(void)
{
	while (!usb_fifo->from_usb_ready)
		;

	return usb_fifo->from_usb_byte;
}

#endif /* HOSTED */

/* Read one input line. */
static int read_input(char *input, size_t size)
{
	char c;
	size_t i = 0;

	while (1) {
		c = getchar();
		putchar(c);
		if (c == '\r') {
			putchar('\n');
			break;
		}
		if (i + 1 < size)
			input[i++] = c;
	}

	if (i + 1 >= size) {
		printf("Input too long.\r\n");
		return 1;
	}

	input[i] = '\0';
	return 0;
}

typedef enum {
	TOKEN_NUMBER,
	TOKEN_PLUS,
	TOKEN_MINUS,
	TOKEN_EOI,
	TOKEN_ERROR,
} token_t;

typedef struct {
	const char *input;
	size_t pos;
} lexer_t;

/* Initialize a lexical analyzer. */
static void lexer_init(lexer_t *lexer, const char *input)
{
	lexer->input = input;
	lexer->pos = 0;
}

/* Get a hexadecimal digit. */
static int getxdigit(char c, int *out)
{
	if (c >= '0' && c <= '9')
		*out = c - '0';
	else if (c >= 'a' && c <= 'f')
		*out = c - 'a' + 10;
	else if (c >= 'A' && c <= 'F')
		*out = c - 'A' + 10;
	else
		return 1;
	return 0;
}

/* Parse a next token. */
static token_t lexer_next_token(lexer_t *lexer, int *number)
{
	char c;
	int digit;

	/* Skip over initial whitespace. */
	while (1) {
		c = lexer->input[lexer->pos];
		if (c == '\0' || c != ' ')
			break;
		lexer->pos++;
	}

	if (getxdigit(c, &digit) == 0) {
		*number = digit;
		while (1) {
			c = lexer->input[++lexer->pos];
			if (getxdigit(c, &digit) != 0)
				break;
			*number = (*number << 4) + digit;
			/* TODO Check for overflow. */
		}
		return TOKEN_NUMBER;
	}

	switch (c) {
		case '+':
			lexer->pos++;
			return TOKEN_PLUS;
		case '-':
			lexer->pos++;
			return TOKEN_MINUS;
		case '\0':
			return TOKEN_EOI;
	}

	return TOKEN_ERROR;
}

/* Parse an expression and calculate its result. */
static int calculate(const char *input, int *result)
{
	lexer_t lexer;
	int number;
	int minus = 0;
	int expect_operator = 0;

	lexer_init(&lexer, input);
	*result = 0;

	while (1) {
		token_t token = lexer_next_token(&lexer, &number);
		switch (token) {
			case TOKEN_NUMBER:
				if (expect_operator) {
					printf("Invalid input.\r\n");
					return 0;
				}
				/* TODO Check for overflow. */
				*result = minus ? (*result - number)
						: (*result + number);
				minus = 0;
				break;
			case TOKEN_PLUS:
				break;
			case TOKEN_MINUS:
				minus = !minus;
				break;
			case TOKEN_EOI:
				return 0;
			case TOKEN_ERROR:
				printf("Invalid input.\r\n");
				return 1;
		}
	}
}

/* Print one hexadecimal digit. */
static void print_xdigit(int hex)
{
	if (hex < 10)
		putchar('0' + hex);
	else if (hex < 16)
		putchar('a' + (hex - 10));
	else
		putchar('?');
}

/* Print an int value. */
static void print_int(int value)
{
	print_xdigit((value >> 28) & 0xf);
	print_xdigit((value >> 24) & 0xf);
	print_xdigit((value >> 20) & 0xf);
	print_xdigit((value >> 16) & 0xf);
	print_xdigit((value >> 12) & 0xf);
	print_xdigit((value >> 8) & 0xf);
	print_xdigit((value >> 4) & 0xf);
	print_xdigit((value >> 0) & 0xf);
	printf("\r\n");
}

/* Read one input line, calculate the expression and print the result. */
static void process_one(void)
{
	char input[128];
	int r;
	int result;

	printf("hex> ");

	r = read_input(input, sizeof(input));
	if (r != 0)
		return;

	r = calculate(input, &result);
	if (r != 0)
		return;

	print_int(result);
}

/* Main loop. */
__attribute((noreturn))
int main(void)
{
	while (1)
		process_one();
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
