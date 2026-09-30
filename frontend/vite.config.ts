import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
      "/ws": {
        target: "ws://127.0.0.1:8000",
        ws: true,
      },
    },
  },
  build: {
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks(id) {
          const normalizedId = id.replace(/\\/g, "/");

          if (
            normalizedId.includes("node_modules/three") ||
            normalizedId.includes("@react-three")
          ) {
            return "vendor-three";
          }
          if (normalizedId.includes("node_modules/pixi.js") || normalizedId.includes("@pixi")) {
            return "vendor-pixi";
          }
          if (normalizedId.includes("@dnd-kit")) {
            return "vendor-dnd";
          }
          if (normalizedId.includes("framer-motion")) {
            return "vendor-motion";
          }
          if (normalizedId.includes("lucide-react")) {
            return "vendor-icons";
          }
          if (normalizedId.includes("html2canvas")) {
            return "vendor-html2canvas";
          }
          if (
            normalizedId.includes("node_modules/react/") ||
            normalizedId.includes("node_modules/react-dom/") ||
            normalizedId.includes("node_modules/react-router") ||
            normalizedId.includes("@tanstack/react-query")
          ) {
            return "vendor-react";
          }
        },
      },
    },
  },
});
