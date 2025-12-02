module matrix_mult (
    input [3:0] a[4][4],
    input [3:0] b[4][4],
    output reg [3:0] c[4][4]
);

    always @(posedge clk or negedge clk) begin
        for (int i = 0; i < 4; i++) begin
            for (int j = 0; j < 4; j++) begin
                c[i][j] = 0;
                for (int k = 0; k < 4; k++) begin
                    c[i][j] += a[i][k] * b[k][j];
                end
            end
        end
    end

endmodule