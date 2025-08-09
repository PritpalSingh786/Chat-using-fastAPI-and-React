// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./components/Login";
import Register from "./components/Register";
import SidebarPage from "./components/SidebarPage";
import ChatPage from "./components/ChatPage";
import UserChat from "./components/UserChat";
import AddPostPage from "./components/AddPostPage";

function App() {
  return (
    <Router>
      <Navbar notificationCount={3} />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Sidebar layout with nested routes */}
        <Route path="/sidebar" element={<SidebarPage />}>
          {/* Make chat a parent route with nested user chat */}
          <Route path="chat" element={<ChatPage />}>
            <Route path=":userId" element={<UserChat />} />
          </Route>

          <Route path="post" element={<AddPostPage />} />
        </Route>

        <Route path="/" element={<h1>Welcome Home</h1>} />
      </Routes>
    </Router>
  );
}

export default App;
