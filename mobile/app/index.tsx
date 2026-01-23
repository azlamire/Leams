import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { ActivityIndicator, View } from 'react-native';

export default function Index() {
	const router = useRouter();
	const [isLoading, setIsLoading] = useState(true);

	useEffect(() => {
		const checkAuth = async () => {
			try {
				const token = await AsyncStorage.getItem("authToken");
				
				// Задержка для монтирования компонента
				setTimeout(() => {
					if (token) {
						router.replace('/(tabs)');
					} else {
						router.replace('/(auth)/login');
					}
				}, 100);
			} catch (error) {
				console.error("Error getting token:", error);
				setTimeout(() => {
					router.replace('/(auth)/login');
				}, 100);
			} finally {
				setIsLoading(false);
			}
		};
		
		checkAuth();
	}, []);

	return (
		<View className="flex-1 bg-gray-900 justify-center items-center">
			<ActivityIndicator size="large" color="#9333EA" />
		</View>
	);
}

