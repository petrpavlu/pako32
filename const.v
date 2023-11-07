// Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
// SPDX-License-Identifier: MIT

`define ALU_OP_ADD 0
`define ALU_OP_SUB 1
`define ALU_OP_AND 2
`define ALU_OP_OR 3
`define ALU_OP_XOR 4
`define ALU_OP_SLL 5
`define ALU_OP_SRL 6
`define ALU_OP_SRA 7
`define ALU_OP_EQ 8
`define ALU_OP_NE 9
`define ALU_OP_LT 10
`define ALU_OP_GE 11
`define ALU_OP_LTU 12
`define ALU_OP_GEU 13

`define MEM_INSTR_ZERO 'h10000
