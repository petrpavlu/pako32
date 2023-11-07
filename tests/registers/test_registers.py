# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.triggers import FallingEdge

import utils

@cocotb.test()
async def test_reset(dut):
    """All registers are zero after the reset."""
    await utils.init_dut(dut)

    assert dut.regs.value == 31 * [0]

    for i in range(32):
        dut.rs1_idx_i.value = i
        dut.rs2_idx_i.value = i
        await FallingEdge(dut.clk_i)
        assert dut.rs1_data_o.value == 0
        assert dut.rs2_data_o.value == 0

@cocotb.test()
async def test_write_x0(dut):
    """Write to x0 is ignored."""
    await utils.init_dut(dut)

    dut.wr_en_i.value = 1;
    dut.rd_idx_i.value = 0
    dut.rd_data_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.wr_en_i.value = 0;
    assert dut.regs.value == 31 * [0]

    dut.rs1_idx_i.value = 0
    dut.rs2_idx_i.value = 0
    await FallingEdge(dut.clk_i)
    assert dut.rs1_data_o.value == 0
    assert dut.rs2_data_o.value == 0

@cocotb.test()
async def test_write_x1_x31(dut):
    """Write to x1..x31 works as expected."""
    await utils.init_dut(dut)

    for i in range(1, 32):
        dut.wr_en_i.value = 1;
        dut.rd_idx_i.value = i
        dut.rd_data_i.value = 0xa
        await FallingEdge(dut.clk_i)
        dut.wr_en_i.value = 0;
        assert dut.regs.value == (31 - i) * [0] + i * [0xa]

        dut.rs1_idx_i.value = i
        dut.rs2_idx_i.value = i
        await FallingEdge(dut.clk_i)
        assert dut.rs1_data_o.value == 0xa
        assert dut.rs2_data_o.value == 0xa

@cocotb.test()
async def test_write_without_en(dut):
    """Write without wr_en_i is ignored."""
    await utils.init_dut(dut)

    dut.wr_en_i.value = 0;
    dut.rd_idx_i.value = 0xa
    dut.rd_data_i.value = 1
    await FallingEdge(dut.clk_i)
    assert dut.regs.value == 31 * [0]

@cocotb.test()
async def test_read_independent(dut):
    """Read ports are independent."""
    await utils.init_dut(dut)

    dut.wr_en_i.value = 1;
    dut.rd_idx_i.value = 1
    dut.rd_data_i.value = 0xa
    await FallingEdge(dut.clk_i)
    dut.rd_idx_i.value = 2
    dut.rd_data_i.value = 0xb
    await FallingEdge(dut.clk_i)
    dut.wr_en_i.value = 0;
    assert dut.regs.value == 29 * [0] + [0xb, 0xa]

    dut.rs1_idx_i.value = 1
    dut.rs2_idx_i.value = 2
    await FallingEdge(dut.clk_i)
    assert dut.rs1_data_o.value == 0xa
    assert dut.rs2_data_o.value == 0xb

    dut.rs1_idx_i.value = 2
    dut.rs2_idx_i.value = 1
    await FallingEdge(dut.clk_i)
    assert dut.rs1_data_o.value == 0xb
    assert dut.rs2_data_o.value == 0xa
