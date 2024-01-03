module demux(a, s, o1, o2);
input a, s;
output reg o1, o2;

always@(a, s) begin
if (s==1) o1 = a;
else o2 = a;
end

endmodule
