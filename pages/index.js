import { signIn, signOut, useSession } from 'next-auth/react';
import styles from '../styles/Home.module.css';
import React, { useState, useEffect } from 'react';

const Home = () => {
    const [currentGoogleAccessToken, setGoogleAccessToken] = useState('');
    const { data: GoogleSession } = useSession();
    console.log("AllDataFromGoogle:", GoogleSession);
    console.log("GoogleAccessToken:", GoogleSession?.user?.accessToken);
    useEffect(() => {
        if (GoogleSession) {
            // Set the Google access token when the GoogleSession object is available
            setGoogleAccessToken(GoogleSession.user.accessToken);
            
            if (currentGoogleAccessToken) {
                // Send the currentGoogleAccessToken to an endpoint
                fetch('https://uploadtoken-3l6j2umkza-uc.a.run.app', {
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
        <div className={styles.container}>
            {!GoogleSession ? (
                <div className={styles.notSignedIn}>
                    <h1>Welcome To EvoCal</h1>
                    <p>Please sign in to start the automated AI processes</p>
                    <button className={styles.signInButton} onClick={() => signIn()}>
                        Sign in
                    </button>
                </div>
            ) : (
                <main className={styles.main}>
                    <div className={styles.header}>
                        <h4>Signed in as {GoogleSession.user.name}</h4>
                        {/* show the profile image */}
                        <img src={GoogleSession.user.picture} className={styles.profileImage} />
                        <button className={styles.signOutButton} onClick={() => signOut()}>
                            Sign out
                        </button>
                    </div>
                    {/* Additional content when signed in */}
                    <p>You are signed into the system</p> {/* Added text */}

                </main>
            )}
        </div>
    );
};

export default Home;