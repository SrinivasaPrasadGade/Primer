"use client";
import { usePathname } from "next/navigation";
import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";
import styles from "@/styles/layout.module.css";

// Routes that are standalone (marketing / auth) and must render full-bleed without the
// dashboard navbar + sidebar chrome.
const BARE_ROUTES = ["/landing", "/login"];

export function AppShell({ children }: { children: React.ReactNode }) {
    const pathname = usePathname();
    const bare = BARE_ROUTES.some((r) => pathname === r || pathname.startsWith(r + "/"));

    if (bare) {
        return <>{children}</>;
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
