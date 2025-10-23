import { useEffect } from "react";
import { type Dispatch, type SetStateAction } from "react";
/*
* NOTE: In NextJS you can't just use document cause'
* NextJS can't understand whether you on server side
* or client side even with "use client" doesn't work.
* But useffect hook always works on client side. That's 
* why this hook is vital.
* */

// Good hook to setting a HTMLElement via useStates
export function useDom({ setState, tagName }: stateType) {
	useEffect(() => {
		const element = document.getElementsByTagName(tagName);
		setState(element);
	}, []);
}
