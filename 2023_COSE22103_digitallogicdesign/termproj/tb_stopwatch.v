`timescale 1ns/1ns
module tb_stopwatch();
reg rst, clk, start_stop;
wire [6:0] m10, m1, s10, s1, s_1, s__1;

stopwatch u0(rst, clk, start_stop, m10, m1, s10, s1, s_1, s__1);

initial begin
  rst <= 0;
  clk <= 0;
  start_stop <= 0;

  #15_000_000; rst <= 1;
  #25_000_000; start_stop <= 1;
  //forever #5_000_000 clk <= !clk;

//  #15; rst <= 1;
//  #35; start_stop <= 1;
//  forever #5 clk <= !clk;

    forever #10 clk <= !clk;

end

endmodule
