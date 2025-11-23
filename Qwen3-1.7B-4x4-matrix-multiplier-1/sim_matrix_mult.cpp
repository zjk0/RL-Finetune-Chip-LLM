#include "Vmatrix_mult.h"
#include "verilated.h"

int main (int argc, char** argv) {
    VerilatedContext* contextp = new VerilatedContext;
    contextp->commandArgs(argc, argv);
    Vmatrix_mult* top = new Vmatrix_mult{contextp};
    while (!contextp->gotFinish()) {
        top->eval();
    }
    delete top;
    delete contextp;
    return 0;
}