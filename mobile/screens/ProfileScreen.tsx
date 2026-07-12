import { ActivityIndicator, ScrollView, StyleSheet, Text, View } from "react-native";
import { AlertTriangle, Phone, QrCode, ScanLine, ShieldCheck } from "lucide-react-native";
import { api, AuthUser, useApi } from "../hooks/useApi";
import { DEMO_CITIZEN_EMAIL } from "../constants/api";
import { colors, radius, spacing } from "../constants/colors";

const APP_VERSION = "1.0.0";

const PROTECTIONS = [
    { icon: Phone, label: "Scam & deepfake call detection" },
    { icon: ScanLine, label: "Counterfeit currency scanning" },
    { icon: QrCode, label: "QR / UPI fraud checks" },
    { icon: ShieldCheck, label: "Phone number reputation" },
    { icon: AlertTriangle, label: "Panic SOS" },
];

export function ProfileScreen() {
    const { data: user, loading, error } = useApi<AuthUser>(() => api.me());

    const name = user?.name ?? "Citizen";
    const email = user?.email ?? DEMO_CITIZEN_EMAIL;
    const role = user?.role ?? "citizen";
    const initial = name.charAt(0).toUpperCase();

    return (
        <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
            <View style={styles.identityCard}>
                <View style={styles.avatar}>
                    {loading ? <ActivityIndicator color={colors.accent500} /> : <Text style={styles.avatarText}>{initial}</Text>}
                </View>
                <View style={{ flex: 1 }}>
                    <Text style={styles.name}>{name}</Text>
                    <Text style={styles.email}>{email}</Text>
                    <View style={styles.roleBadge}>
                        <Text style={styles.roleText}>{role}</Text>
                    </View>
                </View>
            </View>

            {error && <Text style={styles.error}>Showing demo identity — {error}</Text>}

            <Text style={styles.sectionTitle}>What Primer protects you from</Text>
            <View style={styles.card}>
                {PROTECTIONS.map(({ icon: Icon, label }, i) => (
                    <View key={label} style={[styles.row, i < PROTECTIONS.length - 1 && styles.rowDivider]}>
                        <Icon size={18} color={colors.accent500} />
                        <Text style={styles.rowLabel}>{label}</Text>
                    </View>
                ))}
            </View>

            <Text style={styles.sectionTitle}>About</Text>
            <View style={styles.card}>
                <Text style={styles.aboutTitle}>Primer Citizen Shield</Text>
                <Text style={styles.aboutText}>AI-powered digital public safety in your pocket.</Text>
                <Text style={styles.aboutMeta}>Version {APP_VERSION}</Text>
            </View>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    screen: { flex: 1, backgroundColor: colors.bgPrimary },
    content: { padding: spacing.xl, gap: spacing.md },
    identityCard: {
        flexDirection: "row",
        alignItems: "center",
        gap: spacing.lg,
        backgroundColor: colors.layer1,
        borderRadius: radius.lg,
        borderWidth: 1,
        borderColor: colors.borderSubtle,
        padding: spacing.lg,
    },
    avatar: {
        width: 56,
        height: 56,
        borderRadius: radius.full,
        backgroundColor: colors.layer3,
        alignItems: "center",
        justifyContent: "center",
    },
    avatarText: { color: colors.accent500, fontSize: 22, fontWeight: "700" },
    name: { color: colors.textPrimary, fontSize: 18, fontWeight: "700" },
    email: { color: colors.textSecondary, fontSize: 13, marginTop: 2 },
    roleBadge: {
        alignSelf: "flex-start",
        marginTop: spacing.sm,
        backgroundColor: colors.layer3,
        borderRadius: radius.full,
        paddingHorizontal: spacing.md,
        paddingVertical: 2,
    },
    roleText: { color: colors.textSecondary, fontSize: 11, fontWeight: "700", textTransform: "uppercase" },
    error: { color: colors.amber, fontSize: 12 },
    sectionTitle: {
        color: colors.textSecondary,
        fontSize: 12,
        fontWeight: "600",
        textTransform: "uppercase",
        letterSpacing: 0.5,
        marginTop: spacing.md,
    },
    card: {
        backgroundColor: colors.layer1,
        borderRadius: radius.lg,
        borderWidth: 1,
        borderColor: colors.borderSubtle,
        paddingHorizontal: spacing.lg,
    },
    row: { flexDirection: "row", alignItems: "center", gap: spacing.md, paddingVertical: spacing.md },
    rowDivider: { borderBottomWidth: 1, borderBottomColor: colors.borderSubtle },
    rowLabel: { color: colors.textPrimary, fontSize: 14 },
    aboutTitle: { color: colors.textPrimary, fontSize: 15, fontWeight: "600", paddingTop: spacing.lg },
    aboutText: { color: colors.textSecondary, fontSize: 13, marginTop: spacing.xs },
    aboutMeta: { color: colors.textTertiary, fontSize: 12, marginTop: spacing.sm, paddingBottom: spacing.lg },
});
