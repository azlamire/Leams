"use client";
import { AnimatePresence, LayoutGroup, motion } from "motion/react";
import Portal from "@/ui/next-portal";
import { Login } from "./login-form";
import { store } from "@/shared/store";
import { SignIn } from "./signin-form";
import { useModal } from "@/hooks/use-modal";
import { useStore } from "@tanstack/react-store";
import { butRegLog } from "./constant";
import { useEffect } from "react";

export function MainLogin() {
	const isOpen: boolean = useStore(store, (state) => state.isOpen);
	useModal({ isOpen: isOpen });
	const reg: boolean = useStore(store, (state) => state.openReg);
	return (
		<Portal selector="body">
			<AnimatePresence mode="wait">
				{isOpen && (
					<motion.div
						className="fixed inset-0 w-full h-full bg-[#00000090] z-10"
						initial={{ opacity: 0 }}
						exit={{ opacity: 0 }}
						animate={{ opacity: 1 }}
						transition={{ duration: 0.3 }}
					>
						<div className="flex items-center justify-center h-full">
							<div className="relative w-[26%] bg-[#efe6de] shadow-xl rounded-lg flex text-[#373539] items-center flex-col p-5 gap-8">
								<div className="relative h-10 w-full">
									<button
										className="absolute bg-[#dd3a44] right-0 top-0 rounded-full h-[33px] w-[33px] shadow-sm flex flex-col justify-center items-center "
										onClick={() => store.setState((prev) => ({ ...prev, isOpen: false }))}
									>
										<span className="absolute bg-white h-[2.6px] w-[55%] block transition-all rotate-45 "></span>
										<span className="absolute bg-white h-[2.6px] w-[55%] block transition-all -rotate-45 "></span>
									</button>
								</div>
								<div className="h-10 w-full flex flex-row shadow-sm-b gap-10 font-bold text-[20px] border-b-3 border-gray-500 z-0 mb-5">
									<LayoutGroup>
										{butRegLog.map((item) => (
											<div key={item.name} className="relative w-[60%] flex flex-row z-20">
												<button
													className={item.className}
													onClick={item.onClick}
												>
													{item.name}
												</button>
												{item.active && (
													<motion.div
														className="z-20 absolute -bottom-[3px] w-full h-[3px] bg-sakura z-20"
														layoutId="underline"
														id="underline"
													/>
												)}
											</div>
										))}
									</LayoutGroup>
								</div>
								{reg ? <SignIn /> : <Login />}
							</div>
						</div>
					</motion.div>
				)}
			</AnimatePresence>
		</Portal>
	);
}
