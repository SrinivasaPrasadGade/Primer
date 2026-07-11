import { LucideIcon } from "lucide-react-native";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { colors, radius, spacing } from "../constants/colors";

export interface FeatureItem {
    key: string;
    label: string;
    icon: LucideIcon;
    tone?: "red" | "default";
    onPress: () => void;
}

export function FeatureGrid({ items }: { items: FeatureItem[] }) {
    return (
        <View style={styles.grid}>
            {items.map(({ key, label, icon: Icon, tone = "default", onPress }) => (
                <Pressable
                    key={key}
                    style={({ pressed }) => [styles.tile, tone === "red" && styles.tileRed, pressed && styles.tilePressed]}
                    onPress={onPress}
                >
                    <Icon size={24} color={tone === "red" ? colors.red : colors.accent500} />
                    <Text style={styles.label}>{label}</Text>
                </Pressable>
            ))}
        </View>
    );
}

const styles = StyleSheet.create({
    grid: {
        flexDirection: "row",
        flexWrap: "wrap",
        gap: spacing.md,
    },
    tile: {
        width: "47%",
        backgroundColor: colors.layer1,
        borderRadius: radius.lg,
        borderWidth: 1,
        borderColor: colors.borderSubtle,
        padding: spacing.lg,
        gap: spacing.sm,
    },
    tileRed: {
        borderColor: "rgba(239,68,68,0.3)",
    },
    tilePressed: {
        backgroundColor: colors.layer2,
    },
    label: {
        color: colors.textPrimary,
        fontSize: 13,
        fontWeight: "600",
    },
});
