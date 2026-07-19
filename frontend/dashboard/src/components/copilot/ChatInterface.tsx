"use client";
import { FormEvent, useEffect, useRef, useState } from "react";
import { Send } from "lucide-react";
import { api } from "@/lib/api";
import { ChatMessage, ChatMessageData, ToolCall } from "./ChatMessage";
import styles from "@/styles/copilot.module.css";

export function ChatInterface() {
    const [messages, setMessages] = useState<ChatMessageData[]>([
        { role: "assistant", text: "Ask me about scam sessions, fraud entities, or crime stats — I can query the platform directly." },
    ]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const messagesRef = useRef<HTMLDivElement>(null);
    // Don't yank the view back down if the officer scrolled up to re-read an
    // earlier answer; only follow along when they're already at the bottom.
    const pinnedToBottom = useRef(true);

    function handleScroll() {
        const el = messagesRef.current;
        if (!el) return;
        pinnedToBottom.current = el.scrollHeight - el.scrollTop - el.clientHeight < 80;
    }

    // Keep the newest message in view as the conversation grows. Setting
    // scrollTop directly rather than scrollIntoView(), which aligns against the
    // container's bottom padding and leaves the last line clipped. The rAF pass
    // catches markdown that changes height after the first paint (tables, code).
    useEffect(() => {
        const el = messagesRef.current;
        if (!el || !pinnedToBottom.current) return;
        const toBottom = () => {
            el.scrollTop = el.scrollHeight;
        };
        toBottom();
        const raf = requestAnimationFrame(toBottom);
        return () => cancelAnimationFrame(raf);
    }, [messages, loading]);

    async function handleSubmit(e: FormEvent) {
        e.preventDefault();
        const question = input.trim();
        if (!question) return;
        setInput("");
        setMessages((prev) => [...prev, { role: "user", text: question }]);
        setLoading(true);
        try {
            const res = await api.askCopilot(question);
            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    text: res.answer,
                    sources: res.sources,
                    queryExecuted: res.query_executed as ToolCall[] | undefined,
                    // A degraded reply is a status message, not a finding — don't let
                    // it render as though the Copilot answered the question.
                    failed: res.available === false,
                },
            ]);
        } catch (err) {
            setMessages((prev) => [
                ...prev,
                { role: "assistant", text: err instanceof Error ? err.message : "Something went wrong.", failed: true },
            ]);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.chat}>
            <div className={styles.messages} ref={messagesRef} onScroll={handleScroll}>
                {messages.map((m, i) => (
                    <ChatMessage key={i} message={m} />
                ))}
                {loading && <ChatMessage message={{ role: "assistant", text: "Thinking…" }} />}
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
