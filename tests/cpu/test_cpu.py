# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.triggers import ClockCycles, FallingEdge

import utils


async def init_dut(dut):
    await utils.init_dut(dut)

    for i in range(8):
        dut.u_mem_instr.u_mem.mem_01[i].value = 0
        dut.u_mem_instr.u_mem.mem_23[i].value = 0


async def init_instr(dut, offset, instr):
    dut.u_mem_instr.u_mem.mem_01[offset / 4].value = (instr >> 0) & 0xffff
    dut.u_mem_instr.u_mem.mem_23[offset / 4].value = (instr >> 16) & 0xffff


@cocotb.test()
async def test_lui(dut):
    """Check LUI."""
    await init_dut(dut)
    await init_instr(dut, 0, 0xabcde0b7) # lui x1, 0xabcde

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 31 * [0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0xabcde000]


@cocotb.test()
async def test_luilui(dut):
    """Check LUI, followed by another LUI."""
    await init_dut(dut)
    await init_instr(dut, 0, 0xabcde0b7) # lui x1, 0xabcde
    await init_instr(dut, 4, 0xedcba0b7) # lui x1, 0xedcba

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 31 * [0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0xabcde000]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10008
    assert dut.pc_next.value == 0x1000c
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0xedcba000]


@cocotb.test()
async def test_auipc(dut):
    """Check AUIPC."""
    await init_dut(dut)
    await init_instr(dut, 0, 0xabcde097) # auipc x1, 0xabcde

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 31 * [0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0xabcee000]


@cocotb.test()
async def test_jal(dut):
    """Check JAL."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x010000ef) # jal x1, 0x10

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10010
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 31 * [0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10010
    assert dut.pc_next.value == 0x10014
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0x10004]


@cocotb.test()
async def test_jalr(dut):
    """Check JALR."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x010100e7) # jalr x1, x2, 0x10

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[2].value = 0x10010
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10020
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x10010, 0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10020
    assert dut.pc_next.value == 0x10024
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x10010, 0x10004]


@cocotb.test()
async def test_beq(dut):
    """Check BEQ."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x00208863) # beq x1, x2, 0x10
    await init_instr(dut, 4, 0x00418863) # beq x3, x4, 0x10

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x10
    dut.u_registers.regs[2].value = 0x11
    dut.u_registers.regs[3].value = 0x20
    dut.u_registers.regs[4].value = 0x20
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x20, 0x20, 0x11, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10014
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x20, 0x20, 0x11, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10014
    assert dut.pc_next.value == 0x10018
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x20, 0x20, 0x11, 0x10]


@cocotb.test()
async def test_beq_neg(dut):
    """Check BEQ with negative offset (sign extension)."""
    await init_dut(dut)
    await init_instr(dut, 0, 0xfe2088e3) # beq x1, x2, -0x10
    await init_instr(dut, 4, 0xfe4188e3) # beq x3, x4, -0x10

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x10
    dut.u_registers.regs[2].value = 0x11
    dut.u_registers.regs[3].value = 0x20
    dut.u_registers.regs[4].value = 0x20
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x20, 0x20, 0x11, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0xfff4
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x20, 0x20, 0x11, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0xfff4
    assert dut.pc_next.value == 0xfff8
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x20, 0x20, 0x11, 0x10]


@cocotb.test()
async def test_bne(dut):
    """Check BNE."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x00209863) # bne x1, x2, 0x10
    await init_instr(dut, 4, 0x00419863) # bne x3, x4, 0x10

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x10
    dut.u_registers.regs[2].value = 0x10
    dut.u_registers.regs[3].value = 0x20
    dut.u_registers.regs[4].value = 0x21
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x21, 0x20, 0x10, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10014
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x21, 0x20, 0x10, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10014
    assert dut.pc_next.value == 0x10018
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x21, 0x20, 0x10, 0x10]


@cocotb.test()
async def test_blt(dut):
    """Check BLT."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x0020c863) # blt x1, x2, 0x10
    await init_instr(dut, 4, 0x0041c863) # blt x3, x4, 0x10

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x10
    dut.u_registers.regs[2].value = 0x10
    dut.u_registers.regs[3].value = 0xffffffff
    dut.u_registers.regs[4].value = 0x20
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x20, 0xffffffff, 0x10, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10014
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x20, 0xffffffff, 0x10, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10014
    assert dut.pc_next.value == 0x10018
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x20, 0xffffffff, 0x10, 0x10]


@cocotb.test()
async def test_bge(dut):
    """Check BGE."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x0020d863) # bge x1, x2, 0x10
    await init_instr(dut, 4, 0x0041d863) # bge x3, x4, 0x10

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x10
    dut.u_registers.regs[2].value = 0x11
    dut.u_registers.regs[3].value = 0x20
    dut.u_registers.regs[4].value = 0xffffffff
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0xffffffff, 0x20, 0x11, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10014
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0xffffffff, 0x20, 0x11, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10014
    assert dut.pc_next.value == 0x10018
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0xffffffff, 0x20, 0x11, 0x10]


