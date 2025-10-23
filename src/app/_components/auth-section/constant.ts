import { type FormLoginType, type FormType, type FormStateType } from "./types";
import { type Dispatch, type SetStateAction } from "react";
import { BACKEND } from "@/shared/constants";

// TODO: I really don't like this remake in future when will work under this
const logInForm: FormLoginType[] = [
	{ name: "user_email", label: "Username", type: "text", },
	{ name: "password", label: "Password", type: "password" },
];

// TODO: I really don't like this remake in future when will work under this
const signInForm: FormType[] = [
	{
		name: "username", label: "Username", type: "text",
		on_change: async (value: string, hook: Dispatch<SetStateAction<boolean | undefined>>) => {
			await fetch("http://127.0.0.1:8000/has_user", {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({ nickname: value })
			})
				.then(response => response.json())
				.then(data => {
					console.log(data);
					console.log(data.invalidUser);
					hook(data.invalidUser);
				})
		}
	},
	{ name: "password", label: "Password", type: "password" },
	{
		name: "email", label: "Email", type: "email",
		on_change: async (value: string, hook: Dispatch<SetStateAction<boolean | undefined>>) => {
			const some_request = await fetch("http://127.0.0.1:8000/has_email", {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({ Email: value })
			})
				.then(response => response.json())
				.then(data => {
					hook(data.invalidEmail);
				})
		}
	},
];

// TODO: I really don't like this remake in future when will work under this
const butRegLog: RegLogButtsType[] = [
	{
		name: "Log In",
		active: isLogin,
		onClick: () => store.setState(prev => ({ ...prev, isReg: false, isLogin: true })),
		className: "cursor-pointer"
	},
	{
		name: "Sign Up",
		active: !isLogin,
		onClick: () => store.setState(prev => ({ ...prev, isReg: true, isLogin: false })),
		className: "cursor-pointer"
	}
]
