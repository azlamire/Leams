import { Roboto } from "next/font/google";
import { useRef, useState, type Dispatch, type FormEventHandler, type SetStateAction } from "react";
import { useRouter } from 'next/navigation'
import clsx from "clsx";
import { FaGithub } from "react-icons/fa";
import { FcGoogle } from "react-icons/fc";
import { FaEye } from "react-icons/fa";
import { FaEyeSlash } from "react-icons/fa6";

type FormType = {
	name: string;
	label: string;
	type: string;
	on_change?: (value: string, hook: Dispatch<SetStateAction<boolean | undefined>>) => void;
}

type FormStateType = {
	username: string;
	password: string;
	email: string
}

const signInForm: FormType[] = [
	{
		name: "username", label: "Username", type: "text",
		on_change: async (value: string, hook: Dispatch<SetStateAction<boolean | undefined>>) => {
			const some_request = await fetch("http://127.0.0.1:8000/has_user", {
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

const roboto = Roboto({
	subsets: ['latin'],
})

export function SignIn() {
	const router = useRouter()
	// NOTE: idk is it really worth to make mutliple or remain the big one
	const [nickValid, setNickValid] = useState<boolean | undefined>(undefined)
	const [passValid, setPassValid] = useState<boolean | undefined>(undefined)
	const [passType, setPassType] = useState<boolean>(true)
	const [emailValid, setEmailValid] = useState<boolean | undefined>(undefined)
	const [form, setForm] = useState<FormStateType>({
		username: "",
		password: "",
		email: "",
	})

	const timeoutRefs = useRef<{ [key: string]: NodeJS.Timeout }>({})

	const handleSubmit: FormEventHandler<HTMLFormElement> = async (e) => {
		console.log("Form submitted", form);
		e.preventDefault();
		const response = await fetch("http://127.0.0.1:8000/register", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(form)
		})
		const Content = await response.json();
		console.log(Content);
	}

	const GitHubAuth = async () => {
		const response = await fetch("http://127.0.0.1:8000/auth/github", {
			method: "GET",
			headers: {
				"Content-Type": "application/json"
			},
		})
		const Content = await response.json();
		router.push(Content)
	}

	return (
		<>
			<form className="flex flex-col rounded-xl w-full h-[65%] gap-7" onSubmit={handleSubmit}>
				{
					signInForm.map((item, index) => (
						<div key={item.name} className={
							clsx(
								"relative flex gap-2 flex-col w-full mb-5 group border-b-0 [background:linear-gradient(#3b82f6_0_0)_bottom/var(--d,0)_3px_no-repeat] transition-all duration-500 [--d:0]", {
								// For appearing a line when hovering
								"hover:[--d:100%]": form[item.name as keyof typeof form] === "",
								// Line sticks when something written
								"[--d:100%] hover:[--d:100%]": form[item.name as keyof typeof form] !== "",
								// TODO: Try to make this more optimizable cause' it look ugly
								"[background:linear-gradient(#477023_0_0)_bottom/var(--d,0)_3px_no-repeat]": (nickValid === false && item.name === "username") || (emailValid === false && item.name === "email") || (passValid === false && item.name === "password"),
								"[background:linear-gradient(#ff0000_0_0)_bottom/var(--d,0)_3px_no-repeat]": (nickValid === false && item.name === "username") || (emailValid === false && item.name === "email") || (passValid === false && item.name === "password"),
							})}>
							<label
								//form[item.name as keyof FormStateType]
								className={form[item.name as keyof typeof form] === ""
									? "absolute duration-300 group-focus-within:-translate-y-6 z-0"
									: "absolute duration-300 -translate-y-6 z-0 "
								} >
								{item.label}
							</label>
							<div className="flex flex-row">
								<input
									className="outline-none w-full h-full z-10"
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
												e.target.value.length >= 8 && e.target.value.includes("&") && e.target.value != "" ? setPassValid(true) : setPassValid(false);
											case "username": case "email":
												const newValue = e.target.value;
												setForm({ ...form, [item.name]: newValue });

												if (timeoutRefs.current[item.name]) {
													console.log(timeoutRefs.current[item.name]);
													clearTimeout(timeoutRefs.current[item.name]);
												}

												if (item.on_change && newValue.trim() !== "") {
													timeoutRefs.current[item.name] = setTimeout(() => {
														item.on_change!(newValue, item.name === "email" ? setNickValid : setEmailValid);
													}, 1000);
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
							{item.name === "username" && nickValid === true && (
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
					onClick={GitHubAuth}
				>
					<FaGithub size="30px" />
				</button>

				<button
					className="cursor-pointer shadow-sm h-[50px] w-[50px] rounded-xl flex items-center justify-center hover:bg-[#efe6de] duration-300 active:shadow-md"
					onClick={GitHubAuth}
				>
					<FcGoogle size="30px" />
				</button>
			</div>
		</>
	)
}