@cocotb.test()
async def test_bltu(dut):
    """Check BLTU."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x0020e863) # bltu x1, x2, 0x10
    await init_instr(dut, 4, 0x0041e863) # bltu x3, x4, 0x10

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x10
    dut.u_registers.regs[2].value = 0x10
    dut.u_registers.regs[3].value = 0x20
    dut.u_registers.regs[4].value = 0xffffffff
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0xffffffff, 0x20, 0x10, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10014
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0xffffffff, 0x20, 0x10, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10014
    assert dut.pc_next.value == 0x10018
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0xffffffff, 0x20, 0x10, 0x10]


@cocotb.test()
async def test_bgeu(dut):
    """Check BGEU."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x0020f863) # bgeu x1, x2, 0x10
    await init_instr(dut, 4, 0x0041f863) # bgeu x3, x4, 0x10

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x10
    dut.u_registers.regs[2].value = 0x11
    dut.u_registers.regs[3].value = 0xffffffff
    dut.u_registers.regs[4].value = 0x20
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x20, 0xffffffff, 0x11, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10014
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x20, 0xffffffff, 0x11, 0x10]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10014
    assert dut.pc_next.value == 0x10018
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 27 * [0] + [0x20, 0xffffffff, 0x11, 0x10]


@cocotb.test()
async def test_lb(dut):
    """Check LB."""
    await utils.init_dut(dut)
    await init_instr(dut, 0, 0x00710083) # lb x1, x2, 0x7

    dut.u_mem_control.u_mem.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem.mem_01[1].value = 0xef01
    dut.u_mem_control.u_mem.mem_23[1].value = 0xabcd

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]
    dut.u_registers.regs[2].value = 0x20000

    await FallingEdge(dut.clk_i)
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x20000, 0]

    retries = 5
    while dut.pc.value == 0x10000 and retries > 0:
        retries -= 1
        await FallingEdge(dut.clk_i)

    assert dut.pc.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x20000, 0xffffffab]


@cocotb.test()
async def test_lh(dut):
    """Check LH."""
    await utils.init_dut(dut)
    await init_instr(dut, 0, 0x00611083) # lh x1, x2, 0x6

    dut.u_mem_control.u_mem.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem.mem_01[1].value = 0xef01
    dut.u_mem_control.u_mem.mem_23[1].value = 0xabcd

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]
    dut.u_registers.regs[2].value = 0x20000

    await FallingEdge(dut.clk_i)
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x20000, 0]

    retries = 5
    while dut.pc.value == 0x10000 and retries > 0:
        retries -= 1
        await FallingEdge(dut.clk_i)

    assert dut.pc.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x20000, 0xffffabcd]


@cocotb.test()
async def test_lw(dut):
    """Check LW."""
    await utils.init_dut(dut)
    await init_instr(dut, 0, 0x00412083) # lw x1, x2, 0x4

    dut.u_mem_control.u_mem.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem.mem_01[1].value = 0xef01
    dut.u_mem_control.u_mem.mem_23[1].value = 0xabcd

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]
    dut.u_registers.regs[2].value = 0x20000

    await FallingEdge(dut.clk_i)
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x20000, 0]

    retries = 5
    while dut.pc.value == 0x10000 and retries > 0:
        retries -= 1
        await FallingEdge(dut.clk_i)

    assert dut.pc.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x20000, 0xabcdef01]


@cocotb.test()
async def test_lbu(dut):
    """Check LBU."""
    await utils.init_dut(dut)
    await init_instr(dut, 0, 0x00714083) # lbu x1, x2, 0x7

    dut.u_mem_control.u_mem.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem.mem_01[1].value = 0xef01
    dut.u_mem_control.u_mem.mem_23[1].value = 0xabcd

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]
    dut.u_registers.regs[2].value = 0x20000

    await FallingEdge(dut.clk_i)
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x20000, 0]

    retries = 5
    while dut.pc.value == 0x10000 and retries > 0:
        retries -= 1
        await FallingEdge(dut.clk_i)

    assert dut.pc.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x20000, 0x000000ab]


