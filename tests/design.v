module comparator_3bit(
    input [2:0] A,
    input [2:0] B,
    output reg [1:0] A_greater,
    output reg [1:0] A_equal,
    output reg [1:0] A_less
);

always @(*) begin
    if (A > B) begin
        A_greater = 1'b1;
    end else if (A == B) begin
        A_greater = 1'b0;
        A_equal = 1'b1;
    end else begin
        A_greater = 1'b0;
        A_equal = 1'b0;
        A_less = 1'b1;
    end
end

endmodule
