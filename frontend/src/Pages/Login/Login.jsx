// Importing the necessary modules 
import "./Login.css"; 
import { Link } from 'react-router-dom';
import styles from "./Login.module.css";
import React, { Component, Fragment, useState } from 'react' 
import GoogleBtn from '../Components/GoogleBtn/GoogleBtn';

// Creating the functional based component 
const Login = (props) => {
    // Setting the state 
    const [statusMessage, setStatusMessage] = useState(""); 

    // Creating a function for handling the login form 
    const handleSubmit = (props) => {
        // Getting the dom element 
        const email = document.getElementById("email"); 
        const password = document.getElementById("password");
        const flashMessage = document.getElementById("flashMessage"); 

        // Checking if the email address was not filed 
        if (email.value === "") {
            // Setting the flash message 
            setStatusMessage("User email required");
            flashMessage.classList.add("open"); 

            // Remove the menu after 3 seconds 
            setTimeout(() => {
                flashMessage.classList.remove("open"); 
            }, 3000)
        }

        // Checking if the password was not filled 
        else if (password.value === "") {
            // Setting the flash message 
            setStatusMessage("Password required"); 
            flashMessage.classList.add("open"); 

            // Remove the menu after 3 seconds 
            setTimeout(() => {
                flashMessage.classList.remove("open");
            }, 3000)
        }
    }

    // Rendering the login component 
    return(
        <Fragment>
            {/* Adding the flash message */}
            <div className={styles.flashMessage} id="flashMessage"> 
                <p className={styles.flashMessageText}> {statusMessage} </p>
            </div>
            <div className={styles.mainDiv}>
                
                <div className={styles.container}>
                    <div className={styles.rightDiv}> 
                        <div className={styles.div}> 
                            <p className={styles.loginText}> Log In </p>
                            <GoogleBtn InputMethod="Log In"/> 
                        </div>
                        <div> 
                            <hr/> 
                        </div>
                        <div className={styles.div}> 
                            <label className={styles.label} for="Email"> Email </label> <br /> 
                            <input type="email" id="email" placeholder='Email address...' className={styles.inputForm}/>
                        </div>

                        <div className={styles.div}> 
                            <label for="Password" className={styles.label}> Password </label> <br /> 
                            <input type="password" id="password" placeholder='Password...' className={styles.inputForm} />
                        </div>
                        <div className={styles.rememberMeDiv}> 
                            <input type="checkbox" className={styles.checkbox}/> 
                            <label for="rememberme" className={styles.label}> Remember me </label>
                        </div>
                        <div className={styles.div}>
                            <button onClick={handleSubmit} className={styles.loginBtn}> Login </button>
                        </div>

                        <div className={styles.hrLine}> 
                            <hr/> 
                        </div>

                        <div className={styles.dontHaveAnAccount}> 
                            <p> Don't have an account ?</p>
                            <Link to="/register" className={styles.signUpBtn}> Signup </Link>
                        </div>

                    </div>
                </div>

            </div>
        </Fragment>
    )
}

// Exporting the login component 
export default Login; 