"use client"

import { ProfileUser } from "./profile";
import { RightButtons } from "./right-buttons";
import { useState, useEffect } from 'react';
import { AUTH } from "@/shared/constants";
import { api } from "@/lib/api";
export function MainNavRight() {
	const [storage, setStorage] = useState("");
	useEffect(() => {
		let auth_token = localStorage.getItem("auth_token");
		auth_token === null
			? setStorage("")
			: setStorage(auth_token)
	}, [])
	return (
		<div className="flex flex-row flex items-center justify-center">
			{/* TODO: Make here Animation mode on and dark and light mode */}
			{storage !== "" ? <RightButtons /> : <ProfileUser />}
		</div>
	);
}
