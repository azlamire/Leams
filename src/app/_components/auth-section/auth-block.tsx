"use client";
import { AnimatePresence, LayoutGroup, motion } from "motion/react";
import Portal from "@/ui/next-portal";
import { Login } from "./login-form";
import { store } from "@/shared/store";
import { SignIn } from "./signin-form";
import { useModal } from "@/hooks/use-modal";
import { useStore } from "@tanstack/react-store";
import { butRegLog } from "./constant";

export function MainLogin() {
	const isLogin = useStore(store, (state) => state.isLogin);
	const isAuth: boolean = useStore(store, (state) => state.openReg);

	useModal({ isOpen: isAuth });

	return (
		<Portal selector="body">
			<AnimatePresence mode="wait">
				{isAuth && (
					<motion.div
						className="fixed inset-0 w-full h-full bg-[#00000090]"
						initial={{ opacity: 0 }}
						exit={{ opacity: 0 }}
						animate={{ opacity: 1 }}
						transition={{ duration: 0.3 }}
					>
						<div className="flex items-center justify-center h-full">
							<div className="relative w-[26%] bg-[#efe6de] shadow-xl rounded-lg flex text-[#373539] items-center flex-col p-5 gap-8">
								<div className="relative h-10 w-full">
									<button
										className="absolute bg-neutral-100 right-0 top-0 rounded-full h-[30px] w-[30px] shadow-xl flex flex-col justify-center items-center"
										onClick={() => store.setState((prev) => ({ ...prev, openReg: false }))}
									>
										<span className="bg-[#181A1B] h-[4px] w-full block transition-all"></span>
									</button>
								</div>
								<div className="h-10 w-full flex flex-row shadow-sm-b gap-10 font-bold text-[20px] border-b-3 border-gray-500 z-0 mb-5">
									<LayoutGroup>
										{butRegLog.map((item) => (
											<div key={item.name} className="relative w-[60%] flex flex-row">
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
			</AnimatePresence>
		</Portal>
	);
}
