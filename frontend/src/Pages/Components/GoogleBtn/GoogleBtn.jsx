// Importing the necessary modules 
import React, { Fragment } from 'react'
import styles from "./Google.module.css"; 
import googleLogo from "./Images/googleImage.png"; 

// Creating the functional component 
const GoogleBtn = (props) => {
    // Return the google button 
    return (
        <Fragment>
            <div className={styles.mainDiv}>
                <img src={googleLogo} className={styles.googleLogo}/> 
                <p className={styles.googleText}> {props.InputMethod} with Google </p>
            </div>

        </Fragment>
    )
}

// Exporting the component 
export default GoogleBtn; 