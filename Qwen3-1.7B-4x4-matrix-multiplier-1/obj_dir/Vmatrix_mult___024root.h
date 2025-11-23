// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vmatrix_mult.h for the primary calling header

#ifndef VERILATED_VMATRIX_MULT___024ROOT_H_
#define VERILATED_VMATRIX_MULT___024ROOT_H_  // guard

#include "verilated.h"


class Vmatrix_mult__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vmatrix_mult___024root final {
  public:

    // DESIGN SPECIFIC STATE
    CData/*0:0*/ __VstlFirstIteration;
    VlUnpacked<VlUnpacked<CData/*3:0*/, 4>, 4> tb_matrix_mult__DOT__a;
    VlUnpacked<VlUnpacked<CData/*3:0*/, 4>, 4> tb_matrix_mult__DOT__b;
    VlUnpacked<VlUnpacked<CData/*3:0*/, 4>, 4> tb_matrix_mult__DOT__c;
    VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;

    // INTERNAL VARIABLES
    Vmatrix_mult__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vmatrix_mult___024root(Vmatrix_mult__Syms* symsp, const char* namep);
    ~Vmatrix_mult___024root();
    VL_UNCOPYABLE(Vmatrix_mult___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
