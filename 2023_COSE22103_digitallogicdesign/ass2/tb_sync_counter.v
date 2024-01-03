`timescale 1ns/1ns

module tb_sync_counter();
  reg rst, clk;
  wire [3:0] out0, out1, out2, out3;
  sync_counter u0(rst, clk, out0, out1, out2, out3);

  initial
  begin
    rst = 0;
    #32; rst = 1;
  end

  initial
  begin
    clk = 0;
    forever #5 clk = !clk;
  end
endmodule
