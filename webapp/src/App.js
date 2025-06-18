import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [emails, setEmails] = useState([]);
  const [selectedEmailIndex, setSelectedEmailIndex] = useState(null);
  const [finalReply, setFinalReply] = useState("");
  const [loading, setLoading] = useState({
    fetch: false,
    revise: false,
    send: false,
  });

  const fetchEmail = async () => {
    setLoading(prev => ({ ...prev, fetch: true }));
    try {
      const res = await axios.get("http://localhost:5000/api/email/latest");
      setEmails(res.data);
      setSelectedEmailIndex(null);
      setFinalReply("");
    } finally {
      setLoading(prev => ({ ...prev, fetch: false }));
    }
  };

  const generateRevised = async () => {
    if (selectedEmailIndex === null) return;
    setLoading(prev => ({ ...prev, revise: true }));
    try {
      const res = await axios.post("http://localhost:5000/api/reply/revise_final", {
        email_body: emails[selectedEmailIndex].snippet,
      });
      setFinalReply(res.data.revised);
    } finally {
      setLoading(prev => ({ ...prev, revise: false }));
    }
  };

  const sendFinalReply = async () => {
    if (selectedEmailIndex === null) return;
    setLoading(prev => ({ ...prev, send: true }));
    try {
      await axios.post("http://localhost:5000/api/reply/send", {
        email_body: emails[selectedEmailIndex],
        message_body: finalReply,
      });
      alert("Reply sent!");
    } finally {
      setLoading(prev => ({ ...prev, send: false }));
    }
  };

  return (
    <div className="App">
      <h1>Email AI Agent</h1>

      <button
        onClick={fetchEmail}
        disabled={loading.fetch}
        className={loading.fetch ? "button-loading" : ""}
      >
        {loading.fetch ? "Fetching..." : "Fetch Emails"}
      </button>

      <div align="center" >
       {emails!== null && emails.length === 0 ?
        (<h2></h2>) :
        (<h2>{emails.length} Unread Emails List</h2>)
      }
      
      <div
        className="email-list"
        style={{
          maxHeight: "540px",
          maxWidth: "100%",
          overflow: "auto",
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "flex-start",
          gap: "0px",
        }}
      >


      {emails.slice(0, 12).map((email, index) => ( 
        <div
          key={index}
          onClick={() => setSelectedEmailIndex(index)}
          className={`email-card ${selectedEmailIndex === index ? "selected" : ""}`}

        >
          <p><strong>From:</strong> {email.from}</p>
          <p><strong>Snippet:</strong> {email.snippet}</p>
        </div>
      ))}
    </div>
    </div>


{selectedEmailIndex !== null && (
  <div
    className="email-info"
    style={{
      marginTop: "40px",
      maxHeight: "600px",
      overflowY: "auto",
      overflowX: "hidden",
      paddingRight: "16px",
      maxWidth: "90%",
      wordBreak: "break-all",
      overflowWrap: "break-word",     
    }}
  >
    <h3>Selected Email Details</h3>
    <p><strong>From:</strong> {emails[selectedEmailIndex].from}</p>
    <p><strong>Body:</strong> {emails[selectedEmailIndex].body}</p>
  </div>
)}

      <button
        onClick={generateRevised}
        disabled={loading.revise || selectedEmailIndex === null}
        className={loading.revise ? "button-loading" : ""}
      >
        {loading.revise ? "Generating..." : "Generate Final Reply"}
      </button>

      {finalReply && (
        <>
          <h4>Edit Final Reply Before Sending</h4>
          <textarea
            value={finalReply}
            onChange={(e) => setFinalReply(e.target.value)}
            rows={8}
          />
        </>
      )}

      <button
        onClick={sendFinalReply}
        disabled={loading.send || selectedEmailIndex === null}
        className={loading.send ? "button-loading" : ""}
      >
        {loading.send ? "Sending..." : "Send Email"}
      </button>
    </div>
  );
}

export default App;
