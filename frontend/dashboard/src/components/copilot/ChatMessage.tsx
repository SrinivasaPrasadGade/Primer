"use client";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { ChevronDown, ChevronRight } from "lucide-react";
import styles from "@/styles/copilot.module.css";

export interface ToolCall {
    tool: string;
    args: Record<string, unknown>;
}

export interface ChatMessageData {
    role: "user" | "assistant";
    text: string;
    /** Tool names the backend hit for this answer. */
    sources?: string[];
    /** The actual tool invocations, shown on demand so an officer can audit the answer. */
    queryExecuted?: ToolCall[];
    /** False when the model backend was unreachable — a status message, not a finding. */
    failed?: boolean;
}

function ToolTrace({ sources, queryExecuted }: { sources: string[]; queryExecuted: ToolCall[] }) {
    const [open, setOpen] = useState(false);

    return (
        <div className={styles.trace}>
            <div className={styles.sourceRow}>
                {sources.map((s, i) => (
                    <span key={`${s}-${i}`} className={styles.sourceChip}>
                        {s.replace(/_/g, " ")}
                    </span>
                ))}
            </div>
            {queryExecuted.length > 0 && (
                <>
                    <button type="button" className={styles.traceToggle} onClick={() => setOpen((v) => !v)} aria-expanded={open}>
                        {open ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
                        {queryExecuted.length} quer{queryExecuted.length === 1 ? "y" : "ies"} run
                    </button>
                    {open && (
                        <ul className={styles.traceList}>
                            {queryExecuted.map((q, i) => (
                                <li key={i} className={styles.traceItem}>
                                    <code className={styles.traceTool}>{q.tool}</code>
                                    <pre className={styles.traceArgs}>{JSON.stringify(q.args, null, 2)}</pre>
                                </li>
                            ))}
                        </ul>
                    )}
                </>
            )}
        </div>
    );
}

export function ChatMessage({ message }: { message: ChatMessageData }) {
    const isUser = message.role === "user";
    const hasTrace = !isUser && ((message.sources?.length ?? 0) > 0 || (message.queryExecuted?.length ?? 0) > 0);

    return (
        <div
            className={[
                styles.message,
                isUser ? styles.messageUser : styles.messageAssistant,
                message.failed ? styles.messageFailed : "",
            ]
                .filter(Boolean)
                .join(" ")}
            role={message.failed ? "alert" : undefined}
        >
            {isUser ? (
                // User text is never markdown — preserve their line breaks verbatim.
                <p className={styles.userText}>{message.text}</p>
            ) : (
                <div className={styles.markdown}>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.text}</ReactMarkdown>
                </div>
            )}

            {hasTrace && <ToolTrace sources={message.sources ?? []} queryExecuted={message.queryExecuted ?? []} />}
        </div>
    );
}
