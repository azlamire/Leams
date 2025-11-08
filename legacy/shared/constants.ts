import * as z from "zod";
/*
 * BUG: The main problem is that Zod validation is performed in 
 * the browser, where environment variables may be undefined due to 
 * the specifics of Next.js build process with Turbopack.
 * These words are from Claude 4 because there's no articles.
 * TODO: Remain an issue in github
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

// TODO: Write correct variables starting with NEXT_PUBLIC
class config {
	public readonly has_user_check: string | undefined;
	public readonly has_email_check: string | undefined;
	public readonly github_auth: string | undefined;
	public readonly register: string | undefined;
	public readonly auth: string | undefined;
	constructor() {
		this.has_user_check = process.env.has_user_check as string;
		this.has_email_check = process.env.has_email_check
		this.github_auth = process.env.github_auth
		this.register = process.env.register
		this.auth = process.env.auth
	}
}
