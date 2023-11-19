import { signIn, signOut, useSession } from 'next-auth/react';
import styles from '../styles/Home.module.css';
import React, { useState, useEffect } from 'react';

const Home = () => {
    const [currentGoogleAccessToken, setGoogleAccessToken] = useState('');
    const { data: GoogleSession } = useSession();
    const [isDarkMode, setIsDarkMode] = useState(false);

    // console.log("AllDataFromGoogle:", GoogleSession);
    // console.log("GoogleAccessToken:", GoogleSession?.user?.accessToken);
    const toggleDarkMode = () => {
        setIsDarkMode(prevMode => !prevMode);
    };
    useEffect(() => {
        if (GoogleSession) {
            // Set the Google access token when the GoogleSession object is available
            setGoogleAccessToken(GoogleSession.user.accessToken);

            if (currentGoogleAccessToken) {
                // Send the currentGoogleAccessToken to an endpoint
                fetch('https://uploadtoken-3l6j2umkza-uc.a.run.app', {
                    mode: 'no-cors',
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ accessToken: currentGoogleAccessToken })
                })
                    .then(response => {
                        // Handle the response
                    })
                    .catch(error => {
                        // Handle the error
                    });
            }
        }
    }, [GoogleSession, currentGoogleAccessToken]);

    return (
        <div className={`min-h-screen ${isDarkMode ? 'bg-primary text-primary' : 'bg-white text-black'}`}>
            <div class="flex items-center justify-center h-screen">
                <div class="w-1/2 h-1/2">
                    <div className="container md bg-gray-300 text-black py-10 px-5 text-4xl rounded-3xl">
                        <p className="mt-10">Welcome To EvoCal!!</p>
                    </div>
                    <div className="container md bg-gray-200 text-black p-5 text-xl rounded-3xl mt-1 mb-10">
                        A tool automatically add events from Gmail to Google Calendar
                    </div>
                    <div className="container lg flex items-center justify-center">
                        {!GoogleSession ? (
                            <div className="flex flex-col items-center">
                                <div className="container md bg-gray-300 text-black p-5 text-xl rounded-3xl ${isDarkMode ? 'bg-primary text-primary' : 'bg-white text-black'}">
                                    Please sign in to start the automated AI processes
                                </div>
                                <button className={`inline-block mt-4 bg-green-400 text-white p-4 text-xl flex items-center rounded-3xl`} onClick={() => signIn()}>
                                    Sign in
                                </button>
                            </div>
                        ) : (
                            <main className={styles.main}>
                                <div className="container md bg-gray-200 text-black p-2 text-mg rounded-3xl mb-5">
                                    Your Email is subscribed to our service
                                </div>
                                <div className="flex items-center">
                                    <img src={GoogleSession.user.picture} className="rounded-3xl w-auto h-auto mr-4 mb-4" />
                                    <div className="flex flex-col flex items-center">
                                        <h4 className="text-center w-full">
                                            <span style={{ fontWeight: "bold" }}>
                                                Welcome,<br />
                                                {GoogleSession.user.name}{" "}
                                                <span style={{ fontSize: "1.5em" }}>{String.fromCharCode(0x263A)}</span>:
                                            </span>
                                        </h4>
                                        <button className={`inline-block w-auto md p-1 bg-gray-300 rounded-3xl mb-4 ${styles.signOutButton}`} onClick={() => signOut()}>
                                            Sign out
                                        </button>
                                    </div>
                                </div>
                                {/* <button className={`inline-block bg-gray-400 rounded-3xl py-2 px-4 `} onClick={toggleDarkMode}>
                                    Toggle Theme
                                </button> */}
                            </main>
                        )}
                    </div>
                </div>
            </div >
        </div >
    );
};

export default Home;