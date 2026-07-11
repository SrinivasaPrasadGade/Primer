"use client";
import { ReactNode, useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";
import styles from "./layout.module.css";

export function AppShell({ children }: { children: ReactNode }) {
    const pathname = usePathname();
    const router = useRouter();
    const { user, loading } = useAuth();
    const isLoginPage = pathname === "/login";

    useEffect(() => {
        if (!loading && !user && !isLoginPage) router.replace("/login");
    }, [loading, user, isLoginPage, router]);

    if (isLoginPage) return <>{children}</>;

    if (loading || !user) {
        return <div className={styles.fullscreenCenter}>Loading…</div>;
    }

    return (
        <div className={styles.shell}>
            <Navbar />
            <div className={styles.shellBody}>
                <Sidebar />
                <main className={styles.main}>{children}</main>
            </div>
        </div>
    );
}
