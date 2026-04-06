const rawApiUrl =
  process.env.API_BASE_URL ??
  process.env.NEXT_PUBLIC_API_URL ??
  "http://127.0.0.1:8000";

export const env = {
  apiBaseUrl: rawApiUrl.replace(/\/$/, ""),
} as const;