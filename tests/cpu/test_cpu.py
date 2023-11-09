# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.triggers import ClockCycles, FallingEdge

import utils


async def init_dut(dut):
    await utils.init_dut(dut)

    for i in range(32):
        dut.u_mem_instr.mem[i].value = 0


@cocotb.test()
async def test_lui(dut):
    """Check LUI."""
    await init_dut(dut)

    # lui x1, 0xabcde
    dut.u_mem_instr.mem[0].value = 0xb7
    dut.u_mem_instr.mem[1].value = 0xe0
    dut.u_mem_instr.mem[2].value = 0xcd
    dut.u_mem_instr.mem[3].value = 0xab

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

    # auipc x1, 0xabcde
    dut.u_mem_instr.mem[0].value = 0x97
    dut.u_mem_instr.mem[1].value = 0xe0
    dut.u_mem_instr.mem[2].value = 0xcd
    dut.u_mem_instr.mem[3].value = 0xab

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

    # jal x1, 0x10
    dut.u_mem_instr.mem[0].value = 0xef
    dut.u_mem_instr.mem[1].value = 0x00
    dut.u_mem_instr.mem[2].value = 0x00
    dut.u_mem_instr.mem[3].value = 0x01

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

    # jalr x1, x2, 0x10
    dut.u_mem_instr.mem[0].value = 0xe7
    dut.u_mem_instr.mem[1].value = 0x00
    dut.u_mem_instr.mem[2].value = 0x01
    dut.u_mem_instr.mem[3].value = 0x01

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

    # beq x1, x2, 0x10
    dut.u_mem_instr.mem[0].value = 0x63
    dut.u_mem_instr.mem[1].value = 0x88
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x00

    # beq x3, x4, 0x10
    dut.u_mem_instr.mem[4].value = 0x63
    dut.u_mem_instr.mem[5].value = 0x88
    dut.u_mem_instr.mem[6].value = 0x41
    dut.u_mem_instr.mem[7].value = 0x00

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
async def test_bne(dut):
    """Check BNE."""
    await init_dut(dut)

    # bne x1, x2, 0x10
    dut.u_mem_instr.mem[0].value = 0x63
    dut.u_mem_instr.mem[1].value = 0x98
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x00

    # bne x3, x4, 0x10
    dut.u_mem_instr.mem[4].value = 0x63
    dut.u_mem_instr.mem[5].value = 0x98
    dut.u_mem_instr.mem[6].value = 0x41
    dut.u_mem_instr.mem[7].value = 0x00

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

    # blt x1, x2, 0x10
    dut.u_mem_instr.mem[0].value = 0x63
    dut.u_mem_instr.mem[1].value = 0xc8
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x00

    # blt x3, x4, 0x10
    dut.u_mem_instr.mem[4].value = 0x63
    dut.u_mem_instr.mem[5].value = 0xc8
    dut.u_mem_instr.mem[6].value = 0x41
    dut.u_mem_instr.mem[7].value = 0x00

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

    # bge x1, x2, 0x10
    dut.u_mem_instr.mem[0].value = 0x63
    dut.u_mem_instr.mem[1].value = 0xd8
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x00

    # bge x3, x4, 0x10
    dut.u_mem_instr.mem[4].value = 0x63
    dut.u_mem_instr.mem[5].value = 0xd8
    dut.u_mem_instr.mem[6].value = 0x41
    dut.u_mem_instr.mem[7].value = 0x00

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

    # bltu x1, x2, 0x10
    dut.u_mem_instr.mem[0].value = 0x63
    dut.u_mem_instr.mem[1].value = 0xe8
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x00

    # bltu x3, x4, 0x10
    dut.u_mem_instr.mem[4].value = 0x63
    dut.u_mem_instr.mem[5].value = 0xe8
    dut.u_mem_instr.mem[6].value = 0x41
    dut.u_mem_instr.mem[7].value = 0x00

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

    # bgeu x1, x2, 0x10
    dut.u_mem_instr.mem[0].value = 0x63
    dut.u_mem_instr.mem[1].value = 0xf8
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x00

    # bgeu x3, x4, 0x10
    dut.u_mem_instr.mem[4].value = 0x63
    dut.u_mem_instr.mem[5].value = 0xf8
    dut.u_mem_instr.mem[6].value = 0x41
    dut.u_mem_instr.mem[7].value = 0x00

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
    """Check LW."""
    await utils.init_dut(dut)

    # lb x1, x2, 0x7
    dut.u_mem_instr.mem[0].value = 0x83
    dut.u_mem_instr.mem[1].value = 0x00
    dut.u_mem_instr.mem[2].value = 0x71
    dut.u_mem_instr.mem[3].value = 0x00

    dut.u_mem_control.u_mem_data.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem_data.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem_data.mem_01[1].value = 0xef01
    dut.u_mem_control.u_mem_data.mem_23[1].value = 0xabcd

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
    """Check LW."""
    await utils.init_dut(dut)

    # lh x1, x2, 0x6
    dut.u_mem_instr.mem[0].value = 0x83
    dut.u_mem_instr.mem[1].value = 0x10
    dut.u_mem_instr.mem[2].value = 0x61
    dut.u_mem_instr.mem[3].value = 0x00

    dut.u_mem_control.u_mem_data.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem_data.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem_data.mem_01[1].value = 0xef01
    dut.u_mem_control.u_mem_data.mem_23[1].value = 0xabcd

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

    # lw x1, x2, 0x4
    dut.u_mem_instr.mem[0].value = 0x83
    dut.u_mem_instr.mem[1].value = 0x20
    dut.u_mem_instr.mem[2].value = 0x41
    dut.u_mem_instr.mem[3].value = 0x00

    dut.u_mem_control.u_mem_data.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem_data.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem_data.mem_01[1].value = 0xef01
    dut.u_mem_control.u_mem_data.mem_23[1].value = 0xabcd

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
    """Check LW."""
    await utils.init_dut(dut)

    # lb x1, x2, 0x7
    dut.u_mem_instr.mem[0].value = 0x83
    dut.u_mem_instr.mem[1].value = 0x40
    dut.u_mem_instr.mem[2].value = 0x71
    dut.u_mem_instr.mem[3].value = 0x00

    dut.u_mem_control.u_mem_data.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem_data.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem_data.mem_01[1].value = 0xef01
    dut.u_mem_control.u_mem_data.mem_23[1].value = 0xabcd

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
    """Check LW."""
    await utils.init_dut(dut)

    # lh x1, x2, 0x6
    dut.u_mem_instr.mem[0].value = 0x83
    dut.u_mem_instr.mem[1].value = 0x50
    dut.u_mem_instr.mem[2].value = 0x61
    dut.u_mem_instr.mem[3].value = 0x00

    dut.u_mem_control.u_mem_data.mem_01[0].value = 0xbeef
    dut.u_mem_control.u_mem_data.mem_23[0].value = 0xdead
    dut.u_mem_control.u_mem_data.mem_01[1].value = 0xef01
    dut.u_mem_control.u_mem_data.mem_23[1].value = 0xabcd

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
async def test_addi(dut):
    """Check ADDI."""
    await init_dut(dut)

    # addi x1, x1, -2048
    dut.u_mem_instr.mem[0].value = 0x93
    dut.u_mem_instr.mem[1].value = 0x80
    dut.u_mem_instr.mem[2].value = 0x00
    dut.u_mem_instr.mem[3].value = 0x80

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

    # slti x1, x0, -2048
    dut.u_mem_instr.mem[0].value = 0x93
    dut.u_mem_instr.mem[1].value = 0x20
    dut.u_mem_instr.mem[2].value = 0x00
    dut.u_mem_instr.mem[3].value = 0x80

    # slti x2, x0, 2047
    dut.u_mem_instr.mem[4].value = 0x13
    dut.u_mem_instr.mem[5].value = 0x21
    dut.u_mem_instr.mem[6].value = 0xf0
    dut.u_mem_instr.mem[7].value = 0x7f

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

    # sltiu x1, x0, -2048
    dut.u_mem_instr.mem[0].value = 0x93
    dut.u_mem_instr.mem[1].value = 0x30
    dut.u_mem_instr.mem[2].value = 0x00
    dut.u_mem_instr.mem[3].value = 0x80

    # sltiu x2, x0, 0
    dut.u_mem_instr.mem[4].value = 0x13
    dut.u_mem_instr.mem[5].value = 0x31
    dut.u_mem_instr.mem[6].value = 0x00
    dut.u_mem_instr.mem[7].value = 0x00

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

    # xori x1, x1, -(0x1000-0xabc)
    dut.u_mem_instr.mem[0].value = 0x93
    dut.u_mem_instr.mem[1].value = 0xc0
    dut.u_mem_instr.mem[2].value = 0xc0
    dut.u_mem_instr.mem[3].value = 0xab

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

    # ori x1, x1, -(0x1000-0xabc)
    dut.u_mem_instr.mem[0].value = 0x93
    dut.u_mem_instr.mem[1].value = 0xe0
    dut.u_mem_instr.mem[2].value = 0xc0
    dut.u_mem_instr.mem[3].value = 0xab

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

    # andi x1, x1, -(0x1000-0xabc)
    dut.u_mem_instr.mem[0].value = 0x93
    dut.u_mem_instr.mem[1].value = 0xf0
    dut.u_mem_instr.mem[2].value = 0xc0
    dut.u_mem_instr.mem[3].value = 0xab

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

    # slli x1, x1, 4
    dut.u_mem_instr.mem[0].value = 0x93
    dut.u_mem_instr.mem[1].value = 0x90
    dut.u_mem_instr.mem[2].value = 0x40
    dut.u_mem_instr.mem[3].value = 0x00

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

    # srli x1, x1, 4
    dut.u_mem_instr.mem[0].value = 0x93
    dut.u_mem_instr.mem[1].value = 0xd0
    dut.u_mem_instr.mem[2].value = 0x40
    dut.u_mem_instr.mem[3].value = 0x00

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

    # srai x1, x1, 4
    dut.u_mem_instr.mem[0].value = 0x93
    dut.u_mem_instr.mem[1].value = 0xd0
    dut.u_mem_instr.mem[2].value = 0x40
    dut.u_mem_instr.mem[3].value = 0x40

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

    # add x1, x1, x2
    dut.u_mem_instr.mem[0].value = 0xb3
    dut.u_mem_instr.mem[1].value = 0x80
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x00

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

    # sub x1, x1, x2
    dut.u_mem_instr.mem[0].value = 0xb3
    dut.u_mem_instr.mem[1].value = 0x80
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x40

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

    # sll x1, x1, x2
    dut.u_mem_instr.mem[0].value = 0xb3
    dut.u_mem_instr.mem[1].value = 0x90
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x00

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

    # slt x1, x0, x1
    dut.u_mem_instr.mem[0].value = 0xb3
    dut.u_mem_instr.mem[1].value = 0x20
    dut.u_mem_instr.mem[2].value = 0x10
    dut.u_mem_instr.mem[3].value = 0x00

    # slt x2, x0, x2
    dut.u_mem_instr.mem[4].value = 0x33
    dut.u_mem_instr.mem[5].value = 0x21
    dut.u_mem_instr.mem[6].value = 0x20
    dut.u_mem_instr.mem[7].value = 0x00

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

    # sltu x1, x0, x1
    dut.u_mem_instr.mem[0].value = 0xb3
    dut.u_mem_instr.mem[1].value = 0x30
    dut.u_mem_instr.mem[2].value = 0x10
    dut.u_mem_instr.mem[3].value = 0x00

    # sltu x2, x0, x2
    dut.u_mem_instr.mem[4].value = 0x33
    dut.u_mem_instr.mem[5].value = 0x31
    dut.u_mem_instr.mem[6].value = 0x20
    dut.u_mem_instr.mem[7].value = 0x00

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

    # xor x1, x1, x2
    dut.u_mem_instr.mem[0].value = 0xb3
    dut.u_mem_instr.mem[1].value = 0xc0
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x00

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

    # srl x1, x1, x2
    dut.u_mem_instr.mem[0].value = 0xb3
    dut.u_mem_instr.mem[1].value = 0xd0
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x00

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

    # srai x1, x1, x2
    dut.u_mem_instr.mem[0].value = 0xb3
    dut.u_mem_instr.mem[1].value = 0xd0
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x40

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

    # or x1, x1, x2
    dut.u_mem_instr.mem[0].value = 0xb3
    dut.u_mem_instr.mem[1].value = 0xe0
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x00

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

    # and x1, x1, x2
    dut.u_mem_instr.mem[0].value = 0xb3
    dut.u_mem_instr.mem[1].value = 0xf0
    dut.u_mem_instr.mem[2].value = 0x20
    dut.u_mem_instr.mem[3].value = 0x00

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
