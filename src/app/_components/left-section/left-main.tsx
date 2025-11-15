import { Subs } from "./subs";
import { Default } from "./default";

import { Rubik } from 'next/font/google'

// IDK: Change the font?
const rubik = Rubik({
	subsets: ['latin'],
})

export function LeftSide() {
	return (
		<aside className={rubik.className + "w-[12%] flex flex-col h-screen shadow-sm items-center"}>
			<Default />
			<Subs />
		</aside>
	)
}
