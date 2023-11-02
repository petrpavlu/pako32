# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT
#
# Based on
# https://github.com/YosysHQ/icestorm/blob/master/examples/icestick/Makefile.

PROJ = pako32
export PROJ

PIN_DEF = pins.pcf
DEVICE = lp8k
PACKAGE = cm81

HDL_FILES = \
	cpu.v \
	fifo_if.v \
	pako32.v \
	prescaler.v \
	usb_cdc/usb_cdc/bulk_endp.v \
	usb_cdc/usb_cdc/ctrl_endp.v \
	usb_cdc/usb_cdc/in_fifo.v \
	usb_cdc/usb_cdc/out_fifo.v \
	usb_cdc/usb_cdc/phy_rx.v \
	usb_cdc/usb_cdc/phy_tx.v \
	usb_cdc/usb_cdc/sie.v \
	usb_cdc/usb_cdc/usb_cdc.v
export HDL_FILES

.PHONY: all
all: $(PROJ).rpt $(PROJ).bin

$(PROJ).json: $(HDL_FILES)
	yosys -p '$(foreach file,$^,read_verilog $(file);)' -p 'synth_ice40 -top $(PROJ) -json $@'

$(PROJ).asc: $(PIN_DEF) $(PROJ).json
	nextpnr-ice40 --$(DEVICE) --package $(PACKAGE) --asc $@ --pcf $(PIN_DEF) --json $(PROJ).json

$(PROJ).bin: $(PROJ).asc
	icepack $< $@

$(PROJ).rpt: $(PROJ).asc
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

.PHONY: check
check:
	$(MAKE) -f Makefile.cocotb all

.PHONY: clean
clean:
	$(MAKE) -f Makefile.cocotb clean
	rm -f abc.history $(PROJ).json $(PROJ).asc $(PROJ).rpt $(PROJ).bin
