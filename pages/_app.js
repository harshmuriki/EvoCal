require('../styles/globals.css');
const { SessionProvider } = require('next-auth/react');

function App({ Component, pageProps: { session, ...pageProps } }) {
    return (
        <SessionProvider session={session}>
            <Component {...pageProps} />
        </SessionProvider>
    )
}

module.exports = App;
