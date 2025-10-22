"use client"
import { AnimatePresence, LayoutGroup, motion } from "motion/react";
import cslx from "clsx"; import { createPortal } from "react-dom"; import { Login } from "./login-form";
import { SignIn } from "./signin-form";
import { store } from "@/shared/store/store";
import { useStore } from "@tanstack/react-store";
import { useModal } from "@/hooks/use-modal";

export function MainLogin() {
	const isLogin = useStore(store, (state) => state.isLogin);
	const opened: boolean = useStore(store, (state) => state.openReg);
	useModal({
		isOpen: opened
	})
	return (
		<>
			{createPortal(
				<AnimatePresence mode="wait">
					{opened && (
						<motion.div
							className="fixed inset-0 w-full h-full bg-[#00000090]"
							initial={{ opacity: 0 }}
							exit={{ opacity: 0 }}
							animate={{ opacity: 1 }}
							transition={{ duration: 0.3 }}>
							<div className="flex items-center justify-center h-[100%]">
								<div className="relative w-[26%] bg-[#efe6de] shadow-xl rounded-lg flex text-[#373539] items-center flex-col p-5 gap-8">
									<div className="relative h-10 w-full">
										<button
											className="absolute bg-neutral-100 right-0 top-0 rounded-full h-[30px] w-[30px] shadow-xl flex flex-col justify-center items-center 
                                        transition-all duration-300 hover:bg-gray-200 focus:bg-gray-400"
											onClick={() => store.setState(prev => ({ ...prev, openReg: false }))}>
											<span className="bg-[#181A1B] h-[4px] w-[100%] block transition-all 
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
									{isLogin ? <Login /> : <SignIn />}

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
