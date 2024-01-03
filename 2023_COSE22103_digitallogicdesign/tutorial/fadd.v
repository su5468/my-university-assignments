module fadd(x, y, z, s, c); 
  input x, y, z;
  output s, c;
  wire ts, tc0, tc1
  
  hadd u0(.x(x), .y(y), .s(ts), .z(tc0));
  hadd u1(.x(ts), .y(z), .s(s), .z(tc1));
  or2 u2(.a(tc1), .b(tc0), .o(c));
endmodule
