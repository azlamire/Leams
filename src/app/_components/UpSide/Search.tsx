import { FaSearch } from "react-icons/fa";

export function Search() {
    return (
        <div className="flex justify-center items-center">
            <div className="relative h-[40px] w-[400px] flex gap-3 rounded-full ">
                <div className="absolute left-3 top-2.5 flex flex-row gap-4">
                    <FaSearch  />
                </div>
                <input className="px-10 w-full h-full shadow-sm rounded-full focus:border-2 border-white duration-100 outline-none focus:border-gray-700 " placeholder="Search" type="search" />
            </div>
        </div> 
    )
}