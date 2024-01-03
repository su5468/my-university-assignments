module encoder(a, b, v);
input [3:0] a;
output reg [1:0] b;
output reg v;

always@(a) begin
  if (a == 4'b0000) v = 0;
  else v = 1;
  if (a[0] == 1) b = 2'b00;
  else if (a[1] == 1) b = 2'b01;
  else if (a[2] == 1) b = 2'b10;
  else if (a[3] == 1) b = 2'b11;
end

endmodule
