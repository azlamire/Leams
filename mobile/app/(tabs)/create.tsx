import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import React, { useState, useEffect } from 'react';
import {
	ActivityIndicator,
	Alert,
	ScrollView,
	Text,
	TextInput,
	TouchableOpacity,
	View,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function CreateStreamScreen() {
	const [title, setTitle] = useState('');
	const [description, setDescription] = useState('');
	const [thumbnail, setThumbnail] = useState('');
	const [loading, setLoading] = useState(false);
	const [token, setAuthToken] = useState<string | null>();
	const router = useRouter();
	useEffect(() => {
		const checkAuth = async () => {
			try {
				const token = await AsyncStorage.getItem("authToken");
				console.log("Token from storage:", token);
				setAuthToken(token);
				console.log(token, "HEY ITS ME")
			} catch (error) {
				console.error("Error getting token:", error);
			}
		};

		checkAuth();
	}, []);

	const handleCreateStream = async () => {
		if (!token) {
			Alert.alert('Требуется авторизация', 'Войдите в аккаунт, чтобы создать стрим', [
				{ text: 'Отмена' },
				{ text: 'Войти', onPress: () => router.push('/(auth)/login') },
			]);
			return;
		}

		if (!title || !description) {
			Alert.alert('Ошибка', 'Заполните название и описание стрима');
			return;
		}

		try {
			setLoading(true);
			Alert.alert('Успех', 'Стрим создан!', [
			]);
			setTitle('');
			setDescription('');
			setThumbnail('');
		} catch (error: any) {
			Alert.alert('Ошибка', error.response?.data?.message || 'Не удалось создать стрим');
		} finally {
			setLoading(false);
		}
	};

	const handleLogout = async () => {
		Alert.alert('Выход', 'Вы уверены, что хотите выйти?', [
			{
				text: 'Отмена',
				style: 'cancel'
			},
			{
				text: 'Выйти',
				style: 'destructive',
				onPress: async () => {
					try {
						await AsyncStorage.multiRemove([
							'access_token',
						]);
						Alert.alert('Успех', 'Вы успешно вышли из аккаунта');
						router.push('../(auth)/login');
					} catch (error) {
						console.error('Logout error:', error);
						Alert.alert('Ошибка', 'Не удалось выйти из аккаунта');
					}
				}
			},
		]);
	};

	if (!token) {
		return (
			<View className="flex-1 bg-gray-900 justify-center items-center px-6">
				<Ionicons name="lock-closed-outline" size={64} color="#6B7280" />
				<Text className="text-white text-2xl font-bold mt-4 mb-2">
					Требуется авторизация
				</Text>
				<Text className="text-gray-400 text-center mb-6">
					Войдите в аккаунт, чтобы создавать стримы
				</Text>
				<TouchableOpacity
					className="bg-purple-600 px-8 py-3 rounded-lg"
					onPress={() => router.push('/(auth)/login')}
				>
					<Text className="text-white font-semibold text-lg">Войти</Text>
				</TouchableOpacity>
			</View>
		);
	}

	return (
		<ScrollView className="flex-1 bg-gray-900">
			<View className="p-6">
				<View className="flex-row items-center justify-between mb-6">
					<View>
						<Text className="text-white text-2xl font-bold">Создать стрим</Text>
					</View>
					<TouchableOpacity onPress={handleLogout}>
						<Ionicons name="log-out-outline" size={28} color="#EF4444" />
					</TouchableOpacity>
				</View>

				<View className="mb-4">
					<Text className="text-gray-300 mb-2 font-semibold">Название стрима</Text>
					<TextInput
						className="bg-gray-800 text-white px-4 py-3 rounded-lg"
						placeholder="Введите название..."
						placeholderTextColor="#9CA3AF"
						value={title}
						onChangeText={setTitle}
					/>
				</View>

				<View className="mb-4">
					<Text className="text-gray-300 mb-2 font-semibold">Описание</Text>
					<TextInput
						className="bg-gray-800 text-white px-4 py-3 rounded-lg"
						placeholder="Расскажите о чем будет стрим..."
						placeholderTextColor="#9CA3AF"
						value={description}
						onChangeText={setDescription}
						multiline
						numberOfLines={4}
						textAlignVertical="top"
					/>
				</View>

				<View className="mb-6">
					<Text className="text-gray-300 mb-2 font-semibold">URL превью (опционально)</Text>
					<TextInput
						className="bg-gray-800 text-white px-4 py-3 rounded-lg"
						placeholder="https://..."
						placeholderTextColor="#9CA3AF"
						value={thumbnail}
						onChangeText={setThumbnail}
						autoCapitalize="none"
					/>
				</View>

				<TouchableOpacity
					className="bg-purple-600 py-4 rounded-lg"
					onPress={handleCreateStream}
					disabled={loading}
				>
					{loading ? (
						<ActivityIndicator color="white" />
					) : (
						<Text className="text-white text-center font-semibold text-lg">
							Создать стрим
						</Text>
					)}
				</TouchableOpacity>

				<View className="mt-6 p-4 bg-gray-800 rounded-lg">
					<Text className="text-gray-300 text-sm mb-2">
						<Ionicons name="information-circle" size={16} /> Информация
					</Text>
					<Text className="text-gray-400 text-xs">
						После создания стрима вы получите ключ для подключения к серверу трансляции.
						Используйте его в OBS или другом ПО для стриминга.
					</Text>
				</View>
			</View>
		</ScrollView>
	);
}
