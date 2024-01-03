`timescale 1ns/1ns
module tb_gate();
  reg x, y;
  wire s0, s1, s2, s3;
  
  and2 u0(x, y, s0);
  or2 u1(x, y, s1);
  nand2 u2(x, y, s2);
  xor2 u3(x, y, s3);
  
  initial
  begin
    x = 0; y = 0;
    #100; x = 0; y = 1;
    #100; x = 1; y = 0;
    #100; x = 1; y = 1;
  end
  
endmodule


