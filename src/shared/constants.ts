/*
* NOTE:Using a zod much better than using usual class
* cause' ts lives in only in complilation stage not in runtime
* but zod does.
* TL;DR; zod is more reliable than just ts
*/
// NOTE: as in backend part(BaseSettings) it's just more secure
import * as z from "zod";
const backendLinks = z.object({
	HAS_USER_CHECK: z.string(),
})

export const BACKEND = backendLinks.parse(process.env)
