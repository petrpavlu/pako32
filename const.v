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

`define ALU_A_SEL_RS1 0
`define ALU_A_SEL_PC 1

`define ALU_B_SEL_RS2 0
`define ALU_B_SEL_IMM 1

`define RD_SEL_ALU 0
`define RD_SEL_MEM 1

`define PC_NEXT_SEL_STALL 0
`define PC_NEXT_SEL_NEXT 1
`define PC_NEXT_SEL_PC_IMM 2
`define PC_NEXT_SEL_RS1_IMM 3
`define PC_NEXT_SEL_COND_PC_IMM 4

`define MEM_INSTR_ZERO 'h10000
`define MEM_DATA_ZERO 'h20000
`define MEM_USB_IO_ZERO 'h30000

`define MEM_ACCESS_BYTE 0
`define MEM_ACCESS_HALFWORD 1
`define MEM_ACCESS_WORD 2
