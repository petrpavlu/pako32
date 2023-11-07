# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge


CLK_16MHZ_NS = 1_000_000_000 / 16_000_000


async def init_dut(dut):
    clock = Clock(dut.clk_i, CLK_16MHZ_NS, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    dut.rstn_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.rstn_i.value = 0
    await FallingEdge(dut.clk_i)
    dut.rstn_i.value = 1
