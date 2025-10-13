import { defineConfig } from "vite";
import { resolve } from "path";
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  root: ".",
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: resolve("./assets"),
    assetsDir:"django-assets",

    emptyOutDir: true, // Limpa antes de buildar
    rollupOptions: {
      input: {
        main: resolve("./static/js/main.js"), // ← Mudei de 'test' para 'main'
      },
    },
  },
  plugins: [
    tailwindcss(),
  ],
  server: {
    origin: 'http://localhost:5173',
    port: 5173,
  },
}); 