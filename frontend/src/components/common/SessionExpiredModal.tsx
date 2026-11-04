import { useEffect, useState } from 'react';
import { onAuthEvent } from '../../services/api';

export function SessionExpiredModal() {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const unsubscribe = onAuthEvent((evt) => {
      if (evt === 'logout') setOpen(true);
      if (evt === 'refreshed') setOpen(false);
    });
    return () => {
      unsubscribe();
    };
  }, []);

  if (!open) return null;

  return (
    <div 
      className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in"
      role="dialog"
      aria-modal="true"
      aria-labelledby="session-expired-title"
    >
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-sm w-full p-6 text-center transform transition-all">
        <div className="w-14 h-14 mx-auto mb-4 bg-amber-100 dark:bg-amber-950/50 text-amber-600 dark:text-amber-400 rounded-full flex items-center justify-center text-2xl">
          ⏳
        </div>
        <h2 id="session-expired-title" className="text-xl font-bold text-slate-900 dark:text-white mb-2">
          Sesión Finalizada
        </h2>
        <p className="text-slate-600 dark:text-slate-300 text-sm mb-6 leading-relaxed">
          Por motivos de seguridad y resguardo de datos, tu sesión ha caducado. Vuelve a iniciar sesión para continuar gestionando pedidos.
        </p>
        <button
          type="button"
          onClick={() => {
            setOpen(false);
            window.location.reload();
          }}
          className="w-full bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white font-semibold py-3 px-4 rounded-xl shadow-md transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none"
        >
          Volver a Ingresar
        </button>
      </div>
    </div>
  );
}
