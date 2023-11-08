# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.triggers import ClockCycles, FallingEdge

import utils


@cocotb.test()
async def test_read_byte(dut):
    """Check read of a byte."""
    await utils.init_dut(dut)

    dut.u_mem_data.mem_01[1].value = 0x4321
    dut.u_mem_data.mem_23[1].value = 0x8765

    assert dut.state.value == dut.ST_RESET
    assert dut.wr_ready_o.value == 0

    await FallingEdge(dut.clk_i)
    assert dut.state.value == dut.ST_READY
    assert dut.wr_ready_o.value == 1

    dut.acc_r_i.value = 0 # MEM_ACCESS_BYTE
    dut.addr_r_i.value = 0x4
    await FallingEdge(dut.clk_i)
    assert dut.data_r_o.value == 0x21

    dut.acc_r_i.value = 0 # MEM_ACCESS_BYTE
    dut.addr_r_i.value = 0x5
    await FallingEdge(dut.clk_i)
    assert dut.data_r_o.value == 0x43

    dut.acc_r_i.value = 0 # MEM_ACCESS_BYTE
    dut.addr_r_i.value = 0x6
    await FallingEdge(dut.clk_i)
    assert dut.data_r_o.value == 0x65

    dut.acc_r_i.value = 0 # MEM_ACCESS_BYTE
    dut.addr_r_i.value = 0x7
    await FallingEdge(dut.clk_i)
    assert dut.data_r_o.value == 0xffffff87


@cocotb.test()
async def test_read_halfword(dut):
    """Check read of a halfword."""
    await utils.init_dut(dut)

    dut.u_mem_data.mem_01[1].value = 0x4321
    dut.u_mem_data.mem_23[1].value = 0x8765

    assert dut.state.value == dut.ST_RESET
    assert dut.wr_ready_o.value == 0

    await FallingEdge(dut.clk_i)
    assert dut.state.value == dut.ST_READY
    assert dut.wr_ready_o.value == 1

    dut.acc_r_i.value = 1 # MEM_ACCESS_HALFWORD
    dut.addr_r_i.value = 0x4
    await FallingEdge(dut.clk_i)
    assert dut.data_r_o.value == 0x4321

    dut.acc_r_i.value = 1 # MEM_ACCESS_HALFWORD
    dut.addr_r_i.value = 0x6
    await FallingEdge(dut.clk_i)
    assert dut.data_r_o.value == 0xffff8765


@cocotb.test()
async def test_read_word(dut):
    """Check read of a word."""
    await utils.init_dut(dut)

    dut.u_mem_data.mem_01[1].value = 0x4321
    dut.u_mem_data.mem_23[1].value = 0x8765

    assert dut.state.value == dut.ST_RESET
    assert dut.wr_ready_o.value == 0

    await FallingEdge(dut.clk_i)
    assert dut.state.value == dut.ST_READY
    assert dut.wr_ready_o.value == 1

    dut.acc_r_i.value = 2 # MEM_ACCESS_WORD
    dut.addr_r_i.value = 0x4
    await FallingEdge(dut.clk_i)
    assert dut.data_r_o.value == 0x87654321


@cocotb.test()
async def test_write_halfword(dut):
    """Check write of a halfword."""
    await utils.init_dut(dut)

    dut.u_mem_data.mem_01[1].value = 0xdead
    dut.u_mem_data.mem_23[1].value = 0xbeef

    assert dut.state.value == dut.ST_RESET
    assert dut.wr_ready_o.value == 0

    await FallingEdge(dut.clk_i)
    assert dut.state.value == dut.ST_READY
    assert dut.wr_ready_o.value == 1

    dut.wr_en_i.value = 1
    dut.acc_w_i.value = 1 # MEM_ACCESS_HALFWORD
    dut.addr_w_i.value = 0x4
    dut.data_w_i.value = 0x4321
    await FallingEdge(dut.clk_i)
    assert dut.u_mem_data.mem_01[1].value == 0xdead
    assert dut.u_mem_data.mem_23[1].value == 0xbeef
    await FallingEdge(dut.clk_i)
    dut.wr_en_i.value = 0
    assert dut.u_mem_data.mem_01[1].value == 0x4321
    assert dut.u_mem_data.mem_23[1].value == 0xbeef

    dut.wr_en_i.value = 1
    dut.acc_w_i.value = 1 # MEM_ACCESS_HALFWORD
    dut.addr_w_i.value = 0x6
    dut.data_w_i.value = 0x8765
    await FallingEdge(dut.clk_i)
    assert dut.u_mem_data.mem_01[1].value == 0x4321
    assert dut.u_mem_data.mem_23[1].value == 0xbeef
    await FallingEdge(dut.clk_i)
    dut.wr_en_i.value = 0
    assert dut.u_mem_data.mem_01[1].value == 0x4321
    assert dut.u_mem_data.mem_23[1].value == 0x8765


@cocotb.test()
async def test_write_word(dut):
    """Check write of a word."""
    await utils.init_dut(dut)

    dut.u_mem_data.mem_01[1].value = 0xdead
    dut.u_mem_data.mem_23[1].value = 0xbeef

    assert dut.state.value == dut.ST_RESET
    assert dut.wr_ready_o.value == 0

    await FallingEdge(dut.clk_i)
    assert dut.state.value == dut.ST_READY
    assert dut.wr_ready_o.value == 1

    dut.wr_en_i.value = 1
    dut.acc_w_i.value = 2 # MEM_ACCESS_WORD
    dut.addr_w_i.value = 0x4
    dut.data_w_i.value = 0x87654321
    await FallingEdge(dut.clk_i)
    assert dut.u_mem_data.mem_01[1].value == 0xdead
    assert dut.u_mem_data.mem_23[1].value == 0xbeef
    await FallingEdge(dut.clk_i)
    dut.wr_en_i.value = 0
    assert dut.u_mem_data.mem_01[1].value == 0x4321
    assert dut.u_mem_data.mem_23[1].value == 0x8765


@cocotb.test()
async def test_write_32B(dut):
    """Writes to first 32B work as expected."""
    await utils.init_dut(dut)

    assert dut.state.value == dut.ST_RESET
    assert dut.wr_ready_o.value == 0

    await FallingEdge(dut.clk_i)
    assert dut.state.value == dut.ST_READY
    assert dut.wr_ready_o.value == 1

    for i in range(0, 32, 4):
        dut.wr_en_i.value = 1
        dut.acc_w_i.value = 2 # MEM_ACCESS_WORD
        dut.addr_w_i.value = i
        dut.data_w_i.value = 0x12345678
        await FallingEdge(dut.clk_i)
        assert dut.state.value == dut.ST_WRITE_PENDING
        assert dut.wr_ready_o.value == 0

        await FallingEdge(dut.clk_i)
        dut.wr_en_i.value = 0
        assert dut.state.value == dut.ST_READY
        assert dut.wr_ready_o.value == 1

        dut.acc_r_i.value = 2 # MEM_ACCESS_WORD
        dut.addr_r_i.value = i
        await FallingEdge(dut.clk_i)
        assert dut.data_r_o.value == 0x12345678
        assert dut.state.value == dut.ST_READY
        assert dut.wr_ready_o.value == 1
