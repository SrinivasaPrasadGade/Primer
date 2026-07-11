import styles from "@/styles/copilot.module.css";

export interface ChatMessageData {
    role: "user" | "assistant";
    text: string;
}

export function ChatMessage({ message }: { message: ChatMessageData }) {
    return (
        <div className={`${styles.message} ${message.role === "user" ? styles.messageUser : styles.messageAssistant}`}>
            {message.text}
        </div>
    );
}
