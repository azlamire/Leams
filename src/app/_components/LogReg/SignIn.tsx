import { time } from "console";
import type Email from "next-auth/providers/email";
import { Roboto } from "next/font/google";
import { useEffect, useRef, useState, type Dispatch, type FormEventHandler, type SetStateAction } from "react";
import clsx from "clsx";

type FormType = {
    name: string;
    label: string;
    type: string;
    on_change?: (value: string, hook: Dispatch<SetStateAction<boolean>>) => void;
}

type FormStateType = {
    email: string
    password: string;
    birthday: string;
    username: string;
}

const signInForm: FormType[] = [
    {name: "username", label: "Username",type:"text",
        on_change: async (value: string, hook: Dispatch<SetStateAction<boolean>>) => {
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
                hook(data.invalidUser);
            })
        }
    },
    {name: "password", label: "Password", type: "password"},
    {name: "email", label: "Email",type: "email", 
        on_change: async (value: string) => {
            const some_request = await fetch("http://127.0.0.1:8000/has_email", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({Email: value})
            })
        }
    },  
    {name : "birthday", label: "Birthday", type:"date"}, 
];

const roboto = Roboto({
    subsets: ['latin'],
  })

export function SignIn() {
    const [nickValid, setNickValid] = useState<boolean>(false)
    const [passValid, setPassValid] = useState<boolean>(false)
    const [form, setForm] = useState<FormStateType>({
        email: "",
        password: "",
        birthday: "",
        username: "",
    })

    const timeoutRefs = useRef<{[key: string]: NodeJS.Timeout}>({})

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
    return (
        <form className="flex flex-col rounded-xl w-full h-[65%] gap-7 mt-10" onSubmit={handleSubmit}>
            {
                signInForm.map((item, index) => (
                    <div key={item.name} className={clsx(
                        "relative flex gap-2 flex-col w-full mb-5 group border-b-0 [background:linear-gradient(#3b82f6_0_0)_bottom/var(--d,0)_3px_no-repeat] transition-all duration-500 [--d:0]", {
                            "hover:[--d:100%]" : form[item.name as keyof typeof form] === "",
                            "[--d:100%] hover:[--d:100%]" : form[item.name as keyof typeof form] !== "",
                            "[background:linear-gradient(#477023_0_0)_bottom/var(--d,0)_3px_no-repeat]" : nickValid === false && item.name === "username",
                            "[background:linear-gradient(#ff0000_0_0)_bottom/var(--d,0)_3px_no-repeat]" : nickValid === true && item.name === "username",
                            "[background:linear-gradient(#bb0000_0_0)_bottom/var(--d,0)_3px_no-repeat]" : passValid === false && item.name === "password",
                            "[background:linear-gradient(#477020_0_0)_bottom/var(--d,0)_3px_no-repeat]" : passValid === true && item.name === "password",
                        })}>
                        <label 
            
                        htmlFor=""
                        //form[item.name as keyof FormStateType]
                        className={form[item.name as keyof typeof form] === "" && item.name != "birthday" 
                        ? "absolute duration-300 group-focus-within:-translate-y-6 z-0" 
                        : "absolute duration-300 -translate-y-6 z-0 "}>
                            {item.label}
                        </label>
                        { 
                            item.name === "password" ?

                                <input 
                                    className="outline-none w-full h-full z-10"
                                    type="password" 
                                    required minLength={8}
                                    id="" 
                                    autoComplete={item.name}
                                    onChange={e => {
                                        console.log(e.target.value);
                                        setForm({...form, [item.name]: e.target.value})
                                        e.target.value.length >= 8 && e.target.value.includes("&") ? setPassValid(true) : setPassValid(false);
                                        console.log(passValid);
                                    }}
                                />
                                
                                :

                                <input 
                                className="outline-none w-full h-full z-10"
                                required
                                type={item.type}
                                id="" 
                                autoComplete={item.name}
                                onChange={e => {
                                    const newValue = e.target.value;
                                    setForm({...form, [item.name]: newValue});
                                    
                                    if (timeoutRefs.current[item.name]) {
                                        console.log(timeoutRefs.current[item.name]);
                                        clearTimeout(timeoutRefs.current[item.name]);
                                    }
                                    
                                    if (item.on_change && newValue.trim() !== "") {
                                        timeoutRefs.current[item.name] = setTimeout(() => {
                                            item.on_change!(newValue, setNickValid);
                                        }, 1000); 
                                    }
                                }}/>
                                
                        }
                        {item.name === "username" && nickValid === true && (
                            <span className="text-red-500 text-xs absolute -bottom-4 left-0">
                                Username already exists
                            </span>
                        )}
                        {item.name === "password" && passValid === false && form["password" as keyof FormStateType] !== "" && (
                            <span className="text-red-500 text-xs absolute -bottom-4 left-0">
                                Password must be at least 8 characters and contain an "&" character
                            </span>
                        )}
                    </div>  
                ))
            }
            <div className="flex w-full items-center justify-center">
                <button className={roboto.className + " shadow-md h-[60px] w-[120px] text-[20px] font-stretch-125% font-medium rounded-full cursor-pointer"} type="submit">
                    Submit
                </button>
            </div>
        </form>
    )
}