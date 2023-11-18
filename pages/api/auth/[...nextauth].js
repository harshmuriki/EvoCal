import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';

export default NextAuth({
    providers: [
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET,
            authorization: {
                params: {
                    prompt: "consent",
                    access_type: "offline",
                    response_type: "code",
                    scope: "openid profile email https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/calendar",
                },
            },
        }),
    ],
    secret: process.env.NEXTAUTH_SECRET,
    callbacks: {
        async jwt({ token, account }) {
            if (account) {
                token.id = account.id;
                token.expires_at = account.expires_at;
                token.accessToken = account.access_token;
            }
            return token;
        },
        async session({ session, token }) {
            session.user = token;
            return session;
        },
    },
});
