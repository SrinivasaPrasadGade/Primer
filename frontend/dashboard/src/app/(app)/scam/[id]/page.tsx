"use client";
import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/shared/Card";
import { LoadingSkeleton } from "@/components/shared/LoadingSkeleton";
import { SessionDetail } from "@/components/scam/SessionDetail";
import { useApi } from "@/hooks/useApi";
import { api } from "@/lib/api";
import styles from "@/styles/scam.module.css";

export default function ScamSessionDetailPage() {
    const params = useParams<{ id: string }>();
    const router = useRouter();
    const { data: session, error, isLoading, mutate } = useApi(
        params.id ? `scam-session-${params.id}` : null,
        () => api.getScamSession(params.id)
    );

    // Both actions only change server state, so without a pending/error state a failed
    // call is indistinguishable from a successful one.
    const [pendingAction, setPendingAction] = useState<"acknowledge" | "reclassify" | null>(null);
    const [actionError, setActionError] = useState<string | null>(null);

    async function runAction(action: "acknowledge" | "reclassify", call: () => Promise<unknown>) {
        setPendingAction(action);
        setActionError(null);
        try {
            await call();
            await mutate();
        } catch (err) {
            setActionError(err instanceof Error ? err.message : `Failed to ${action} this session`);
        } finally {
            setPendingAction(null);
        }
    }

    const handleAcknowledge = () => runAction("acknowledge", () => api.acknowledgeScamSession(params.id));
    const handleReclassify = () => runAction("reclassify", () => api.classifyScamSession(params.id));

    if (error) {
        return (
            <>
                <PageHeader title="Session Detail" />
                <Card>
                    <p style={{ color: "var(--color-text-secondary)", fontSize: 13 }}>
                        {error instanceof Error ? error.message : "Session not found."}
                    </p>
                    <button className={styles.actionButton} style={{ marginTop: 16 }} onClick={() => router.push("/scam")}>
                        Back to Live Monitor
                    </button>
                </Card>
            </>
        );
    }

    if (isLoading || !session) {
        return (
            <>
                <PageHeader title="Session Detail" />
                <LoadingSkeleton height={400} />
            </>
        );
    }

    return (
        <>
            <PageHeader
                title={`Session ${session.id.slice(0, 8)}`}
                subtitle={`${session.caller_number} → ${session.callee_number}`}
                actions={
                    <button className={styles.actionButton} onClick={() => router.push("/scam")}>
                        Back to Live Monitor
                    </button>
                }
            />
            <SessionDetail
                session={session}
                onAcknowledge={handleAcknowledge}
                onReclassify={handleReclassify}
                pendingAction={pendingAction}
                actionError={actionError}
            />
        </>
    );
}
