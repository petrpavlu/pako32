# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

CC = clang
CFLAGS = --target=riscv32-unknown-elf -march=rv32i -nostdlib -Wall -pedantic
LDFLAGS = -T calc.lds

.PHONY: all
CALC_TEXT=calc.text.txt calc.text.txt01 calc.text.txt23
CALC_DATA=calc.data.txt calc.data.txt01 calc.data.txt23
all: $(CALC_TEXT) $(CALC_DATA)

calc: calc.c calc.lds

calc.text.raw: calc
	objcopy --dump-section .text=$@ $< /dev/null

calc.data.raw: calc
	objcopy --dump-section .data=$@ $< /dev/null

%.txt01: %.raw
	hexdump -v -e '2/2 "%04x " "\n"' $< | cut -d" " -f1 >$@

%.txt23: %.raw
	hexdump -v -e '2/2 "%04x " "\n"' $< | cut -d" " -f2 >$@

%.txt: %.raw
	od --address-radix=none --format=x1 --output-duplicates --width=1 $< | tr --delete ' ' > $@

.PHONY: clean
clean:
	rm -f calc $(CALC_TEXT) $(CALC_DATA)
