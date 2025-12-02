// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmatrix_mult.h for the primary calling header

#include "Vmatrix_mult__pch.h"

void Vmatrix_mult___024root___ctor_var_reset(Vmatrix_mult___024root* vlSelf);

Vmatrix_mult___024root::Vmatrix_mult___024root(Vmatrix_mult__Syms* symsp, const char* namep)
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vmatrix_mult___024root___ctor_var_reset(this);
}

void Vmatrix_mult___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vmatrix_mult___024root::~Vmatrix_mult___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
