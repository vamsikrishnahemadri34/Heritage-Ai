import axios from "axios";

import { env } from "@/config/env";

// eslint-disable-next-line import/no-named-as-default-member
const apiClient = axios.create({
  baseURL: env.apiUrl,
  headers: {
    Accept: "application/json",
  },
  timeout: 15000,
});

apiClient.interceptors.request.use(async (config) => {
  console.log(
    "[API TRACE] request:",
    config.method?.toUpperCase(),
    config.url,
  );

  return config;
});

export default apiClient;

