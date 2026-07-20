import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from "react-native";
import { AlertTriangle, X } from "lucide-react-native";
import * as Location from "expo-location";
import { colors, radius, spacing } from "../constants/colors";
import { api, PanicResult } from "../hooks/useApi";
import type { RootStackParamList } from "../App";

type Props = NativeStackScreenProps<RootStackParamList, "Panic">;

/** Never let a slow GPS fix hold up the SOS itself. */
const LOCATION_TIMEOUT_MS = 5000;

/**
 * Best-effort coordinates. Returns undefined if permission is denied, the device
 * can't get a fix, or it takes too long — the alert still goes out either way,
 * because an SOS without a location beats an SOS that never sends.
 */
async function getLocation(): Promise<{ lat: number; lng: number } | undefined> {
    try {
        const { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== "granted") return undefined;

        const position = await Promise.race([
            Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Balanced }),
            new Promise<null>((resolve) => setTimeout(() => resolve(null), LOCATION_TIMEOUT_MS)),
        ]);
        if (!position) return undefined;

        return { lat: position.coords.latitude, lng: position.coords.longitude };
    } catch {
        return undefined;
    }
}

export function PanicScreen({ navigation }: Props) {
    const [triggering, setTriggering] = useState(false);
    const [result, setResult] = useState<PanicResult | null>(null);
    const [locationSent, setLocationSent] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function handleTrigger() {
        setTriggering(true);
        setError(null);
        try {
            const location = await getLocation();
            setLocationSent(location !== undefined);
            const res = await api.triggerPanic({ location });
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
                    <Text style={styles.confirmText}>Your alert has been logged and sent to law enforcement.</Text>
                    <Text style={styles.confirmText}>
                        {locationSent ? "Your location was included." : "Your location could not be shared."}
                    </Text>
                    {result.emergency_contact_on_file && !result.emergency_contact_notified && (
                        <Text style={styles.confirmText}>
                            Your emergency contact is on file. Call them directly — we cannot contact them for you.
                        </Text>
                    )}
                    {result.emergency_contact_notified && <Text style={styles.confirmText}>Your emergency contact has been notified.</Text>}
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
