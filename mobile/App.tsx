import { DarkTheme, NavigationContainer, NavigatorScreenParams, Theme } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { StatusBar } from "expo-status-bar";
import { Home, MessageCircle, QrCode, ScanLine, User } from "lucide-react-native";
import { useEffect, useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from "react-native";
import { colors } from "./constants/colors";
import { api, ApiError, NoteVerifyResult, QRScanResult } from "./hooks/useApi";
import { CallScreeningScreen } from "./screens/CallScreeningScreen";
import { ChatScreen } from "./screens/ChatScreen";
import { HomeScreen } from "./screens/HomeScreen";
import { NoteScannerScreen } from "./screens/NoteScannerScreen";
import { NumberCheckScreen } from "./screens/NumberCheckScreen";
import { PanicScreen } from "./screens/PanicScreen";
import { ProfileScreen } from "./screens/ProfileScreen";
import { QRResultScreen } from "./screens/QRResultScreen";
import { QRScannerScreen } from "./screens/QRScannerScreen";
import { ScanResultScreen } from "./screens/ScanResultScreen";

// ─── Navigation param lists (co-located with the navigators, per doc §6) ───
export type ScanStackParamList = {
    NoteScanner: undefined;
    ScanResult: { result: NoteVerifyResult };
    QRScanner: undefined;
    QRResult: { result: QRScanResult };
};
export type HomeStackParamList = {
    HomeMain: undefined;
    NumberCheck: undefined;
};
export type TabParamList = {
    Home: NavigatorScreenParams<HomeStackParamList>;
    Scan: NavigatorScreenParams<ScanStackParamList>;
    Chat: undefined;
    Profile: undefined;
};
export type RootStackParamList = {
    MainTabs: NavigatorScreenParams<TabParamList>;
    Panic: undefined;
    CallScreening: { callerNumber?: string } | undefined;
};

declare global {
    // eslint-disable-next-line @typescript-eslint/no-namespace
    namespace ReactNavigation {
        interface RootParamList extends RootStackParamList {}
    }
}

const stackScreenOptions = {
    headerStyle: { backgroundColor: colors.layer1 },
    headerTintColor: colors.textPrimary,
    headerShadowVisible: false,
} as const;

const HomeStack = createNativeStackNavigator<HomeStackParamList>();
function HomeStackNavigator() {
    return (
        <HomeStack.Navigator screenOptions={stackScreenOptions}>
            <HomeStack.Screen name="HomeMain" component={HomeScreen} options={{ title: "Primer" }} />
            <HomeStack.Screen name="NumberCheck" component={NumberCheckScreen} options={{ title: "Number Check" }} />
        </HomeStack.Navigator>
    );
}

const ScanStack = createNativeStackNavigator<ScanStackParamList>();
function ScanStackNavigator() {
    return (
        <ScanStack.Navigator screenOptions={stackScreenOptions}>
            <ScanStack.Screen
                name="NoteScanner"
                component={NoteScannerScreen}
                options={({ navigation }) => ({
                    title: "Scan Currency Note",
                    headerRight: () => (
                        <Pressable onPress={() => navigation.navigate("QRScanner")} accessibilityLabel="Switch to QR scanner">
                            <QrCode size={20} color={colors.accent500} />
                        </Pressable>
                    ),
                })}
            />
            <ScanStack.Screen name="ScanResult" component={ScanResultScreen} options={{ title: "Result" }} />
            <ScanStack.Screen
                name="QRScanner"
                component={QRScannerScreen}
                options={({ navigation }) => ({
                    title: "Scan QR Code",
                    headerRight: () => (
                        <Pressable onPress={() => navigation.navigate("NoteScanner")} accessibilityLabel="Switch to note scanner">
                            <ScanLine size={20} color={colors.accent500} />
                        </Pressable>
                    ),
                })}
            />
            <ScanStack.Screen name="QRResult" component={QRResultScreen} options={{ title: "Result" }} />
        </ScanStack.Navigator>
    );
}

const Tab = createBottomTabNavigator<TabParamList>();
function TabNavigator() {
    return (
        <Tab.Navigator
            screenOptions={{
                headerShown: false,
                tabBarStyle: { backgroundColor: colors.bgPrimary, borderTopColor: colors.borderSubtle },
                tabBarActiveTintColor: colors.accent500,
                tabBarInactiveTintColor: colors.textTertiary,
            }}
        >
            <Tab.Screen name="Home" component={HomeStackNavigator} options={{ tabBarIcon: ({ color, size }) => <Home color={color} size={size} /> }} />
            <Tab.Screen name="Scan" component={ScanStackNavigator} options={{ tabBarIcon: ({ color, size }) => <ScanLine color={color} size={size} /> }} />
            <Tab.Screen
                name="Chat"
                component={ChatScreen}
                options={{
                    headerShown: true,
                    title: "AI Assistant",
                    ...stackScreenOptions,
                    tabBarIcon: ({ color, size }) => <MessageCircle color={color} size={size} />,
                }}
            />
            <Tab.Screen
                name="Profile"
                component={ProfileScreen}
                options={{
                    headerShown: true,
                    title: "Profile",
                    ...stackScreenOptions,
                    tabBarIcon: ({ color, size }) => <User color={color} size={size} />,
                }}
            />
        </Tab.Navigator>
    );
}

const RootStack = createNativeStackNavigator<RootStackParamList>();

const navigationTheme: Theme = {
    ...DarkTheme,
    colors: {
        ...DarkTheme.colors,
        background: colors.bgPrimary,
        card: colors.layer1,
        border: colors.borderSubtle,
        primary: colors.accent500,
        text: colors.textPrimary,
    },
};

export default function App() {
    const [ready, setReady] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function bootstrap() {
        setError(null);
        try {
            await api.ensureLoggedIn();
            setReady(true);
        } catch (err) {
            setError(err instanceof ApiError ? err.message : "Could not reach the Primer backend. Check your connection and try again.");
        }
    }

    useEffect(() => {
        bootstrap();
    }, []);

    if (!ready) {
        return (
            <View style={styles.splash}>
                <StatusBar style="light" />
                {error ? (
                    <>
                        <Text style={styles.errorText}>{error}</Text>
                        <Pressable style={styles.retryButton} onPress={bootstrap}>
                            <Text style={styles.retryText}>Retry</Text>
                        </Pressable>
                    </>
                ) : (
                    <ActivityIndicator size="large" color={colors.accent500} />
                )}
            </View>
        );
    }

    return (
        <NavigationContainer theme={navigationTheme}>
            <StatusBar style="light" />
            <RootStack.Navigator screenOptions={{ headerShown: false }}>
                <RootStack.Screen name="MainTabs" component={TabNavigator} />
                <RootStack.Screen name="Panic" component={PanicScreen} options={{ presentation: "modal" }} />
                <RootStack.Screen
                    name="CallScreening"
                    component={CallScreeningScreen}
                    options={{ presentation: "transparentModal", animation: "fade" }}
                />
            </RootStack.Navigator>
        </NavigationContainer>
    );
}

const styles = StyleSheet.create({
    splash: {
        flex: 1,
        backgroundColor: colors.bgPrimary,
        alignItems: "center",
        justifyContent: "center",
        gap: 16,
        padding: 24,
    },
    errorText: {
        color: colors.textSecondary,
        fontSize: 14,
        textAlign: "center",
    },
    retryButton: {
        backgroundColor: colors.accent500,
        paddingVertical: 12,
        paddingHorizontal: 24,
        borderRadius: 8,
    },
    retryText: {
        color: "#fff",
        fontWeight: "700",
    },
});
