`timescale 1ns/1ns
module tb_fadd();
  reg x, y, z;
  wire s, c;
  
  fadd u0(x, y, z, s, c);
  
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


