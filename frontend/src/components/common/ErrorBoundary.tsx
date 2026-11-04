/**
 * @file ErrorBoundary.tsx
 * @description Límite de error (ErrorBoundary) reactivo con diseño LeoFit y recuperación automática
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import React, { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error("ErrorBoundary capturó una excepción en la interfaz:", error, errorInfo);
  }

  handleReload = (): void => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  handleReset = (): void => {
    this.setState({ hasError: false, error: null });
  };

  render(): ReactNode {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-[#0F223D] flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl border border-slate-200 text-center animate-in zoom-in-95">
            <div className="w-16 h-16 bg-red-100 text-red-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-inner">
              <span className="material-icons" style={{ fontSize: "36px" }}>warning</span>
            </div>

            <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 mb-2">
              Se produjo una incidencia visual
            </h2>

            <p className="text-xs sm:text-sm text-slate-600 mb-4 leading-relaxed font-medium">
              El sistema protegió los datos de la sesión para evitar pérdida de información.
            </p>

            {this.state.error && (
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-left text-xs text-slate-700 font-mono overflow-x-auto max-h-32 mb-5">
                {this.state.error.message}
              </div>
            )}

            <div className="flex flex-col sm:flex-row gap-2.5">
              <button
                onClick={this.handleReset}
                className="flex-1 py-3 bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold rounded-xl text-xs sm:text-sm transition-all"
              >
                Volver a intentar
              </button>
              <button
                onClick={this.handleReload}
                className="flex-1 py-3 bg-[#E63946] hover:bg-[#C62828] text-white font-bold rounded-xl text-xs sm:text-sm transition-all shadow-md shadow-red-500/20 active:scale-95"
              >
                Recargar Sistema
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
