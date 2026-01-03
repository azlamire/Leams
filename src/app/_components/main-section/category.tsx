import { api } from "@/lib/api";
import { MAIN } from "@/shared/constants";
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useInView } from "react-intersection-observer";
import Link from "next/link";

export function MainCategory() {
	const [links, setLinks] = useState<string[]>([])
	const { ref, inView } = useInView({
		threshold: 0.5,
	});
	useEffect(() => {
		for (let i = 0; i <= 10; i++) {
			api.get(MAIN.NEXT_PUBLIC_GET_CATEGORIES + i)
				.then(data => data.data)
				.then((data: string) => {
					setLinks(prev => [...prev, data])
				})
		}
	}, []);

	// const info = useQuery({ queryKey: ['todos'], queryFn: () => api.get(MAIN.NEXT_PUBLIC_GET_CATEGORIES) })

	return (
		<div ref={ref} className="flex flex-row w-full justify-between p-2 pl-2">
			{links.map((category, ind) => (
				<Link
					key={ind}
					className="flex flex-col g-1"
					href={"/category/" + category[0].replace(/\s+/g, "")}>
					<div className="w-[120px] h-[160px]">
						<img src={category[1]} />
					</div>
					<div>
						<h2 className="text-xs">{category[0]}</h2>
						<h2 className="text-xs">0 viewers</h2>
					</div>
				</Link>
			))}
		</div>
	)
}
