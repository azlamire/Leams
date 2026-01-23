"use client"
import { useStore } from "@tanstack/react-store";
import { store } from "@/shared/store";
import { useEffect, useState } from "react";
import { Switch } from "@mui/material";
import { Tooltip } from "@mui/material";

export function RightButtons() {


	const checked = useStore(store, (store) => store.isDemo)
	return (
		<div className="flex flex-row">
			<div>
				<Tooltip title="Demo mode">
					<Switch
						checked={checked}
						onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
							store.setState((prev) => ({ ...prev, isDemo: !store.state.isDemo }))
							console.log(store.state.isDemo)
						}
						}
					/>
				</Tooltip>
			</div>
			<div className="flex items-center justify-center">
				<button
					className="w-[100px] h-[40px] shadow-sm text-white bg-[#dd3a44] rounded-sm cursor-pointer font-semibold hover:text-[#373539] hover:text-[#373539] transition-colors text-"
					onClick={() => store.setState((prev) => ({ ...prev, openReg: true, isOpen: true }))}>
					<div >
						<span className="flex flex-row items-center justify-center gap-2">Sign In</span>
					</div>
				</button>
			</div>

			<div className="flex items-center justify-center">
				<button
					className="w-[100px] h-[40px] shadow-sm rounded-sm cursor-pointer font-semibold hover:bg-gray-50 transition-colors text-"
					onClick={() => store.setState((prev) => ({ ...prev, openReg: false, isOpen: true }))}>
					<div >
						<span className="flex flex-row items-center justify-center gap-2">Log In</span>
					</div>
				</button>
			</div>
		</div>
	)
}
