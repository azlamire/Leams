import { useRouter } from 'expo-router';
import React, { useState } from 'react';
import { ActivityIndicator, Alert, Text, TextInput, TouchableOpacity, View } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function LoginScreen() {
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [loading, setLoading] = useState(false);
	const router = useRouter();

	const handleLogin = async () => {
		if (!email || !password) {
			Alert.alert('Ошибка', 'Заполните все поля');
			return;
		}

		try {
			setLoading(true);
			const formData = new URLSearchParams();
			formData.append("grant_type", "password");
			formData.append("username", email);
			formData.append("password", password);
			const loginResponse = await fetch("http://192.168.0.103:8000/auth/jwt/login", {
				method: "POST",
				headers: {
					"Content-Type": "application/x-www-form-urlencoded"
				},
				body: formData.toString()
			});
			if (!loginResponse.ok) {
				console.log(loginResponse)
				throw new Error("Login failed");
			}
			const loginData = await loginResponse.json();
			console.log("You've logged", loginData.access_token)
			await AsyncStorage.setItem('authToken', loginData.access_token);
			console.log(await AsyncStorage.getItem("authToken"), "You've logged")
			router.replace('/(tabs)');
		} catch (error: any) {
			console.log(error, "this is error")
			Alert.alert('Ошибка логина', error.response?.data?.message || 'Не удалось войти в аккаунт');
		} finally {
			setLoading(false);
		}
	};
	return (
		<View className="flex-1 bg-gray-900 justify-center px-6">
			<Text className="text-4xl font-bold text-white text-center mb-8">Вход</Text>

			<View className="mb-4">
				<Text className="text-gray-300 mb-2">Email</Text>
				<TextInput
					className="bg-gray-800 text-white px-4 py-3 rounded-lg"
					placeholder="your@email.com"
					placeholderTextColor="#9CA3AF"
					value={email}
					onChangeText={setEmail}
					keyboardType="email-address"
					autoCapitalize="none"
				/>
			</View>

			<View className="mb-6">
				<Text className="text-gray-300 mb-2">Пароль</Text>
				<TextInput
					className="bg-gray-800 text-white px-4 py-3 rounded-lg"
					placeholder="••••••••"
					placeholderTextColor="#9CA3AF"
					value={password}
					onChangeText={setPassword}
					secureTextEntry
				/>
			</View>

			<TouchableOpacity
				className="bg-purple-600 py-4 rounded-lg mb-4"
				onPress={handleLogin}
				disabled={loading}
			>
				{loading ? (
					<ActivityIndicator color="white" />
				) : (
					<Text className="text-white text-center font-semibold text-lg">Войти</Text>
				)}
			</TouchableOpacity>

			<TouchableOpacity onPress={() => router.push('/(auth)/register')}>
				<Text className="text-gray-400 text-center">
					Нет аккаунта? <Text className="text-purple-500">Зарегистрироваться</Text>
				</Text>
			</TouchableOpacity>
		</View>
	);
}