@cocotb.test()
async def test_lhu(dut):
    """Check LHU."""
    await utils.init_dut(dut)
    await init_instr(dut, 0, 0x00615083) # lhu x1, x2, 0x6

    dut.u_mem_control.u_mem.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem.mem_01[1].value = 0xef01
    dut.u_mem_control.u_mem.mem_23[1].value = 0xabcd

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]
    dut.u_registers.regs[2].value = 0x20000

    await FallingEdge(dut.clk_i)
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x20000, 0]

    retries = 5
    while dut.pc.value == 0x10000 and retries > 0:
        retries -= 1
        await FallingEdge(dut.clk_i)

    assert dut.pc.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x20000, 0x0000abcd]


@cocotb.test()
async def test_sb(dut):
    """Check SB."""
    await utils.init_dut(dut)
    await init_instr(dut, 0, 0x002083a3) # sb x2, 0x7(x1)

    dut.u_mem_control.u_mem.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem.mem_01[1].value = 0xbeef
    dut.u_mem_control.u_mem.mem_23[1].value = 0xdead

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]
    dut.u_registers.regs[1].value = 0x20000
    dut.u_registers.regs[2].value = 0xabcdef01

    await FallingEdge(dut.clk_i)
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xabcdef01, 0x20000]

    retries = 5
    while dut.pc.value == 0x10000 and retries > 0:
        retries -= 1
        await FallingEdge(dut.clk_i)

    assert dut.pc.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xabcdef01, 0x20000]

    print(dut.u_mem_control.u_mem.mem_01[1].value)
    print(dut.u_mem_control.u_mem.mem_23[1].value)
    assert dut.u_mem_control.u_mem.mem_01[1].value == 0xbeef
    assert dut.u_mem_control.u_mem.mem_23[1].value == 0x01ad


@cocotb.test()
async def test_sh(dut):
    """Check SH."""
    await utils.init_dut(dut)
    await init_instr(dut, 0, 0x00209323) # sh x2, 0x6(x1)

    dut.u_mem_control.u_mem.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem.mem_01[1].value = 0xbeef
    dut.u_mem_control.u_mem.mem_23[1].value = 0xdead

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]
    dut.u_registers.regs[1].value = 0x20000
    dut.u_registers.regs[2].value = 0xabcdef01

    await FallingEdge(dut.clk_i)
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xabcdef01, 0x20000]

    retries = 5
    while dut.pc.value == 0x10000 and retries > 0:
        retries -= 1
        await FallingEdge(dut.clk_i)

    assert dut.pc.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xabcdef01, 0x20000]

    assert dut.u_mem_control.u_mem.mem_01[1].value == 0xbeef
    assert dut.u_mem_control.u_mem.mem_23[1].value == 0xef01


@cocotb.test()
async def test_sw(dut):
    """Check SW."""
    await utils.init_dut(dut)
    await init_instr(dut, 0, 0x0020a223) # sw x2, 0x4(x1)

    dut.u_mem_control.u_mem.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem.mem_01[1].value = 0xbeef
    dut.u_mem_control.u_mem.mem_23[1].value = 0xdead

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]
    dut.u_registers.regs[1].value = 0x20000
    dut.u_registers.regs[2].value = 0xabcdef01

    await FallingEdge(dut.clk_i)
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xabcdef01, 0x20000]

    retries = 5
    while dut.pc.value == 0x10000 and retries > 0:
        retries -= 1
        await FallingEdge(dut.clk_i)

    assert dut.pc.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xabcdef01, 0x20000]

    assert dut.u_mem_control.u_mem.mem_01[1].value == 0xef01
    assert dut.u_mem_control.u_mem.mem_23[1].value == 0xabcd


@cocotb.test()
async def test_addi(dut):
    """Check ADDI."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x80008093) # addi x1, x1, -2048

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x400
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0x400]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0xfffffc00]


@cocotb.test()
async def test_slti(dut):
    """Check SLTI."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x80002093) # slti x1, x0, -2048
    await init_instr(dut, 4, 0x7ff02113) # slti x2, x0, 2047

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0xdeadbeef
    dut.u_registers.regs[2].value = 0xdeadbeef
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + 2 * [0xdeadbeef]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xdeadbeef, 0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10008
    assert dut.pc_next.value == 0x1000c
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [1, 0]


