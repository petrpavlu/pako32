// Copyright (C) 2023 Michal Koutný <mkoutny@suse.com>
// SPDX-License-Identifier: MIT

`include "const.v"

module mem_instr
  (
    input logic clk_i,
    // read port
    input  logic [31:0] pc_i,
    output logic [31:0] pc_data_o
  );

  parameter PROG_FILE = "examples/calc/calc.text.txt";
  parameter SIZE   = 1024; // words
  parameter SIZE_B = 1024; // bytes
  // XXX BYTES_PER_WIDTH, INSTS_PER_WIDTH
  parameter WIDTH   = 8;    // bits

  logic [WIDTH-1:0] mem [SIZE-1:0];
  logic [31:0] pc_phys;

  // initialization
  initial begin
    $readmemh(PROG_FILE, mem, 0, SIZE);
  end
  always_comb begin
    pc_phys = pc_i - `MEM_INSTR_ZERO;
  end

  // reading
  always_ff @(posedge clk_i) begin
    if (pc_phys < 0 ||  pc_phys >= SIZE_B)
      pc_data_o <= 32'd0;
    else begin
      pc_data_o <= {mem[pc_phys + 3], mem[pc_phys + 2], mem[pc_phys + 1], mem[pc_phys + 0]};
    end
  end

  // no writing, readonly mem
endmodule


