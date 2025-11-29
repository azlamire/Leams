import { api } from "@/lib/api";
import { MAIN } from "@/shared/constants";
import { FaUserFriends } from "react-icons/fa";

// XTODO: I really don't like this make with s3
export function Subs() {
	const getSubs = api.get(MAIN.NEXT_PUBLIC_GET_SUBS)
		.then(data => console.log(data))
	return (
		<div className="w-[80%] border-t-1 pr-5 pt-5 pb-5 pl-1">
			<h1 className="flex flex-row items-center gap-3">
				<FaUserFriends size="20" /> Subscriptions
			</h1>
			<div className="pl-5">
				getSubs.
			</div>
		</div>
	)
}
