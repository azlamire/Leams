import { Subs } from "./subs";
import { Default } from "./default";

import { Rubik } from 'next/font/google'

import { useStore } from "@tanstack/react-store";
import { store } from "@/shared/store";

export function LeftSide() {
	const asideOpen: boolean = useStore(store, (state) => state.aside);
	return (
		<>
			{asideOpen &&
				<aside className="w-[13%] p-2 flex flex-col h-screen shadow-sm items-center sticky block top-0 right-0 left-0 z-4">
					<>
						<Default />
						<Subs />
					</>

				</aside>
			}
		</>
	)
}
