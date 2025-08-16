import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
  build: {
    outDir: "static", // 👈 Vite build output goes here
    emptyOutDir: true,
  },
});
