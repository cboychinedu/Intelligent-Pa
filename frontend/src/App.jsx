// Importing the necessary modules 
import "./App.css"; 
import React, { Component, Fragment } from 'react'; 
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './Pages/Login/Login';
import Register from './Pages/Register/Register';


// Creating the class based component 
class App extends Component {
  // Rendering the component 
  render() {

    return(
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login/>} /> 
          <Route path="/register" element={<Register /> } />
        </Routes>
      </BrowserRouter>
    )

  }
}

// exporting the app component 
export default App; 