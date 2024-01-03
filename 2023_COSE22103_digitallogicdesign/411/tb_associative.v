`timescale 1ns/1ns
module tb_associative();
  reg x, y, z;
  wire s0, temp0, s1, temp1;
  
  or2 u0(x, y, temp0);
  or2 u1(temp0, z, s0);
  
  or2 u2(y, z, temp1);
  or2 u3(temp1, x, s1);
  
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

