import { AuthProvider } from "@/hooks/useAuth";
import "@/styles/globals.css";

// Generic by default so the public landing page reads correctly; the (app)
// group overrides this with the console title.
export const metadata = {
  title: "Primer — Digital Public Safety Intelligence Platform",
  description: "Primer — AI-Powered Digital Public Safety Intelligence Platform",
};

// Only the auth context and global styles live here. The signed-in chrome
// (navbar + sidebar) belongs to the (app) route group, so public pages such as
// the landing page and login screen render without it.
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
