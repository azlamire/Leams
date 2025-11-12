"use client"
import { store } from "@/shared/store";
import { useEffect } from "react";
import { api } from "@/lib/api";
import { AUTH } from "@/shared/constants";

export function ProfileUser() {
	api.get(AUTH.NEXT_PUBLIC_GET_USER)
	return (
		<div className="flex flex-row">
			<div>
				<image />
			</div>

		</div>
	)
}
