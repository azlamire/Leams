import { BACKEND } from "@/shared/constants";
import { type Dispatch, type SetStateAction } from "react";
import { type RegLogButtsType } from "./types";
import { type FormLoginType, type FormType } from "./types";
import { store } from "@/shared/store";
import { type AppRouterInstance } from 'next/dist/shared/lib/app-router-context.shared-runtime'

// PERF: Yep, it's for perfomance but unreusable
export const logInForm: FormLoginType[] = [
	{ name: "username", label: "Username", type: "text", },
	{ name: "password", label: "Password", type: "password" },
];

// PERF: Yep, it's for perfomance but unreusable
export const butRegLog: RegLogButtsType[] = [
	{
		name: "Log In",
		active: !store.state.openReg,
		onClick: () => {
			console.log(store.state.openReg)
			store.setState(prev => ({ ...prev, openReg: false }))
		},
		className: "cursor-pointer"
	},
	{
		name: "Sign Up",
		active: store.state.openReg,
		onClick: () => {

			console.log(store.state.openReg)
			store.setState(prev => ({ ...prev, openReg: true }))
		},
		className: "cursor-pointer"
	}
]

// TODO: Make it reusable when it'll be a case for this
export const GitHubAuth = async (router: AppRouterInstance) => {
	const response = await fetch(BACKEND.NEXT_PUBLIC_GITHUB_AUTH, {
		method: "GET",
		headers: {
			"Content-Type": "application/json"
		},
	})
	const Content = await response.json();
	router.push(Content.authorization_url)
}



// TODO: I really don't like this remake in future when will work under this
export const signInForm: FormType[] = [
	{
		name: "username", label: "Username", type: "text",
		on_change: async (value: string, hook: Dispatch<SetStateAction<boolean | undefined>>) => {
			await fetch(BACKEND.NEXT_PUBLIC_HAS_USER_CHECK, {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({ nickname: value })
			})
				.then(response => response.json())
				.then(data => {
					console.log(data)
					hook(data.validUser);
				})
		}
	},
	{ name: "password", label: "Password", type: "password" },
	{
		name: "email", label: "Email", type: "email",
		on_change: async (value: string, hook: Dispatch<SetStateAction<boolean | undefined>>) => {
			await fetch(BACKEND.NEXT_PUBLIC_HAS_EMAIL_CHECK, {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({ email: value })
			})
				.then(response => response.json())
				.then(data => {
					console.log(data)
					console.log(data.validEmail);
					hook(data.validEmail);
				})
		}
	},
];

