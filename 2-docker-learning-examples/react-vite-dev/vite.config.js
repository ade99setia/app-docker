import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import process from 'process'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 18089,
    strictPort: true,
    watch:
      process.env.VITE_USE_POLLING === 'true'
        ? {
            usePolling: true,
            interval: 1000,
          }
        : undefined,
  },
})