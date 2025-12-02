module tb_matrix_mult;

    reg [3:0] a[4][4];
    reg [3:0] b[4][4];
    reg [3:0] c[4][4];
    reg clk;

    initial begin
        // Initialize input matrices
        a[0][0] = 1; a[0][1] = 2; a[0][2] = 3; a[0][3] = 4;
        a[1][0] = 5; a[1][1] = 6; a[1][2] = 7; a[1][3] = 8;
        a[2][0] = 9; a[2][1] = 10; a[2][2] = 11; a[2][3] = 12;
        a[3][0] = 13; a[3][1] = 14; a[3][2] = 15; a[3][3] = 16;

        b[0][0] = 1; b[0][1] = 2; b[0][2] = 3; b[0][3] = 4;
        b[1][0] = 5; b[1][1] = 6; b[1][2] = 7; b[1][3] = 8;
        b[2][0] = 9; b[2][1] = 10; b[2][2] = 11; b[2][3] = 12;
        b[3][0] = 13; b[3][1] = 14; b[3][2] = 15; b[3][3] = 16;

        // Clock setup
        clk = 0;
        #1000 clk = 1;
        #1000 clk = 0;

        // Output the result
        $display("Result matrix c:");
        for (int i = 0; i < 4; i++) begin
            for (int j = 0; j < 4; j++) begin
                $display("%d ", c[i][j]);
            end
            $display("");
        end
    end

endmodule