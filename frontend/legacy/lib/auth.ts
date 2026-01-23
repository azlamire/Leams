// DEPRECATED: In nextjs we have cookie() 
"use client"
import { AUTH } from "@/shared/constants";

export function getAuthToken() {
	return localStorage.getItem(AUTH.NEXT_PUBLIC_AUTH_TOKEN)
}

export function logOut() {
	localStorage.removeItem(AUTH.NEXT_PUBLIC_AUTH_TOKEN)
}


export function isAuthenticated() {
	return getAuthToken() !== null ? true : false;
}
