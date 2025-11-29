"use client"
import { store } from "@/shared/store";
import { useEffect } from "react";
import { api } from "@/lib/api";
import { MAIN } from "@/shared/constants";

export function ProfileUser() {
	useEffect(() => {
		api.get(MAIN.NEXT_PUBLIC_GET_USER)
	}, []);
	return (
		<div className="flex flex-row">
			<div>
				<img />
			</div>

		</div>
	)
}
