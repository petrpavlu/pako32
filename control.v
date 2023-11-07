// Copyright (C) 2023 Michal Koutný <mkoutny@suse.com>
// SPDX-License-Identifier: MIT

`include "const.v"

module control
  (
    //input logic clk_i,
    //input logic rstn_i, // XXX for internal state
    input logic [15:0] pc_data_i,

    output  logic        wr_en_o,
    output  logic [4:0]  rd_idx_o,

    output  logic [4:0]  rs1_idx_o,
    //output  logic [4:0]  rs2_idx_o,

    output  logic [31:0] imm_data_o,
    output  logic [3:0] alu_ctrl_o,
    output  logic alu_input_o, // 0: imm, 1: rs2
    output  logic reg_input_o // 0: alu, 1: mem
  );

  logic [6:0] opcode;

  always_comb begin
    opcode = pc_data_i[6:0];
    case (opcode)
    7'b0110111: begin // LUI
      wr_en_o = 1;
      rd_idx_o = pc_data_i[11:7];
      imm_data_o = {pc_data_i[31:12], 12'h000};
      rs1_idx_o = 0;
      alu_ctrl_o = `ALU_OP_ADD;
      alu_input_o = 0;
      reg_input_o = 0;
      end
    default: begin// fallback
      wr_en_o = 0;
      rd_idx_o = 0;
      imm_data_o = 0;
      rs1_idx_o = 0;
      alu_ctrl_o = `ALU_OP_ADD;
      alu_input_o = 0;
      reg_input_o = 0;
      end
    endcase
  end

endmodule


