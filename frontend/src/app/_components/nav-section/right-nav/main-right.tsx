"use client"

import { ProfileUser } from "./profile";
import { RightButtons } from "./right-buttons";
import { useState, useEffect } from 'react';
import { AUTH } from "@/shared/constants";
import { api } from "@/lib/api";
export function MainNavRight() {
	const [storage, setStorage] = useState<string | null>(null);
	useEffect(() => {
		setStorage(localStorage.getItem("access_token"))
		console.log(localStorage.getItem("access_token"))
	}, [])

	return (
		<div className="flex flex-row  items-center justify-center relative overflow-visible">
			{storage ? <ProfileUser /> : <RightButtons />}
		</div>
	);
}
