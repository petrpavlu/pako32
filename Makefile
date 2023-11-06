# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT
#
# Based on
# https://github.com/YosysHQ/icestorm/blob/master/examples/icestick/Makefile.

PROJ = pako32

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
	yosys -p '$(foreach file,$^,read_verilog -sv $(file);)' -p 'synth_ice40 -top $(PROJ) -json $@'

$(PROJ).asc: $(PIN_DEF) $(PROJ).json
	nextpnr-ice40 --$(DEVICE) --package $(PACKAGE) --asc $@ --pcf $(PIN_DEF) --json $(PROJ).json

$(PROJ).bin: $(PROJ).asc
	icepack $< $@

$(PROJ).rpt: $(PROJ).asc
	icetime -d $(DEVICE) -mtr $@ $<

.PHONY: prog
prog: $(PROJ).bin
	tinyprog -p $<

.PHONY: check
check:
	$(MAKE) -C tests all

.PHONY: clean
clean:
	$(MAKE) -C tests clean
	rm -f abc.history $(PROJ).json $(PROJ).asc $(PROJ).rpt $(PROJ).bin
