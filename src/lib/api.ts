"use client"

import axios from "axios";

export const api = axios.create({
	timeout: 10000,
	headers: {
		"Content-Type": "application/json",
	}
})

document
api.interceptors.request.use(
	(config) => {
		config.headers['X-User-Login'] = 'Dambarioid';
		if (typeof window !== 'undefined') {
			const token = localStorage.getItem("auth_token");
			if (token) {
				config.headers.Authorization = `Bearer ${token}`;
			}
		}
		return config;
	},
	(error) => {
		console.error(`❌ [2025-11-11 02:39:43] Request error for Dambarioid:`, error);
		return Promise.reject(error);
	}
);
