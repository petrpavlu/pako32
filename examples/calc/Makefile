# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

CC = clang
CFLAGS = --target=riscv32-unknown-elf -march=rv32i -nostdlib -Wall -pedantic
LDFLAGS = -T calc.lds

.PHONY: all
all: calc.text.txt calc.data.txt

calc: calc.c calc.lds

calc.text.raw: calc
	objcopy --dump-section .text=$@ $<

calc.text.txt: calc.text.raw
	od --address-radix=none --format=x1 --output-duplicates --width=1 $< | tr --delete ' ' > $@

calc.data.raw: calc
	objcopy --dump-section .data=$@ $<

calc.data.txt: calc.data.raw
	od --address-radix=none --format=x1 --output-duplicates --width=1 $< | tr --delete ' ' > $@

.PHONY: clean
clean:
	rm -f calc calc.text.raw calc.text.txt calc.data.raw calc.data.txt
