"use client";
import { FormEvent, useState } from "react";
import { Sparkles } from "lucide-react";
import { api } from "@/lib/api";
import styles from "@/styles/graph.module.css";

// `context` is an optional hint (e.g. the currently-selected entity value) that gets
// prepended to the officer's question so the Copilot answers about the graph in view.
export function CopilotBar({ context }: { context?: string | null }) {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e: FormEvent) {
        e.preventDefault();
        const q = question.trim();
        if (!q || loading) return;
        setLoading(true);
        setAnswer(null);
        try {
            const framed = context ? `Regarding entity ${context}: ${q}` : q;
            const res = await api.askCopilot(framed);
            setAnswer(res.answer || "No answer returned.");
        } catch (err) {
            setAnswer(err instanceof Error ? err.message : "Copilot query failed");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.copilotBar}>
            <form onSubmit={handleSubmit} className={styles.copilotForm}>
                <Sparkles size={16} color="var(--accent-500)" />
                <input
                    className={styles.copilotInput}
                    placeholder={context ? `Ask about ${context}…` : "Ask the Copilot about this graph…"}
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                />
                <button className={styles.copilotSubmit} type="submit" disabled={loading || !question.trim()}>
                    {loading ? "Asking…" : "Ask"}
                </button>
            </form>
            {(answer || loading) && (
                <p className={styles.copilotAnswer}>{loading ? "Querying the fraud platform…" : answer}</p>
            )}
        </div>
    );
}
