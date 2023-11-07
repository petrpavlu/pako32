// Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
// SPDX-License-Identifier: MIT

`include "const.v"

module alu
  (
    input logic [31:0] a,
    input logic [31:0] b,
    input logic [2:0] control,
    output logic [31:0] result
  );

  always_comb begin
    case (control)
      `ALU_OP_ADD: result = a + b;
    endcase
  end
endmodule
