import { useEffect, useRef, useState } from "react";
import { FlatList, KeyboardAvoidingView, Platform, Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Send } from "lucide-react-native";
import { ChatBubble, ChatMessage } from "../components/ChatBubble";
import { CHAT_SESSION_STORAGE_KEY } from "../constants/api";
import { colors, radius, spacing } from "../constants/colors";
import { api } from "../hooks/useApi";

const GREETING: ChatMessage = {
    role: "assistant",
    text: "Hi, I'm Citizen Shield. Ask me about a scam call, a suspicious message, or how to report fraud.",
};

export function ChatScreen() {
    const [messages, setMessages] = useState<ChatMessage[]>([GREETING]);
    const [input, setInput] = useState("");
    const [sending, setSending] = useState(false);
    const [ending, setEnding] = useState(false);
    const sessionId = useRef<string | null>(null);
    const listRef = useRef<FlatList>(null);

    // Restore an interrupted conversation on reopen. A failure here is silent —
    // the citizen still gets a working chat, just starting fresh.
    useEffect(() => {
        let cancelled = false;
        (async () => {
            const stored = await AsyncStorage.getItem(CHAT_SESSION_STORAGE_KEY);
            if (!stored || cancelled) return;
            try {
                const history = await api.getCitizenChatHistory(stored);
                if (cancelled || history.length === 0) return;
                sessionId.current = stored;
                setMessages([GREETING, ...history.map((m) => ({ role: m.role, text: m.content }))]);
            } catch {
                await AsyncStorage.removeItem(CHAT_SESSION_STORAGE_KEY);
            }
        })();
        return () => {
            cancelled = true;
        };
    }, []);

    async function persistSession(id: string | null) {
        sessionId.current = id;
        if (id) await AsyncStorage.setItem(CHAT_SESSION_STORAGE_KEY, id);
        else await AsyncStorage.removeItem(CHAT_SESSION_STORAGE_KEY);
    }

    async function handleEndChat() {
        const current = sessionId.current;
        setEnding(true);
        try {
            if (current) await api.closeCitizenChat(current);
        } catch {
            // Closing is best-effort; the local reset below is what the citizen sees.
        } finally {
            await persistSession(null);
            setMessages([GREETING]);
            setEnding(false);
        }
    }

    async function handleSend() {
        const text = input.trim();
        if (!text || sending) return;
        setInput("");
        setMessages((prev) => [...prev, { role: "user", text }]);
        setSending(true);
        try {
            const res = await api.citizenChat(text, sessionId.current);
            await persistSession(res.session_id ?? res.id ?? sessionId.current);
            setMessages((prev) => [...prev, { role: "assistant", text: res.reply }]);
        } catch (err) {
            setMessages((prev) => [...prev, { role: "assistant", text: err instanceof Error ? err.message : "Something went wrong." }]);
        } finally {
            setSending(false);
            requestAnimationFrame(() => listRef.current?.scrollToEnd({ animated: true }));
        }
    }

    return (
        <KeyboardAvoidingView style={styles.screen} behavior={Platform.OS === "ios" ? "padding" : undefined}>
            {messages.length > 1 && (
                <View style={styles.sessionBar}>
                    <Pressable onPress={handleEndChat} disabled={ending}>
                        <Text style={styles.endChatText}>{ending ? "Ending…" : "End chat"}</Text>
                    </Pressable>
                </View>
            )}
            <FlatList
                ref={listRef}
                data={messages}
                keyExtractor={(_, i) => String(i)}
                renderItem={({ item }) => <ChatBubble message={item} />}
                contentContainerStyle={styles.list}
                onContentSizeChange={() => listRef.current?.scrollToEnd({ animated: true })}
            />
            <View style={styles.inputBar}>
                <TextInput
                    style={styles.input}
                    placeholder="Type a message…"
                    placeholderTextColor={colors.textTertiary}
                    value={input}
                    onChangeText={setInput}
                    onSubmitEditing={handleSend}
                />
                <Pressable style={styles.sendButton} onPress={handleSend} disabled={sending}>
                    <Send size={16} color="#fff" />
                </Pressable>
            </View>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    screen: { flex: 1, backgroundColor: colors.bgPrimary },
    sessionBar: {
        flexDirection: "row",
        justifyContent: "flex-end",
        paddingHorizontal: spacing.lg,
        paddingTop: spacing.sm,
    },
    endChatText: { color: colors.textSecondary, fontSize: 12, fontWeight: "600" },
    list: { padding: spacing.lg },
    inputBar: {
        flexDirection: "row",
        gap: spacing.sm,
        padding: spacing.lg,
        borderTopWidth: 1,
        borderTopColor: colors.borderSubtle,
    },
    input: {
        flex: 1,
        backgroundColor: colors.layer2,
        borderWidth: 1,
        borderColor: colors.borderDefault,
        borderRadius: radius.md,
        paddingHorizontal: spacing.md,
        color: colors.textPrimary,
        fontSize: 14,
    },
    sendButton: {
        backgroundColor: colors.accent500,
        borderRadius: radius.md,
        alignItems: "center",
        justifyContent: "center",
        paddingHorizontal: spacing.md,
    },
});
