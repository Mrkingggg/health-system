import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./ChatHistory.css"
function ChatHistory() {
    const { mpId, patientId } = useParams();
    const [chatHistory, setChatHistory] = useState([]);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetch chat history
    useEffect(() => {
        const fetchChatHistory = async () => {
            try {
                const response = await fetch(`/api/gen/view_chat_history?MPid=${mpId}&patientid=${patientId}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setChatHistory(data);
            } catch (error) {
                setError(error.message);
            }
            setLoading(false);
        };

        fetchChatHistory();
    }, [mpId, patientId]);

    // Function to send message
    const sendMessage = async () => {
        const payload = {
            MPid: mpId,
            patientid: patientId,
            direction: 'send',  
            message: message,
            sendtime: new Date().toISOString(),
            status: 'sent'
        };

        try {
            const response = await fetch('/api/gen/send_store_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            if (response.ok) {
                setChatHistory([...chatHistory, { ...payload, content: message }]);  // Assuming the API returns the new message formatted similarly
                setMessage('');
            } else {
                throw new Error(data.error || 'Failed to send message');
            }
        } catch (error) {
            setError(error.message);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className='container'>
            <div className='chat-history'>
                <h2>Chat History with patient id: {patientId}</h2>
                <ul>
                    {chatHistory.map((msg, index) => (
                        <li key={index}>
                            <p>{msg.username} {msg.sendtime} : {msg.message}</p>
                        </li>
                    ))}
                </ul>
            </div>
            <div className='send-msg'>
                <input 
                    type="text"
                    value={message}
                    onChange={e => setMessage(e.target.value)}
                    placeholder="Type a message..."
                />
                <button onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
}

export default ChatHistory;
