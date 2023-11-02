# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge


CLK_16MHZ_NS = 1_000_000_000 / 16_000_000


async def init_dut(dut):
    clock = Clock(dut.clk, CLK_16MHZ_NS, units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    dut.lock.value = 1
    await FallingEdge(dut.clk)
    dut.lock.value = 0
    await FallingEdge(dut.clk)
    dut.lock.value = 1


@cocotb.test()
async def test_first(dut):
    """Try accessing the design."""
    await init_dut(dut)

    dut._log.info("dut.up_cnt is %s", dut.up_cnt.value)
    assert dut.up_cnt.value == 0

    await ClockCycles(dut.clk, 16 + 16 + (8 - 1), rising=False)
    dut._log.info("dut.up_cnt is %s", dut.up_cnt.value)
    assert dut.up_cnt.value == 0

    await FallingEdge(dut.clk)
    dut._log.info("dut.up_cnt is %s", dut.up_cnt.value)
    assert dut.up_cnt.value == 1
