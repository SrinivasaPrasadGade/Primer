"use client";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { ShieldAlert } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { ApiError } from "@/lib/api";

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
            router.push(user.role === "bank_manager" ? "/notes" : "/dashboard");
        } catch (err) {
            setError(err instanceof ApiError ? err.message : "Unable to sign in. Try again.");
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <div className="login-page">
            <form className="login-card" onSubmit={handleSubmit}>
                <div className="login-brand">
                    <ShieldAlert size={28} color="var(--accent-500)" />
                    <span>Primer</span>
                </div>
                <p className="login-subtitle">Digital Public Safety Intelligence Platform</p>

                <label className="login-label" htmlFor="email">
                    Email
                </label>
                <input
                    id="email"
                    className="login-input"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@primer.demo"
                    required
                    autoFocus
                />

                <label className="login-label" htmlFor="password">
                    Password
                </label>
                <input
                    id="password"
                    className="login-input"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                />

                {error && <p className="login-error">{error}</p>}

                <button className="login-submit" type="submit" disabled={submitting}>
                    {submitting ? "Signing in…" : "Sign in"}
                </button>
            </form>
        </div>
    );
}
