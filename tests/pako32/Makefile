# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

# Configuration for cocotb.
VERILOG_SOURCES = \
	$(addprefix ../../, $(HDL_FILES)) \
	$(shell yosys-config --datdir)/ice40/cells_sim.v
TOPLEVEL = pako32
MODULE = test_pako32

include ../Makefile.common
