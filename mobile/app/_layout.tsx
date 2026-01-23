import { Stack } from "expo-router";
import "../global.css";

export default function RootLayout() {
	return (
		<Stack screenOptions={{ headerShown: false }}>
			<Stack.Screen name="index" />
			<Stack.Screen name="(auth)/login" />
			<Stack.Screen name="(auth)/register" />
			<Stack.Screen name="(tabs)" />
			<Stack.Screen name="stream/[id]" />
		</Stack>
	);
}
