// Copyright (C) 2023 Michal Koutný <mkoutny@suse.com>
// SPDX-License-Identifier: MIT

module mem_instr
  (
    input logic clk_i,
    // read port
    input  logic [31:0] pc_i,
    output logic [15:0] pc_data_o
  );

  parameter PROG_FILE = "examples/calc/calc.text.txt";
  parameter SIZE   = 1024; // words
  parameter SIZE_B = 1024; // bytes
  // XXX BYTES_PER_WIDTH, INSTS_PER_WIDTH
  parameter WIDTH   = 8;    // bits

  logic [WIDTH-1:0] mem [SIZE-1:0];

  logic [7:0] inst_lo;
  logic [7:0] inst_hi;
 
  // initialization
  initial begin
    $readmemh(PROG_FILE, mem);
  end

  always_comb begin
    inst_lo = mem[pc_i];
    inst_hi = mem[pc_i + 1];
  end

  // reading
  always_ff @(posedge clk_i) begin
    if (pc_i >= SIZE_B)
      pc_data_o <= 16'd0;
    else begin
      pc_data_o <= {inst_hi, inst_lo};
    end
  end

  // no writing, readonly mem
endmodule


