module fadd(x, y, cin, s, c);
  input x, y, cin;
  output s, c;
  
  wire ts, tc0, tc1;
  
  hadd u0(x, y, ts, tc0);
  hadd u1(ts, cin, s, tc1);
  or2 u2(tc0, tc1, c);
endmodule
