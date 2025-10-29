// import * as z from "zod";
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

/*
 * BUG: The main problem is that Zod validation is performed in 
 * the browser, where environment variables may be undefined due to 
 * the specifics of Next.js build process with Turbopack.
 * These words are from Claude 4 because there's no articles.
 * TODO: Remain an issue in github
* */
// const backendLinks = z.object({
// 	NEXT_PUBLIC_HAS_USER_CHECK: z.string().refine(
// 		(url) => url.startsWith("http") || url.startsWith("https"),
// 		"Invalid url"
// 	),
// 	NEXT_PUBLIC_HAS_EMAIL_CHECK: z.string().refine(
// 		(url) => url.startsWith("http") || url.startsWith("https"),
// 		"Invalid url"
// 	),
// 	NEXT_PUBLIC_GITHUB_AUTH: z.string().refine(
// 		(url) => url.startsWith("http") || url.startsWith("https"),
// 		"Invalid url"
// 	),
// 	NEXT_PUBLIC_REGISTER: z.string().refine(
// 		(url) => url.startsWith("http") || url.startsWith("https"),
// 		"Invalid url"
// 	),
// 	NEXT_PUBLIC_AUTH: z.string().refine(
// 		(url) => url.startsWith("http") || url.startsWith("https"),
// 		"Invalid url"
// 	),
// })
//
// type Env = z.infer<typeof backendLinks>;
export const BACKEND = {
	HAS_USER_CHECK: process.env.NEXT_PUBLIC_HAS_USER_CHECK,
	HAS_EMAIL_CHECK: process.env.NEXT_PUBLIC_HAS_EMAIL_CHECK,
	GITHUB_AUTH: process.env.NEXT_PUBLIC_GITHUB_AUTH,
	REGISTER: process.env.NEXT_PUBLIC_REGISTER,
	AUTH: process.env.NEXT_PUBLIC_AUTH,
} as const;


