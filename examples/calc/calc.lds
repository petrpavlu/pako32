/*
 * Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
 * SPDX-License-Identifier: MIT
 */

SECTIONS
{
	. = 0x8000;
	.prog : {
		*(.text)
		*(.data)
		*(.bss)
	}
}
