module rca_4bit(x, y, c_in, sum, c_out);
  input [3:0] x, y;
  input c_in;
  output [3:0] sum;
  output c_out;
  
  wire tc0, tc1, tc2;
  
  full_adder u0(x[0], y[0], c_in, sum[0], tc0);
  full_adder u1(x[1], y[1], tc0, sum[1], tc1);
  full_adder u2(x[2], y[2], tc1, sum[2], tc2);
  full_adder u3(x[3], y[3], tc2, sum[3], c_out);
endmodule