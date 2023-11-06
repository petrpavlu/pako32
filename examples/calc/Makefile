# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

CC = clang
CFLAGS = --target=riscv32-unknown-elf -march=rv32i -nostdlib -Wall -pedantic
LDFLAGS = -T calc.lds

.PHONY: all
all: calc.raw

calc: calc.c

calc.raw: calc
	objcopy --dump-section .prog=$@ $<

.PHONY: clean
clean:
	rm -f calc.raw calc
