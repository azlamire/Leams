"use client"
import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { MAIN } from "@/shared/constants";

interface UserInfo {
	email: string;
}

export function ProfileUser() {
	const [isModalOpen, setIsModalOpen] = useState(false);
	const [token, setToken] = useState<string | null>(null)
	useEffect(() => setToken(localStorage.getItem("access_token")), [])

	const { data: userInfo, isLoading, isError } = useQuery<UserInfo>({
		queryKey: ['user-profile'],
		queryFn: async () => {
			const response = await api.post('http://127.0.0.1:8000/main/user_info', {}, {
				params: { access_token: token }
			});
			return response.data;
		},
		retry: 1,
		staleTime: 5 * 60 * 1000,
	});

	if (isLoading) {
		return (
			<div className="h-10 w-10 rounded-full bg-gray-200 animate-pulse" />
		);
	}
	if (isError || !userInfo) {
		return null;
	}
	const avatarUrl = userInfo.email ||
		`https://ui-avatars.com/api/?name=${encodeURIComponent(userInfo.email)}&background=0D8ABC&color=fff&bold=true&size=200`;

	return (
		<div className="relative overflow-visible">
			<button
				onClick={() => setIsModalOpen(prev => !prev)}
				className="flex items-center justify-center rounded-full hover:opacity-80 transition-opacity overflow-visible"
				aria-label="User profile"
			>
				<img
					src={avatarUrl}
					alt={`${userInfo.email} avatar`}
					className="h-10 w-10 rounded-full"
					width={40}
					height={40}
				/>
			</button>

			{isModalOpen && (
				<>
					<div className="absolute right-0 mt-2 w-48 bg-black rounded-lg shadow-lg border border-gray-200 z-40 overflow-visible"
						style={{ overflow: "visible" }}>
						<ul className="py-2">
							<li className="px-4 py-2 border-b border-gray-100">
								<p className="text-sm font-medium text-gray-900">
									{userInfo.email}
								</p>
								<p className="text-xs text-gray-500 truncate">
									{userInfo.email}
								</p>
							</li>

							<li>
								<button
									onClick={() => {
										setIsModalOpen(false);
										const userInput = prompt("Please enter your name:");
									}}
									className="w-full cursor-pointer text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
								>
									⚙️ Settings
								</button>
							</li>

							<li>
								<button
									onClick={() => {
										setIsModalOpen(false);
									}}
									className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
								>
									👤 Profile
								</button>
							</li>

							<li className="border-t border-gray-100">
								<button
									onClick={() => {
										setIsModalOpen(false);
									}}
									className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
								>
									Logout
								</button>
							</li>
						</ul>
					</div>
				</>
			)}
		</div>
	);
}
