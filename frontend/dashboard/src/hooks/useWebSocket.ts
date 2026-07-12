"use client";
import { useEffect, useRef, useState } from "react";

// Live feed hook (doc §5.4). Same shape/return as the doc, but the reconnect
// is corrected: the doc's snippet reopens the socket without re-attaching the
// onopen/onmessage/onclose handlers, so a reconnected socket would go silent.
// Here connect() re-binds every handler, and teardown cancels a pending retry.
export function useWebSocket<T>(url: string) {
    const [messages, setMessages] = useState<T[]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const ws = useRef<WebSocket | null>(null);
    const reconnectTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
    const closedByClient = useRef(false);

    useEffect(() => {
        closedByClient.current = false;

        function connect() {
            const socket = new WebSocket(url);
            ws.current = socket;

            socket.onopen = () => setIsConnected(true);
            socket.onclose = () => {
                setIsConnected(false);
                // Auto-reconnect after 3 seconds (unless the component unmounted)
                if (!closedByClient.current) {
                    reconnectTimer.current = setTimeout(connect, 3000);
                }
            };
            socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data) as T;
                    setMessages((prev) => [data, ...prev].slice(0, 100)); // Keep last 100
                } catch {
                    // ignore non-JSON keep-alive frames
                }
            };
        }

        connect();

        return () => {
            closedByClient.current = true;
            if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
            ws.current?.close();
        };
    }, [url]);

    return { messages, isConnected };
}
