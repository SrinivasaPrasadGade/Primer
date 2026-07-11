import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { ScrollView, StyleSheet, Text } from "react-native";
import { RiskCard } from "../components/RiskCard";
import { colors, spacing } from "../constants/colors";
import type { ScanStackParamList } from "../App";

type Props = NativeStackScreenProps<ScanStackParamList, "QRResult">;

export function QRResultScreen({ route }: Props) {
    const { result } = route.params;

    return (
        <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
            <RiskCard
                title={result.content_type === "upi" ? "UPI Payment" : "QR Code"}
                level={result.risk_level}
                subtitle={result.explanation}
                details={result.flags}
            />
            {result.destination_account && <Text style={styles.detail}>Destination: {result.destination_account}</Text>}
            {result.destination_url && <Text style={styles.detail}>URL: {result.destination_url}</Text>}
            {result.complaint_count > 0 && (
                <Text style={styles.warning}>{result.complaint_count} complaint(s) linked to this destination.</Text>
            )}
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    screen: { flex: 1, backgroundColor: colors.bgPrimary },
    content: { padding: spacing.xl, gap: spacing.sm },
    detail: { color: colors.textSecondary, fontSize: 13, marginTop: spacing.sm },
    warning: { color: colors.red, fontSize: 13, marginTop: spacing.sm },
});
