"use client";
import { useState } from "react";
import Link from "next/link";
import { Bell, LogOut, ShieldAlert, Siren } from "lucide-react";
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
    // SOS events are lea_officer-only on the backend; requesting them as any other
    // role just 403s, so don't ask.
    const { data: sosEvents } = useApi(
        user?.role === "lea_officer" ? "notifications-sos" : null,
        () => api.getPanicEvents(5),
        { refreshInterval: 15000 }
    );
    const sosCount = sosEvents?.length ?? 0;
    const count = (redSessions?.length ?? 0) + sosCount;

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
                        <div className={styles.userDropdown} style={{ width: 300 }}>
                            {count === 0 ? (
                                <div className={styles.dropdownItem}>No active alerts</div>
                            ) : (
                                <>
                                    {/* Citizen SOS outranks everything else in here. */}
                                    {sosEvents?.map((e) => (
                                        <div key={e.id} className={styles.dropdownItem} style={{ alignItems: "flex-start" }}>
                                            <Siren size={14} color="var(--color-red)" style={{ flexShrink: 0, marginTop: 2 }} />
                                            <div style={{ display: "flex", flexDirection: "column", gap: 2, minWidth: 0 }}>
                                                <span style={{ color: "var(--color-red)", fontWeight: 600 }}>
                                                    SOS · {e.user_name ?? e.user_email ?? "Unknown citizen"}
                                                </span>
                                                <span style={{ color: "var(--color-text-tertiary)", fontSize: 12 }}>
                                                    {new Date(e.triggered_at).toLocaleString()}
                                                    {e.location ? ` · ${e.location.lat.toFixed(4)}, ${e.location.lng.toFixed(4)}` : " · no location"}
                                                </span>
                                            </div>
                                        </div>
                                    ))}
                                    {redSessions?.map((s) => (
                                        <Link
                                            key={s.id}
                                            href={`/scam/${s.id}`}
                                            className={styles.dropdownItem}
                                            onClick={() => setNotifOpen(false)}
                                        >
                                            <span>{s.caller_number}</span>
                                            <span style={{ marginLeft: "auto", color: "var(--color-text-tertiary)" }}>{s.scam_type}</span>
                                        </Link>
                                    ))}
                                </>
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
