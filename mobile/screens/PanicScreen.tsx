import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from "react-native";
import { AlertTriangle, X } from "lucide-react-native";
import { colors, radius, spacing } from "../constants/colors";
import { api, PanicResult } from "../hooks/useApi";
import type { RootStackParamList } from "../App";

type Props = NativeStackScreenProps<RootStackParamList, "Panic">;

export function PanicScreen({ navigation }: Props) {
    const [triggering, setTriggering] = useState(false);
    const [result, setResult] = useState<PanicResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    async function handleTrigger() {
        setTriggering(true);
        setError(null);
        try {
            const res = await api.triggerPanic({});
            setResult(res);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Could not send SOS. Try again.");
        } finally {
            setTriggering(false);
        }
    }

    return (
        <View style={styles.screen}>
            <Pressable style={styles.closeButton} onPress={() => navigation.goBack()}>
                <X size={22} color={colors.textSecondary} />
            </Pressable>

            {result ? (
                <View style={styles.center}>
                    <AlertTriangle size={48} color={colors.green} />
                    <Text style={styles.confirmTitle}>SOS Sent</Text>
                    <Text style={styles.confirmText}>
                        {result.emergency_contact_notified ? "Your emergency contact has been notified." : "Your alert has been logged."}
                    </Text>
                    {result.fraud_report_generated && <Text style={styles.confirmText}>A fraud report has been generated.</Text>}
                </View>
            ) : (
                <View style={styles.center}>
                    <Text style={styles.title}>Panic Button</Text>
                    <Text style={styles.subtitle}>Press and hold if you're in danger or being scammed right now.</Text>
                    <Pressable style={styles.sosButton} onPress={handleTrigger} disabled={triggering}>
                        {triggering ? <ActivityIndicator color="#fff" size="large" /> : <Text style={styles.sosText}>SOS</Text>}
                    </Pressable>
                    {error && <Text style={styles.error}>{error}</Text>}
                </View>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    screen: { flex: 1, backgroundColor: colors.bgPrimary },
    closeButton: { position: "absolute", top: spacing.xxl, right: spacing.xl, zIndex: 1 },
    center: { flex: 1, alignItems: "center", justifyContent: "center", padding: spacing.xl, gap: spacing.md },
    title: { color: colors.textPrimary, fontSize: 22, fontWeight: "700" },
    subtitle: { color: colors.textSecondary, fontSize: 13, textAlign: "center", marginBottom: spacing.xl },
    sosButton: {
        width: 160,
        height: 160,
        borderRadius: radius.full,
        backgroundColor: colors.red,
        alignItems: "center",
        justifyContent: "center",
        shadowColor: colors.red,
        shadowOpacity: 0.5,
        shadowRadius: 24,
        shadowOffset: { width: 0, height: 0 },
    },
    sosText: { color: "#fff", fontSize: 28, fontWeight: "800", letterSpacing: 1 },
    confirmTitle: { color: colors.textPrimary, fontSize: 20, fontWeight: "700" },
    confirmText: { color: colors.textSecondary, fontSize: 14, textAlign: "center" },
    error: { color: colors.red, fontSize: 12, marginTop: spacing.md },
});
