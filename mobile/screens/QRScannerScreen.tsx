import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { CameraView, useCameraPermissions } from "expo-camera";
import { useRef, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { colors, radius, spacing } from "../constants/colors";
import { api } from "../hooks/useApi";
import type { ScanStackParamList } from "../App";

type Props = NativeStackScreenProps<ScanStackParamList, "QRScanner">;

export function QRScannerScreen({ navigation }: Props) {
    const [permission, requestPermission] = useCameraPermissions();
    const scanned = useRef(false);
    const [error, setError] = useState<string | null>(null);

    async function handleScanned(qrContent: string) {
        if (scanned.current) return;
        scanned.current = true;
        try {
            const result = await api.scanQR(qrContent);
            navigation.navigate("QRResult", { result });
        } catch (err) {
            setError(err instanceof Error ? err.message : "QR scan failed");
            scanned.current = false;
        }
    }

    if (!permission) return <View style={styles.screen} />;

    if (!permission.granted) {
        return (
            <View style={[styles.screen, styles.center]}>
                <Text style={styles.message}>Camera access is needed to scan QR codes.</Text>
                <Pressable style={styles.button} onPress={requestPermission}>
                    <Text style={styles.buttonText}>Grant Permission</Text>
                </Pressable>
            </View>
        );
    }

    return (
        <View style={styles.screen}>
            <CameraView
                style={styles.camera}
                facing="back"
                barcodeScannerSettings={{ barcodeTypes: ["qr"] }}
                onBarcodeScanned={(scan) => handleScanned(scan.data)}
            />
            {error && (
                <View style={styles.controls}>
                    <Text style={styles.error}>{error}</Text>
                </View>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    screen: { flex: 1, backgroundColor: colors.bgPrimary },
    camera: { flex: 1 },
    center: { alignItems: "center", justifyContent: "center", padding: spacing.xl, gap: spacing.lg },
    message: { color: colors.textSecondary, fontSize: 14, textAlign: "center" },
    controls: { padding: spacing.lg },
    button: {
        backgroundColor: colors.accent500,
        borderRadius: radius.md,
        paddingVertical: spacing.md,
        paddingHorizontal: spacing.xl,
    },
    buttonText: { color: "#fff", fontWeight: "700", fontSize: 14 },
    error: { color: colors.red, fontSize: 12, textAlign: "center" },
});
