# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT
#
# Based on
# https://github.com/YosysHQ/icestorm/blob/master/examples/icestick/Makefile.

PROJ = pako32

PIN_DEF = tinyfpga-bx/pins.pcf
DEVICE = lp8k
PACKAGE = cm81

.PHONY: all
all: $(PROJ).rpt $(PROJ).bin

%.json: %.v
	yosys -p 'synth_ice40 -top top -json $@' $<

%.asc: $(PIN_DEF) %.json
	nextpnr-ice40 --$(DEVICE) --package $(PACKAGE) --asc $@ --pcf $< --json $*.json

%.bin: %.asc
	icepack $< $@

%.rpt: %.asc
	icetime -d $(DEVICE) -mtr $@ $<

# TODO Review.
#%_tb: %_tb.v %.v
#	iverilog -o $@ $^
#
#%_tb.vcd: %_tb
#	vvp -N $< +vcd=$@
#
#%_syn.v: %.json
#	yosys -p 'read_json $^; write_verilog $@'
#
#%_syntb: %_tb.v %_syn.v
#	iverilog -o $@ $^ `yosys-config --datdir/ice40/cells_sim.v`
#
#%_syntb.vcd: %_syntb
#	vvp -N $< +vcd=$@
#
#sim: $(PROJ)_tb.vcd
#
#postsim: $(PROJ)_syntb.vcd

.PHONY: prog
prog: $(PROJ).bin
	tinyprog -p $<

.PHONY: clean
clean:
	rm -f abc.history $(PROJ).json $(PROJ).asc $(PROJ).rpt $(PROJ).bin

.SECONDARY:
