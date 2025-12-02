// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vmatrix_mult__pch.h"

//============================================================
// Constructors

Vmatrix_mult::Vmatrix_mult(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vmatrix_mult__Syms(contextp(), _vcname__, this)}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vmatrix_mult::Vmatrix_mult(const char* _vcname__)
    : Vmatrix_mult(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vmatrix_mult::~Vmatrix_mult() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vmatrix_mult___024root___eval_debug_assertions(Vmatrix_mult___024root* vlSelf);
#endif  // VL_DEBUG
void Vmatrix_mult___024root___eval_static(Vmatrix_mult___024root* vlSelf);
void Vmatrix_mult___024root___eval_initial(Vmatrix_mult___024root* vlSelf);
void Vmatrix_mult___024root___eval_settle(Vmatrix_mult___024root* vlSelf);
void Vmatrix_mult___024root___eval(Vmatrix_mult___024root* vlSelf);

void Vmatrix_mult::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vmatrix_mult::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vmatrix_mult___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vmatrix_mult___024root___eval_static(&(vlSymsp->TOP));
        Vmatrix_mult___024root___eval_initial(&(vlSymsp->TOP));
        Vmatrix_mult___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vmatrix_mult___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vmatrix_mult::eventsPending() { return false; }

uint64_t Vmatrix_mult::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vmatrix_mult::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vmatrix_mult___024root___eval_final(Vmatrix_mult___024root* vlSelf);

VL_ATTR_COLD void Vmatrix_mult::final() {
    Vmatrix_mult___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vmatrix_mult::hierName() const { return vlSymsp->name(); }
const char* Vmatrix_mult::modelName() const { return "Vmatrix_mult"; }
unsigned Vmatrix_mult::threads() const { return 1; }
void Vmatrix_mult::prepareClone() const { contextp()->prepareClone(); }
void Vmatrix_mult::atClone() const {
    contextp()->threadPoolpOnClone();
}
