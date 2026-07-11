import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { ScrollView, StyleSheet, Text } from "react-native";
import { RiskCard } from "../components/RiskCard";
import { colors, spacing } from "../constants/colors";
import type { ScanStackParamList } from "../App";

type Props = NativeStackScreenProps<ScanStackParamList, "ScanResult">;

export function ScanResultScreen({ route }: Props) {
    const { result } = route.params;

    return (
        <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
            <RiskCard
                title={`₹${result.denomination} Note`}
                level={result.verdict}
                subtitle={`Confidence ${result.confidence.toFixed(1)}%`}
            />
            {result.is_known_counterfeit && <Text style={styles.warning}>This serial number is on the counterfeit registry.</Text>}

            <Text style={styles.sectionTitle}>Explainable AI Breakdown</Text>
            {Object.entries(result.feature_analysis).map(([name, score]) => (
                <Text key={name} style={styles.featureRow}>
                    {name.replace(/_/g, " ")}: {(score * 100).toFixed(0)}%
                </Text>
            ))}
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    screen: { flex: 1, backgroundColor: colors.bgPrimary },
    content: { padding: spacing.xl, gap: spacing.md },
    warning: { color: colors.red, fontSize: 13 },
    sectionTitle: {
        color: colors.textSecondary,
        fontSize: 12,
        textTransform: "uppercase",
        marginTop: spacing.lg,
        marginBottom: spacing.sm,
    },
    featureRow: {
        color: colors.textPrimary,
        fontSize: 13,
        textTransform: "capitalize",
        paddingVertical: spacing.xs,
    },
});
