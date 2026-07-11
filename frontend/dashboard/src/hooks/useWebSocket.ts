"use client";
import { useEffect, useRef, useState } from "react";

export function useWebSocket<T>(url: string) {
    const [messages, setMessages] = useState<T[]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const wsRef = useRef<WebSocket | null>(null);
    const reconnectTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
    const closedByClient = useRef(false);

    useEffect(() => {
        closedByClient.current = false;

        function connect() {
            const ws = new WebSocket(url);
            wsRef.current = ws;

            ws.onopen = () => setIsConnected(true);
            ws.onclose = () => {
                setIsConnected(false);
                if (!closedByClient.current) {
                    reconnectTimer.current = setTimeout(connect, 3000);
                }
            };
            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data) as T;
                    setMessages((prev) => [data, ...prev].slice(0, 100));
                } catch {
                    // ignore non-JSON keep-alive messages
                }
            };
        }

        connect();

        return () => {
            closedByClient.current = true;
            if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
            wsRef.current?.close();
        };
    }, [url]);

    return { messages, isConnected };
}
