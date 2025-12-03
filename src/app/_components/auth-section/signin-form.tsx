"use client"
import { BACKEND, AUTH } from "@/shared/constants";
import clsx from "clsx";
import { FaGithub } from "react-icons/fa";
import { FcGoogle } from "react-icons/fc";
import { FaEye } from "react-icons/fa";
import { FaEyeSlash } from "react-icons/fa6";
import { type FormStateType } from "./types";
import { GitHubAuth, signInForm } from "./constant";
import { Roboto } from "next/font/google";
import { useEffect, useRef, useState, type FormEventHandler } from "react";
import { useRouter } from 'next/navigation';

const roboto = Roboto({ subsets: ['latin'] })

export function SignIn() {
	// TEST: This is just testing so controll it 
	let nickInput = useRef("")
	// NOTE: idk is it really worth to make mutliple or remain the big one
	const [emailValid, setEmailValid] = useState<boolean | undefined>(undefined)
	const [nickValid, setNickValid] = useState<boolean | undefined>(undefined)
	const [passValid, setPassValid] = useState<boolean | undefined>(undefined)
	const [passType, setPassType] = useState<boolean>(true)
	const [form, setForm] = useState<FormStateType>({
		username: "",
		password: "",
		email: "",
	})

	const timeoutRefs = useRef<{ [key: string]: NodeJS.Timeout }>({})
	const router = useRouter()

	// IDK: Do I need to make this reusabl think in future, OK?
	const handleSubmit: FormEventHandler<HTMLFormElement> = async (e) => {
		e.preventDefault();
		await fetch(BACKEND.NEXT_PUBLIC_REGISTER, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(form)
		})
			.then(response => response.json())
			.then(() => {
				localStorage.getItem("auth_token");
				window.location.reload();
			})
			.catch((err) => {
				alert(err);
				console.log(err);
			})
	}
	useEffect(() => {
		console.log(nickValid, passValid, emailValid)
	}, [nickValid, passValid, emailValid])

	return (
		<>
			<form className="flex flex-col rounded-xl w-full h-[65%] gap-7" onSubmit={handleSubmit} z-15>
				{
					signInForm.map((item) => (
						<div key={item.name} className={
							clsx(
								"relative flex gap-2 flex-col w-full mb-5 group border-b-0 [background:linear-gradient(#3b82f6_0_0)_bottom/var(--d,0)_3px_no-repeat] transition-all duration-500 [--d:0]", {
								// For appearing a line when hovering
								"hover:[--d:100%]": form[item.name as keyof typeof form] === "",
								// Line sticks when something written
								"[--d:100%] hover:[--d:100%]": form[item.name as keyof typeof form] !== "",
								// TODO: Try to make this more optimizable cause' it look ugly
								"[background:linear-gradient(#477023_0_0)_bottom/var(--d,0)_3px_no-repeat]": (nickValid === true && item.name === "username") || (emailValid === true && item.name === "email") || (passValid === true && item.name === "password"),
								"[background:linear-gradient(#ff0000_0_0)_bottom/var(--d,0)_3px_no-repeat]": (nickValid === false && item.name === "username") || (emailValid === false && item.name === "email") || (passValid === false && item.name === "password"),
							})}>
							<label
								// NOTE:form[item.name as keyof FormStateType]
								className={form[item.name as keyof typeof form] === ""
									? "absolute duration-300 group-focus-within:-translate-y-6 z-0"
									: "absolute duration-300 -translate-y-6 z-0 "
								} >
								{item.label}
							</label>
							<div className="flex flex-row z-15">
								{/* BUG: JSON.parse: unexpected character at line 1 column 1 of the JSON data*/
								}
								<input
									className="outline-none w-full h-full z-20"
									type={
										item.name === "password"
											? passType
												? "password" : "text"
											: item.name
									}
									required
									minLength={item.name === 'password' ? 8 : undefined}
									id=""
									autoComplete={item.name}
									onChange={(e: React.ChangeEvent<any>) => {
										switch (item.name) {

											case "password":
												setForm({ ...form, [item.name]: e.target.value })
												if (e.target.value.trim() != "") {
													if (e.target.value.length >= 8 && e.target.value.includes("&")) setPassValid(true);
													else setPassValid(false);
												} else setPassValid(undefined);

											case "username": case "email":
												const newValue = e.target.value;
												setForm({ ...form, [item.name]: newValue });

												if (timeoutRefs.current[item.name]) {
													clearTimeout(timeoutRefs.current[item.name]);
												}
												if (newValue.trim() === "") item.name === "email" ? setEmailValid(undefined) : setNickValid(undefined);
												else {
													if (item.on_change) {
														timeoutRefs.current[item.name] = setTimeout(() => {
															item.on_change!(newValue, item.name === "email" ? setEmailValid : setNickValid);
														}, 1000);
													}
												}
										}
									}}
								/>
								{
									item.name === "password"
										?
										<div className="h-[30px] cursor-pointer flex items-center justify-center z-9">
											<button className="cursor-pointer h-full w-full"
												type="button"
												onClick={() => {
													setPassType(!passType)
												}}
											>
												{passType ? < FaEyeSlash size="17px" /> : < FaEye size="17px" />}
											</button>
										</div>
										:
										<></>
								}
							</div>
							{item.name === "username" && nickValid === false && (
								<span className="text-red-500 text-xs absolute -bottom-4 left-0">
									Username already exists
								</span>
							)}
							{item.name === "password" && passValid === false && form["password" as keyof FormStateType] !== "" && (
								<span className="text-red-500 text-xs absolute -bottom-4 left-0">
									Password must be at least 8 characters and contain special characters
								</span>
							)}
						</div >
					))
				}
				<div className="flex w-full items-center justify-center">
					<button className={roboto.className + " shadow-md h-[60px] w-[120px] text-[20px] font-stretch-125% font-medium rounded-full cursor-pointer"} type="submit">
						Sign In
					</button>
				</div>
			</form >
			<div className="cursor-pointer flex justify-center items-center gap-7">
				<button
					className="cursor-pointer shadow-sm h-[50px] w-[50px] rounded-xl flex items-center justify-center hover:bg-[#efe6de] duration-300 active:shadow-md"
					onClick={() => GitHubAuth(router)}
				>
					<FaGithub size="30px" />
				</button>

				<button
					className="cursor-pointer shadow-sm h-[50px] w-[50px] rounded-xl flex items-center justify-center hover:bg-[#efe6de] duration-300 active:shadow-md"
					onClick={() => GitHubAuth(router)}
				>
					<FcGoogle size="30px" />
				</button>
			</div>
		</>
	)
}
