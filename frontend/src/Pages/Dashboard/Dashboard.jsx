// Importing the necessary modules
import React, { Fragment, useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Speech from "react-text-to-speech"; 
import styles from "./Dashboard.module.css"; 
import Navbar from '../Components/Navbar/Navbar';

// Creating the dashboard component
const Dashboard = (props) => {
  // Setting the state 
  const [message, setMessage] = useState(""); 
  const [messages, setMessages] = useState([]);
  const [response, setResponse] = useState(""); 

  // Reference to the messages container div
  const messagesEndRef = useRef(null);

  // Scroll to bottom function
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Scroll to bottom whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handling input change
  const handleChange = (e) => {
    setMessage(e.target.value);
  };

  // Handling form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (message.trim() !== "") {
      // Add the user's message to the list
      setMessages([...messages, { text: message, type: 'user' }]);

      // Prepare the user data to be sent
      const userData = JSON.stringify({
        chatData: message
      });

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

      // Send the POST request
      const serverIpAddress = `http://localhost:3001/dashboard/`; 
      axios.post(serverIpAddress, userData, config)
        .then((responseData) => {
          // Checking 
          if (responseData.data.status === "success") {
            console.log(responseData); 
            speakText(responseData.data.message)
            setResponse(responseData.data.message)

            // Delay for 3 seconds 
            setTimeout(() => {
              // Display the response message 
              setMessages(prevMessages => [...prevMessages, { text: responseData.data.message, type: 'response' }]);
            }, 3000)
  
            // Clear the input after submission
            setMessage(""); 
          } else {
            setMessages(prevMessages => [...prevMessages, { text: responseData.data.message, type: 'response' }]);
            speakText(responseData.data.message); 

            // Clear the input after submission
            setMessage(""); 
          }

        })
    }
  };

  // Speak text 
  const speakText = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text); 
      window.speechSynthesis.speak(utterance); 
    } else {
      alert("Your browser does not support speech synthesis.");
    }
  };

  // Rendering the component
  return (
    <Fragment>
      {/* Adding the navbar */}
      <Navbar /> 
      
      <div className={styles.messagesContainerDiv}>
        {messages.map((msg, index) => (
          <div key={index} className={`${styles.messagesContainer} ${msg.type === 'user' ? styles.userMessage : styles.responseMessage}`}>
            <p className={styles.message}>{msg.text}</p>
            <Speech text={response} /> 
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.container}>
        <form onSubmit={handleSubmit} className={styles.formList}>
          <input 
            type="text" 
            className={styles.inputForm} 
            placeholder="Type here..." 
            value={message}
            onChange={handleChange}
          />
          <button type="submit" className={styles.submitButton}>Send</button>
        </form>
      </div>
    </Fragment>
  );
}

// Exporting the dashboard component
export default Dashboard;
