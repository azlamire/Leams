"use client"
import { store } from "@/shared/store/test";
export function SignIn() {
	return (
		<div className="flex flex-row">
			<div className="flex items-center justify-center">
				<button
					className="w-[100px] h-[40px] shadow-sm text-white bg-[#dd3a44] rounded-sm cursor-pointer font-semibold hover:text-[#373539] hover:text-[#373539] transition-colors text-"
					onClick={() => {
						store.setState({ openReg: true })
						console.log(store.state.openReg)
					}}>
					<div >
						<span className="flex flex-row items-center justify-center gap-2">Sign In</span>
					</div>
				</button>
			</div>

			<div className="flex items-center justify-center">
				<button
					className="w-[100px] h-[40px] shadow-sm rounded-sm cursor-pointer font-semibold hover:bg-gray-50 transition-colors text-">
					<div >
						<span className="flex flex-row items-center justify-center gap-2">Log In</span>
					</div>
				</button>
			</div>
		</div>
	)
}
