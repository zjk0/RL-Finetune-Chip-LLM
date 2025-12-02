//~ `New testbench
`timescale  1ns / 1ps

module tb_matrix_mult;

  // matrix_mult Inputs
  reg [3:0] a[3:0][3:0];
  reg [3:0] b[3:0][3:0];

  // matrix_mult Outputs
  wire [3:0] c[3:0][3:0];

  matrix_mult u_matrix_mult (
    .a(a),
    .b(b),
    .c(c)
  );

  // initial begin
  //   for (int i = 0; i < 4; i++) begin
  //     for (int j = 0; j < 4; j++) begin
  //       a[i][j] = 4'b0000;
  //       b[i][j] = 4'b0000;
  //     end
  //   end

  //   $display("test1");
  //   // #10;
  //   $display("test2");
  // end

  initial begin
    int temp;

    for (int i = 0; i < 4; i++) begin
      for (int j = 0; j < 4; j++) begin
        a[i][j] = 4'b0000;
        b[i][j] = 4'b0000;
      end
    end

    for (int i = 0; i < 4; i++) begin
      for (int j = 0; j < 4; j++) begin
        temp = i + j;
        a[i][j] = temp[3:0];
        $display("a[%d][%d] = %b", i, j, a[i][j]);
        temp = i * 2;
        b[i][j] = temp[3:0];
      end
    end

    $display("Hello");
    // #10;
    $display("World");

    for (int i = 0; i < 4; i++) begin
      for (int j = 0; j < 4; j++) begin
        $display("%b ", c[i][j]);
      end
    end

    $finish;
  end

endmodule