@cocotb.test()
async def test_sltiu(dut):
    """Check SLTIU."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x80003093) # sltiu x1, x0, -2048
    await init_instr(dut, 4, 0x00003113) # sltiu x2, x0, 0

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0xdeadbeef
    dut.u_registers.regs[2].value = 0xdeadbeef
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + 2 * [0xdeadbeef]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xdeadbeef, 1]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10008
    assert dut.pc_next.value == 0x1000c
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0, 1]


@cocotb.test()
async def test_xori(dut):
    """Check XORI."""
    await init_dut(dut)
    await init_instr(dut, 0, 0xabc0c093) # xori x1, x1, -(0x1000-0xabc)

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x12345678
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0x12345678]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0xedcbacc4]


@cocotb.test()
async def test_ori(dut):
    """Check ORI."""
    await init_dut(dut)
    await init_instr(dut, 0, 0xabc0e093) # ori x1, x1, -(0x1000-0xabc)

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x12345678
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0x12345678]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0xfffffefc]


@cocotb.test()
async def test_andi(dut):
    """Check ANDI."""
    await init_dut(dut)
    await init_instr(dut, 0, 0xabc0f093) # andi x1, x1, -(0x1000-0xabc)

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x12345678
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0x12345678]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0x12345238]


@cocotb.test()
async def test_slli(dut):
    """Check SLLI."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x00409093) # slli x1, x1, 4

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x87654321
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0x87654321]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0x76543210]


@cocotb.test()
async def test_srli(dut):
    """Check SRLI."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x0040d093) # srli x1, x1, 4

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x87654321
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0x87654321]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0x08765432]


@cocotb.test()
async def test_srai(dut):
    """Check SRAI."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x4040d093) # srai x1, x1, 4

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x87654321
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0x87654321]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 30 * [0] + [0xf8765432]


@cocotb.test()
async def test_add(dut):
    """Check ADD."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x002080b3) # add x1, x1, x2

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x400
    dut.u_registers.regs[2].value = 0x800
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x800, 0x400]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x800, 0x00000c00]


@cocotb.test()
async def test_sub(dut):
    """Check SUB."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x402080b3) # sub x1, x1, x2

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x400
    dut.u_registers.regs[2].value = 0x800
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x800, 0x400]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0x800, 0xfffffc00]


@cocotb.test()
async def test_sll(dut):
    """Check SLL."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x002090b3) # sll x1, x1, x2

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x87654321
    dut.u_registers.regs[2].value = 4
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [4, 0x87654321]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [4, 0x76543210]


@cocotb.test()
async def test_slt(dut):
    """Check SLT."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x001020b3) # slt x1, x0, x1
    await init_instr(dut, 4, 0x00202133) # slt x2, x0, x2

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0xfffff800 # -2048
    dut.u_registers.regs[2].value = 2047
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [2047, 0xfffff800]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [2047, 0]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10008
    assert dut.pc_next.value == 0x1000c
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [1, 0]


@cocotb.test()
async def test_sltu(dut):
    """Check SLTU."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x001030b3) # sltu x1, x0, x1
    await init_instr(dut, 4, 0x00203133) # sltu x2, x0, x2

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0xfffff800 # -2048
    dut.u_registers.regs[2].value = 0
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0, 0xfffff800]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0, 1]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10008
    assert dut.pc_next.value == 0x1000c
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0, 1]


@cocotb.test()
async def test_xor(dut):
    """Check XOR."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x0020c0b3) # xor x1, x1, x2

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x12345678
    dut.u_registers.regs[2].value = 0xfffffabc
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xfffffabc, 0x12345678]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xfffffabc, 0xedcbacc4]



@cocotb.test()
async def test_srl(dut):
    """Check SRL."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x0020d0b3) # srl x1, x1, x2

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x87654321
    dut.u_registers.regs[2].value = 4
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [4, 0x87654321]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [4, 0x08765432]


@cocotb.test()
async def test_sra(dut):
    """Check SRA."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x4020d0b3) # srai x1, x1, x2

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x87654321
    dut.u_registers.regs[2].value = 4
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [4, 0x87654321]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [4, 0xf8765432]


@cocotb.test()
async def test_or(dut):
    """Check OR."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x0020e0b3) # or x1, x1, x2

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x12345678
    dut.u_registers.regs[2].value = 0xfffffabc
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xfffffabc, 0x12345678]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xfffffabc, 0xfffffefc]


@cocotb.test()
async def test_and(dut):
    """Check AND."""
    await init_dut(dut)
    await init_instr(dut, 0, 0x0020f0b3) # and x1, x1, x2

    await ClockCycles(dut.clk_i, 2, rising=False)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10000
    assert dut.u_control.state == dut.u_control.ST_RESET.value
    assert dut.u_registers.regs.value == 31 * [0]

    dut.u_registers.regs[1].value = 0x12345678
    dut.u_registers.regs[2].value = 0xfffffabc
    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10000
    assert dut.pc_next.value == 0x10004
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xfffffabc, 0x12345678]

    await FallingEdge(dut.clk_i)
    assert dut.pc.value == 0x10004
    assert dut.pc_next.value == 0x10008
    assert dut.u_control.state == dut.u_control.ST_EXEC.value
    assert dut.u_registers.regs.value == 29 * [0] + [0xfffffabc, 0x12345238]
