// Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
// SPDX-License-Identifier: MIT

// TODO Replace, this temporary example is taken from
// https://github.com/ulixxe/usb_cdc/blob/main/examples/TinyFPGA-BX/hdl/soc/app.v.

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
   logic [31:0] pc_data;
   logic        wr_en;
   logic [4:0]  rd_idx, rs1_idx, rs2_idx;
   logic [31:0] rs1_data, rs2_data, imm_data;
   logic [3:0]  alu_ctrl;
   logic [31:0] rd_data_mx, alu_b_mx;
   logic        reg_input, alu_input;
   logic [31:0] alu_result;

   mem_instr u_mem_instr (
        .clk_i(clk_i),
        .pc_i(pc),
        .pc_data_o(pc_data)
   );

   registers u_registers (
        .clk_i(clk_i),
        .rstn_i(rstn),

        .wr_en_i(wr_en),
        .rd_idx_i(rd_idx),
        .rd_data_i(rd_data_mx),

        .rs1_idx_i(rs1_idx),
        .rs1_data_o(rs1_data),

        .rs2_idx_i(rs2_idx),
        .rs2_data_o(rs2_data)
   );

   alu u_alu(
        .a(rs1_data),
        .b(alu_b_mx),
        .control(alu_ctrl),
        .result(alu_result)
   );

   control u_control(
        .pc_data_i(pc_data),
        .wr_en_o(wr_en),
        .rd_idx_o(rd_idx),
        .rs1_idx_o(rs1_idx),
        //.rs2_idx_o(rs2_idx),
        .imm_data_o(imm_data),
        .alu_ctrl_o(alu_ctrl),
        .alu_input_o(alu_input),
        .reg_input_o(reg_input)
   );

   assign rd_data_mx = (reg_input == 1) ? 0 : alu_result; // XXX 0 should be memory
   assign alu_b_mx = (alu_input == 1) ? rs2_data : imm_data;

  always_ff @(posedge clk_i or negedge rstn) begin
    if (~rstn)
       pc = 'h10000;
    else
       pc = pc + 4;	// XXX output of AGU
  end
endmodule
