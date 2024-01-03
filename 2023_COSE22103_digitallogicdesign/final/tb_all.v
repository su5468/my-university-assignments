`timescale 1ns/1ns
module tb_all();
reg clk, rst, a, b, s;
reg [2:0] c;
reg [1:0] d;
wire [1:0] o_enc;
wire [2:0] o_dec;
wire o_comp, o_mux, o_dem1, o_dem2, o_dff;

comparator u0(a, b, o_comp);
encoder u1(c, o_enc);
decoder u2(d, o_dec);
mux u3(a, b, s, o_mux);
demux u4(a, s, o_dem1, o_dem2);
dff u5(clk, rst, a, o_dff);

initial begin
rst = 0;
#32; rst = 1;
end

initial begin
clk = 0;
forever #5 clk = !clk;
end

initial begin
a = 0;
forever #4 a = !a;
end

initial begin
b = 0;
forever #8 b = !b;
end

endmodule
