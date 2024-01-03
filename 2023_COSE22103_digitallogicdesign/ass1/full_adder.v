module full_adder(x, y, c_in, s_out, c_out);
  input x, y, c_in;
  output s_out, c_out;
  wire temp_sum, temp_carry1, temp_carry2;
  
  half_adder u0(x, y, temp_sum, temp_carry1);
  half_adder u1(temp_sum, c_in, s_out, temp_carry2);
  or2 u2(temp_carry1, temp_carry2, c_out);
endmodule