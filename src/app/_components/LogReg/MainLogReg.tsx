"use client"
import { createPortal } from "react-dom";
import { store } from "@/shared/store/test";
import { useStore } from "@tanstack/react-store";
import { useEffect, useState } from "react";
import { SignIn } from "./SignIn";
import cslx from "clsx";
import { Login } from "./Login";
import { AnimatePresence, LayoutGroup, motion } from "motion/react";



type RegLogButtsType = {
    name: string;
    active: boolean;
    onClick: () => void;
    className: string;
}

const underline: React.CSSProperties = {
    position: "absolute",
    bottom: -2,
    left: 0,
    right: 0,
    height: 2,
    background: "var(--accent)",
}



export function MainLogin() {
    const isLogin = useStore(store, (state) => state.isLogin);
    const [testing, setTesting] = useState(false)
    const opened: boolean = useStore(store, (state) => state.openReg);
    const butRegLog: RegLogButtsType[] = [
        {name: "Log In", active: isLogin, onClick: () => store.setState(prev => ({...prev, isReg: false, isLogin: true})), className : cslx("cursor-pointer", {
            "border-b-0" : isLogin,
    
        })},
        {name: "Sign Up",active: !isLogin, onClick: () => store.setState(prev => ({...prev, isReg: true, isLogin: false})), className : cslx("cursor-pointer ", {
            "border-b-0" : !isLogin,

        })},
    ]
    useEffect(() => {
        if (opened) {
            document.body.style.overflow = "hidden";
            const handleKeyDown = (event: KeyboardEvent) => {
                if (event.key == "Escape") {
                    store.setState(prev => ({...prev, openReg: false }));
                }
            }
            document.addEventListener("keydown", handleKeyDown);
            return () => {
                document.removeEventListener("keydown", handleKeyDown);
            };
        }
        else if (!opened){
            document.body.style.overflow = "auto";
        }
    }, [opened]);
    return(
        <>
            {createPortal(
                <AnimatePresence mode="wait">
                    {opened && (
                        <motion.div 
                        className="fixed inset-0 w-full h-full bg-[#00000090]"
                        initial={{opacity: 0}}
                        exit={{opacity: 0}}
                        animate={{opacity: 1}}
                        transition={{duration: 0.3}}>
                            <div className="flex items-center justify-center h-full">
                                <div className="relative w-[26%] bg-[#111b2fc0] shadow-xl rounded-lg flex text-bamble items-center flex-col p-5 gap-8">
                                    <div className="relative h-10 w-full">
                                        <button 
                                        className="absolute bg-neutral-100 right-0 top-0 rounded-full h-[30px] w-[30px] shadow-xl flex flex-col justify-center items-center 
                                        transition-all duration-300 hover:bg-gray-200 focus:bg-gray-400"
                                        onClick={() => store.setState(prev => ({...prev, openReg: false}))}> 
                                            <span 
                                            className="bg-[#181A1B] h-[4px] w-[100%] block transition-all 
                                            duration-300 rotate-50 translate-y-[3px]"></span>
                                            <span 
                                            className="bg-[#181A1B] h-[4px] w-[100%] block transition-all 
                                            duration-300 rotate-132 -translate-y-[3px]"></span>
                                        </button>
                                    </div>
                                    <div className="h-10 w-full flex flex-row shadow-sm-b gap-10 font-bold text-[20px] border-b-3 border-gray-500 z-0 mb-5">
                                        <LayoutGroup>
                                            {butRegLog.map((item, index) => (
                                                <div key={item.name} className="relative w-60% flex flex-row">
                                                    <button
                                                        className={item.className}
                                                        onClick={item.onClick}
                                                    >
                                                        {item.name}
                                                    </button>
                                                    {item.active && (
                                                        <motion.div
                                                            className="z-20 absolute -bottom-[3px] w-full h-[3px] bg-sakura"
                                                            layoutId="underline"
                                                            id="underline"
                                                            
                                                        />
                                                    )}
                                                </div>
                                            ))}
                                        </LayoutGroup>
                                    </div>
                                    { isLogin ? <Login /> : <SignIn /> }
                                    
                                </div>
                            </div>
                        </motion.div>
                    )}
                    </AnimatePresence>,
                document.body
            )}
        </>
    )
}
