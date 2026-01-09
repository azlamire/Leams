"use client"

import { api } from "@/lib/api";
import Link from "next/link";
import { MAIN } from "@/shared/constants";
import { useEffect, useState, useReducer, useRef } from "react";
import { useQuery } from "@tanstack/react-query";
import { useInView } from "react-intersection-observer";
import { MainCategory } from "./category";
import { store } from "@/shared/store";
import { useStore } from "@tanstack/react-store";
export function MainStreams() {
	const [count, setCount] = useState<number>(0);
	const [links, setLinks] = useState<string[]>([])

	const testing = useRef(null);
	const { ref, inView } = useInView({
		root: testing.current,
		threshold: 1,
	});


	useEffect(() => {
		for (let i = 2; i <= count; i++) {
			api.get(MAIN.NEXT_PUBLIC_GET_STREAMS + i)
				.then(data => data.data)
				.then((data: string) => {
					setLinks(prev => [...prev, data[1]])
				})
		}
	}, [count]);

	// TODO: Make it as supposed to be
	useEffect(() => {
		if (inView) {
			setCount(num => num + 30);
		}
	}, [inView]);

	useEffect(() => {
		console.log(links)
		console.log("this is links")
	}, [links]);

	useEffect(() => { console.log(count) }, [count])

	const reg: boolean = useStore(store, (state) => state.isDemo);
	return (
		<div ref={testing} className="!overflow-y-auto h-[100%] p-5">
			<MainCategory />
			{reg &&
				<div className="flex flex-col">
					{Array(Math.ceil(count / 5)).fill(1).map((_, i) =>
						<div className="flex flex-row gap-5 w-full justify-between" key={i}>
							{links.slice(5 * i, (i + 1) * 5).map((link: string, idx) => (
								<div className="h-[300px] w-[300px]">
									<Link
										href={"/category/" + link[0].replace(/\s+/g, "")}
										key={idx}
										className="">
										<div className="relative">
											{ // TODO: Make it possible in future
												// <Image src={link[1]} loading="lazy" alt="" width="240" height="180" />}
											}
											<div className="relative z-0">
												<img
													src={link[1][1]}
													className="z-0"
													loading="lazy"
													alt=""
													width="300"
													height="160" />
											</div>
											<div className="absolute top-0 z-5 ">
												<div className="bg-[#dd3a44] m-2 text-white rounded-sm text-xs font-medium p-[2px]">
													<span className=""> LIVE </span>
												</div>
											</div>
											<div className="absolute bottom-0 right-0 z-5 text-sm text-white m-2 bg-[#00000040] pl-1 pr-1">
												<h3 className="">0 viewers</h3>
											</div>
										</div>
										<div className="flex flex-row mt-2">

											<div className="h-[40px] w-[40px] shrink-0">
												<img className="rounded-full" src={link[1][0]} />
											</div>
											<div className="flex flex-col pl-2 ">
												<p className="truncate font-medium">{link[0]}</p>
												<p className="text-sm">{link[1][2]}</p>
											</div>
										</div>
									</Link>
								</div>
							))}
						</div>
					)}
				</div>
			}
			<div ref={ref} className="h-1"></div>
		</div>
	)
}

