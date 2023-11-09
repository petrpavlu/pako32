# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.triggers import FallingEdge

import utils


@cocotb.test(skip=True)
async def test_init_read(dut):
    """Read data from initialization."""
    await utils.init_dut_noreset(dut)
    # This test is skipped because it would need pass parameters:
    # dut.DATA_FILE_01=./data.txt01
    # dut.DATA_FILE_02=./data.txt02

    dut.addr_r_i.value = 0
    await FallingEdge(dut.clk_i)
    assert dut.data_r_o.value == 0x203e


@cocotb.test()
async def test_write_32B(dut):
    """Writes to first 32B work as expected."""
    await utils.init_dut_noreset(dut)

    for i in range(0, 32, 4):
        dut.wr_en_i.value = 1
        dut.addr_w_i.value = i
        dut.data_w_i.value = 0x12345678
        await FallingEdge(dut.clk_i)
        dut.wr_en_i.value = 0

        dut.r_en_i.value = 1
        dut.addr_r_i.value = i
        await FallingEdge(dut.clk_i)
        assert dut.data_r_o.value == 0x12345678
        dut.r_en_i.value = 0


@cocotb.test()
async def test_write_without_en(dut):
    """Write without wr_en_i is ignored."""
    await utils.init_dut_noreset(dut)

    dut.wr_en_i.value = 0
    dut.addr_w_i.value = 2
    dut.data_w_i.value = 0xa
    await FallingEdge(dut.clk_i)
    assert dut.data_r_o.value != 0xa 
