import { useRef, useState } from "react";
import { FlatList, KeyboardAvoidingView, Platform, Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import { Send } from "lucide-react-native";
import { ChatBubble, ChatMessage } from "../components/ChatBubble";
import { colors, radius, spacing } from "../constants/colors";
import { api } from "../hooks/useApi";

export function ChatScreen() {
    const [messages, setMessages] = useState<ChatMessage[]>([
        { role: "assistant", text: "Hi, I'm Citizen Shield. Ask me about a scam call, a suspicious message, or how to report fraud." },
    ]);
    const [input, setInput] = useState("");
    const [sending, setSending] = useState(false);
    const sessionId = useRef<string | null>(null);
    const listRef = useRef<FlatList>(null);

    async function handleSend() {
        const text = input.trim();
        if (!text || sending) return;
        setInput("");
        setMessages((prev) => [...prev, { role: "user", text }]);
        setSending(true);
        try {
            const res = await api.citizenChat(text, sessionId.current);
            sessionId.current = res.session_id ?? res.id ?? sessionId.current;
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
