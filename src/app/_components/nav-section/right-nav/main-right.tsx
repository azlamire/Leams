"use client"

import { ProfileUser } from "./profile";
import { RightButtons } from "./right-buttons";
import { useState, useEffect } from 'react';
import { AUTH } from "@/shared/constants";
import { api } from "@/lib/api";
export function MainNavRight() {
	return (
		<div className="flex flex-row flex items-center justify-center">
			{/* TODO: Make here Animation mode on and dark and light mode */}
			{localStorage.getItem("auth_token") !== null ? <RightButtons /> : <ProfileUser />}
		</div>
	);
}
