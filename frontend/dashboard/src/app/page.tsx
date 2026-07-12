"use client";
import { PhoneCall, ShieldCheck, FileWarning, Activity } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { StatCard } from "@/components/dashboard/StatCard";
import { ThreatLevel } from "@/components/dashboard/ThreatLevel";
import { LiveAlertFeed } from "@/components/dashboard/LiveAlertFeed";
import { MiniMap } from "@/components/dashboard/MiniMap";
import { LoadingSkeleton } from "@/components/shared/LoadingSkeleton";
import { useApi } from "@/hooks/useApi";
import { api } from "@/lib/api";
import styles from "@/styles/dashboard.module.css";

export default function HomeDashboard() {
    const { data: stats, isLoading: statsLoading } = useApi("scam-stats", () => api.getScamStats(), {
        refreshInterval: 15000,
    });
    const { data: sessions, isLoading: sessionsLoading } = useApi(
        "scam-sessions-recent",
        () => api.getScamSessions({ limit: 20 }),
        { refreshInterval: 10000 }
    );

    const redCount = Number(stats?.red_count ?? 0);
    const amberCount = Number(stats?.amber_count ?? 0);
    const yellowCount = Number(stats?.yellow_count ?? 0);
    const totalSessions = Number(stats?.total_sessions ?? redCount + amberCount + yellowCount);

    return (
        <>
            <PageHeader title="Home Dashboard" subtitle="Real-time overview across all Primer modules" />

            <div className={styles.statGrid}>
                {statsLoading ? (
                    Array.from({ length: 4 }).map((_, i) => <LoadingSkeleton key={i} height={78} />)
                ) : (
                    <>
                        <StatCard label="Total Sessions" value={totalSessions} icon={<Activity size={16} />} />
                        <StatCard label="Red Alerts" value={redCount} icon={<PhoneCall size={16} />} tone="red" />
                        <StatCard label="Amber Alerts" value={amberCount} icon={<FileWarning size={16} />} tone="amber" />
                        <StatCard label="Resolved" value={yellowCount} icon={<ShieldCheck size={16} />} tone="green" />
                    </>
                )}
            </div>

            <div className={styles.dashboardGrid}>
                {sessionsLoading ? (
                    <LoadingSkeleton height={320} />
                ) : (
                    <LiveAlertFeed sessions={sessions ?? []} />
                )}
                <div className={styles.rightRail}>
                    <ThreatLevel redCount={redCount} amberCount={amberCount} yellowCount={yellowCount} />
                    <MiniMap />
                </div>
            </div>
        </>
    );
}
