"use client"
import { createPortal } from "react-dom";
import { store } from "@/shared/store/test";
import { useStore } from "@tanstack/react-store";
import { useEffect } from "react";
import { SignIn } from "./SignIn";
import { opendir } from "fs";

export function MainLogin() {
    const opened: boolean = useStore(store, (state) => state.openReg);
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
            {opened && createPortal(
                <div className="fixed inset-0 w-full h-full bg-[#00000090] flex items-center justify-center">
                    <div className="relative h-[70%] w-[30%] bg-white shadow-xl rounded-lg flex items-center flex-col p-5 gap-8">
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
                        <div className="h-10 w-full flex flex-row border-b-2 gap-10 font-bold text-[20px]">
                            <button className="cursor-pointer text-[#181A1B] border-b-2 focus:border-[#181A1B]">
                                Log In
                            </button>
                            <button className="cursor-pointer text-[#181A1B] border-b-2 focus:border-[#181A1B]">
                                Sign Up
                            </button>
                        </div>
                        <SignIn />
                        <div>
                            
                        </div>
                    </div>
                </div>,
                document.body
            )}
        </>
    )
}