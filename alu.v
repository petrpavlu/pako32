// Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
// SPDX-License-Identifier: MIT

`include "const.v"

module alu
  (
    input logic [31:0] a,
    input logic [31:0] b,
    input logic [3:0] control,
    output logic [31:0] result
  );

  always_comb begin
    case (control)
      `ALU_OP_ADD: result = a + b;
      `ALU_OP_SUB: result = a - b;
      `ALU_OP_AND: result = a & b;
      `ALU_OP_OR:  result = a | b;
      `ALU_OP_XOR: result = a ^ b;
      `ALU_OP_SLL: result = a << b;
      `ALU_OP_SRL: result = a >> b;
      `ALU_OP_SRA: result = signed'(a) >>> b;
      `ALU_OP_EQ:  result = a == b;
      `ALU_OP_NE:  result = a != b;
      `ALU_OP_LT:  result = signed'(a) < signed'(b);
      `ALU_OP_GE:  result = signed'(a) >= signed'(b);
      `ALU_OP_LTU: result = a < b;
      `ALU_OP_GEU: result = a >= b;
      default: result = 'x;
    endcase
  end
endmodule
