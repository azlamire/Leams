import { useStore } from "@tanstack/react-store";
import { Rubik } from "next/font/google";
import { store } from "@/shared/store";
import { Default } from "./default";
import { Subs } from "./subs";

export function LeftSide() {
	const asideOpen: boolean = useStore(store, (state) => state.aside);
	return (
		<>
			{asideOpen && (
				<aside className="w-[13%] p-2 flex flex-col h-screen shadow-sm items-center sticky block top-0 right-0 left-0 z-4">
					<>
						<Default />
						<Subs />
					</>
				</aside>
			)}
		</>
	);
}
