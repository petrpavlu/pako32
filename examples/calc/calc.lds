/*
 * Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
 * SPDX-License-Identifier: MIT
 */

SECTIONS
{
	. = 0x10000;
	.text : {
		*(.text._start)
		*(.text)
	}
	. = 0x20000;
	.data : {
		*(*rodata.*)
		*(.data)
		*(.bss)
	}
}
