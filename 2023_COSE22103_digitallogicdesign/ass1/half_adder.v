module half_adder(x, y, s, c);
  input x, y;
  output s, c;
  reg s, c;
  
always@(x, y)
begin
  if (x ^ y) s = 1;
  else s = 0;
end

always@(x, y)
begin
  if (x & y) c = 1;
  else c = 0;
end
endmodule