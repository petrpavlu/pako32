# Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.triggers import Timer

import utils


@cocotb.test()
async def test_add(dut):
    """Check addition."""
    dut.a.value = 1
    dut.b.value = 2
    dut.control.value = 0
    await Timer(1)
    assert dut.result.value == 3


@cocotb.test()
async def test_sub(dut):
    """Check substraction."""
    dut.a.value = 1
    dut.b.value = 2
    dut.control.value = 1
    await Timer(1)
    assert dut.result.value == 0xffffffff


@cocotb.test()
async def test_and(dut):
    """Check bitwise and."""
    dut.a.value = 0b1010
    dut.b.value = 0b1100
    dut.control.value = 2
    await Timer(1)
    assert dut.result.value == 0b1000


@cocotb.test()
async def test_or(dut):
    """Check bitwise or."""
    dut.a.value = 0b1010
    dut.b.value = 0b1100
    dut.control.value = 3
    await Timer(1)
    assert dut.result.value == 0b1110


@cocotb.test()
async def test_xor(dut):
    """Check bitwise xor."""
    dut.a.value = 0b1010
    dut.b.value = 0b1100
    dut.control.value = 4
    await Timer(1)
    assert dut.result.value == 0b0110


@cocotb.test()
async def test_sll(dut):
    """Check logical shift left."""
    dut.a.value = 0xaaaaaaaa
    dut.b.value = 4
    dut.control.value = 5
    await Timer(1)
    assert dut.result.value == 0xaaaaaaa0


@cocotb.test()
async def test_srl(dut):
    """Check logical shift right."""
    dut.a.value = 0xaaaaaaaa
    dut.b.value = 4
    dut.control.value = 6
    await Timer(1)
    assert dut.result.value == 0x0aaaaaaa


@cocotb.test()
async def test_sra(dut):
    """Check arithmetic shift right."""
    dut.a.value = 0xaaaaaaaa
    dut.b.value = 4
    dut.control.value = 7
    await Timer(1)
    assert dut.result.value == 0xfaaaaaaa


@cocotb.test()
async def test_eq(dut):
    """Check equality comparison."""
    dut.a.value = 1
    dut.b.value = 2
    dut.control.value = 8
    await Timer(1)
    assert dut.result.value == 0

    dut.a.value = 1
    dut.b.value = 1
    dut.control.value = 8
    await Timer(1)
    assert dut.result.value == 1


@cocotb.test()
async def test_ne(dut):
    """Check inequality comparison."""
    dut.a.value = 1
    dut.b.value = 2
    dut.control.value = 9
    await Timer(1)
    assert dut.result.value == 1

    dut.a.value = 1
    dut.b.value = 1
    dut.control.value = 9
    await Timer(1)
    assert dut.result.value == 0


@cocotb.test()
async def test_lt(dut):
    """Check less-than comparison."""
    dut.a.value = 0xffffffff
    dut.b.value = 1
    dut.control.value = 10
    await Timer(1)
    assert dut.result.value == 1

    dut.a.value = 1
    dut.b.value = 1
    dut.control.value = 10
    await Timer(1)
    assert dut.result.value == 0


@cocotb.test()
async def test_ge(dut):
    """Check greater-equal comparison."""
    dut.a.value = 1
    dut.b.value = 0xffffffff
    dut.control.value = 11
    await Timer(1)
    assert dut.result.value == 1

    dut.a.value = 0
    dut.b.value = 1
    dut.control.value = 11
    await Timer(1)
    assert dut.result.value == 0


@cocotb.test()
async def test_ltu(dut):
    """Check less-than unsigned comparison."""
    dut.a.value = 0xffffffff
    dut.b.value = 1
    dut.control.value = 12
    await Timer(1)
    assert dut.result.value == 0

    dut.a.value = 0
    dut.b.value = 1
    dut.control.value = 12
    await Timer(1)
    assert dut.result.value == 1


@cocotb.test()
async def test_geu(dut):
    """Check greater-equal unsigned comparison."""
    dut.a.value = 1
    dut.b.value = 0xffffffff
    dut.control.value = 13
    await Timer(1)
    assert dut.result.value == 0

    dut.a.value = 1
    dut.b.value = 1
    dut.control.value = 13
    await Timer(1)
    assert dut.result.value == 1
