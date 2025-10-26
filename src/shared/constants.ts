import * as z from "zod";

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

const backendLinks = z.object({
	NEXT_PUBLIC_HAS_USER_CHECK: z.string().refine(
		(url) => url.startsWith("http") || url.startsWith("https"),
		"Invalid url"
	),
	NEXT_PUBLIC_HAS_EMAIL_CHECK: z.string().refine(
		(url) => url.startsWith("http") || url.startsWith("https"),
		"Invalid url"
	),
	NEXT_PUBLIC_GITHUB_AUTH: z.string().refine(
		(url) => url.startsWith("http") || url.startsWith("https"),
		"Invalid url"
	),
	NEXT_PUBLIC_REGISTER: z.string().refine(
		(url) => url.startsWith("http") || url.startsWith("https"),
		"Invalid url"
	),
	NEXT_PUBLIC_AUTH: z.string().refine(
		(url) => url.startsWith("http") || url.startsWith("https"),
		"Invalid url"
	),
})

type Env = z.infer<typeof backendLinks>;

export const BACKEND: Env = backendLinks.parse(process.env)
