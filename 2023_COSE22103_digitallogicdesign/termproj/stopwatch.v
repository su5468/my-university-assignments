module stopwatch(rst, clk_in, start_stop, m10, m1, s10, s1, s_1, s__1);
input rst, clk_in, start_stop;
output [6:0] m10, m1, s10, s1, s_1, s__1;
reg [3:0] rm10, rm1, rs10, rs1, rs_1, rs__1;
reg [3:0] tm10, tm1, ts10, ts1, ts_1, ts__1;
reg [15:0] p;
wire clk;

segment u0(rm10, m10);
segment u1(rm1, m1);
segment u2(rs10, s10);
segment u3(rs1, s1);
segment u4(rs_1, s_1);
segment u5(rs__1, s__1);

divider u6(rst, clk_in, clk);


always@(posedge clk, negedge rst) begin
  if (!rst) begin
    rm10 <= 7'b000_0000;
    rm1 <= 7'b000_0000;
    rs10 <= 7'b000_0000;
    rs1 <= 7'b000_0000;
    rs_1 <= 7'b000_0000;
    rs__1 <= 7'b000_0000;
    tm10 <= 4'b0000;
    tm1 <= 4'b0000;
    ts10 <= 4'b0000;
    ts1 <= 4'b0000;
    ts_1 <= 4'b0000;
    ts__1 <= 4'b0000;
    p <= 15'b000_0000_0000_0000;
  end
  else if (start_stop) begin
    ts__1 <= (ts__1+1)%10;
    rs__1 <= ts__1;
    p <= (p+1)%60000;
    if (!(p%10)) begin
      ts_1 <= (ts_1+1)%10;
      rs_1 <= ts_1;
    end
    if (!(p%100)) begin
      ts1 <= (ts1+1)%10;
      rs1 <= ts1;
    end
    if (!(p%1000)) begin
      ts10 <= (ts10+1)%6;
      rs10 <= ts10;
    end
    if (!(p%6000)) begin
      tm1 <= (tm1+1)%10;
      rm1 <= tm1;
    end
    if (!p) begin
      tm10 <= (tm10+1)%6;
      rm10 <= tm10;
    end
  end
end

endmodule
