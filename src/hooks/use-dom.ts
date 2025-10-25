// DEPRECATED: 
import { useEffect } from "react";
import { type Dispatch, type SetStateAction } from "react";
/*
* NOTE: In NextJS you can't just use document cause'
* NextJS can't understand whether you on server side
* or client side even with "use client" doesn't work.
* But useffect hook always works on client side. That's 
* why this hook is vital. 
*/

interface stateType {
	setState: Dispatch<SetStateAction<Element | undefined>>
	tagName: string
}
/* XXX: After 4 hours I think that it'll be reused in future
 * but for now it'll use just body*/

// Good hook to setting a HTMLElement via useStates
export function useDom({ setState, tagName }: stateType) {
	useEffect(() => {
		const element = document.body;
		setState(element);
	}, []);
}
