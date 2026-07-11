"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, PhoneCall, Landmark, Share2, Map, MessageSquareText, FileSearch } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import styles from "@/styles/layout.module.css";

const NAV_ITEMS = [
    { href: "/", label: "Dashboard", icon: Home },
    { href: "/scam", label: "Scam Sentinel", icon: PhoneCall },
    { href: "/notes", label: "Note Verify", icon: Landmark },
    { href: "/graph", label: "Fraud Graph", icon: Share2 },
    { href: "/geo", label: "Geo Intel", icon: Map },
    { href: "/copilot", label: "AI Copilot", icon: MessageSquareText },
    { href: "/case", label: "Case Summarizer", icon: FileSearch },
];

export function Sidebar() {
    const pathname = usePathname();
    const { user } = useAuth();

    if (!user) return null;

    return (
        <nav className={styles.sidebar}>
            {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
                const active = href === "/" ? pathname === "/" : pathname.startsWith(href);
                return (
                    <Link key={href} href={href} className={`${styles.navItem} ${active ? styles.navItemActive : ""}`}>
                        <Icon size={17} />
                        <span>{label}</span>
                    </Link>
                );
            })}
        </nav>
    );
}
