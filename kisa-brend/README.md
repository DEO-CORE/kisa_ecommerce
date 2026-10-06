# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  # KISA Shop frontend

  React storefront for [kisa_shop_backend](https://github.com/Mardon-programm/kisa_shop_backend).

  ## Run locally

  1. Start the Django backend on `http://127.0.0.1:8000` and make sure its database contains active products, colors, sizes, and stock records.
  2. Copy `.env.example` to `.env.local`. The default `/api` URL uses the Vite proxy to reach Django; `/media` images use the same proxy.
  3. Install dependencies and start Vite:

  ```bash
  npm install
  npm run dev
  ```

  The storefront loads `/api/catalog/products/` and submits checkouts to `/api/orders/`. If the API is unavailable, the storefront uses its demo catalogue.

  For deployment, set `VITE_API_URL` to the API base ending in `/api`. Since the backend does not enable cross-origin requests, serve the frontend and API through the same origin or configure a reverse proxy.
        tsconfigRootDir: import.meta.dirname,
