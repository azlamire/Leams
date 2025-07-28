import Link from "next/link";

import { CgGames } from "react-icons/cg";
import { CiChat1 } from "react-icons/ci";
import { CiMusicNote1 } from "react-icons/ci";
import { FaPaintBrush } from "react-icons/fa";
import { MdOutlineSportsEsports } from "react-icons/md";


interface NavigationItem {
    name: string;
    icon: React.ReactNode;
    href?: string;
    options?: SubNavigationItem[];
};

interface SubNavigationItem {
    name: string;
    href: string;
};


const exploreItems: NavigationItem[] = [
    {name: "All categories", icon: <CiChat1 />, href: "Categories"},
    {
        name: "Games",
        icon: <CgGames />,
        options: [
            {name: "ALL", href: "Games/ALL"},
            {name: "VALORANT", href: "Games/VALORANT"},
            {name: "CS", href: "Games/CS"},
            {name: "WOW", href: "Games/WOW"},
            {name: "VALORANT", href: "Games/VALORANT"},
        ],
    },
    {name: "Chatting", icon: <CiChat1 />, href: "Chatting"},
    {name: "Music", icon: <CiMusicNote1 />, href: "Music"},
    {name: "Creative", icon: <FaPaintBrush />, href: "Creative"},
    {name: "Esports", icon: <MdOutlineSportsEsports />, href: "Esports"},
];


export function LeftSide() { 
    return(
        <aside className="w-[12%] flex flex-col justify-between h-screen">
            <div className="h-full p-5">
                <ul className="flex flex-col justify-between gap-3 text-[20px] font-semibold">
                    {exploreItems.map((items, index) => (
                        <li key={index}>
                          {items.options ? (
                            <details>
                                <summary className="flex flex-row items-center list-none gap-5">{items.icon} {items.name}</summary>
                                {items.options.map((option, index) => (
                                    <li key={index}>
                                        <Link href={option.href}>
                                            {option.name}
                                        </Link>
                                    </li>
                                ))}
                            </details>
   
                          ) : (
                            <Link href={items.href || "#"} className="flex items-center gap-5">
                                {items.icon} {items.name}
                            </Link>
                          )}  
                        </li>
                    ))}
                </ul>
            </div>
        </aside>
    )
}