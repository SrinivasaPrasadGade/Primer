import { AuthProvider } from "@/hooks/useAuth";
import { AppShell } from "@/components/layout/AppShell";
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
          <AppShell>{children}</AppShell>
        </AuthProvider>
      </body>
    </html>
  );
}
