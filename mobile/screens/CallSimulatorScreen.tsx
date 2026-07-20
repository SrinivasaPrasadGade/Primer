import { useNavigation } from "@react-navigation/native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import { PhoneIncoming } from "lucide-react-native";
import { colors, radius, spacing } from "../constants/colors";
import type { HomeStackParamList, RootStackParamList } from "../App";

type CallSimulatorNavigation = NativeStackNavigationProp<HomeStackParamList, "CallSimulator"> &
    NativeStackNavigationProp<RootStackParamList>;

/**
 * Numbers straight from the seed data, chosen so each preset lands on a different
 * screening verdict. Keep them in sync with scam_sentinel.number_reputation.
 */
const PRESETS = [
    { phone: "+917861999412", label: "Blacklisted — tax evasion", hint: "Expect: Block" },
    { phone: "+918963153449", label: "Some risk signals", hint: "Expect: Caution" },
    { phone: "+919000000001", label: "No reports on file", hint: "Expect: Allow" },
];

export function CallSimulatorScreen() {
    const navigation = useNavigation<CallSimulatorNavigation>();
    const [phone, setPhone] = useState("");

    const trimmed = phone.trim();

    return (
        <View style={styles.screen}>
            <Text style={styles.title}>Simulate an Incoming Call</Text>
            <Text style={styles.subtitle}>
                Primer screens a caller before you answer. Pick a number below to see the pre-answer overlay.
            </Text>

            <TextInput
                style={styles.input}
                placeholder="e.g. +917861999412"
                placeholderTextColor={colors.textTertiary}
                keyboardType="phone-pad"
                autoCapitalize="none"
                value={phone}
                onChangeText={setPhone}
            />
            <Pressable
                style={[styles.button, !trimmed && styles.buttonDisabled]}
                disabled={!trimmed}
                onPress={() => navigation.navigate("IncomingCall", { phone: trimmed })}
            >
                <PhoneIncoming size={16} color="#fff" />
                <Text style={styles.buttonText}>Simulate Call</Text>
            </Pressable>

            <Text style={styles.presetHeading}>Demo numbers</Text>
            {PRESETS.map((preset) => (
                <Pressable
                    key={preset.phone}
                    style={({ pressed }) => [styles.preset, pressed && styles.presetPressed]}
                    onPress={() => navigation.navigate("IncomingCall", { phone: preset.phone })}
                >
                    <View style={styles.presetText}>
                        <Text style={styles.presetPhone}>{preset.phone}</Text>
                        <Text style={styles.presetLabel}>{preset.label}</Text>
                    </View>
                    <Text style={styles.presetHint}>{preset.hint}</Text>
                </Pressable>
            ))}
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
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "center",
        gap: spacing.sm,
    },
    buttonDisabled: { opacity: 0.4 },
    buttonText: { color: "#fff", fontWeight: "700", fontSize: 14 },
    presetHeading: {
        color: colors.textTertiary,
        fontSize: 12,
        fontWeight: "600",
        textTransform: "uppercase",
        letterSpacing: 1,
        marginTop: spacing.xxl,
        marginBottom: spacing.md,
    },
    preset: {
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
        backgroundColor: colors.layer1,
        borderWidth: 1,
        borderColor: colors.borderSubtle,
        borderRadius: radius.lg,
        padding: spacing.lg,
        marginBottom: spacing.md,
    },
    presetPressed: { backgroundColor: colors.layer2 },
    presetText: { gap: 2, flexShrink: 1 },
    presetPhone: { color: colors.textPrimary, fontSize: 14, fontWeight: "600" },
    presetLabel: { color: colors.textSecondary, fontSize: 12 },
    presetHint: { color: colors.textTertiary, fontSize: 11, marginLeft: spacing.md },
});
