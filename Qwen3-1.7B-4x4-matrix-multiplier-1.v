module matrix_mult (
    input [3:0] a[3:0][3:0],  // First 4x4 matrix
    input [3:0] b[3:0][3:0],  // Second 4x4 matrix
    output reg [3:0] c[3:0][3:0]  // Result 4x4 matrix
);

    // Initialize result matrix
    initial begin
        c[0][0] = 0;
        c[0][1] = 0;
        c[0][2] = 0;
        c[0][3] = 0;
        c[1][0] = 0;
        c[1][1] = 0;
        c[1][2] = 0;
        c[1][3] = 0;
        c[2][0] = 0;
        c[2][1] = 0;
        c[2][2] = 0;
        c[2][3] = 0;
        c[3][0] = 0;
        c[3][1] = 0;
        c[3][2] = 0;
        c[3][3] = 0;
    end

    // Compute the result matrix
    always @(a or b) begin
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