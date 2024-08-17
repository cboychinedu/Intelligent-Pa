// Importing the necessary modules 
import React, { Component, Fragment } from 'react'
import { Link } from 'react-router-dom';
import styles from "./Login.module.css"; 
import GoogleBtn from '../Components/GoogleBtn/GoogleBtn';

// Creating the functional based component 
const Login = (props) => {
    // Rendering the login component 
    return(
        <Fragment>
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
                            <input type="email" placeholder='Email address...' className={styles.inputForm}/>
                        </div>

                        <div className={styles.div}> 
                            <label for="Password" className={styles.label}> Password </label> <br /> 
                            <input type="password" placeholder='Password...' className={styles.inputForm} />
                        </div>
                        <div className={styles.rememberMeDiv}> 
                            <input type="checkbox" className={styles.checkbox}/> 
                            <label for="rememberme" className={styles.label}> Remember me </label>
                        </div>
                        <div className={styles.div}>
                            <button className={styles.loginBtn}> Login </button>
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