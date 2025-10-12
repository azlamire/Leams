"use client"
import { createPortal } from "react-dom";
import { useState, type FormEventHandler } from "react";
import { type Dispatch, type SetStateAction } from "react";
import { Roboto } from "next/font/google";
import { signIn } from "next-auth/react";
import clsx from "clsx";

type FormLoginType = {
    name: string;
    label: string;
    type: string;
    on_change?: (value: string ) => void;
}

type FormLoginStateType = {
    user_email: string
    password: string;
}

const roboto = Roboto({
    subsets: ['latin'],
  })

const logInForm: FormLoginType[] = [
    {name: "user_email", label: "Username",type:"text",
        on_change: async (value: string) => {
            const some_request = await fetch("http://127.0.0.1:8000/has_user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({nickname: value})
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                console.log(data.invalidUser);
            })
        }
    },
    {name: "password", label: "Password", type: "password"},
];

export function Login() {
    const [form, setForm] = useState<FormLoginStateType>({
        user_email: "",
        password: "",
    })
    const handleSubmit: FormEventHandler<HTMLFormElement> = async (e) => {
        console.log("Form submitted", form);
        e.preventDefault();
        const response = await fetch("http://127.0.0.1:8000/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(form)
        })
        const Content = await response.json();
        console.log(Content);
    }
    return(
        <form className="flex flex-col rounded-xl w-full h-[65%] gap-7 mt-10" onSubmit={handleSubmit}>
            {logInForm.map((item,index) => (
                <div key={item.name} className="relative border-2 flex gap-2 flex-col w-full mb-5 group border-b-0 [background:linear-gradient(#3b82f6_0_0)_bottom/var(--d,0)_3px_no-repeat] transition-all duration-500 [--d:0]">
                    <label 
                    htmlFor=""
                    //form[item.name as keyof FormStateType]
                    className={form[item.name as keyof typeof form] === "" && item.name != "birthday" 
                    ? "absolute duration-300 group-focus-within:-translate-y-6 z-0" 
                    : "absolute duration-300 -translate-y-6 z-0 "}>
                        {item.label}
                    </label>
                    <input 
                        className="outline-none w-full h-full z-10"
                        required
                        type={item.type}
                        id="" 
                        autoComplete={item.name}
                        onChange={e => {
                            const newValue = e.target.value;
                            setForm({...form, [item.name]: newValue});
                    }}/>
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
