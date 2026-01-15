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

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['streams', count],
    queryFn:  () => api.get(`/streams/${count}`),
  });
	const testing = useRef(null);
	const { ref, inView } = useInView({
		root: testing.current,
		threshold: 1,
	});


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

