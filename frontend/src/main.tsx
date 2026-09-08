/**
 * @file main.tsx
 * @description Bootstrap y renderizado raíz del DOM para LeoFit PWA
 * @project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
 * @author Lady Luz Loayza Rodriguez (@LadyyLuz) <168585420+luzylay@users.noreply.github.com>
 * @copyright (c) 2026 Grupo 01 - UTP. All rights reserved.
 */

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
