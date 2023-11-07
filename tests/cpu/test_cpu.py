# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.triggers import ClockCycles, FallingEdge

import utils


@cocotb.test()
async def test_lui(dut):
    """Check LUI."""
    await utils.init_dut(dut)

    # lui x1, 0xabcde
    dut.u_mem_instr.mem[0].value = 0xb7
    dut.u_mem_instr.mem[1].value = 0xe0
    dut.u_mem_instr.mem[2].value = 0xcd
    dut.u_mem_instr.mem[3].value = 0xab

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.u_registers.regs.value == 31 * [0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.u_registers.regs.value == 30 * [0] + [0xabcde000]

@cocotb.test()
async def test_luilui(dut):
    """Check LUI."""
    await utils.init_dut(dut)

    # lui x1, 0xabcde
    dut.u_mem_instr.mem[0].value = 0xb7
    dut.u_mem_instr.mem[1].value = 0xe0
    dut.u_mem_instr.mem[2].value = 0xcd
    dut.u_mem_instr.mem[3].value = 0xab

    # lui x1, 0xedcba
    dut.u_mem_instr.mem[4].value = 0xb7
    dut.u_mem_instr.mem[5].value = 0xa0
    dut.u_mem_instr.mem[6].value = 0xcb
    dut.u_mem_instr.mem[7].value = 0xed

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.u_registers.regs.value == 31 * [0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.u_registers.regs.value == 30 * [0] + [0xabcde000]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10008
    assert dut.u_registers.regs.value == 30 * [0] + [0xedcba000]
