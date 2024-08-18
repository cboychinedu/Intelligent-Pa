// Importing the necessary modules
import React, { Fragment, useState } from 'react';
import styles from "./Dashboard.module.css"; 

// Creating the dashboard component
const Dashboard = (props) => {
  // Setting the state 
  const [message, setMessage] = useState(""); 
  const [messages, setMessages] = useState([]);

  // Handling input change
  const handleChange = (e) => {
    setMessage(e.target.value);
  };

  // Handling form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() !== "") {
      setMessages([...messages, message]);
      setMessage(""); // Clear the input after submission
    }
  };

  // Rendering the component
  return (
    <Fragment>

      <div className={styles.messagesContainer}>
            {messages.map((msg, index) => (
              <p key={index} className={styles.message}>{msg}</p>
            ))}
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
