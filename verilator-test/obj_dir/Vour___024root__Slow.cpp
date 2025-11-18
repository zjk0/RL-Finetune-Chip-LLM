// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vour.h for the primary calling header

#include "Vour__pch.h"

void Vour___024root___ctor_var_reset(Vour___024root* vlSelf);

Vour___024root::Vour___024root(Vour__Syms* symsp, const char* namep)
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vour___024root___ctor_var_reset(this);
}

void Vour___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vour___024root::~Vour___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
