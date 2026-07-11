import { useNavigation } from "@react-navigation/native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { AlertTriangle, MessageCircle, PhoneCall, QrCode, ScanLine } from "lucide-react-native";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { FeatureGrid } from "../components/FeatureGrid";
import { colors, spacing } from "../constants/colors";
import type { HomeStackParamList, RootStackParamList } from "../App";

type HomeNavigation = NativeStackNavigationProp<HomeStackParamList, "HomeMain"> & NativeStackNavigationProp<RootStackParamList>;

export function HomeScreen() {
    const navigation = useNavigation<HomeNavigation>();
    return (
        <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
            <Text style={styles.title}>Primer Citizen Shield</Text>
            <Text style={styles.subtitle}>Stay ahead of scams, counterfeit notes, and fraud.</Text>

            <FeatureGrid
                items={[
                    {
                        key: "note",
                        label: "Scan Currency Note",
                        icon: ScanLine,
                        onPress: () => navigation.navigate("MainTabs", { screen: "Scan", params: { screen: "NoteScanner" } }),
                    },
                    {
                        key: "qr",
                        label: "Scan QR Code",
                        icon: QrCode,
                        onPress: () => navigation.navigate("MainTabs", { screen: "Scan", params: { screen: "QRScanner" } }),
                    },
                    {
                        key: "number",
                        label: "Check Phone Number",
                        icon: PhoneCall,
                        onPress: () => navigation.navigate("NumberCheck"),
                    },
                    {
                        key: "chat",
                        label: "Ask AI Assistant",
                        icon: MessageCircle,
                        onPress: () => navigation.navigate("MainTabs", { screen: "Chat" }),
                    },
                ]}
            />

            <View style={{ marginTop: spacing.xl }}>
                <FeatureGrid
                    items={[
                        {
                            key: "panic",
                            label: "Panic SOS",
                            icon: AlertTriangle,
                            tone: "red",
                            onPress: () => navigation.navigate("Panic"),
                        },
                    ]}
                />
            </View>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        backgroundColor: colors.bgPrimary,
    },
    content: {
        padding: spacing.xl,
    },
    title: {
        color: colors.textPrimary,
        fontSize: 22,
        fontWeight: "700",
        marginBottom: spacing.xs,
    },
    subtitle: {
        color: colors.textSecondary,
        fontSize: 13,
        marginBottom: spacing.xl,
    },
});
