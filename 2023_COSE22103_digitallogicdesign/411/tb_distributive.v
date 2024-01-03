`timescale 1ns/1ns
module tb_distributive();
  reg x, y, z;
  wire s0, temp0, s1, temp1, temp2;
  
  and2 u0(y, z, temp0);
  or2 u1(temp0, x, s0);
  
  or2 u2(x, y, temp1);
  or2 u3(x, z, temp2);
  and2 u4(temp1, temp2, s1);
  
  initial
  begin
    x = 0; y = 0; z = 0;
    #100; x = 0; y = 0; z = 1;
    #100; x = 0; y = 1; z = 0;
    #100; x = 0; y = 1; z = 1;
    #100; x = 1; y = 0; z = 0;
    #100; x = 1; y = 0; z = 1;
    #100; x = 1; y = 1; z = 0;
    #100; x = 1; y = 1; z = 1;
  end
  
endmodule


