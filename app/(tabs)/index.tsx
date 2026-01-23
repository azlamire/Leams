import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import {
	ActivityIndicator,
	Alert,
	FlatList,
	Image,
	RefreshControl,
	Text,
	TouchableOpacity,
	View,
} from 'react-native';

interface Stream {
	id: string;
	title: string;
	description: string;
	thumbnail?: string;
	username: string;
	isLive: boolean;
	viewerCount: number;
}

export default function MainScreen() {
	const [streams, setStreams] = useState<Stream[]>([]);
	const [loading, setLoading] = useState(true);
	const [refreshing, setRefreshing] = useState(false);
	const router = useRouter();

	useEffect(() => {
		loadStreams();
	}, []);

	const loadStreams = async () => {
		try {
			const response = await fetch("http://192.168.0.103:8000/get_list_streams", {
				method: "GET",
				headers: {
					"Content-Type": "application/x-www-form-urlencoded"
				},
			});
			console.log(response)

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			console.log("Streams loaded:", data);

			setStreams(data);
		} catch (error) {
			console.error("Error loading streams:", error);
			Alert.alert('Ошибка', 'Не удалось загрузить стримы');
		} finally {
			setLoading(false);
		}
	};

	const onRefresh = async () => {
		setRefreshing(true);
		await loadStreams();
		setRefreshing(false);
	};

	const renderStreamCard = ({ item }: { item: Stream }) => (
		<TouchableOpacity
			className="bg-gray-800 rounded-lg mb-4 overflow-hidden"
			onPress={() => router.push(`/stream/${item.id}`)}
		>
			<View className="relative">
				<Image
					source={{ uri: item.thumbnail || 'https://via.placeholder.com/400x225' }}
					className="w-full h-48"
					resizeMode="cover"
				/>
				{item.isLive && (
					<View className="absolute top-2 left-2 bg-red-600 px-3 py-1 rounded-full">
						<Text className="text-white font-bold text-xs">● LIVE</Text>
					</View>
				)}
				<View className="absolute bottom-2 right-2 bg-black/70 px-2 py-1 rounded">
					<Text className="text-white text-xs">
						<Ionicons name="eye" size={12} /> {item.viewerCount}
					</Text>
				</View>
			</View>

			<View className="p-4">
				<Text className="text-white font-bold text-lg mb-1" numberOfLines={1}>
					{item.title}
				</Text>
				<Text className="text-gray-400 text-sm mb-2" numberOfLines={2}>
					{item.description}
				</Text>
				<Text className="text-purple-400 text-sm">@{item.username}</Text>
			</View>
		</TouchableOpacity>
	);

	if (loading) {
		return (
			<View className="flex-1 bg-gray-900 justify-center items-center">
				<ActivityIndicator size="large" color="#9333EA" />
			</View>
		);
	}

	return (
		<View className="flex-1 bg-gray-900">
			<FlatList
				data={streams}
				renderItem={renderStreamCard}
				keyExtractor={(item) => item.id}
				contentContainerStyle={{ padding: 16 }}
				refreshControl={
					<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#9333EA" />
				}
				ListEmptyComponent={
					<View className="flex-1 justify-center items-center py-20">
						<Ionicons name="videocam-off-outline" size={64} color="#6B7280" />
						<Text className="text-gray-400 text-lg mt-4">Нет активных стримов</Text>
					</View>
				}
			/>
		</View>
	);
}
