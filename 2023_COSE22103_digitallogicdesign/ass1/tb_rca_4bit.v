`timescale 1ns/1ns
module tb_rca_4bit();
  reg [3:0] x, y;
  reg c_in;
  wire [3:0] sum;
  wire c_out;
  
  rca_4bit u0(x, y, c_in, sum, c_out);
  
  initial
  begin
    x = 4'b1111; y = 4'b0000; c_in = 0;
    #100; y = 4'b0001;
    #100; y = 4'b0010;
    #100; y = 4'b0011;
    #100; y = 4'b0100;
    #100; y = 4'b0101;
    #100; y = 4'b0110;
    #100; y = 4'b1111;
  end
endmodule