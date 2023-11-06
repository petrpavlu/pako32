// Copyright (C) 2023 Michal Koutný <mkoutny@suse.com>
// SPDX-License-Identifier: MIT

module registers
  (
    input logic clk_i,
    input logic rstn_i,
    // write port
    input  logic        wr_en_i,
    input  logic [4:0]  rd_idx_i,
    input  logic [31:0] rd_data_i,
    // read port 1
    input  logic [4:0]  rs1_idx_i,
    output logic [31:0] rs1_data_o,
    // read port 2
    input  logic [4:0]  rs2_idx_i,
    output logic [31:0] rs2_data_o
  );

  logic [31:0] regs [31:1];

  // reading
  always_comb begin
    if (rs1_idx_i == 5'd0)
       rs1_data_o = 32'd0;
    else
       rs1_data_o = regs[rs1_idx_i];

    if (rs2_idx_i == 5'd0)
       rs2_data_o = 32'd0;
    else
       rs2_data_o = regs[rs2_idx_i];
  end

  // writing & reset
  always_ff @(posedge clk_i or negedge rstn_i) begin
    if (~rstn_i) begin
       // initialization
       for (int i = 1; i <= 31; i++) begin
         regs[i] <= 32'd0;
       end
    end
    else if (wr_en_i && rd_idx_i != 5'd0)
       regs[rd_idx_i] <= rd_data_i;
  end
endmodule


