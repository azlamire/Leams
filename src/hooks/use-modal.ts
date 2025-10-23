import { useEffect } from "react";
import { store } from "@/shared/store/store"

interface UseModalOptions {
	isOpen: boolean
}

// TODO: When you need to reuse it make something with store
export function useModal({ isOpen }: UseModalOptions) {
	useEffect(() => {
		if (isOpen) {
			document.body.style.overflow = "hidden";
			const handleKeyDown = (event: KeyboardEvent) => {
				if (event.key == "Escape") {
					store.setState(prev => ({ ...prev, openReg: false }));
				}
			}
			document.addEventListener("keydown", handleKeyDown);
			return () => {
				document.removeEventListener("keydown", handleKeyDown);
			};
		}
		else if (!isOpen) {
			document.body.style.overflow = "auto";
		}
	}, [isOpen]);
}

