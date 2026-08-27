// Firebase App
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js";

// Firebase Authentication
import {
    getAuth,
    GoogleAuthProvider,
    signInWithPopup,
    signOut
} from "https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js";

const firebaseConfig = {

    apiKey: "AIzaSyCPAdIPgID8VVsn5XVr9lUb38W6vXk70CI",

    authDomain: "rcti-students-jobs-porta-fea0e.firebaseapp.com",

    projectId: "rcti-students-jobs-porta-fea0e",

    storageBucket: "rcti-students-jobs-porta-fea0e.firebasestorage.app",

    messagingSenderId: "935440502386",

    appId: "1:935440502386:web:58ed8dad995a6d4672fceb"

};

const app = initializeApp(firebaseConfig);

const auth = getAuth(app);

const provider = new GoogleAuthProvider();

export {

    auth,

    provider,

    signInWithPopup,

    signOut

};