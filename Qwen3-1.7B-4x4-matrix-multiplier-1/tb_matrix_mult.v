//~ `New testbench
`timescale  1ns / 1ps

module tb_matrix_mult;

  // matrix_mult Parameters
  parameter PERIOD  = 10;

  // matrix_mult Inputs
  reg   [3:0]  a[3:0][3:0] = 0 ;
  reg   [3:0]  b[3:0][3:0] = 0 ;

  // matrix_mult Outputs
  wire  [3:0]  c[3:0][3:0];

  reg clk = 0;
  reg rst_n = 0;


  initial
  begin
    forever
      #(PERIOD/2)  clk=~clk;
  end

  initial
  begin
    #(PERIOD*2) rst_n  =  1;
  end

  matrix_mult  u_matrix_mult (
                 .a(a),
                 .b(b),

                 .c(c)
               );

  initial
  begin

    $finish;
  end

endmodule

// `timescale 1ns / 1ps

// module tb_matrix_mult;

// // matrix_mult Parameters
// parameter PERIOD  = 10;

// // matrix_mult Inputs
// reg   [3:0]  a[3:0][3:0]  = 0;
// reg   [3:0]  b[3:0][3:0]  = 0;

// // matrix_mult Outputs
// wire  [3:0]  c[3:0][3:0];

// // Clock and reset signals
// reg clk = 0;
// reg rst_n = 0;

// initial begin
//     forever #(PERIOD/2) clk = ~clk;  // Clock generation
// end

// initial begin
//     #(PERIOD*2) rst_n = 1;  // Reset signal after 2 periods
// end

// // Instantiate the matrix multiplication module
// matrix_mult u_matrix_mult (
//     .a(a),
//     .b(b),
//     .c(c)
// );

// initial begin
//     // Apply test vectors to 'a' and 'b' and monitor 'c'
//     a[0][0] = 4'd1; b[0][0] = 4'd1;
//     a[0][1] = 4'd2; b[0][1] = 4'd2;
//     // More initialization...

//     #100;  // Wait for 100 time units

//     $finish;  // End the simulation
// end

// endmodule

