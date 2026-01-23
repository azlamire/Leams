import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Video, ResizeMode } from 'expo-av';
import React, { useEffect, useRef, useState } from 'react';
import {
	ActivityIndicator,
	Alert,
	KeyboardAvoidingView,
	Platform,
	Text,
	View,
	Dimensions,
	StatusBar,
} from 'react-native';
import * as ScreenOrientation from 'expo-screen-orientation';

export default function StreamViewScreen() {
	const { id } = useLocalSearchParams<{ id: string }>();
	const [loading, setLoading] = useState(true);
	const [orientation, setOrientation] = useState('portrait');
	const videoRef = useRef<Video>(null);
	const router = useRouter();

	const streamSlug = Array.isArray(id) ? id[0] : id;

	useEffect(() => {
		console.log("Stream slug:", streamSlug);

		if (!streamSlug) {
			Alert.alert('Ошибка', 'ID стрима не найден');
			router.back();
		}

		// Разрешить все ориентации
		ScreenOrientation.unlockAsync();

		// Слушать изменения ориентации
		const subscription = ScreenOrientation.addOrientationChangeListener((event) => {
			const orientationType = event.orientationInfo.orientation;
			if (
				orientationType === ScreenOrientation.Orientation.LANDSCAPE_LEFT ||
				orientationType === ScreenOrientation.Orientation.LANDSCAPE_RIGHT
			) {
				setOrientation('landscape');
			} else {
				setOrientation('portrait');
			}
		});

		// Получить текущую ориентацию
		ScreenOrientation.getOrientationAsync().then((currentOrientation) => {
			if (
				currentOrientation === ScreenOrientation.Orientation.LANDSCAPE_LEFT ||
				currentOrientation === ScreenOrientation.Orientation.LANDSCAPE_RIGHT
			) {
				setOrientation('landscape');
			} else {
				setOrientation('portrait');
			}
		});

		return () => {
			subscription.remove();
			// Вернуть портретную ориентацию при выходе
			ScreenOrientation.lockAsync(ScreenOrientation.OrientationLock.PORTRAIT_UP);
		};
	}, [streamSlug]);

	if (!streamSlug) {
		return (
			<View className="flex-1 bg-gray-900 justify-center items-center">
				<ActivityIndicator size="large" color="#9333EA" />
			</View>
		);
	}

	const videoUrl = `http://192.168.0.103:80/hls/${streamSlug}.m3u8`;
	const isLandscape = orientation === 'landscape';
	const { width, height } = Dimensions.get('window');

	return (
		<KeyboardAvoidingView
			behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
			className="flex-1 bg-gray-900"
		>
			{isLandscape && <StatusBar hidden />}

			<View className="flex-1">
				{/* Video Player */}
				<View
					className="bg-black"
					style={
						isLandscape
							? { width: width, height: height } // Полный экран в landscape
							: { width: width, aspectRatio: 16 / 9 } // 16:9 в portrait
					}
				>
					<Video
						ref={videoRef}
						source={{ uri: videoUrl }}
						style={{ width: '100%', height: '100%' }}
						useNativeControls
						resizeMode={ResizeMode.CONTAIN}
						shouldPlay
						isLooping={false}
						onLoad={() => {
							console.log("Video loaded successfully:", videoUrl);
							setLoading(false);
						}}
						onError={(error) => {
							console.error('Video error:', error);
							console.error('Failed URL:', videoUrl);
							Alert.alert('Ошибка', `Не удалось загрузить стрим: ${streamSlug}`);
							setLoading(false);
						}}
					/>
					{loading && (
						<View className="absolute inset-0 justify-center items-center bg-black">
							<ActivityIndicator size="large" color="#9333EA" />
						</View>
					)}
				</View>

				{/* Stream Info - скрыть в landscape */}
				{!isLandscape && (
					<View className="bg-gray-800 p-4 border-b border-gray-700">
						<Text className="text-white font-bold text-lg">
							Stream:  {streamSlug}
						</Text>
						<Text className="text-gray-400 text-xs mt-1">
							{videoUrl}
						</Text>
						<View className="flex-row items-center mt-2">
							<View className="bg-red-600 px-3 py-1 rounded-full">
								<Text className="text-white font-bold text-xs">● LIVE</Text>
							</View>
						</View>
					</View>
				)}

				{/* Chat Placeholder - скрыть в landscape */}
				{!isLandscape && (
					<View className="flex-1 justify-center items-center">
						<Ionicons name="chatbubbles-outline" size={64} color="#6B7280" />
						<Text className="text-gray-500 mt-4">Чат скоро будет добавлен</Text>
					</View>
				)}
			</View>
		</KeyboardAvoidingView>
	);
}
