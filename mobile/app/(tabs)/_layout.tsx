import { Ionicons } from '@expo/vector-icons';
import { Tabs } from 'expo-router';

export default function TabLayout() {
	return (
		<Tabs
			screenOptions={{
				tabBarActiveTintColor: '#9333EA',
				tabBarInactiveTintColor: '#6B7280',
				tabBarStyle: {
					backgroundColor: '#1F2937',
					borderTopColor: '#374151',
				},
				headerStyle: {
					backgroundColor: '#1F2937',
				},
				headerTintColor: '#FFFFFF',
			}}
		>
			<Tabs.Screen
				name="index"
				options={{
					title: 'COVER',
					tabBarIcon: ({ color, size }) => (
						<Ionicons name="play-circle-outline" size={size} color={color} />
					),
				}}
			/>
			<Tabs.Screen
				name="create"
				options={{
					title: 'Создать',
					tabBarIcon: ({ color, size }) => (
						<Ionicons name="add-circle-outline" size={size} color={color} />
					),
				}}
			/>
		</Tabs>
	);
}
