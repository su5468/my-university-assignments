module cnt0(rst, clk, out);
  input rst, clk;
  output [3:0] out;
  reg [3:0] out, temp;

  always@(posedge clk, negedge rst)
  begin
  if(!rst)
    begin
    temp <= 0;
    out <= 0;
    end
  else
    begin
    temp <= temp + 1;
    out <= temp;
    end
  end
endmodule
