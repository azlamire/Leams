import { type ReactNode, useState, useEffect, useRef } from "react";
import { createPortal } from "react-dom";

type PortalType = {
	children: ReactNode;
	selector?: any;
}
/*
* NOTE: In NextJS you can't just use document cause'
* NextJS can't understand whether you on server side
* or client side even with "use client" doesn't work.
* But useffect hook always works on client side. That's 
* why this hook is vital. 
*/

const Portal = ({ children, selector = "#portal-root" }: PortalType) => {
	const [mounted, setMounted] = useState(false);
	// NOTE: Ref for saving a value even when page reloads
	const elRef = useRef<HTMLElement | null>(null);

	useEffect(() => {
		setMounted(true);
		elRef.current = document.querySelector(selector);
	}, [selector]);

	if (!mounted || !elRef.current) return null;
	return createPortal(children, elRef.current);
};

export default Portal;
