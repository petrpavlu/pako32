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
    await utils.init_dut(dut)

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
async def test_addi(dut):
    """Check ADDI."""
    await utils.init_dut(dut)

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
    await utils.init_dut(dut)

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
    await utils.init_dut(dut)

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
    await utils.init_dut(dut)

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
    await utils.init_dut(dut)

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
    await utils.init_dut(dut)

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
    await utils.init_dut(dut)

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
    await utils.init_dut(dut)

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
    await utils.init_dut(dut)

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
