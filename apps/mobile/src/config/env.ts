const FALLBACK_API_URL = "https://heritageai-api.onrender.com/api/v1";

export const env = {
  apiUrl:
    process.env.EXPO_PUBLIC_API_URL?.replace(/\/+$/, "") ??
    FALLBACK_API_URL,



} as const;

