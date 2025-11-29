"use client"

import { api } from "@/lib/api";
import Link from "next/link";
import { MAIN } from "@/shared/constants";
import { useEffect, useState, useReducer } from "react";
import { useQuery } from "@tanstack/react-query";
import { useInView } from "react-intersection-observer";
import Image from "next/image";

export default function Categories() {
	const [count, setCount] = useState<number>(0);
	const [links, setLinks] = useState<string[]>([])

	const { ref, inView } = useInView({
		threshold: 1,
	});


	useEffect(() => {
		for (let i = 2; i <= count; i++) {
			api.get(MAIN.NEXT_PUBLIC_GET_CATEGORIES + i)
				.then(data => data.data)
				.then((data: string) => {
					setLinks(prev => [...prev, data])
				})
		}
	}, [count]);

	// TODO: Make it as supposed to be
	useEffect(() => {
		if (inView) {
			setCount(num => num + 31);
		}
	}, [inView]);

	return (
		<div className="w-full">
			<div>

			</div>
			<div ref={ref} className="grid grid-cols-7 gap-10">
				{links.map((link, idx) => (
					<div className="h-[240px] w-[140px]">
						<Link
							href={"/category/" + link[0].replace(/\s+/g, "")}
							key={idx}>
							<div>
								{ // TODO: Make it possible in future
									// <Image src={link[1]} loading="lazy" alt="" width="240" height="180" />}
								}
								<img
									src={link[1]}
									loading="lazy"
									alt=""
									width="240"
									height="180" />
							</div>
							<div>
								<h2>{link[0]}</h2>
								<h3>0 viewers</h3>
							</div>
						</Link>
					</div>
				))}
			</div>
		</div>
	)
}
