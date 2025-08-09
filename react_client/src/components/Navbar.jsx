// src/components/Navbar.jsx
import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { FaBell } from "react-icons/fa";
import { useSelector, useDispatch } from "react-redux";
import { logoutUser, clearAuthError } from "../features/authSlice";
import "./Navbar.css";

const Navbar = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { isLoggedIn } = useSelector((state) => state.auth);
  const notificationCount = useSelector(
    (state) => state.notifications?.count || 0
  );

  const handleLogout = () => {
    dispatch(logoutUser()).then(() => {
      navigate("/login"); // Redirect after logout
    });
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <h2 className="logo">MyApp</h2>
      </div>

      <div className="navbar-right">
        {!isLoggedIn && (
          <>
            <Link
              to="/login"
              className="nav-link"
              onClick={() => dispatch(clearAuthError())}
            >
              Login
            </Link>
            <Link
              to="/register"
              className="nav-link"
              onClick={() => dispatch(clearAuthError())}
            >
              Register
            </Link>
          </>
        )}

        {isLoggedIn && (
          <>
            <button className="nav-link logout-btn" onClick={handleLogout}>
              Logout
            </button>
            <div className="notification">
              <FaBell size={20} />
              {notificationCount > 0 && (
                <span className="badge">{notificationCount}</span>
              )}
            </div>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
