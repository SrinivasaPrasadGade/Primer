"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSWRConfig } from "swr";
import { PageHeader } from "@/components/layout/PageHeader";
import { SessionCard } from "@/components/scam/SessionCard";
import { LoadingSkeleton } from "@/components/shared/LoadingSkeleton";
import { useApi } from "@/hooks/useApi";
import { useWebSocket } from "@/hooks/useWebSocket";
import { api } from "@/lib/api";
import { wsScamLiveUrl } from "@/lib/constants";
import styles from "@/styles/scam.module.css";

const FILTERS = ["ALL", "RED", "AMBER", "YELLOW"] as const;

interface LiveEvent {
    session_id: string;
    alert_level: string;
    overall_confidence: number;
}

export default function ScamLiveMonitor() {
    const router = useRouter();
    const { mutate } = useSWRConfig();
    const [filter, setFilter] = useState<(typeof FILTERS)[number]>("ALL");
    const key = `scam-sessions-${filter}`;

    const { data: sessions, isLoading } = useApi(key, () =>
        api.getScamSessions(filter === "ALL" ? { limit: 50 } : { alert_level: filter, limit: 50 })
    );
    const { messages, isConnected } = useWebSocket<LiveEvent>(wsScamLiveUrl(api.getToken()));

    useEffect(() => {
        if (messages.length > 0) mutate(key);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [messages.length]);

    return (
        <>
            <PageHeader
                title="Scam Sentinel — Live Monitor"
                subtitle={isConnected ? "Live feed connected" : "Reconnecting to live feed…"}
            />

            <div className={styles.filterBar}>
                {FILTERS.map((f) => (
                    <button
                        key={f}
                        className={`${styles.filterButton} ${filter === f ? styles.filterButtonActive : ""}`}
                        onClick={() => setFilter(f)}
                    >
                        {f}
                    </button>
                ))}
            </div>

            <div className={styles.sessionGrid}>
                {isLoading
                    ? Array.from({ length: 6 }).map((_, i) => <LoadingSkeleton key={i} height={140} />)
                    : (sessions ?? []).map((session) => (
                          <SessionCard key={session.id} session={session} onClick={() => router.push(`/scam/${session.id}`)} />
                      ))}
            </div>
        </>
    );
}
