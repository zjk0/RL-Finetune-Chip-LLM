// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VMATRIX_MULT__SYMS_H_
#define VERILATED_VMATRIX_MULT__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vmatrix_mult.h"

// INCLUDE MODULE CLASSES
#include "Vmatrix_mult___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vmatrix_mult__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vmatrix_mult* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vmatrix_mult___024root         TOP;

    // CONSTRUCTORS
    Vmatrix_mult__Syms(VerilatedContext* contextp, const char* namep, Vmatrix_mult* modelp);
    ~Vmatrix_mult__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard
