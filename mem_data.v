// Copyright (C) 2023 Michal Koutný <mkoutny@suse.com>
// SPDX-License-Identifier: MIT

`include "const.v"

module mem_data
  (
    input logic clk_i,
    // read port
    input  logic [31:0] addr_r_i,
    output logic [31:0] data_r_o,

    // write port
    input  logic        wr_en_i,
    input  logic [31:0] addr_w_i,
    input  logic [31:0] data_w_i
  );

  parameter DATA_FILE = "";
  parameter ROWS      = 512;

  logic [15:0] mem_01 [ROWS-1:0];
  logic [15:0] mem_23 [ROWS-1:0];

  logic [31:0] addr_r, addr_w;

  // TODO init
 
  always_comb begin
    addr_r = addr_r_i >> 2;
    addr_w = addr_w_i >> 2;
  end

  always_ff @(posedge clk_i) begin
    if (wr_en_i) begin
      mem_23[addr_w] <= data_w_i[31:16];
      mem_01[addr_w] <= data_w_i[15:0];
    end
    data_r_o <= {mem_23[addr_r], mem_01[addr_r]};
  end

endmodule


