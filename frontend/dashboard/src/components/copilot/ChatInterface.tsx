"use client";
import { FormEvent, useState } from "react";
import { Send } from "lucide-react";
import { api } from "@/lib/api";
import { ChatMessage, ChatMessageData } from "./ChatMessage";
import styles from "@/styles/copilot.module.css";

export function ChatInterface() {
    const [messages, setMessages] = useState<ChatMessageData[]>([
        { role: "assistant", text: "Ask me about scam sessions, fraud entities, or crime stats — I can query the platform directly." },
    ]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e: FormEvent) {
        e.preventDefault();
        const question = input.trim();
        if (!question) return;
        setInput("");
        setMessages((prev) => [...prev, { role: "user", text: question }]);
        setLoading(true);
        try {
            const res = await api.askCopilot(question);
            setMessages((prev) => [...prev, { role: "assistant", text: res.answer }]);
        } catch (err) {
            setMessages((prev) => [...prev, { role: "assistant", text: err instanceof Error ? err.message : "Something went wrong." }]);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.chat}>
            <div className={styles.messages}>
                {messages.map((m, i) => (
                    <ChatMessage key={i} message={m} />
                ))}
                {loading && <ChatMessage message={{ role: "assistant", text: "", pending: true }} />}
            </div>
            <form className={styles.inputBar} onSubmit={handleSubmit}>
                <input
                    className={styles.input}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a question…"
                />
                <button className={styles.sendButton} type="submit" disabled={loading}>
                    <Send size={16} />
                </button>
            </form>
        </div>
    );
}
