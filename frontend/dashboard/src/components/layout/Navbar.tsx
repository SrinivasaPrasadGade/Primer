"use client";
import { useState } from "react";
import Link from "next/link";
import { Bell, LogOut, ShieldAlert } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { useApi } from "@/hooks/useApi";
import { api } from "@/lib/api";
import styles from "@/styles/layout.module.css";

export function Navbar() {
    const { user, logout } = useAuth();
    const [menuOpen, setMenuOpen] = useState(false);
    const [notifOpen, setNotifOpen] = useState(false);

    const { data: redSessions } = useApi(
        user ? "notifications-red" : null,
        () => api.getScamSessions({ alert_level: "RED", limit: 5 }),
        { refreshInterval: 15000 }
    );
    const count = redSessions?.length ?? 0;

    if (!user) return null;

    return (
        <header className={styles.navbar}>
            <div className={styles.navbarBrand}>
                <ShieldAlert size={20} color="var(--accent-500)" />
                <span>Primer</span>
            </div>
            <div className={styles.navbarActions}>
                {/* Notification dropdown */}
                <div className={styles.userMenu}>
                    <button className={styles.iconButton} aria-label="Notifications" onClick={() => setNotifOpen((v) => !v)}>
                        <Bell size={18} />
                        {count > 0 && <span className={styles.notificationDot}>{count}</span>}
                    </button>
                    {notifOpen && (
                        <div className={styles.userDropdown} style={{ width: 280 }}>
                            {count === 0 ? (
                                <div className={styles.dropdownItem}>No active RED alerts</div>
                            ) : (
                                redSessions!.map((s) => (
                                    <Link
                                        key={s.id}
                                        href={`/scam/${s.id}`}
                                        className={styles.dropdownItem}
                                        onClick={() => setNotifOpen(false)}
                                    >
                                        <span>{s.caller_number}</span>
                                        <span style={{ marginLeft: "auto", color: "var(--color-text-tertiary)" }}>{s.scam_type}</span>
                                    </Link>
                                ))
                            )}
                        </div>
                    )}
                </div>

                <div className={styles.userMenu}>
                    <button className={styles.userButton} onClick={() => setMenuOpen((v) => !v)}>
                        <span className={styles.userName}>{user.name}</span>
                        <span className={styles.userRole}>{user.role}</span>
                    </button>
                    {menuOpen && (
                        <div className={styles.userDropdown}>
                            <button className={styles.dropdownItem} onClick={logout}>
                                <LogOut size={14} />
                                <span>Log out</span>
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
}
