// Copyright (C) 2023 Michal Koutný <mkoutny@suse.com>
// SPDX-License-Identifier: MIT

`include "const.v"

module control
  (
    input logic clk_i,
    input logic rstn_i,
    input logic [31:0] pc_data_i,

    output  logic        reg_wr_en_o,
    output  logic [4:0]  rd_idx_o,

    output  logic [4:0]  rs1_idx_o,
    output  logic [4:0]  rs2_idx_o,

    output  logic [31:0] imm_data_o,
    output  logic [3:0] alu_op_o,
    output  logic alu_a_sel_o,
    output  logic alu_b_sel_o,
    output  logic rd_sel_o,
    output  logic [2:0] pc_isize_o,
    output  logic [31:0] pc_next_off_o,
    output  logic [2:0] pc_next_sel_o,

    input   logic mem_wr_ready_i,
    output  logic mem_wr_en_o,
    output  logic mem_r_sext_o,
    output  logic mem_r_en_o,
    output  logic [1:0] mem_acc_r_o, mem_acc_w_o
  );

  localparam [2:0] ST_RESET = 'd0,
                   ST_EXEC = 'd1,
                   ST_READ_STALL = 'd2;

  logic [2:0] state;
  logic [2:0] state_next;

  always_ff @(posedge clk_i or negedge rstn_i) begin
    if (~rstn_i)
      state <= ST_RESET;
    else
      state <= state_next;
  end

  always_comb begin
    reg_wr_en_o = 0;
    rd_idx_o = pc_data_i[11:7];
    rs1_idx_o = pc_data_i[19:15];
    rs2_idx_o = pc_data_i[24:20];
    imm_data_o = 0;
    alu_op_o = `ALU_OP_ADD;
    alu_a_sel_o = `ALU_A_SEL_RS1;
    alu_b_sel_o = `ALU_B_SEL_RS2;
    rd_sel_o = `RD_SEL_ALU;
    pc_isize_o = 4;
    pc_next_off_o = 0;
    pc_next_sel_o = `PC_NEXT_SEL_STALL;
    mem_wr_en_o = 0;
    mem_r_sext_o = 0;
    mem_r_en_o = 0;
    mem_acc_r_o = `MEM_ACCESS_BYTE;
    mem_acc_w_o = `MEM_ACCESS_BYTE;

    state_next = ST_EXEC;

    if (state > ST_RESET) begin
      pc_next_sel_o = `PC_NEXT_SEL_NEXT;

      case (pc_data_i[6:0])
        7'b0110111: begin // LUI
          reg_wr_en_o = 1;
          imm_data_o = {pc_data_i[31:12], 12'h000};
          rs1_idx_o = 0;
          alu_b_sel_o = `ALU_B_SEL_IMM;
        end
        7'b0010111: begin // AUIPC
          reg_wr_en_o = 1;
          imm_data_o = {pc_data_i[31:12], 12'h000};
          alu_a_sel_o = `ALU_A_SEL_PC;
          alu_b_sel_o = `ALU_B_SEL_IMM;
        end
        7'b1101111: begin // JAL
          reg_wr_en_o = 1;
          imm_data_o = 4;
          alu_a_sel_o = `ALU_A_SEL_PC;
          alu_b_sel_o = `ALU_B_SEL_IMM;
          pc_next_sel_o = `PC_NEXT_SEL_PC_IMM;
          pc_next_off_o = signed'({pc_data_i[31], pc_data_i[19:12], pc_data_i[20], pc_data_i[30:21], 1'b0});
        end
        7'b1100111: begin // JALR
          reg_wr_en_o = 1;
          imm_data_o = 4;
          alu_a_sel_o = `ALU_A_SEL_PC;
          alu_b_sel_o = `ALU_B_SEL_IMM;
          pc_next_off_o = signed'(pc_data_i[31:20]);
          pc_next_sel_o = `PC_NEXT_SEL_RS1_IMM;
        end
        7'b1100011: begin // B-type
          case (pc_data_i[14:12])
            3'b000: begin // BEQ
              alu_op_o = `ALU_OP_EQ;
              pc_next_off_o = signed'({pc_data_i[31], pc_data_i[7], pc_data_i[30:25], pc_data_i[11:8], 1'b0});
              pc_next_sel_o = `PC_NEXT_SEL_COND_PC_IMM;
            end
            3'b001: begin // BNE
              alu_op_o = `ALU_OP_NE;
              pc_next_off_o = signed'({pc_data_i[31], pc_data_i[7], pc_data_i[30:25], pc_data_i[11:8], 1'b0});
              pc_next_sel_o = `PC_NEXT_SEL_COND_PC_IMM;
            end
            3'b100: begin // BLT
              alu_op_o = `ALU_OP_LT;
              pc_next_off_o = signed'({pc_data_i[31], pc_data_i[7], pc_data_i[30:25], pc_data_i[11:8], 1'b0});
              pc_next_sel_o = `PC_NEXT_SEL_COND_PC_IMM;
            end
            3'b101: begin // BGE
              alu_op_o = `ALU_OP_GE;
              pc_next_off_o = signed'({pc_data_i[31], pc_data_i[7], pc_data_i[30:25], pc_data_i[11:8], 1'b0});
              pc_next_sel_o = `PC_NEXT_SEL_COND_PC_IMM;
            end
            3'b110: begin // BLTU
              alu_op_o = `ALU_OP_LTU;
              pc_next_off_o = signed'({pc_data_i[31], pc_data_i[7], pc_data_i[30:25], pc_data_i[11:8], 1'b0});
              pc_next_sel_o = `PC_NEXT_SEL_COND_PC_IMM;
            end
            3'b111: begin // BGEU
              alu_op_o = `ALU_OP_GEU;
              pc_next_off_o = signed'({pc_data_i[31], pc_data_i[7], pc_data_i[30:25], pc_data_i[11:8], 1'b0});
              pc_next_sel_o = `PC_NEXT_SEL_COND_PC_IMM;
            end
          endcase
        end
        7'b0000011: begin // LW{B,H,W,BU,HU}
          reg_wr_en_o = 1;
          imm_data_o = signed'(pc_data_i[31:20]);
          alu_b_sel_o = `ALU_B_SEL_IMM;
          rd_sel_o = `RD_SEL_MEM;
          pc_next_sel_o = state == ST_READ_STALL ? `PC_NEXT_SEL_NEXT : `PC_NEXT_SEL_STALL;
          mem_r_sext_o = ~pc_data_i[14];
          mem_r_en_o = 1;
          mem_acc_r_o = pc_data_i[13:12];

          state_next = state == ST_READ_STALL ? ST_EXEC : ST_READ_STALL;
        end
        7'b0010011: begin // I-type
          case (pc_data_i[14:12])
            3'b000: begin // ADDI
              reg_wr_en_o = 1;
              imm_data_o = signed'(pc_data_i[31:20]);
              alu_b_sel_o = `ALU_B_SEL_IMM;
            end
            3'b010: begin // SLTI
              reg_wr_en_o = 1;
              imm_data_o = signed'(pc_data_i[31:20]);
              alu_op_o = `ALU_OP_LT;
              alu_b_sel_o = `ALU_B_SEL_IMM;
            end
            3'b011: begin // SLTIU
              reg_wr_en_o = 1;
              imm_data_o = signed'(pc_data_i[31:20]);
              alu_op_o = `ALU_OP_LTU;
              alu_b_sel_o = `ALU_B_SEL_IMM;
            end
            3'b100: begin // XORI
              reg_wr_en_o = 1;
              imm_data_o = signed'(pc_data_i[31:20]);
              alu_op_o = `ALU_OP_XOR;
              alu_b_sel_o = `ALU_B_SEL_IMM;
            end
            3'b110: begin // ORI
              reg_wr_en_o = 1;
              imm_data_o = signed'(pc_data_i[31:20]);
              alu_op_o = `ALU_OP_OR;
              alu_b_sel_o = `ALU_B_SEL_IMM;
            end
            3'b111: begin // ANDI
              reg_wr_en_o = 1;
              imm_data_o = signed'(pc_data_i[31:20]);
              alu_op_o = `ALU_OP_AND;
              alu_b_sel_o = `ALU_B_SEL_IMM;
            end
            3'b001: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // SLLI
                  reg_wr_en_o = 1;
                  imm_data_o = pc_data_i[24:20];
                  alu_op_o = `ALU_OP_SLL;
                  alu_b_sel_o = `ALU_B_SEL_IMM;
                end
              endcase
            end
            3'b101: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // SRLI
                  reg_wr_en_o = 1;
                  imm_data_o = pc_data_i[24:20];
                  alu_op_o = `ALU_OP_SRL;
                  alu_b_sel_o = `ALU_B_SEL_IMM;
                end
                7'b0100000: begin // SRAI
                  reg_wr_en_o = 1;
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
                  reg_wr_en_o = 1;
                end
                7'b0100000: begin // SUB
                  reg_wr_en_o = 1;
                  alu_op_o = `ALU_OP_SUB;
                end
              endcase
            end
            3'b001: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // SLL
                  reg_wr_en_o = 1;
                  alu_op_o = `ALU_OP_SLL;
                end
              endcase
            end
            3'b010: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // SLT
                  reg_wr_en_o = 1;
                  alu_op_o = `ALU_OP_LT;
                end
              endcase
            end
            3'b011: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // SLTU
                  reg_wr_en_o = 1;
                  alu_op_o = `ALU_OP_LTU;
                end
              endcase
            end
            3'b100: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // XOR
                  reg_wr_en_o = 1;
                  alu_op_o = `ALU_OP_XOR;
                end
              endcase
            end
            3'b101: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // SRL
                  reg_wr_en_o = 1;
                  alu_op_o = `ALU_OP_SRL;
                end
                7'b0100000: begin // SRA
                  reg_wr_en_o = 1;
                  alu_op_o = `ALU_OP_SRA;
                end
              endcase
            end
            3'b110: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // OR
                  reg_wr_en_o = 1;
                  alu_op_o = `ALU_OP_OR;
                end
              endcase
            end
            3'b111: begin
              case (pc_data_i[31:25])
                7'b0000000: begin // AND
                  reg_wr_en_o = 1;
                  alu_op_o = `ALU_OP_AND;
                end
              endcase
            end
          endcase
        end
      endcase
    end // state
  end
endmodule
