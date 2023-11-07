# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.triggers import ReadOnly

import utils

@cocotb.test()
async def test_add(dut):
    """Addition sums two inputs."""

    dut.a.value = 1
    dut.b.value = 2
    dut.control.value = 0
    await ReadOnly()
    assert dut.result.value == 3
