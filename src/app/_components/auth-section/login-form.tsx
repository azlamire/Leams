"use client"
import { BACKEND } from "@/shared/constants";
import { type FormLoginStateType } from "./types";
import { Roboto } from "next/font/google";
import { logInForm } from "./constant";
import { signIn } from "next-auth/react";
import { useState, type FormEventHandler } from "react";

const roboto = Roboto({
	subsets: ['latin'],
})


export function Login() {
	const [form, setForm] = useState<FormLoginStateType>({
		user_email: "",
		password: "",
	})

	const handleSubmit: FormEventHandler<HTMLFormElement> = async (e) => {
		console.log("Form submitted", form);
		e.preventDefault();
		const response = await fetch(BACKEND.NEXT_PUBLIC_AUTH, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(form)
		})
			// .then((resp) => localStorage.setItem("authToken", resp.json()))
			.then((resp) => console.log(resp))
	}

	// TODO: make useRef for saving a content even if it's closed or even reloaded 
	return (
		<form className="align-top flex flex-col rounded-xl w-full h-[65%] gap-7 mt-10" onSubmit={handleSubmit}>
			{logInForm.map((item) => (
				<div key={item.name} className="relative border-2 flex gap-2 flex-col w-full mb-5 group border-b-0 [background:linear-gradient(#3b82f6_0_0)_bottom/var(--d,0)_3px_no-repeat] transition-all duration-500 [--d:0]">
					<label
						htmlFor=""
						//form[item.name as keyof FormStateType]
						className={form[item.name as keyof typeof form] === "" && item.name != "birthday"
							? "absolute duration-300 group-focus-within:-translate-y-6 z-25"
							: "absolute duration-300 -translate-y-6 z-25 "}>
						{item.label}
					</label>
					<input
						className="outline-none w-full h-full z-30"
						required
						type={item.type}
						id=""
						autoComplete={item.name}
						onChange={e => {
							const newValue = e.target.value;
							setForm({ ...form, [item.name]: newValue });
						}} />
				</div>
			))}
			<div className="flex w-full items-center justify-center">
				<button className={roboto.className + " shadow-md h-[60px] w-[120px] text-[20px] font-stretch-125% font-medium rounded-full cursor-pointer"} type="submit">
					Submit
				</button>
			</div>
			<div>
				<button onClick={() => signIn('github')}>Sign in with GitHub</button>
			</div>
		</form>

	)
}
