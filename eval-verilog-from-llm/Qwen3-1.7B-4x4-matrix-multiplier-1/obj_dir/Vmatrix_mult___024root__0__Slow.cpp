// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmatrix_mult.h for the primary calling header

#include "Vmatrix_mult__pch.h"

VL_ATTR_COLD void Vmatrix_mult___024root___eval_static(Vmatrix_mult___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmatrix_mult___024root___eval_static\n"); );
    Vmatrix_mult__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vmatrix_mult___024root___eval_initial__TOP(Vmatrix_mult___024root* vlSelf);

VL_ATTR_COLD void Vmatrix_mult___024root___eval_initial(Vmatrix_mult___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmatrix_mult___024root___eval_initial\n"); );
    Vmatrix_mult__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vmatrix_mult___024root___eval_initial__TOP(vlSelf);
}

VL_ATTR_COLD void Vmatrix_mult___024root___eval_initial__TOP(Vmatrix_mult___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmatrix_mult___024root___eval_initial__TOP\n"); );
    Vmatrix_mult__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tb_matrix_mult__DOT__a[0U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[0U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[0U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[0U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[0U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[0U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[0U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[0U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[1U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[1U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[1U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[1U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[1U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[1U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[1U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[1U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[2U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[2U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[2U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[2U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[2U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[2U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[2U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[2U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[3U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[3U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[3U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[3U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[3U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[3U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[3U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__b[3U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[0U][0U] = 0U;
    VL_WRITEF_NX("a[          0][          0] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [0U][0U]);
    vlSelfRef.tb_matrix_mult__DOT__b[0U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[0U][1U] = 1U;
    VL_WRITEF_NX("a[          0][          1] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [0U][1U]);
    vlSelfRef.tb_matrix_mult__DOT__b[0U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[0U][2U] = 2U;
    VL_WRITEF_NX("a[          0][          2] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [0U][2U]);
    vlSelfRef.tb_matrix_mult__DOT__b[0U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[0U][3U] = 3U;
    VL_WRITEF_NX("a[          0][          3] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [0U][3U]);
    vlSelfRef.tb_matrix_mult__DOT__b[0U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__a[1U][0U] = 1U;
    VL_WRITEF_NX("a[          1][          0] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [1U][0U]);
    vlSelfRef.tb_matrix_mult__DOT__b[1U][0U] = 2U;
    vlSelfRef.tb_matrix_mult__DOT__a[1U][1U] = 2U;
    VL_WRITEF_NX("a[          1][          1] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [1U][1U]);
    vlSelfRef.tb_matrix_mult__DOT__b[1U][1U] = 2U;
    vlSelfRef.tb_matrix_mult__DOT__a[1U][2U] = 3U;
    VL_WRITEF_NX("a[          1][          2] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [1U][2U]);
    vlSelfRef.tb_matrix_mult__DOT__b[1U][2U] = 2U;
    vlSelfRef.tb_matrix_mult__DOT__a[1U][3U] = 4U;
    VL_WRITEF_NX("a[          1][          3] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [1U][3U]);
    vlSelfRef.tb_matrix_mult__DOT__b[1U][3U] = 2U;
    vlSelfRef.tb_matrix_mult__DOT__a[2U][0U] = 2U;
    VL_WRITEF_NX("a[          2][          0] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [2U][0U]);
    vlSelfRef.tb_matrix_mult__DOT__b[2U][0U] = 4U;
    vlSelfRef.tb_matrix_mult__DOT__a[2U][1U] = 3U;
    VL_WRITEF_NX("a[          2][          1] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [2U][1U]);
    vlSelfRef.tb_matrix_mult__DOT__b[2U][1U] = 4U;
    vlSelfRef.tb_matrix_mult__DOT__a[2U][2U] = 4U;
    VL_WRITEF_NX("a[          2][          2] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [2U][2U]);
    vlSelfRef.tb_matrix_mult__DOT__b[2U][2U] = 4U;
    vlSelfRef.tb_matrix_mult__DOT__a[2U][3U] = 5U;
    VL_WRITEF_NX("a[          2][          3] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [2U][3U]);
    vlSelfRef.tb_matrix_mult__DOT__b[2U][3U] = 4U;
    vlSelfRef.tb_matrix_mult__DOT__a[3U][0U] = 3U;
    VL_WRITEF_NX("a[          3][          0] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [3U][0U]);
    vlSelfRef.tb_matrix_mult__DOT__b[3U][0U] = 6U;
    vlSelfRef.tb_matrix_mult__DOT__a[3U][1U] = 4U;
    VL_WRITEF_NX("a[          3][          1] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [3U][1U]);
    vlSelfRef.tb_matrix_mult__DOT__b[3U][1U] = 6U;
    vlSelfRef.tb_matrix_mult__DOT__a[3U][2U] = 5U;
    VL_WRITEF_NX("a[          3][          2] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [3U][2U]);
    vlSelfRef.tb_matrix_mult__DOT__b[3U][2U] = 6U;
    vlSelfRef.tb_matrix_mult__DOT__a[3U][3U] = 6U;
    VL_WRITEF_NX("a[          3][          3] = %b\n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__a
                 [3U][3U]);
    vlSelfRef.tb_matrix_mult__DOT__b[3U][3U] = 6U;
    VL_WRITEF_NX("Hello\nWorld\n%b \n%b \n%b \n%b \n%b \n%b \n%b \n%b \n%b \n%b \n%b \n%b \n%b \n%b \n%b \n%b \n",0,
                 4,vlSelfRef.tb_matrix_mult__DOT__c
                 [0U][0U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [0U][1U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [0U][2U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [0U][3U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [1U][0U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [1U][1U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [1U][2U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [1U][3U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [2U][0U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [2U][1U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [2U][2U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [2U][3U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [3U][0U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [3U][1U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [3U][2U],4,vlSelfRef.tb_matrix_mult__DOT__c
                 [3U][3U]);
    VL_FINISH_MT("tb_matrix_mult.v", 62, "");
    vlSelfRef.tb_matrix_mult__DOT__c[0U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[0U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[0U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[0U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[1U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[1U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[1U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[1U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[2U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[2U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[2U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[2U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[3U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[3U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[3U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[3U][3U] = 0U;
}

VL_ATTR_COLD void Vmatrix_mult___024root___eval_final(Vmatrix_mult___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmatrix_mult___024root___eval_final\n"); );
    Vmatrix_mult__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmatrix_mult___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vmatrix_mult___024root___eval_phase__stl(Vmatrix_mult___024root* vlSelf);

VL_ATTR_COLD void Vmatrix_mult___024root___eval_settle(Vmatrix_mult___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmatrix_mult___024root___eval_settle\n"); );
    Vmatrix_mult__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00000064U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vmatrix_mult___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("tb_matrix_mult.v", 4, "", "Settle region did not converge after 100 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
    } while (Vmatrix_mult___024root___eval_phase__stl(vlSelf));
}

VL_ATTR_COLD void Vmatrix_mult___024root___eval_triggers__stl(Vmatrix_mult___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmatrix_mult___024root___eval_triggers__stl\n"); );
    Vmatrix_mult__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VstlTriggered
                                      [0U]) | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
    vlSelfRef.__VstlFirstIteration = 0U;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vmatrix_mult___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
}

VL_ATTR_COLD bool Vmatrix_mult___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmatrix_mult___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmatrix_mult___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vmatrix_mult___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vmatrix_mult___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmatrix_mult___024root___trigger_anySet__stl\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

VL_ATTR_COLD void Vmatrix_mult___024root___stl_sequent__TOP__0(Vmatrix_mult___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmatrix_mult___024root___stl_sequent__TOP__0\n"); );
    Vmatrix_mult__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tb_matrix_mult__DOT__c[0U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[0U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[0U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[0U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[0U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[0U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [0U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [0U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[1U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[1U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[1U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[1U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[1U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [1U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [1U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[2U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[2U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[2U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[2U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[2U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [2U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [2U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][0U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[3U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][0U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [0U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [0U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][1U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[3U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][1U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [1U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [1U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][2U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[3U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][2U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [2U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [2U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][3U] = 0U;
    vlSelfRef.tb_matrix_mult__DOT__c[3U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [0U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [0U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [1U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [1U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [2U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [2U]
                                                    [3U])));
    vlSelfRef.tb_matrix_mult__DOT__c[3U][3U] = (0x0000000fU 
                                                & (vlSelfRef.tb_matrix_mult__DOT__c
                                                   [3U]
                                                   [3U] 
                                                   + 
                                                   (vlSelfRef.tb_matrix_mult__DOT__a
                                                    [3U]
                                                    [3U] 
                                                    * 
                                                    vlSelfRef.tb_matrix_mult__DOT__b
                                                    [3U]
                                                    [3U])));
}

VL_ATTR_COLD void Vmatrix_mult___024root___eval_stl(Vmatrix_mult___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmatrix_mult___024root___eval_stl\n"); );
    Vmatrix_mult__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
        Vmatrix_mult___024root___stl_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD bool Vmatrix_mult___024root___eval_phase__stl(Vmatrix_mult___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmatrix_mult___024root___eval_phase__stl\n"); );
    Vmatrix_mult__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    Vmatrix_mult___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = Vmatrix_mult___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        Vmatrix_mult___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

VL_ATTR_COLD void Vmatrix_mult___024root___ctor_var_reset(Vmatrix_mult___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmatrix_mult___024root___ctor_var_reset\n"); );
    Vmatrix_mult__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 4; ++__Vi1) {
            vlSelf->tb_matrix_mult__DOT__a[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10760500097490481659ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 4; ++__Vi1) {
            vlSelf->tb_matrix_mult__DOT__b[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2726402534628582702ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 4; ++__Vi1) {
            vlSelf->tb_matrix_mult__DOT__c[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18141784476703465338ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
}
