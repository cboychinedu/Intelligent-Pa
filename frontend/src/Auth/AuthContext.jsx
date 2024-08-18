// Importing the necessary modules 
import React, { Component, createContext, Fragment } from 'react';

// Creating the AuthContext object 
const AuthContext = createContext(); 

// Creating the AuthContextProvider class 
class AuthContextProvider extends Component {
    // Setting the state 
    state = {
        isLoggedIn: false, 
        xAuthToken: null  
    }

    // Creating a function for changing the xAuthToken state 
    setToken = (xTokenValue) => {
        // Setting the state if the user's token was validated 
        this.setState({
            isLoggedIn: true, 
            xAuthToken: xTokenValue, 
        })
    }

    // Creating a function for logging the user or removing the 
    // user's token 
    removeToken = () => {
        // Changing the state 
        this.setState({
            isLoggedIn: false, 
            xAuthToken: null, 
        })
    }

    // Rendering the AuthContextProvider 
    render() {
        // Return the AuthContext Provider 
        return(
            <Fragment> 
                <AuthContext.Provider 
                    value={{
                        ...this.state, 
                        setToken: this.setToken, 
                        removeToken: this.removeToken
                    }} >
                    { this.props.children }
                </AuthContext.Provider>
            </Fragment>
        )
    }
}

// Exporting the AuthContext 
export {
    AuthContext, 
    AuthContextProvider
}


