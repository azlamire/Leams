import { useRouter } from 'expo-router';
import React, { useState } from 'react';
import { ActivityIndicator, Alert, Text, TextInput, TouchableOpacity, View } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function RegisterScreen() {
	const [username, setUsername] = useState('');
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [confirmPassword, setConfirmPassword] = useState('');
	const [loading, setLoading] = useState(false);
	const router = useRouter();


	const handleRegister = async () => {
		if (!username || !email || !password || !confirmPassword) {
			Alert.alert('Ошибка', 'Заполните все поля');
			return;
		}

		if (password !== confirmPassword) {
			Alert.alert('Ошибка', 'Пароли не совпадают');
			return;
		}

		if (password.length < 6) {
			Alert.alert('Ошибка', 'Пароль должен быть не менее 6 символов');
			return;
		}

		try {
			setLoading(true);


			const reg = await fetch("http://192.168.0.103:8000/auth/register", {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({ "username": username, "password": password, "email": email })
			})
			console.log(reg)
			if (!reg.ok) {
				throw new Error("Registration failed");
			}

			const registerData = await reg.json();
			console.log("Registration successful:", registerData);
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

			await AsyncStorage.setItem('authToken', loginData.access_token);
			router.replace('/(tabs)');
		} catch (error: any) {
			console.log(error)
			Alert.alert('Ошибка регистрации', error.response?.data?.message || 'Не удалось создать аккаунт');
		} finally {
			setLoading(false);
		}
	};

	return (
		<View className="flex-1 bg-gray-900 justify-center px-6">
			<Text className="text-4xl font-bold text-white text-center mb-8">Регистрация</Text>

			<View className="mb-4">
				<Text className="text-gray-300 mb-2">Имя пользователя</Text>
				<TextInput
					className="bg-gray-800 text-white px-4 py-3 rounded-lg"
					placeholder="username"
					placeholderTextColor="#9CA3AF"
					value={username}
					onChangeText={setUsername}
					autoCapitalize="none"
				/>
			</View>

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

			<View className="mb-4">
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

			<View className="mb-6">
				<Text className="text-gray-300 mb-2">Подтвердите пароль</Text>
				<TextInput
					className="bg-gray-800 text-white px-4 py-3 rounded-lg"
					placeholder="••••••••"
					placeholderTextColor="#9CA3AF"
					value={confirmPassword}
					onChangeText={setConfirmPassword}
					secureTextEntry
				/>
			</View>

			<TouchableOpacity
				className="bg-purple-600 py-4 rounded-lg mb-4"
				onPress={handleRegister}
				disabled={loading}
			>
				{loading ? (
					<ActivityIndicator color="white" />
				) : (
					<Text className="text-white text-center font-semibold text-lg">Зарегистрироваться</Text>
				)}
			</TouchableOpacity>

			<TouchableOpacity onPress={() => router.back()}>
				<Text className="text-gray-400 text-center">
					Уже есть аккаунт? <Text className="text-purple-500">Войти</Text>
				</Text>
			</TouchableOpacity>
		</View>
	);
}
