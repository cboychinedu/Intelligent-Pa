// Importing the necessary modules 
import React, { Fragment } from 'react'; 
import styles from "./Navbar.module.css"; 
import { Link } from 'react-router-dom';

// Creating the navbar 
const Navbar = (props) => {
    // Creating a function for logging out the user 
    const logoutUser = (event) => {
        // Clearing the local storage 
        localStorage.clear(); 

        // Redirecting the user to the login page 
        setInterval(() => {
            window.location.href = "/login"; 
        }, 2000); 
    }

    // Rendering the component 
    return(
        <Fragment>
            {/* Adding the navbar */}
            <nav className={styles.mainNav}>
                {/* Adding the navbar container */}
                <div className={styles.navContainerDiv}>
                    <nav className={styles.leftNav}>
                        <Link to="/dashboard"> Home </Link>
                        <Link to="#"> About </Link>
                        <Link to="#"> ContactUs</Link>
                        <Link to="#" onClick={logoutUser}> Logout </Link> 

                    </nav>

                    {/* Adding the right navbar */}
                    <nav className={styles.rightNav}>
                        <div>
                            <input className={styles.searchInputForm} type="search" placeholder='Search Contact...' /> 
                        </div>

                        <div>
                            <button className={styles.submitButton} id="submitButton"type="submit" >Submit</button>
                        </div>
                    </nav>
                </div>
            </nav>
        </Fragment>
    )
}

// Exporting the navbar 
export default Navbar; 
