/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_API_GATEWAY_URL: string
  readonly VITE_AWS_REGION: string
  readonly VITE_ENABLE_DEMO_MODE: string
  readonly VITE_ENABLE_OFFLINE_MODE: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
