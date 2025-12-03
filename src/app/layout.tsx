"use client"
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { UpSide } from "./_components/nav-section//UpSide";
import { MainLogin } from "./_components/auth-section/auth-block";
import { LeftSide } from "./_components/left-section/left-main";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";
import { Rubik } from 'next/font/google'

const geistSans = Geist({
	variable: "--font-geist-sans",
	subsets: ["latin"],
});

const geistMono = Geist_Mono({
	variable: "--font-geist-mono",
	subsets: ["latin"],
});

const rubik = Rubik({
	subsets: ['latin'],
})

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	const [queryClient] = useState(() => new QueryClient())
	return (
		<QueryClientProvider client={queryClient}>
			<html lang="en">
				<body className={`${geistSans.variable} ${geistMono.variable} antialiased ${rubik.className}`}>
					<MainLogin />
					<div className="h-screen">
						<UpSide />
						<div className="inline-flex h-full w-full">
							<LeftSide />
							{children}
						</div>
					</div>
				</body>
			</html>
		</QueryClientProvider>
	);
}
