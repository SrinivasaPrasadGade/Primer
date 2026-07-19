import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";
import styles from "@/styles/layout.module.css";

export const metadata = {
    title: "Primer Dashboard",
};

// Chrome for every authenticated route. useAuth bounces unauthenticated
// visitors to /login before any of these pages render.
export default function AppLayout({ children }: { children: React.ReactNode }) {
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
