import { ReactNode, useEffect } from "react";

interface ModalProps {
  titulo: string;
  onCerrar: () => void;
  children: ReactNode;
}

export default function Modal({ titulo, onCerrar, children }: ModalProps) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onCerrar(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onCerrar]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/50 backdrop-blur-sm"
      onClick={(e) => { if (e.target === e.currentTarget) onCerrar(); }}
    >
      <div className="bg-white rounded-t-3xl sm:rounded-2xl w-full sm:max-w-lg max-h-[92vh] overflow-y-auto shadow-2xl">
        <div className="flex items-center justify-between px-5 py-4 border-b border-gray-100 sticky top-0 bg-white rounded-t-3xl sm:rounded-t-2xl">
          <h2 className="text-base font-bold text-[#1D3557]">{titulo}</h2>
          <button
            onClick={onCerrar}
            className="p-1.5 rounded-xl hover:bg-gray-100 transition-colors"
            aria-label="Cerrar"
          >
            <span className="material-icons text-gray-400" style={{ fontSize: "20px" }}>close</span>
          </button>
        </div>
        <div className="p-5">{children}</div>
      </div>
    </div>
  );
}
