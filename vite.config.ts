import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    host: true, // Listen on all addresses
    watch: {
      usePolling: true, // Enable polling for Docker
      interval: 1000, // Poll every second
    },
    hmr: {
      clientPort: 5173, // HMR client port
    },
  },
  base: './',
})

