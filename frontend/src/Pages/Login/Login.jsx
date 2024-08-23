// Importing the necessary modules 
import "./Login.css"; 
import { Link } from 'react-router-dom';
import styles from "./Login.module.css";
import React, { Component, Fragment, useState, useContext } from 'react' 
import GoogleBtn from '../Components/GoogleBtn/GoogleBtn';
import axios from "axios";
import { AuthContext } from "../../Auth/AuthContext";

// Creating the functional based component 
const Login = (props) => {
    // Accessing the Auth context 
    const { setToken } = useContext(AuthContext); 

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

        // else if all field was filled 
        else {
            // Get all the user's login data 
            let userData = JSON.stringify({
                "emailAddress": email.value, 
                "password": password.value,
            }); 

            // Setting the axios headers config 
            const config = {
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    "x-auth-token": "null", 
                },
            }

            // Setting the remote server ip address 
            const serverIpAddress = `http://localhost:3001/login`; 

            // Making a post request to the server ip address 
            axios.post(serverIpAddress, userData, config) 
            .then((responseData) => {
                if (responseData.data.status === "success") {
                    // Setting the state 
                    setStatusMessage("Welcome..."); 
                    flashMessage.classList.add("open"); 

                    // Remove the menu after 3 seconds 
                    setTimeout(() => {
                        flashMessage.classList.remove("open");
                    }, 3000)

                    // Delay the login duration for 3 seconds 
                    setTimeout(() => {
                        // Saving the x-auth token into the local storage memory
                        localStorage.setItem('x-auth-token', responseData.data['x-auth-token']);
                        setToken(responseData.data['x-auth-token']);

                        // Redirect the user to the dashboard page 
                        window.location.href = "/dashboard"; 
                    }, 3000)
                    
                }

                // Else if the data from the request was an error 
                else {
                    setStatusMessage("Invalid email or password");
                    flashMessage.classList.add("open"); 

                    // Remove the menu after 3 seconds 
                    setTimeout(() => {
                        flashMessage.classList.remove("open");
                    }, 3000) 
                }
            })
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