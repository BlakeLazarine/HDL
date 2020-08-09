// Task 1

`timescale 1ns / 1ps

module ha1_task1(
input [6:0] A,
  output [31:0] X3;
  output [31:0] X2,X1, X0;
);

// your code here

  assign X0 = 32'b0 | ((A[6:5] == 0) << A[4:0]);
  assign X1 = 32'b0 | ((A[6:5] == 1) << A[4:0]);
  assign X2 = 32'b0 | ((A[6:5] == 2) << A[4:0]);
  assign X3 = 32'b0 | ((A[6:5] == 3) << A[4:0]);

endmodule