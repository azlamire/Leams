import TLogo from "../../../../public/kick-logo.svg"
import Image from "next/image"
import Link from "next/link";

import { MainNavRight } from "./right-nav/main-right";
import { Search } from "./Search";

export function UpSide() {
	return (
		<header className="w-full flex flex-row items-center shadow-xs">
			<div className="flex flex-row justify-between w-full px-4 h-[60px]">
				<div className="flex items-center gap-3 ">
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
				<Search />
				<MainNavRight />
			</div>
		</header>
	)
}
