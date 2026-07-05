export const metadata = {
  title: "Primer Dashboard",
  description: "Primer — AI-Powered Digital Public Safety Intelligence Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
