"use client";
import { FormEvent, useState } from "react";
import { Sparkles } from "lucide-react";
import { api } from "@/lib/api";
import styles from "@/styles/graph.module.css";

export function CopilotBar() {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState<string | null>(null);
    const [failed, setFailed] = useState(false);
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e: FormEvent) {
        e.preventDefault();
        if (!question.trim()) return;
        setLoading(true);
        setAnswer(null);
        setFailed(false);
        try {
            const res = await api.askCopilot(question);
            setAnswer(res.answer);
            // A degraded reply is a status message, not a finding — don't let it
            // render as though the Copilot answered the question.
            setFailed(res.available === false);
        } catch (err) {
            setAnswer(err instanceof Error ? err.message : "Copilot query failed");
            setFailed(true);
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
                    placeholder="Ask the Copilot about this graph…"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                />
                <button className={styles.copilotSubmit} type="submit" disabled={loading}>
                    {loading ? "…" : "Ask"}
                </button>
            </form>
            {loading && <p className={styles.copilotAnswer}>Searching fraud records…</p>}
            {answer && !loading && (
                <p className={`${styles.copilotAnswer} ${failed ? styles.copilotAnswerError : ""}`} role={failed ? "alert" : undefined}>
                    {answer}
                </p>
            )}
        </div>
    );
}
