const SystemConfig = {
    BACKEND_IP: "http://127.0.0.1",
    BACKEND_PORT: "8000",
    BASE_URL: import.meta.env.VITE_APP_BASE_API || "http://127.0.0.1:8000/api/v1",
}

export default SystemConfig