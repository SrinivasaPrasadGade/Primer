import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { useEffect, useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from "react-native";
import { Phone, PhoneOff, ShieldAlert } from "lucide-react-native";
import { api, ScreenNumberResult } from "../hooks/useApi";
import { colors, radius, spacing } from "../constants/colors";
import type { RootStackParamList } from "../App";

type Props = NativeStackScreenProps<RootStackParamList, "CallScreening">;

const RISK_TONE: Record<string, { color: string; label: string }> = {
    high: { color: colors.red, label: "High risk — likely scam" },
    medium: { color: colors.amber, label: "Caution — possible scam" },
    low: { color: colors.green, label: "Looks safe" },
};

export function CallScreeningScreen({ route, navigation }: Props) {
    const callerNumber = route.params?.callerNumber ?? "+91 98765 43210";
    const [result, setResult] = useState<ScreenNumberResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let active = true;
        setResult(null);
        setError(null);
        api
            .screenNumber(callerNumber)
            .then((r) => active && setResult(r))
            .catch((e) => active && setError(e instanceof Error ? e.message : "Could not screen this number"));
        return () => {
            active = false;
        };
    }, [callerNumber]);

    const tone = result ? RISK_TONE[result.risk_level] ?? RISK_TONE.low : null;

    return (
        <View style={styles.overlay}>
            <View style={styles.callHeader}>
                <Text style={styles.incoming}>Incoming call</Text>
                <Text style={styles.number}>{callerNumber}</Text>
            </View>

            <View style={styles.riskArea}>
                {!result && !error && (
                    <>
                        <ActivityIndicator size="large" color={colors.accent500} />
                        <Text style={styles.checking}>Primer is checking this number…</Text>
                    </>
                )}

                {error && <Text style={styles.error}>{error}</Text>}

                {result && tone && (
                    <>
                        <View style={styles.riskBarTrack}>
                            <View
                                style={[
                                    styles.riskBarFill,
                                    { width: `${Math.min(100, Math.max(8, result.risk_score))}%`, backgroundColor: tone.color },
                                ]}
                            />
                        </View>
                        <View style={styles.riskLabelRow}>
                            <ShieldAlert size={18} color={tone.color} />
                            <Text style={[styles.riskLabel, { color: tone.color }]}>{tone.label}</Text>
                        </View>
                        {result.flags.length > 0 && (
                            <View style={styles.flags}>
                                {result.flags.map((f) => (
                                    <Text key={f} style={styles.flag}>
                                        • {f.replace(/_/g, " ")}
                                    </Text>
                                ))}
                            </View>
                        )}
                        <Text style={styles.recommendation}>Recommended action: {result.recommendation}</Text>
                    </>
                )}
            </View>

            <View style={styles.actions}>
                <Pressable style={[styles.button, styles.reject]} onPress={() => navigation.goBack()} accessibilityLabel="Reject call">
                    <PhoneOff size={24} color="#fff" />
                    <Text style={styles.rejectText}>Reject</Text>
                </Pressable>
                <Pressable style={[styles.button, styles.answer]} onPress={() => navigation.goBack()} accessibilityLabel="Answer anyway">
                    <Phone size={16} color={colors.textSecondary} />
                    <Text style={styles.answerText}>Answer anyway</Text>
                </Pressable>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    overlay: {
        flex: 1,
        backgroundColor: "rgba(10,10,15,0.94)",
        paddingHorizontal: spacing.xl,
        paddingVertical: spacing.xxl,
        justifyContent: "space-between",
    },
    callHeader: { alignItems: "center", marginTop: spacing.xxl, gap: spacing.sm },
    incoming: { color: colors.textSecondary, fontSize: 14, letterSpacing: 0.5, textTransform: "uppercase" },
    number: { color: colors.textPrimary, fontSize: 28, fontWeight: "700" },
    riskArea: { alignItems: "center", gap: spacing.md, paddingHorizontal: spacing.md },
    checking: { color: colors.textSecondary, fontSize: 14 },
    error: { color: colors.red, fontSize: 14, textAlign: "center" },
    riskBarTrack: {
        width: "100%",
        height: 12,
        borderRadius: radius.full,
        backgroundColor: colors.layer3,
        overflow: "hidden",
    },
    riskBarFill: { height: "100%", borderRadius: radius.full },
    riskLabelRow: { flexDirection: "row", alignItems: "center", gap: spacing.sm, marginTop: spacing.sm },
    riskLabel: { fontSize: 16, fontWeight: "700" },
    flags: { alignItems: "center", gap: 2, marginTop: spacing.sm },
    flag: { color: colors.textSecondary, fontSize: 13, textTransform: "capitalize" },
    recommendation: { color: colors.textTertiary, fontSize: 13, marginTop: spacing.sm },
    actions: { flexDirection: "row", alignItems: "center", justifyContent: "center", gap: spacing.lg, marginBottom: spacing.xl },
    button: { alignItems: "center", justifyContent: "center", gap: spacing.xs },
    reject: {
        backgroundColor: colors.red,
        width: 120,
        height: 120,
        borderRadius: radius.full,
        shadowColor: colors.red,
        shadowOpacity: 0.4,
        shadowRadius: 20,
        shadowOffset: { width: 0, height: 0 },
    },
    rejectText: { color: "#fff", fontSize: 14, fontWeight: "700" },
    answer: {
        flexDirection: "row",
        backgroundColor: colors.layer2,
        borderWidth: 1,
        borderColor: colors.borderDefault,
        borderRadius: radius.full,
        paddingHorizontal: spacing.lg,
        paddingVertical: spacing.md,
    },
    answerText: { color: colors.textSecondary, fontSize: 13, fontWeight: "600" },
});
