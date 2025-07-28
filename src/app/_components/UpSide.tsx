import TLogo from "../../../public/kick-logo.svg"
import Image from "next/image"
import Link from "next/link";

import { FaSearch } from "react-icons/fa";

export function UpSide() {
    return (
        <header className="w-full flex flex-row items-center shadow-xs ">
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
                    <Link href="/">
                        <Image src={TLogo} alt="Logo" width={120} height={40} priority />
                    </Link>
                </div>
                <div className="flex justify-center items-center">
                    <div className="relative h-[40px] w-[400px] flex gap-3 border-2 border-gray-700 rounded-full">
                        <div className="absolute left-3 top-2.5 flex flex-row gap-4">
                            <FaSearch  />
                        </div>
                        <input className="px-10 w-full h-full shadow-sm rounded-full" placeholder="Search" type="search" />
                    </div>
                </div>    
                <div>
                    <button>

                    </button>
                    <button>

                    </button>
                </div>
            </div>
        </header>
    )
}