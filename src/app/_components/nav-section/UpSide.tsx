import TLogo from "../../../../public/kick-logo.svg"
import Image from "next/image"
import Link from "next/link";
import { FaHome } from "react-icons/fa";


import { MainNavRight } from "./right-nav/main-right";
import { useStore } from "@tanstack/react-store";
import { store } from "@/shared/store";
import { Search } from "./Search";

export function UpSide() {
	const asideOpen: boolean = useStore(store, (state) => state.aside);
	return (
		<header className="sticky block top-0 right-0 left-0 z-4">
			<nav className="w-full flex flex-row items-center shadow-xs">
				<div className="flex flex-row justify-between w-full px-4 h-[60px]">
					<div className="flex flex-row gap-5">
						<div
							className="flex items-center gap-3 "
							onClick={() => store.setState((prev) => ({ ...prev, aside: !asideOpen }))}>
							<button className="p-2 group cursor-pointer duration-300 rounded-sm hover:shadow-sm">
								<div className=" w-[18px] h-[18px] flex flex-col justify-between">
									<span
										className="bg-[#181A1B] h-[2px] w-full block transition-all 
														 duration-300 group-hover:translate-y-2
														 group-hover:rotate-45 "/>
									<span
										className="bg-[#181A1B] h-[2px] w-full block transition-all 
														 duration-300 group-hover:rotate-47 group-hover:-translate-y-0.4
														 group-hover:translate-x-0  "/>
									<span
										className="bg-[#181A1B] h-[2px] w-full block transition-all 
														 duration-300 group-hover:-translate-y-2
														 group-hover:-rotate-47 group-hover:h-[2.4px]"/>
								</div>
							</button>
						</div>
						<div className="flex justify-center items-center">
							<Link href="/">
								<FaHome size="30" />
							</Link>
						</div>
					</div>
					<Search />
					<MainNavRight />
				</div>
			</nav>
		</header >
	)
}
