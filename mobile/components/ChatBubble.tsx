import { StyleSheet, Text, View } from "react-native";
import { colors, radius, spacing } from "../constants/colors";

export interface ChatMessage {
    role: "user" | "assistant";
    text: string;
}

export function ChatBubble({ message }: { message: ChatMessage }) {
    const isUser = message.role === "user";
    return (
        <View style={[styles.bubble, isUser ? styles.bubbleUser : styles.bubbleAssistant]}>
            <Text style={[styles.text, isUser && styles.textUser]}>{message.text}</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    bubble: {
        maxWidth: "78%",
        borderRadius: radius.lg,
        paddingHorizontal: spacing.lg,
        paddingVertical: spacing.md,
        marginBottom: spacing.sm,
    },
    bubbleAssistant: {
        alignSelf: "flex-start",
        backgroundColor: colors.layer2,
    },
    bubbleUser: {
        alignSelf: "flex-end",
        backgroundColor: colors.accent500,
    },
    text: {
        color: colors.textPrimary,
        fontSize: 14,
        lineHeight: 20,
    },
    textUser: {
        color: "#fff",
    },
});
