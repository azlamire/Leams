import { type Dispatch, type SetStateAction } from "react";

type FormLoginType = {
	name: string;
	label: string;
	type: string;
	on_change?: (value: string) => void;
}

type FormType = {
	name: string;
	label: string;
	type: string;
	on_change?: (value: string, hook: Dispatch<SetStateAction<boolean | undefined>>) => void;
}

type FormStateType = {
	username: string;
	password: string;
	email: string
}


type FormLoginStateType = {
	username: string
	password: string;
}

type RegLogButtsType = {
	name: string;
	active: boolean;
	onClick: () => void;
	className: string;
}

export type { FormType, FormLoginStateType, FormStateType, FormLoginType, RegLogButtsType }
