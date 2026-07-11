import { useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import { RiskCard } from "../components/RiskCard";
import { colors, radius, spacing } from "../constants/colors";
import { api, NumberCheckResult } from "../hooks/useApi";

export function NumberCheckScreen() {
    const [phone, setPhone] = useState("");
    const [result, setResult] = useState<NumberCheckResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function handleCheck() {
        if (!phone.trim()) return;
        setLoading(true);
        setError(null);
        try {
            const res = await api.numberCheck(phone.trim());
            setResult(res);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Lookup failed");
        } finally {
            setLoading(false);
        }
    }

    return (
        <View style={styles.screen}>
            <Text style={styles.title}>Check a Phone Number</Text>
            <Text style={styles.subtitle}>See if a number has been reported for scam activity.</Text>

            <TextInput
                style={styles.input}
                placeholder="e.g. 9198XXXXXXXX"
                placeholderTextColor={colors.textTertiary}
                keyboardType="phone-pad"
                value={phone}
                onChangeText={setPhone}
            />
            <Pressable style={styles.button} onPress={handleCheck} disabled={loading}>
                {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Check Number</Text>}
            </Pressable>

            {error && <Text style={styles.error}>{error}</Text>}

            {result && (
                <View style={{ marginTop: spacing.xl }}>
                    <RiskCard
                        title={result.phone}
                        level={result.is_blacklisted ? "high" : result.risk_score > 40 ? "medium" : "low"}
                        subtitle={result.message ?? `Risk score: ${result.risk_score}`}
                    />
                </View>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    screen: { flex: 1, backgroundColor: colors.bgPrimary, padding: spacing.xl },
    title: { color: colors.textPrimary, fontSize: 20, fontWeight: "700", marginBottom: spacing.xs },
    subtitle: { color: colors.textSecondary, fontSize: 13, marginBottom: spacing.xl },
    input: {
        backgroundColor: colors.layer2,
        borderWidth: 1,
        borderColor: colors.borderDefault,
        borderRadius: radius.md,
        padding: spacing.md,
        color: colors.textPrimary,
        fontSize: 14,
        marginBottom: spacing.md,
    },
    button: {
        backgroundColor: colors.accent500,
        borderRadius: radius.md,
        paddingVertical: spacing.md,
        alignItems: "center",
    },
    buttonText: { color: "#fff", fontWeight: "700", fontSize: 14 },
    error: { color: colors.red, fontSize: 12, marginTop: spacing.md },
});
