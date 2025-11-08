import type { AuthOptions } from "next-auth";
import GogleProvider from "next-auth/providers/google";

export const authConfig: AuthOptions = {
    providers: [
        GogleProvider({
            clientId: '',
            clientSecret: '',
        })
    ]
}