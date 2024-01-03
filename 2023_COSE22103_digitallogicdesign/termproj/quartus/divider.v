module divider(rst, in, out);
input in, rst;
output reg out;
reg [17:0] cnt;

always@(posedge in, negedge rst) begin
  if (!rst) begin
    out <= 0;
    cnt <= 0;
  end
  else begin
//    cnt <= (cnt+1)%250000;
	 cnt <= (cnt+1)%2500;
    if (!cnt) out <= !out;
  end
end


endmodule
