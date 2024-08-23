// Importing the necessary modules 
import "./Register.css"; 
import axios from 'axios'; 
import React, { Fragment, useState } from 'react'; 
import styles from "./Register.module.css"; 
import { Link } from 'react-router-dom';
import GoogleBtn from '../Components/GoogleBtn/GoogleBtn';

// Creating the functional based component 
const Register = (props) => {
    // Setting the state 
    const [statusMessage, setStatusMessage] = useState("User registered"); 

    // Creating a function for handling the submit button 
    const handleSubmit =() => {
        // Getting the dom elements 
        const fullname = document.getElementById("fullname"); 
        const email = document.getElementById("email"); 
        const password = document.getElementById("password"); 
        const confirmPassword = document.getElementById("confirmPassword"); 
        const flashMessage = document.getElementById("flashMessage");

        // Checking if the fields are filled 
        if (fullname.value === "") {
            setStatusMessage("Fullname required");
            flashMessage.classList.add("open"); 
            
            // Remove the menu after 3 seconds 
            setTimeout(() => {
                flashMessage.classList.remove('open');
            }, 3000)
        }

        else if (email.value === "") {
            setStatusMessage("Email address required");
            flashMessage.classList.add('open'); 

            // Remove the menu after 3 seconds 
            setTimeout(() => {
                flashMessage.classList.remove('open');
            }, 3000)
        }

        else if (password.value === "") {
            setStatusMessage("Password required")
            flashMessage.classList.add('open'); 

            // Remove the menu after 3 seconds 
            setTimeout(() => {
                flashMessage.classList.remove('open');
            }, 3000)
        }

        else if (confirmPassword.value === "") {
            setStatusMessage("Confirm password field is required"); 
            flashMessage.classList.add('open'); 

            // Remove the menu after 3 seconds 
            setTimeout(() => {
                flashMessage.classList.remove('open');
            }, 3000)
        }

        else if (password.value !== confirmPassword.value) {
            setStatusMessage("Passwords are not correct")
            flashMessage.classList.add('open'); 

            // Remove the menu after 3 seconds 
            setTimeout(() => {
                flashMessage.classList.remove('open');
            }, 3000)
        }

        else {
            // Get all the user's data 
            let userData = JSON.stringify({
                "fullname": fullname.value,
                "emailAddress": email.value, 
                "password": password.value
            })

            // Setting the headers configuration 
            const config = {
                headers: {
                        'Content-Type': 'application/json; charset=UTF-8',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'POST',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        "x-auth-token": "null", 
                    },
            };

            // Setting the remote server ip address 
            const serverIpAddress = `http://localhost:3001/register`; 

            // Making a post request to the server ip address 
            axios.post(serverIpAddress, userData, config)
            .then((responseData) => {
                if (responseData.data.status === "success") {
                    setStatusMessage(responseData.data.message); 
                    flashMessage.classList.add('open'); 

                    // Remove the menu after 3 seconds 
                    setTimeout(() => {
                        flashMessage.classList.remove('open');
                    }, 3000)

                    // Redirecting the user to the login page 
                    setTimeout(() => {
                        window.location.href ="/"; 
                    }, 4000)
                }

                else if (responseData.data.status === "error") {
                    alert(responseData.data.message); 
                }

            })
        }
        
    }
    // Rendering the register component 
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
                            <p className={styles.registerText}> Register </p>
                            <GoogleBtn InputMethod="Register" />
                        </div>
                        <div> 
                            <hr/> 
                        </div>
                        <div className={styles.div}> 
                            <label className={styles.label}> Fullname </label> <br /> 
                            <input id="fullname" type="text" placeholder='Enter your fullname' className={styles.inputForm} />
                        </div>
                        <div className={styles.div}>
                            <label className={styles.label}> Email </label> <br /> 
                            <input id="email" type="text" placeholder='Enter your Email ' className={styles.inputForm} />  
                        </div>
                        <div className={styles.div}>
                            <label className={styles.label}> Password </label> <br /> 
                            <input id="password" type="password" placeholder='At least 8 characters' className={styles.inputForm} />
                        </div>
                        <div className={styles.div}>
                            <label className={styles.label}> Repeat Password </label> <br /> 
                            <input id="confirmPassword" type="password" placeholder='At least 8 characters' className={styles.inputForm} /> 

                        </div>
                        <div className={styles.iagree}>
                            <input type="checkbox" className={styles.checkbox} /> 
                            <label for="iagree"> I agree with <Link className={styles.terms}> Terms </Link> and <Link className={styles.terms}> Privacy </Link></label>
                        </div>

                        <div className={styles.registerBtnDiv}>
                            <button className={styles.registerBtn} onClick={handleSubmit}> Register </button>
                        </div>

                        <div className={styles.hrLine}>
                            <hr /> 
                        </div>

                        <div className={styles.haveAnAccount}>
                            <p> Already have an account?</p>
                            <Link to="/" className={styles.loginBtn}> Login </Link> 

                        </div>
                    </div>
                </div>

            </div>
        </Fragment>
    )
}

// Exporting the register component 
export default Register; 