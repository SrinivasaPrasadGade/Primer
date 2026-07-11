import { AuthProvider } from "@/hooks/useAuth";
import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";
import styles from "@/styles/layout.module.css";
import "@/styles/globals.css";

export const metadata = {
  title: "Primer Dashboard",
  description: "Primer — AI-Powered Digital Public Safety Intelligence Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <div className={styles.shell}>
            <Navbar />
            <div className={styles.shellBody}>
              <Sidebar />
              <main className={styles.main}>{children}</main>
            </div>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
