module matrix_mult (
    input [3:0] A[3:0][3:0],
    input [3:0] B[3:0][3:0],
    output reg [3:0] C[3:0][3:0]
);

    // Initialize C to 0
    initial begin
        for (int i = 0; i < 4; i++) begin
            for (int j = 0; j < 4; j++) begin
                C[i][j] = 0;
                for (int k = 0; k < 4; k++) begin
                    C[i][j] += A[i][k] * B[k][j];
                end
            end
        end
    end

endmodule
