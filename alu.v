// Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
// SPDX-License-Identifier: MIT

`include "const.v"

module alu
  (
    input logic [31:0] a,
    input logic [31:0] b,
    input logic [3:0] op,
    output logic [31:0] res
  );

  always_comb begin
    case (op)
      `ALU_OP_ADD: res = a + b;
      `ALU_OP_SUB: res = a - b;
      `ALU_OP_AND: res = a & b;
      `ALU_OP_OR:  res = a | b;
      `ALU_OP_XOR: res = a ^ b;
      `ALU_OP_SLL: res = a << b;
      `ALU_OP_SRL: res = a >> b;
      `ALU_OP_SRA: res = signed'(a) >>> b;
      `ALU_OP_EQ:  res = a == b;
      `ALU_OP_NE:  res = a != b;
      `ALU_OP_LT:  res = signed'(a) < signed'(b);
      `ALU_OP_GE:  res = signed'(a) >= signed'(b);
      `ALU_OP_LTU: res = a < b;
      `ALU_OP_GEU: res = a >= b;
      default: res = 'x;
    endcase
  end
endmodule
