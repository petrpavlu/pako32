// TODO Replace, this temporary example is taken from
// https://github.com/ulixxe/usb_cdc/blob/main/examples/TinyFPGA-BX/hdl/soc/app.v.

// APP module shall implement an example of application module for USB_CDC.
// APP shall:
//   - TBD

module app
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

endmodule
