import { initializeApp } from
    "https://www.gstatic.com/firebasejs/12.19.0/firebase-app.js";

import {
    getAuth,
    GoogleAuthProvider,
    signInWithPopup,
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword
} from
    "https://www.gstatic.com/firebasejs/12.19.0/firebase-auth.js";


const firebaseConfig = {
    apiKey: "AIzaSyC33nE-8sz-Mvsuq9KbLYv7iLUw4sWbmD4",
    authDomain: "productivity-agent-8ad3c.firebaseapp.com",
    projectId: "productivity-agent-8ad3c",
    storageBucket: "productivity-agent-8ad3c.firebasestorage.app",
    messagingSenderId: "65707458299",
    appId: "1:65707458299:web:008c72dc8137ec979bba5e",
    measurementId: "G-80V5LMDS94"
};


const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const button = document.getElementById("google-login-button");
const errorMessage = document.getElementById("login-error");
const emailLoginForm = document.getElementById("email-login-form");
const registerForm = document.getElementById("register-form");


async function createFlaskSession(user) {
    const idToken = await user.getIdToken();

    const response = await fetch("/session-login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ idToken: idToken })
    });

    if (!response.ok) {
        throw new Error("Could not create a login session.");
    }

    window.location.href = "/";
}


// This code runs only on the login page.
if (button) {
    button.addEventListener("click", async () => {
        try {
            errorMessage.textContent = "";
            button.disabled = true;
            button.textContent = "Signing in...";

            const result = await signInWithPopup(auth, provider);
            await createFlaskSession(result.user);
        }
        catch (error) {
            console.error(error);
            errorMessage.textContent = "Google sign-in failed. Please try again.";
            button.disabled = false;
            button.textContent = "Sign in with Google";
        }
    });
}


// This code runs only on the login page.
if (emailLoginForm) {
    emailLoginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        try {
            errorMessage.textContent = "";

            const email = document.getElementById("login-email").value;
            const password = document.getElementById("login-password").value;

            const result = await signInWithEmailAndPassword(auth, email, password);
            await createFlaskSession(result.user);
        }
        catch (error) {
            console.error(error);
            errorMessage.textContent =
                "Email/password login failed. Please check your email and password.";
        }
    });
}


// This code runs only on the register page.
if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        try {
            errorMessage.textContent = "";

            const email = document.getElementById("register-email").value;
            const password = document.getElementById("register-password").value;

            const result = await createUserWithEmailAndPassword(auth, email, password);
            await createFlaskSession(result.user);
        }
        catch (error) {
            console.error(error);
            errorMessage.textContent =
                "Could not create the account. Passwords must have at least 6 characters.";
        }
    });
}