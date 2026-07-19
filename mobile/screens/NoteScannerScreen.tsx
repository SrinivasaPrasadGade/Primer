import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { CameraView, useCameraPermissions } from "expo-camera";
import { useRef, useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from "react-native";
import { colors, radius, spacing } from "../constants/colors";
import { api, NOTE_DENOMINATIONS, type NoteDenomination } from "../hooks/useApi";
import type { ScanStackParamList } from "../App";

type Props = NativeStackScreenProps<ScanStackParamList, "NoteScanner">;

export function NoteScannerScreen({ navigation }: Props) {
    const [permission, requestPermission] = useCameraPermissions();
    const cameraRef = useRef<CameraView>(null);
    const [capturing, setCapturing] = useState(false);
    const [error, setError] = useState<string | null>(null);
    // The model scores authenticity features only — it cannot read the
    // denomination, so the scanner has to tell us which note is in frame.
    const [denomination, setDenomination] = useState<NoteDenomination>(500);

    async function handleCapture() {
        if (!cameraRef.current || capturing) return;
        setCapturing(true);
        setError(null);
        try {
            const photo = await cameraRef.current.takePictureAsync({ base64: true, quality: 0.7 });
            if (!photo?.base64) throw new Error("Could not capture photo");
            const result = await api.verifyNote({
                image_base64: `data:image/jpeg;base64,${photo.base64}`,
                denomination,
                scan_source: "mobile",
            });
            navigation.navigate("ScanResult", { result });
        } catch (err) {
            setError(err instanceof Error ? err.message : "Verification failed");
        } finally {
            setCapturing(false);
        }
    }

    if (!permission) return <View style={styles.screen} />;

    if (!permission.granted) {
        return (
            <View style={[styles.screen, styles.center]}>
                <Text style={styles.message}>Camera access is needed to scan currency notes.</Text>
                <Pressable style={styles.button} onPress={requestPermission}>
                    <Text style={styles.buttonText}>Grant Permission</Text>
                </Pressable>
            </View>
        );
    }

    return (
        <View style={styles.screen}>
            <CameraView ref={cameraRef} style={styles.camera} facing="back" />
            <View style={styles.controls}>
                {error && <Text style={styles.error}>{error}</Text>}
                <View style={styles.denominationRow}>
                    {NOTE_DENOMINATIONS.map((value) => (
                        <Pressable
                            key={value}
                            style={[styles.denominationChip, value === denomination && styles.denominationChipActive]}
                            onPress={() => setDenomination(value)}
                            disabled={capturing}
                        >
                            <Text style={[styles.denominationText, value === denomination && styles.denominationTextActive]}>
                                ₹{value}
                            </Text>
                        </Pressable>
                    ))}
                </View>
                <Pressable style={styles.captureButton} onPress={handleCapture} disabled={capturing}>
                    {capturing ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Capture Note</Text>}
                </Pressable>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    screen: { flex: 1, backgroundColor: colors.bgPrimary },
    camera: { flex: 1 },
    center: { alignItems: "center", justifyContent: "center", padding: spacing.xl, gap: spacing.lg },
    message: { color: colors.textSecondary, fontSize: 14, textAlign: "center" },
    controls: { padding: spacing.lg, gap: spacing.sm },
    denominationRow: { flexDirection: "row", flexWrap: "wrap", gap: spacing.sm, justifyContent: "center" },
    denominationChip: {
        borderRadius: radius.md,
        borderWidth: 1,
        borderColor: colors.accent500,
        paddingVertical: spacing.sm,
        paddingHorizontal: spacing.md,
    },
    denominationChipActive: { backgroundColor: colors.accent500 },
    denominationText: { color: colors.accent500, fontSize: 13, fontWeight: "600" },
    denominationTextActive: { color: "#fff" },
    captureButton: {
        backgroundColor: colors.accent500,
        borderRadius: radius.md,
        paddingVertical: spacing.md,
        alignItems: "center",
    },
    button: {
        backgroundColor: colors.accent500,
        borderRadius: radius.md,
        paddingVertical: spacing.md,
        paddingHorizontal: spacing.xl,
    },
    buttonText: { color: "#fff", fontWeight: "700", fontSize: 14 },
    error: { color: colors.red, fontSize: 12, textAlign: "center" },
});
