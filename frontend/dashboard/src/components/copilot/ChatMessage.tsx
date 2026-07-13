import { Sparkles, User } from "lucide-react";
import styles from "@/styles/copilot.module.css";

export interface ChatMessageData {
    role: "user" | "assistant";
    text: string;
    pending?: boolean;
}

// Lightweight rendering of the model's plain-text answer: preserve paragraph breaks and
// render leading "-"/"•" lines as a bulleted list so multi-part answers stay readable
// without pulling in a full markdown dependency.
function renderBody(text: string) {
    const blocks = text.split(/\n{2,}/);
    return blocks.map((block, i) => {
        const lines = block.split("\n");
        const isList = lines.length > 1 && lines.every((l) => /^\s*[-•*]\s+/.test(l));
        if (isList) {
            return (
                <ul key={i} className={styles.msgList}>
                    {lines.map((l, j) => (
                        <li key={j}>{l.replace(/^\s*[-•*]\s+/, "")}</li>
                    ))}
                </ul>
            );
        }
        return (
            <p key={i} className={styles.msgParagraph}>
                {block}
            </p>
        );
    });
}

export function ChatMessage({ message }: { message: ChatMessageData }) {
    const isUser = message.role === "user";
    return (
        <div className={`${styles.row} ${isUser ? styles.rowUser : styles.rowAssistant}`}>
            <div className={`${styles.avatar} ${isUser ? styles.avatarUser : styles.avatarAssistant}`}>
                {isUser ? <User size={15} /> : <Sparkles size={15} />}
            </div>
            <div className={styles.bubbleWrap}>
                <span className={styles.roleLabel}>{isUser ? "You" : "Copilot"}</span>
                <div
                    className={`${styles.bubble} ${isUser ? styles.bubbleUser : styles.bubbleAssistant} ${
                        message.pending ? styles.bubblePending : ""
                    }`}
                >
                    {message.pending ? (
                        <span className={styles.typing}>
                            <span /> <span /> <span />
                        </span>
                    ) : (
                        renderBody(message.text)
                    )}
                </div>
            </div>
        </div>
    );
}
