module decoder(a, b);
input [1:0] a;
output reg [3:0] b;

always@(a) begin
case(a)
0: b = 4'b0001;
1: b = 4'b0010;
2: b = 4'b0100;
default: b = 4'b1000;
endcase

end
endmodule
