import Link from "next/link";

import { TbCategoryPlus } from "react-icons/tb";
import { MdOutlineSubscriptions } from "react-icons/md";


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


/*
	TODO: If a person isn't authenticated then he will have
	the list replacing subscriptions that shows the most popular 
	streamers in own category
*/

const exploreItems: NavigationItem[] = [

];
export function Default() {
	return (
		<div className="h-auto p-5">
			<ul className={"flex flex-col justify-between text-[16px]"}>
				<li>
					<Link href="/category" className="flex items-center gap-3 rounded-[10px] p-2">
						<TbCategoryPlus size="20px" /> Categories
					</Link>
				</li>
				<li>
					<Link href="Subs" className="flex items-center gap-3 mt-2 rounded-[10px] p-2">
						<MdOutlineSubscriptions size="20px" /> Subscriptions
					</Link>
				</li>
			</ul>
		</div>
	)
}
