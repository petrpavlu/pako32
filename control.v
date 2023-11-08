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
    output  logic [4:0]  rs2_idx_o,

    output  logic [31:0] imm_data_o,
    output  logic [3:0] alu_op_o,
    output  logic alu_a_sel_o,
    output  logic alu_b_sel_o,
    output  logic reg_sel_o,
    output  logic pc_next_sel_o
  );

  localparam [2:0] ST_RESET = 'd0,
                   ST_EXEC = 'd1;

  logic [2:0] state;

  always_ff @(posedge clk_i or negedge rstn_i) begin
    if (~rstn_i) begin
      state <= ST_RESET;
      pc_next_sel_o <= `PC_NEXT_SEL_SAME;
    end
    else begin
      state <= ST_EXEC;
      pc_next_sel_o <= `PC_NEXT_SEL_INC;
    end
  end

  always_comb begin
    wr_en_o = 0;
    rd_idx_o = pc_data_i[11:7];
    imm_data_o = 0;
    rs1_idx_o = pc_data_i[19:15];
    rs2_idx_o = pc_data_i[24:20];
    alu_op_o = `ALU_OP_ADD;
    alu_a_sel_o = `ALU_A_SEL_RS1;
    alu_b_sel_o = `ALU_B_SEL_RS2;
    reg_sel_o = `REG_SEL_ALU;

    if (state == ST_EXEC) begin
      case (pc_data_i[6:0])
        7'b0110111: begin // LUI
          wr_en_o = 1;
          imm_data_o = {pc_data_i[31:12], 12'h000};
          rs1_idx_o = 0;
          alu_b_sel_o = `ALU_B_SEL_IMM;
        end
        7'b0010111: begin // AUIPC
          wr_en_o = 1;
          imm_data_o = {pc_data_i[31:12], 12'h000};
          alu_a_sel_o = `ALU_A_SEL_PC;
          alu_b_sel_o = `ALU_B_SEL_IMM;
        end
        7'b0010011: begin // I-type
          case (pc_data_i[14:12])
            3'b000: begin // ADDI
              wr_en_o = 1;
              imm_data_o = signed'(pc_data_i[31:20]);
              alu_b_sel_o = `ALU_B_SEL_IMM;
            end
            3'b010: begin // SLTI
              wr_en_o = 1;
              imm_data_o = signed'(pc_data_i[31:20]);
              alu_op_o = `ALU_OP_LT;
              alu_b_sel_o = `ALU_B_SEL_IMM;
            end
            3'b011: begin // SLTIU
              wr_en_o = 1;
              imm_data_o = signed'(pc_data_i[31:20]);
              alu_op_o = `ALU_OP_LTU;
              alu_b_sel_o = `ALU_B_SEL_IMM;
            end
            3'b100: begin // XORI
              wr_en_o = 1;
              imm_data_o = signed'(pc_data_i[31:20]);
              alu_op_o = `ALU_OP_XOR;
              alu_b_sel_o = `ALU_B_SEL_IMM;
            end
            3'b110: begin // ORI
              wr_en_o = 1;
              imm_data_o = signed'(pc_data_i[31:20]);
              alu_op_o = `ALU_OP_OR;
              alu_b_sel_o = `ALU_B_SEL_IMM;
            end
            3'b111: begin // ANDI
              wr_en_o = 1;
              imm_data_o = signed'(pc_data_i[31:20]);
              alu_op_o = `ALU_OP_AND;
              alu_b_sel_o = `ALU_B_SEL_IMM;
            end
            3'b001: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // SLLI
                  wr_en_o = 1;
                  imm_data_o = pc_data_i[24:20];
                  alu_op_o = `ALU_OP_SLL;
                  alu_b_sel_o = `ALU_B_SEL_IMM;
                end
              endcase
            end
            3'b101: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // SRLI
                  wr_en_o = 1;
                  imm_data_o = pc_data_i[24:20];
                  alu_op_o = `ALU_OP_SRL;
                  alu_b_sel_o = `ALU_B_SEL_IMM;
                end
                7'b0100000: begin // SRAI
                  wr_en_o = 1;
                  imm_data_o = pc_data_i[24:20];
                  alu_op_o = `ALU_OP_SRA;
                  alu_b_sel_o = `ALU_B_SEL_IMM;
                end
              endcase
            end
          endcase
        end
        7'b0110011: begin // R-type
          case (pc_data_i[14:12])
            3'b000: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // ADD
                  wr_en_o = 1;
                end
                7'b0100000: begin // SUB
                  wr_en_o = 1;
                  alu_op_o = `ALU_OP_SUB;
                end
              endcase
            end
            3'b001: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // SLL
                  wr_en_o = 1;
                  alu_op_o = `ALU_OP_SLL;
                end
              endcase
            end
            3'b010: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // SLT
                  wr_en_o = 1;
                  alu_op_o = `ALU_OP_LT;
                end
              endcase
            end
            3'b011: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // SLTU
                  wr_en_o = 1;
                  alu_op_o = `ALU_OP_LTU;
                end
              endcase
            end
            3'b100: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // XOR
                  wr_en_o = 1;
                  alu_op_o = `ALU_OP_XOR;
                end
              endcase
            end
            3'b101: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // SRL
                  wr_en_o = 1;
                  alu_op_o = `ALU_OP_SRL;
                end
                7'b0100000: begin // SRA
                  wr_en_o = 1;
                  alu_op_o = `ALU_OP_SRA;
                end
              endcase
            end
          endcase
        end
      endcase
    end
  end
endmodule
