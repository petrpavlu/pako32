// Copyright (C) 2023 Petr Pavlu <petr.pavlu@dagobah.cz>
// SPDX-License-Identifier: MIT

`include "const.v"

module mem_control
  #(
    // Datafiles contain 16b values
    parameter DATA_FILE_01 = "",
    parameter DATA_FILE_23 = "",
    parameter ROWS         = 512,
    parameter MAP_ZERO     = 0
  )
  (
    input logic clk_i,
    input logic rstn_i,

    // read port
    input  logic        sext_i,
    input  logic        r_en_i,
    input  logic [1:0]  acc_r_i,
    input  logic [31:0] addr_r_i,
    output logic [31:0] data_r_o,

    // write port
    input  logic        wr_en_i,
    input  logic [1:0]  acc_w_i,
    input  logic [31:0] addr_w_i,
    input  logic [31:0] data_w_i,
    output logic        wr_ready_o
  );

  localparam [1:0] ST_RESET = 'd0,
                   ST_READY = 'd1,
                   ST_WRITE_PENDING = 'd2;

  logic [1:0]  state;
  logic [1:0]  state_next;

  logic        r_en;
  logic [31:0] addr_r;
  logic [31:0] data_r;
  logic [1:0]  addr_r_post;
  logic [1:0]  acc_r_post;
  logic        sext_post;

  logic        wr_en;
  logic [31:0] addr_w;
  logic [31:0] data_w;

  // TODO Check correct alignment.

  always_comb begin
    r_en = r_en_i && (addr_r_i >= MAP_ZERO && addr_r_i < MAP_ZERO + 4 * ROWS);
    addr_r = 0;
    data_r_o = 0;
    wr_en = 0;
    addr_w = 0;
    data_w = 0;
    state_next = ST_READY;

    wr_ready_o = state == ST_READY;

    if (state == ST_READY && wr_en_i && (addr_w_i >= MAP_ZERO && addr_w_i < MAP_ZERO + 4 * ROWS)) begin
      // writing -- read of the original data
      r_en = 1;
      addr_r = (addr_w_i & 'hfffffffc) - MAP_ZERO;
      state_next = ST_WRITE_PENDING;
    end
    else if (state == ST_WRITE_PENDING) begin
      // writing -- store of the updated data
      wr_en = 1;
      addr_w = (addr_w_i & 'hfffffffc) - MAP_ZERO;

      case (acc_w_i)
        `MEM_ACCESS_BYTE: begin
          case (addr_w_i & 3)
            2'b00: data_w = (data_r & 'hffffff00) | ((data_w_i & 'hff) << 0);
            2'b01: data_w = (data_r & 'hffff00ff) | ((data_w_i & 'hff) << 8);
            2'b10: data_w = (data_r & 'hff00ffff) | ((data_w_i & 'hff) << 16);
            2'b11: data_w = (data_r & 'h00ffffff) | ((data_w_i & 'hff) << 24);
          endcase
        end
        `MEM_ACCESS_HALFWORD: begin
          case (addr_w_i & 2)
            2'b00: data_w = (data_r & 'hffff0000) | ((data_w_i & 'hffff) << 0);
            2'b10: data_w = (data_r & 'h0000ffff) | ((data_w_i & 'hffff) << 16);
          endcase
        end
        default: data_w = data_w_i; // MEM_ACCESS_WORD
      endcase
    end
    else if (r_en_i) begin
      // reading
      addr_r = (addr_r_i & 'hfffffffc) - MAP_ZERO;

      // post posedge clk_i
      case (acc_r_post)
        `MEM_ACCESS_BYTE: begin
          if (sext_post == 1)
            data_r_o =   signed'(8'(data_r >> (8 * (addr_r_post & 3))));
          else
            data_r_o = unsigned'(8'(data_r >> (8 * (addr_r_post & 3))));
        end
        `MEM_ACCESS_HALFWORD: begin
          if (sext_post == 1)
             data_r_o =   signed'(16'(data_r >> (8 * (addr_r_post & 2))));
           else
             data_r_o = unsigned'(16'(data_r >> (8 * (addr_r_post & 2))));
        end
        default:              data_r_o = data_r; // MEM_ACCESS_WORD
      endcase
    end
  end

  always_ff @(posedge clk_i) begin
    addr_r_post <= addr_r_i;
    acc_r_post <= acc_r_i;
    sext_post <= sext_i;
  end

  always_ff @(posedge clk_i or negedge rstn_i) begin
    if (~rstn_i)
      state <= ST_RESET;
    else
      state <= state_next;
  end

  mem #(
    .DATA_FILE_01(DATA_FILE_01),
    .DATA_FILE_23(DATA_FILE_23),
    .ROWS(ROWS)
  ) u_mem (
    .clk_i(clk_i),
    .r_en_i(r_en),
    .addr_r_i(addr_r),
    .data_r_o(data_r),
    .wr_en_i(wr_en),
    .addr_w_i(addr_w),
    .data_w_i(data_w)
  );
endmodule
