import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import io from "socket.io-client";
import "./UserChat.css";
import { useSelector } from "react-redux";

const SOCKET_SERVER_URL = "http://localhost:8000";

function UserChat() {
  const { userId } = useParams();
  const loggedInUserId = useSelector((state) => state.auth.user.id);
  const userList = useSelector((state) => state.users.list);
  
  const currentChatUser = userList.find(user => user.id === userId);
  
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [socket, setSocket] = useState(null);

  // Initialize socket connection
  useEffect(() => {
    const newSocket = io(SOCKET_SERVER_URL, {
      query: { userId: loggedInUserId }
    });
    setSocket(newSocket);

    newSocket.emit("register_user", loggedInUserId);

    return () => {
      if (newSocket) {
        newSocket.disconnect();
      }
    };
  }, [userId, loggedInUserId]);

  // Handle incoming messages
  useEffect(() => {
    if (!socket) return;

    const handleReceiveMessage = (data) => {
      if (
        (data.sender_id === userId || data.receiver_id === userId) &&
        (data.sender_id === loggedInUserId || data.receiver_id === loggedInUserId)
      ) {
        setMessages(prev => {
          const messageExists = prev.some(msg => 
            msg.text === data.message && 
            new Date(msg.time).getTime() === new Date(data.timestamp).getTime()
          );
          
          if (!messageExists) {
            return [
              ...prev,
              {
                text: data.message,
                from: data.sender_id === loggedInUserId ? "me" : "other",
                time: new Date(data.timestamp),
                senderId: data.sender_id
              }
            ];
          }
          return prev;
        });
      }
    };

    socket.on("receive_message", handleReceiveMessage);

    return () => {
      if (socket) {
        socket.off("receive_message", handleReceiveMessage);
      }
    };
  }, [socket, loggedInUserId, userId]);

  const handleSend = () => {
    if (!message.trim() || !socket) return;

    const timestamp = new Date();
    const newMessage = {
      text: message,
      from: "me",
      time: timestamp,
      senderId: loggedInUserId
    };

    setMessages(prev => [...prev, newMessage]);
    
    socket.emit("send_message", {
      sender_id: loggedInUserId,
      receiver_id: userId,
      message: message,
      timestamp: timestamp.toISOString()
    });

    setMessage("");
  };

  const getDisplayName = (senderId) => {
    if (senderId === loggedInUserId) return "You";
    const sender = userList.find(user => user.id === senderId);
    return sender?.userId || "User";
  };

  const formatDateTime = (date) => {
    if (!(date instanceof Date)) date = new Date(date);
    return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
  };

  // Group consecutive messages from the same sender
  const groupConsecutiveMessages = (messages) => {
    if (messages.length === 0) return [];
    
    const grouped = [];
    let currentGroup = [messages[0]];
    
    for (let i = 1; i < messages.length; i++) {
      const prevMsg = messages[i - 1];
      const currentMsg = messages[i];
      
      if (currentMsg.from === prevMsg.from && 
          currentMsg.senderId === prevMsg.senderId &&
          (currentMsg.time - prevMsg.time) < 60000) {
        currentGroup.push(currentMsg);
      } else {
        grouped.push(currentGroup);
        currentGroup = [currentMsg];
      }
    }
    
    grouped.push(currentGroup);
    return grouped;
  };

  const sortedMessages = [...messages].sort((a, b) => a.time - b.time);
  const groupedMessages = groupConsecutiveMessages(sortedMessages);

  return (
    <div className="userchat-container">
      <h2>Chat with {currentChatUser?.userId || "User"}</h2>

      <div className="messages-section">
        {groupedMessages.length === 0 ? (
          <p className="no-messages">No messages yet. Start the conversation!</p>
        ) : (
          groupedMessages.map((messageGroup, groupIdx) => (
            <div
              key={`group-${groupIdx}`}
              className={`message-group ${messageGroup[0].from === "me" ? "sent" : "received"}`}
            >
              {messageGroup[0].from !== "me" && (
                <div className="message-sender">
                  {getDisplayName(messageGroup[0].senderId)}
                </div>
              )}
              {messageGroup.map((msg, msgIdx) => (
                <div
                  key={`${msg.time.getTime()}-${msgIdx}`}
                  className={`message-bubble ${msg.from === "me" ? "sent" : "received"}`}
                >
                  <span className="message-text">{msg.text}</span>
                  {msgIdx === messageGroup.length - 1 && (
                    <span className="message-time">
                      {formatDateTime(msg.time)}
                    </span>
                  )}
                </div>
              ))}
            </div>
          ))
        )}
      </div>

      <div className="send-message-section">
        <input
          type="text"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default UserChat;