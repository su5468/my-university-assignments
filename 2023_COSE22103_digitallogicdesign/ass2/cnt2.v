module cnt2(rst, clk, out);
  input rst, clk;
  output [3:0] out;
  reg clk2;
  reg [6:0] temp2;
  reg [3:0] out, temp;

  always@(posedge clk, negedge rst)
  begin
  if(!rst)
    begin
    temp2 <= 0;
    clk2 <= 0;
    end
  else
    begin
    temp2 <= (temp2+1)%50;
    if(temp2==0) clk2 <= ~clk2;
    end
  end

  always@(posedge clk2, negedge rst)
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
