import { StyleSheet, Text, View } from "react-native";
import { colors, radius, spacing } from "../constants/colors";

type Tone = "red" | "amber" | "green" | "neutral";

const TONE_COLORS: Record<Tone, { fg: string; bg: string }> = {
    red: { fg: colors.red, bg: colors.redBg },
    amber: { fg: colors.amber, bg: colors.amberBg },
    green: { fg: colors.green, bg: colors.greenBg },
    neutral: { fg: colors.textSecondary, bg: colors.layer3 },
};

export function Badge({ label, tone = "neutral" }: { label: string; tone?: Tone }) {
    const { fg, bg } = TONE_COLORS[tone];
    return (
        <View style={[styles.badge, { backgroundColor: bg }]}>
            <Text style={[styles.text, { color: fg }]}>{label}</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    badge: {
        paddingHorizontal: spacing.md,
        paddingVertical: spacing.xs,
        borderRadius: radius.full,
        alignSelf: "flex-start",
    },
    text: {
        fontSize: 11,
        fontWeight: "700",
        textTransform: "uppercase",
        letterSpacing: 0.4,
    },
});
