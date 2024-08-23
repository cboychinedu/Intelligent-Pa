// Importing the necessary modules 
import "./App.css"; 
import React, { Component, Fragment } from 'react'; 
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './Pages/Login/Login';
import { AuthContext } from "./Auth/AuthContext"; 
import Dashboard from "./Pages/Dashboard/Dashboard";
import Register from './Pages/Register/Register';

// Setting the token if present
let tokenValue = localStorage.getItem("x-auth-token") || null; 

// Creating the class based component 
class App extends Component {
  // Getting the auth context 
  static contextType = AuthContext; 

  // Rendering the component 
  render() {
    // Getting the context data 
    const { isLoggedIn, xAuthToken, setToken } = this.context; 

    // Setting the token value 
    setToken(tokenValue)

    // Returning the component 
    return(
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login/>} /> 
          <Route path="/register" element={<Register /> } />

          {isLoggedIn && xAuthToken ? (
            <>
              <Route path="/dashboard" element={<Dashboard />} /> 
            </>
          ): (
            <>
               <Route path="/" element={<Login/>} /> 
               <Route path="/register" element={<Register /> } />
               <Route path="*" element={<Login />} />
            </>
          )}
        
        </Routes>
      </BrowserRouter>
    )

  }
}

// exporting the app component 
export default App; 