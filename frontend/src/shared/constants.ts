/*
* NOTE:Using a zod much better than using usual class
* cause' ts lives in only in complilation stage not in runtime
* but zod does.
* TL;DR; zod is more reliable than just ts
*/
// NOTE: as in backend part(BaseSettings) it's just more secure
/* NOTE: IDK really why developers doesn't write about such thing:
 * https://dev.to/schead/ensuring-environment-variable-integrity-with-zod-in-typescript-3di5/
 */

// TODO: Make a function for checking on undefined, OK :)?
export const BACKEND = {
	NEXT_PUBLIC_HAS_USER_CHECK: process.env.NEXT_PUBLIC_HAS_USER_CHECK as string,
	NEXT_PUBLIC_HAS_EMAIL_CHECK: process.env.NEXT_PUBLIC_HAS_EMAIL_CHECK as string,
	NEXT_PUBLIC_GITHUB_AUTH: process.env.NEXT_PUBLIC_GITHUB_AUTH as string,
	NEXT_PUBLIC_REGISTER: process.env.NEXT_PUBLIC_REGISTER as string,
	NEXT_PUBLIC_AUTH: process.env.NEXT_PUBLIC_REGISTER as string,
} as const

export const AUTH = {
	NEXT_PUBLIC_AUTH_TOKEN: process.env.NEXT_PUBLIC_AUTH_TOKEN as string,
} as const 
