// Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
// SPDX-License-Identifier: MIT

`include "const.v"

module cpu
  (
    input logic clk_i,
    input logic rstn_i,

    // to/from USB_CDC
    output logic [7:0] in_data_o,
    output logic       in_valid_o,
    input  logic       in_ready_i,
    input  logic [7:0] out_data_i,
    input  logic       out_valid_i,
    output logic       out_ready_o
  );

  logic [1:0] rstn_sync;
  logic       rstn;

  assign rstn = rstn_sync[0];

  always @(posedge clk_i or negedge rstn_i) begin
    if (~rstn_i)
      rstn_sync <= 2'd0;
    else
      rstn_sync <= {1'b1, rstn_sync[1]};
  end

  // CPU logic
  logic [31:0] pc;
  logic [31:0] pc_next;
  logic [31:0] pc_data;
  logic [2:0]  pc_isize;
  logic [31:0] pc_next_off;
  logic [2:0]  pc_next_sel;
  logic [31:0] mem_data_r;
  logic [31:0] bus_data;
  logic        reg_wr_en, mem_wr_en, mem_r_en;
  logic [4:0]  rd_idx, rs1_idx, rs2_idx;
  logic [31:0] rs1_data, rs2_data, imm_data;
  logic [3:0]  alu_op;
  logic [31:0] rd_data_mx, alu_a_mx, alu_b_mx;
  logic        rd_sel, alu_a_sel, alu_b_sel;
  logic [31:0] alu_res;
  logic [1:0]  mem_acc_r, mem_acc_w;
  logic        mem_wr_ready;
  logic        mem_r_sext;

  mem_instr #(
    .PROG_FILE("examples/calc/calc.text.txt")
  ) u_mem_instr (
    .clk_i(clk_i),
    .pc_i(pc_next),
    .pc_data_o(pc_data)
  );

  registers u_registers (
    .clk_i(clk_i),
    .rstn_i(rstn),

    .wr_en_i(reg_wr_en),
    .rd_idx_i(rd_idx),
    .rd_data_i(rd_data_mx),

    .rs1_idx_i(rs1_idx),
    .rs1_data_o(rs1_data),

    .rs2_idx_i(rs2_idx),
    .rs2_data_o(rs2_data)
  );

  alu u_alu(
    .a(alu_a_mx),
    .b(alu_b_mx),
    .op(alu_op),
    .res(alu_res)
  );

  mem_control #(
    .DATA_FILE_01("examples/calc/calc.data.txt01"),
    .DATA_FILE_23("examples/calc/calc.data.txt23"),
    .MAP_ZERO(`MEM_DATA_ZERO)
  ) u_mem_control (
    .clk_i(clk_i),
    .rstn_i(rstn),

    .sext_i(mem_r_sext),
    .r_en_i(mem_r_en),
    .acc_r_i(mem_acc_r),
    .addr_r_i(alu_res),
    .data_r_o(mem_data_r),

    .wr_en_i(mem_wr_en),
    .acc_w_i(mem_acc_w),
    .addr_w_i(alu_res),
    .data_w_i(rs2_data),
    .wr_ready_o(mem_wr_ready)
  );

  control u_control(
    .clk_i(clk_i),
    .rstn_i(rstn),

    .pc_data_i(pc_data),
    .reg_wr_en_o(reg_wr_en),
    .rd_idx_o(rd_idx),
    .rs1_idx_o(rs1_idx),
    .rs2_idx_o(rs2_idx),

    .imm_data_o(imm_data),
    .alu_op_o(alu_op),
    .alu_a_sel_o(alu_a_sel),
    .alu_b_sel_o(alu_b_sel),
    .rd_sel_o(rd_sel),

    .pc_isize_o(pc_isize),
    .pc_next_off_o(pc_next_off),
    .pc_next_sel_o(pc_next_sel),

    .mem_wr_ready_i(mem_wr_ready),
    .mem_wr_en_o(mem_wr_en),
    .mem_r_sext_o(mem_r_sext),
    .mem_r_en_o(mem_r_en),
    .mem_acc_r_o(mem_acc_r),
    .mem_acc_w_o(mem_acc_w)
  );

  assign bus_data = mem_data_r | fifo_rddata;
  assign rd_data_mx = rd_sel == `RD_SEL_ALU ? alu_res : bus_data;
  assign alu_a_mx = alu_a_sel == `ALU_A_SEL_RS1 ? rs1_data : pc;
  assign alu_b_mx = alu_b_sel == `ALU_B_SEL_RS2 ? rs2_data : imm_data;
  always_comb begin
    case (pc_next_sel)
      `PC_NEXT_SEL_NEXT: pc_next = pc + pc_isize;
      `PC_NEXT_SEL_PC_IMM: pc_next = pc + pc_next_off;
      `PC_NEXT_SEL_RS1_IMM: pc_next = rs1_data + pc_next_off;
      `PC_NEXT_SEL_COND_PC_IMM: pc_next = alu_res ? pc + pc_next_off : pc + pc_isize;
      default: pc_next = pc; // PC_NEXT_SEL_STALL
    endcase
  end

  always_ff @(posedge clk_i or negedge rstn) begin
    if (~rstn)
      pc <= `MEM_INSTR_ZERO;
    else
      pc <= pc_next;
  end

  // USB FIFO
  logic       fifo_sel;
  logic       fifo_rd, fifo_wr;
  logic [1:0] fifo_addr;
  logic [7:0] fifo_wrdata;
  logic [7:0] fifo_rddata;
  logic       fifo_out_irq, fifo_in_irq; // unused

  always_comb begin
    fifo_sel = (mem_r_en || mem_wr_en) && alu_res >= `MEM_USB_IO_ZERO &&
      alu_res < `MEM_USB_IO_ZERO + 4;
    fifo_sel = mem_r_en || mem_wr_en;
    fifo_rd = fifo_sel && mem_r_en;
    fifo_wr = fifo_sel && mem_wr_en;
    fifo_addr = 2'(alu_res - `MEM_USB_IO_ZERO);
    fifo_wrdata = rs2_data;
  end

  fifo_if u_fifo_if (.clk_i(clk_i),
                     .rstn_i(rstn),
                     .sel_i(fifo_sel),
                     .read_i(fifo_rd),
                     .write_i(fifo_wr),
                     .addr_i(fifo_addr),
                     .data_i(fifo_wrdata),
                     .data_o(fifo_rddata),
                     .in_irq_o(fifo_in_irq),
                     .out_irq_o(fifo_out_irq),
                     .in_data_o(in_data_o),
                     .in_valid_o(in_valid_o),
                     .in_ready_i(in_ready_i),
                     .out_data_i(out_data_i),
                     .out_valid_i(out_valid_i),
                     .out_ready_o(out_ready_o));
endmodule
