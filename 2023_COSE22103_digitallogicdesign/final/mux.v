module mux(a, b, s, o);
input a, b, s;
output reg o;

always@(a,b,s)begin
if (s==1) o = a;
else o = b;
end

endmodule
