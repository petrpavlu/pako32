/*
 * Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
 * SPDX-License-Identifier: MIT
 */

typedef unsigned int size_t;

typedef enum {
	TOKEN_NUMBER,
	TOKEN_PLUS,
	TOKEN_MINUS,
} token_t;

typedef struct {
	const char *input;
	size_t pos;
} lexer_t;

/* Read one input line. */
int read_input(char *input, size_t size)
{
	/* TODO */
	input[0] = '7';
	input[1] = '\0';

	return 0;
}

/* Output one character. */
void putchar(char c)
{
	/* TODO */
}

/* Output a string. */
void puts(const char *s)
{
	while (*s != '\0')
		putchar(*s++);
}

/* Parse an expression and calculate its result. */
int calculate(const char *input)
{
	/* TODO */
	return 7;
}

/* Print an int value. */
void print_int(int value)
{
	char c;

	if (value < 0)
		putchar('-');

	while (value != 0) ;
	/* TODO */
}

/* Read one input line, calculate the expression and print the result. */
void process_one(void)
{
	char input[128];
	int ret;

	puts("> ");

	ret = read_input(input, sizeof(input));
	if (ret != 0)
		return;

	ret = calculate(input);
	print_int(ret);
}

/* Main loop. */
void _start(void)
{
	while (1)
		process_one();
}
