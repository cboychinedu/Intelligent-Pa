// Importing the necessary modules 
import React, { Fragment } from 'react'; 
import styles from "./Register.module.css"; 
import { Link } from 'react-router-dom';
import GoogleBtn from '../Components/GoogleBtn/GoogleBtn';

// Creating the functional based component 
const Register = (props) => {
    // Rendering the register component 
    return(
        <Fragment> 
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
                            <input type="text" placeholder='Enter your fullname' className={styles.inputForm} />
                        </div>
                        <div className={styles.div}>
                            <label className={styles.label}> Email </label> <br /> 
                            <input type="text" placeholder='Enter your Email ' className={styles.inputForm} />  
                        </div>
                        <div className={styles.div}>
                            <label className={styles.label}> Password </label> <br /> 
                            <input type="password" placeholder='At least 8 characters' className={styles.inputForm} />
                        </div>
                        <div className={styles.div}>
                            <label className={styles.label}> Repeat Password </label> <br /> 
                            <input type="password" placeholder='At least 8 characters' className={styles.inputForm} /> 

                        </div>
                        <div className={styles.iagree}>
                            <input type="checkbox" className={styles.checkbox} /> 
                            <label for="iagree"> I agree with <Link className={styles.terms}> Terms </Link> and <Link className={styles.terms}> Privacy </Link></label>
                        </div>

                        <div className={styles.registerBtnDiv}>
                            <button className={styles.registerBtn}> Register </button>
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