import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { useEffect, useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from "react-native";
import { LucideIcon, Phone, PhoneOff, ShieldAlert, ShieldCheck, ShieldX } from "lucide-react-native";
import { colors, radius, spacing } from "../constants/colors";
import { api, ScreenNumberResult } from "../hooks/useApi";
import type { RootStackParamList } from "../App";

type Props = NativeStackScreenProps<RootStackParamList, "IncomingCall">;

interface Verdict {
    icon: LucideIcon;
    tone: string;
    toneBg: string;
    title: string;
    body: string;
}

const VERDICTS: Record<string, Verdict> = {
    block: {
        icon: ShieldX,
        tone: colors.red,
        toneBg: colors.redBg,
        title: "Likely Scam",
        body: "This number has been reported for fraud. Primer recommends declining.",
    },
    caution: {
        icon: ShieldAlert,
        tone: colors.amber,
        toneBg: colors.amberBg,
        title: "Proceed with Caution",
        body: "This number has some risk signals. Never share OTPs, PINs, or bank details.",
    },
    allow: {
        icon: ShieldCheck,
        tone: colors.green,
        toneBg: colors.greenBg,
        title: "No Known Risk",
        body: "Primer has no scam reports for this number.",
    },
};

export function IncomingCallScreen({ route, navigation }: Props) {
    const { phone } = route.params;
    const [screening, setScreening] = useState<ScreenNumberResult | null>(null);
    const [failed, setFailed] = useState(false);

    useEffect(() => {
        let cancelled = false;
        api.screenNumber(phone)
            .then((res) => {
                if (!cancelled) setScreening(res);
            })
            .catch(() => {
                // A screening failure must never look like a clean number — the UI
                // falls back to "couldn't screen", not to "allow".
                if (!cancelled) setFailed(true);
            });
        return () => {
            cancelled = true;
        };
    }, [phone]);

    const verdict = screening ? VERDICTS[screening.recommendation] ?? VERDICTS.caution : null;
    const Icon = verdict?.icon;

    return (
        <View style={styles.screen}>
            <View style={styles.callerBlock}>
                <Text style={styles.incomingLabel}>Incoming call</Text>
                <Text style={styles.phone}>{phone}</Text>
                <Text style={styles.unknown}>Unknown caller</Text>
            </View>

            <View style={styles.screeningBlock}>
                {!screening && !failed && (
                    <View style={styles.screeningPending}>
                        <ActivityIndicator color={colors.accent500} />
                        <Text style={styles.pendingText}>Screening this call…</Text>
                    </View>
                )}

                {failed && (
                    <View style={[styles.verdictCard, { backgroundColor: colors.layer2, borderColor: colors.borderDefault }]}>
                        <ShieldAlert size={28} color={colors.textSecondary} />
                        <Text style={[styles.verdictTitle, { color: colors.textPrimary }]}>Couldn&apos;t Screen This Call</Text>
                        <Text style={styles.verdictBody}>Primer could not reach the screening service. Treat this call as unverified.</Text>
                    </View>
                )}

                {screening && verdict && Icon && (
                    <View style={[styles.verdictCard, { backgroundColor: verdict.toneBg, borderColor: verdict.tone }]}>
                        <Icon size={28} color={verdict.tone} />
                        <Text style={[styles.verdictTitle, { color: verdict.tone }]}>{verdict.title}</Text>
                        <Text style={styles.verdictBody}>{verdict.body}</Text>
                        <Text style={styles.riskScore}>Risk score: {screening.risk_score}/100</Text>
                        {screening.flags.length > 0 && (
                            <View style={styles.flagRow}>
                                {screening.flags.map((flag) => (
                                    <View key={flag} style={[styles.flag, { borderColor: verdict.tone }]}>
                                        <Text style={[styles.flagText, { color: verdict.tone }]}>{flag.replace(/_/g, " ")}</Text>
                                    </View>
                                ))}
                            </View>
                        )}
                    </View>
                )}
            </View>

            <View style={styles.actions}>
                <Pressable style={[styles.actionButton, styles.decline]} onPress={() => navigation.goBack()}>
                    <PhoneOff size={26} color="#fff" />
                    <Text style={styles.actionLabel}>Decline</Text>
                </Pressable>
                <Pressable
                    style={[styles.actionButton, screening?.recommendation === "block" ? styles.answerMuted : styles.answer]}
                    onPress={() => navigation.goBack()}
                >
                    <Phone size={26} color="#fff" />
                    <Text style={styles.actionLabel}>Answer</Text>
                </Pressable>
            </View>

            {screening?.recommendation === "block" && (
                <Text style={styles.blockHint}>Answering is not recommended for this number.</Text>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    screen: { flex: 1, backgroundColor: colors.bgPrimary, padding: spacing.xl, justifyContent: "space-between" },
    callerBlock: { alignItems: "center", marginTop: spacing.xxl * 2, gap: spacing.xs },
    incomingLabel: { color: colors.textTertiary, fontSize: 13, letterSpacing: 1, textTransform: "uppercase" },
    phone: { color: colors.textPrimary, fontSize: 30, fontWeight: "700" },
    unknown: { color: colors.textSecondary, fontSize: 14 },
    screeningBlock: { justifyContent: "center" },
    screeningPending: { flexDirection: "row", alignItems: "center", justifyContent: "center", gap: spacing.sm },
    pendingText: { color: colors.textSecondary, fontSize: 14 },
    verdictCard: { borderWidth: 1, borderRadius: radius.xl, padding: spacing.lg, alignItems: "center", gap: spacing.sm },
    verdictTitle: { fontSize: 18, fontWeight: "700" },
    verdictBody: { color: colors.textSecondary, fontSize: 13, textAlign: "center" },
    riskScore: { color: colors.textTertiary, fontSize: 12 },
    flagRow: { flexDirection: "row", flexWrap: "wrap", gap: spacing.sm, justifyContent: "center" },
    flag: { borderWidth: 1, borderRadius: radius.full, paddingHorizontal: spacing.md, paddingVertical: spacing.xs },
    flagText: { fontSize: 11, fontWeight: "600", textTransform: "capitalize" },
    actions: { flexDirection: "row", justifyContent: "space-around", marginBottom: spacing.xl },
    actionButton: { alignItems: "center", justifyContent: "center", gap: spacing.sm, width: 96, height: 96, borderRadius: radius.full },
    decline: { backgroundColor: colors.red },
    answer: { backgroundColor: colors.green },
    // Answering a flagged number stays possible — the citizen decides — but it
    // shouldn't look like the encouraged path.
    answerMuted: { backgroundColor: colors.layer4 },
    actionLabel: { color: "#fff", fontSize: 12, fontWeight: "700" },
    blockHint: { color: colors.red, fontSize: 12, textAlign: "center", marginTop: -spacing.md, marginBottom: spacing.md },
});
