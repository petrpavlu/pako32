// Copyright (C) 2023 Michal Koutný <mkoutny@suse.com>
// SPDX-License-Identifier: MIT

`include "const.v"

module mem_data
  (
    input logic clk_i,
    // read port
    input  logic        r_en_i,
    input  logic [31:0] addr_r_i,
    output logic [31:0] data_r_o,

    // write port
    input  logic        wr_en_i,
    input  logic [31:0] addr_w_i,
    input  logic [31:0] data_w_i
  );

  // Datafiles contain 16b values
  parameter DATA_FILE_01 = "";
  parameter DATA_FILE_23 = "";
  parameter ROWS      = 512;

  logic [15:0] mem_01 [ROWS-1:0];
  logic [15:0] mem_23 [ROWS-1:0];

  logic [31:0] addr_r, addr_w;

  initial begin
    if (DATA_FILE_01 != "" && DATA_FILE_23 != "") begin
      $readmemh(DATA_FILE_01, mem_01, 0, ROWS - 1);
      $readmemh(DATA_FILE_23, mem_23, 0, ROWS - 1);
    end
  end
 
  always_comb begin
    addr_r = addr_r_i >> 2;
    addr_w = addr_w_i >> 2;
  end

  always_ff @(posedge clk_i) begin
    if (wr_en_i) begin
      mem_23[addr_w] <= data_w_i[31:16];
      mem_01[addr_w] <= data_w_i[15:0];
    end
    if (r_en_i) begin
      data_r_o <= {mem_23[addr_r], mem_01[addr_r]};
    end
  end

endmodule


