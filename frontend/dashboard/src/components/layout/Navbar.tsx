"use client";
import { useState } from "react";
import { Bell, LogOut, ShieldAlert } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import styles from "./layout.module.css";

export function Navbar() {
    const { user, logout } = useAuth();
    const [menuOpen, setMenuOpen] = useState(false);

    return (
        <header className={styles.navbar}>
            <div className={styles.navbarBrand}>
                <ShieldAlert size={20} color="var(--accent-500)" />
                <span>Primer</span>
            </div>
            <div className={styles.navbarActions}>
                <button className={styles.iconButton} aria-label="Notifications">
                    <Bell size={18} />
                </button>
                <div className={styles.userMenu}>
                    <button className={styles.userButton} onClick={() => setMenuOpen((v) => !v)}>
                        <span className={styles.userName}>{user?.name ?? "..."}</span>
                        <span className={styles.userRole}>{user?.role}</span>
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
