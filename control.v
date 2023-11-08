// Copyright (C) 2023 Michal Koutný <mkoutny@suse.com>
// SPDX-License-Identifier: MIT

`include "const.v"

module control
  (
    input logic clk_i,
    input logic rstn_i,
    input logic [31:0] pc_data_i,

    output  logic        wr_en_o,
    output  logic [4:0]  rd_idx_o,

    output  logic [4:0]  rs1_idx_o,
    //output  logic [4:0]  rs2_idx_o,

    output  logic [31:0] imm_data_o,
    output  logic [3:0] alu_ctrl_o,
    output  logic alu_input_o, // 0: imm, 1: rs2
    output  logic reg_input_o, // 0: alu, 1: mem
    output  logic pc_sel_next_o // 0: same, 1: inc
  );

  localparam [2:0] ST_RESET = 'd0,
                   ST_EXEC = 'd1;

  logic [2:0] state;

  always_ff @(posedge clk_i or negedge rstn_i) begin
    if (~rstn_i) begin
      state <= ST_RESET;
      pc_sel_next_o <= 0;
    end
    else begin
      state <= ST_EXEC;
      pc_sel_next_o <= 1;
    end
  end

  logic [6:0] opcode;

  always_comb begin
    opcode = pc_data_i[6:0];
    if (state == ST_EXEC) begin
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
    else begin // ST_RESET or an invalid state
      wr_en_o = 0;
      rd_idx_o = 0;
      imm_data_o = 0;
      rs1_idx_o = 0;
      alu_ctrl_o = `ALU_OP_ADD;
      alu_input_o = 0;
      reg_input_o = 0;
    end
  end

endmodule


