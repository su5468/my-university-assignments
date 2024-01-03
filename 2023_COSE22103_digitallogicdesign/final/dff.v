module dff(clk, rst, d, o);
input clk, rst, d;
output reg o;

always@(posedge clk, negedge rst) begin
if(!rst)
o <= 0;
else o <= d;
end

endmodule
