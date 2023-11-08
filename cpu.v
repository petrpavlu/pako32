// Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
// SPDX-License-Identifier: MIT

// TODO Replace, this temporary example is taken from
// https://github.com/ulixxe/usb_cdc/blob/main/examples/TinyFPGA-BX/hdl/soc/app.v.

`include "const.v"

module cpu
  (
    input        clk_i,
    input        rstn_i,

    // ---- to/from USB_CDC ------------------------------------------
    output [7:0] in_data_o,
    output       in_valid_o,
    // While in_valid_o is high, in_data_o shall be valid.
    input        in_ready_i,
    // When both in_ready_i and in_valid_o are high, in_data_o shall
    //   be consumed.
    input [7:0]  out_data_i,
    input        out_valid_i,
    // While out_valid_i is high, the out_data_i shall be valid and both
    //   out_valid_i and out_data_i shall not change until consumed.
    output       out_ready_o,
    // When both out_valid_i and out_ready_o are high, the out_data_i shall
    //   be consumed.

    // ---- to TOP --------------------------------------------------
    output       sleep_o
  );

  reg [1:0]    rstn_sq;

  wire         rstn;

  assign rstn = rstn_sq[0];

  always @(posedge clk_i or negedge rstn_i) begin
    if (~rstn_i) begin
      rstn_sq <= 2'd0;
    end else begin
      rstn_sq <= {1'b1, rstn_sq[1]};
    end
  end

  localparam [3:0] ST_RESET = 'd0,
                   ST_OUT_SLEEP = 'd3,
                   ST_IN_SLEEP = 'd9;

  reg [3:0]        status_q, status_d;
  reg              fifo_irq_q, fifo_irq_d;
  reg [7:0]        data_q, data_d;

  assign sleep_o = (status_q == ST_OUT_SLEEP || status_q == ST_IN_SLEEP) ? 1'b1 : 1'b0;

  always @(posedge clk_i or negedge rstn) begin
    if (~rstn) begin
      status_q <= ST_RESET;
      fifo_irq_q <= 1'b0;
      data_q <= 'd0;
    end else begin
      status_q <= status_d;
      fifo_irq_q <= fifo_irq_d;
      data_q <= data_d;
    end
  end


  logic       fifo_sel;
  logic       cpu_rd, cpu_wr;
  logic [1:0] cpu_addr;
  logic [7:0] cpu_wrdata;

  logic [7:0] fifo_rddata;
  logic       fifo_out_irq, fifo_in_irq;

  always_comb begin
    // dummy values, always zero
    fifo_sel = 1'b0;
    cpu_rd = 1'b0;
    cpu_wr = 1'b0;
    cpu_addr = 2'b00;
    cpu_wrdata = 8'd0;
    // unused: fifo_rddata = 8'd0;
    // unused: fifo_in_irq
    // unised: fifo_out_irq

    // app API
    // in_data_o = 0;
    // in_valid_o = 0;
    //  in_ready_i = 0;
    //  out_data_i = 0;
    //  out_valid_i = 0;
    // out_ready_o = 0;
 end

 fifo_if u_fifo_if (.clk_i(clk_i),
                    .rstn_i(rstn),
                    .sel_i(fifo_sel),
                    .read_i(cpu_rd),
                    .write_i(cpu_wr),
                    .addr_i(cpu_addr),
                    .data_i(cpu_wrdata),
                    .data_o(fifo_rddata),
                    .in_irq_o(fifo_in_irq),
                    .out_irq_o(fifo_out_irq),
                    .in_data_o(in_data_o),
                    .in_valid_o(in_valid_o),
                    .in_ready_i(in_ready_i),
                    .out_data_i(out_data_i),
                    .out_valid_i(out_valid_i),
                    .out_ready_o(out_ready_o));

  // CPU begins here
  logic [31:0] pc;
  logic [31:0] pc_next;
  logic [31:0] pc_data;
  logic [31:0] pc_next_off;
  logic [1:0]  pc_next_sel;
  logic [31:0] mem_data;
  logic        reg_wr_en, mem_wr_en;
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

  mem_control u_mem_control(
    .clk_i(clk_i),
    .rstn_i(rstn),

    .sext_i(mem_r_sext),
    .acc_r_i(mem_acc_r),
    .addr_r_i(alu_res),
    .data_r_o(mem_data),

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
    .pc_next_off_o(pc_next_off),
    .pc_next_sel_o(pc_next_sel),

    .mem_wr_ready_i(mem_wr_ready),
    .mem_wr_en_o(mem_wr_en),
    .mem_r_sext_o(mem_r_sext),
    .mem_acc_r_o(mem_acc_r),
    .mem_acc_w_o(mem_acc_w)
  );

  assign rd_data_mx = rd_sel == `RD_SEL_ALU ? alu_res : 0; // XXX 0 should be memory
  assign alu_a_mx = alu_a_sel == `ALU_A_SEL_RS1 ? rs1_data : pc;
  assign alu_b_mx = alu_b_sel == `ALU_B_SEL_RS2 ? rs2_data : imm_data;
  always_comb begin
    case (pc_next_sel)
      `PC_NEXT_SEL_PC_IMM: pc_next = pc + pc_next_off;
      `PC_NEXT_SEL_RS1_IMM: pc_next = rs1_data + pc_next_off;
      default: pc_next = pc; // PC_NEXT_SEL_STALL
    endcase
  end

  always_ff @(posedge clk_i or negedge rstn) begin
    if (~rstn)
      pc <= `MEM_INSTR_ZERO;
    else
      pc <= pc_next;
  end
endmodule
