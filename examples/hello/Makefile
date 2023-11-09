# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

CC = clang
CFLAGS = --target=riscv32-unknown-elf -march=rv32i -Oz -nostdlib -Wall -pedantic
LDFLAGS = -T hello.lds

.PHONY: all
HELLO_TEXT=hello.text.txt hello.text.txt01 hello.text.txt23
HELLO_DATA=hello.data.txt hello.data.txt01 hello.data.txt23
all: $(HELLO_TEXT) $(HELLO_DATA)

hello: hello.c hello.lds

hello.text.raw: hello
	objcopy --dump-section .text=$@ $< /dev/null

hello.data.raw: hello
	objcopy --dump-section .data=$@ $< /dev/null

%.txt01: %.raw
	hexdump -v -e '2/2 "%04x " "\n"' $< | cut -d" " -f1 >$@

%.txt23: %.raw
	hexdump -v -e '2/2 "%04x " "\n"' $< | cut -d" " -f2 >$@

%.txt: %.raw
	od --address-radix=none --format=x1 --output-duplicates --width=1 $< | tr --delete ' ' > $@

.PHONY: clean
clean:
	rm -f hello $(HELLO_TEXT) $(HELLO_DATA)
