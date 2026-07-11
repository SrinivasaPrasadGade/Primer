import { StyleSheet, Text, View } from "react-native";
import { colors, radius, spacing } from "../constants/colors";
import { Badge } from "./Badge";

type Tone = "red" | "amber" | "green" | "neutral";

const LEVEL_TONE: Record<string, Tone> = {
    high: "red",
    HIGH: "red",
    COUNTERFEIT: "red",
    medium: "amber",
    MEDIUM: "amber",
    SUSPECT: "amber",
    low: "green",
    LOW: "green",
    GENUINE: "green",
};

export function RiskCard({ title, level, subtitle, details }: { title: string; level: string; subtitle?: string; details?: string[] }) {
    const tone = LEVEL_TONE[level] ?? "neutral";
    return (
        <View style={styles.card}>
            <View style={styles.header}>
                <Text style={styles.title}>{title}</Text>
                <Badge label={level} tone={tone} />
            </View>
            {subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
            {details?.map((line, i) => (
                <Text key={i} style={styles.detail}>
                    • {line}
                </Text>
            ))}
        </View>
    );
}

const styles = StyleSheet.create({
    card: {
        backgroundColor: colors.layer1,
        borderRadius: radius.lg,
        borderWidth: 1,
        borderColor: colors.borderSubtle,
        padding: spacing.lg,
        gap: spacing.sm,
    },
    header: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
    },
    title: {
        color: colors.textPrimary,
        fontSize: 16,
        fontWeight: "700",
    },
    subtitle: {
        color: colors.textSecondary,
        fontSize: 13,
    },
    detail: {
        color: colors.textTertiary,
        fontSize: 12,
    },
});
