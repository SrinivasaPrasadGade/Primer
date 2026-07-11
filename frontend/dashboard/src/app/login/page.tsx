"use client";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { ShieldAlert } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { ApiError } from "@/lib/api";
import styles from "./login.module.css";

export default function LoginPage() {
    const { login } = useAuth();
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState(false);

    async function handleSubmit(e: FormEvent) {
        e.preventDefault();
        setError(null);
        setSubmitting(true);
        try {
            const user = await login(email, password);
            router.push(user.role === "bank_manager" ? "/notes" : "/");
        } catch (err) {
            setError(err instanceof ApiError ? err.message : "Unable to sign in. Try again.");
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <div className={styles.page}>
            <form className={styles.card} onSubmit={handleSubmit}>
                <div className={styles.brand}>
                    <ShieldAlert size={28} color="var(--accent-500)" />
                    <span>Primer</span>
                </div>
                <p className={styles.subtitle}>Digital Public Safety Intelligence Platform</p>

                <label className={styles.label} htmlFor="email">
                    Email
                </label>
                <input
                    id="email"
                    className={styles.input}
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@primer.demo"
                    required
                    autoFocus
                />

                <label className={styles.label} htmlFor="password">
                    Password
                </label>
                <input
                    id="password"
                    className={styles.input}
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                />

                {error && <p className={styles.error}>{error}</p>}

                <button className={styles.submit} type="submit" disabled={submitting}>
                    {submitting ? "Signing in…" : "Sign in"}
                </button>
            </form>
        </div>
    );
}
