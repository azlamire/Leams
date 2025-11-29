import { api } from "@/lib/api";
import { MAIN } from "@/shared/constants";
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useInView } from "react-intersection-observer";

export function Categories() {
	let num = 0;
	const [test, setTest] = useState(null);
	const { ref, inView } = useInView({
		threshold: 0.5, // процент видимости элемента
	});
	useEffect(() => {
	});

	// TODO: Make it as supposed to be
	const info = useQuery({
		queryKey: ['todos'],
		queryFn: () => api.get(MAIN.NEXT_PUBLIC_GET_CATEGORIES)
	})

	return (
		<div ref={ref}>
			{inView ? 'Я в зоне видимости!' : 'Меня не видно'}
		</div>
	)
}
