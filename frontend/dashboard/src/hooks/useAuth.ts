"use client";
import { createContext, createElement, useContext, useEffect, useState, ReactNode } from "react";
import { usePathname, useRouter } from "next/navigation";
import { api, ApiError } from "@/lib/api";
import { AuthUser, USER_STORAGE_KEY } from "@/lib/constants";

interface AuthContextValue {
    user: AuthUser | null;
    loading: boolean;
    login: (email: string, password: string) => Promise<AuthUser>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<AuthUser | null>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();
    const pathname = usePathname();

    useEffect(() => {
        const token = api.loadToken();
        if (!token) {
            setLoading(false);
            return;
        }
        api
            .me()
            .then((me) => {
                setUser(me);
                window.localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(me));
            })
            .catch((err: unknown) => {
                if (err instanceof ApiError && (err.status === 401 || err.status === 403)) {
                    api.setToken(null);
                    window.localStorage.removeItem(USER_STORAGE_KEY);
                }
            })
            .finally(() => setLoading(false));
    }, []);

    // Redirect unauthenticated users to /login (folded in from the old AppShell)
    useEffect(() => {
        if (!loading && !user && pathname !== "/login") router.replace("/login");
    }, [loading, user, pathname, router]);

    async function login(email: string, password: string) {
        const { access_token, user: loggedInUser } = await api.login(email, password);
        api.setToken(access_token);
        window.localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(loggedInUser));
        setUser(loggedInUser);
        return loggedInUser;
    }

    function logout() {
        api.setToken(null);
        window.localStorage.removeItem(USER_STORAGE_KEY);
        setUser(null);
        router.replace("/login");
    }

    return createElement(AuthContext.Provider, { value: { user, loading, login, logout } }, children);
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used within AuthProvider");
    return ctx;
}
