import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchUsers } from "../features/usersSlice";
import { Link, Outlet, useNavigate } from "react-router-dom";
import "./ChatPage.css";

function ChatPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user } = useSelector((state) => state.auth);
  const { list, loading, error, page, perPage, hasNext, hasPrev } = useSelector(
    (state) => state.users
  );

  useEffect(() => {
    // Redirect if not logged in
    if (!user) {
      navigate("/login");
      return;
    }

    dispatch(fetchUsers({ page: 1, perPage }));
  }, [dispatch, user, perPage, navigate]);

  const handleNext = () => {
    if (hasNext) dispatch(fetchUsers({ page: page + 1, perPage }));
  };

  const handlePrev = () => {
    if (hasPrev) dispatch(fetchUsers({ page: page - 1, perPage }));
  };

  // Return null or loading spinner if no user
  if (!user) {
    return null;
  }

  return (
    <div className="chatpage-container" style={{ display: "flex", gap: "1rem" }}>
      {/* User List */}
      <div style={{ flex: "1 1 300px" }}>
        <h3>Welcome, {user?.userId || "User"}</h3>

        {loading && <p>Loading users...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        <ul className="users-list">
          {list.map((u) => (
            <li key={u.id}>
              <Link to={`${u.id}`}>{u.userId}</Link>
            </li>
          ))}
        </ul>

        <div className="pagination-controls">
          <button onClick={handlePrev} disabled={!hasPrev}>
            ⬅ Previous
          </button>
          <span>Page {page}</span>
          <button onClick={handleNext} disabled={!hasNext}>
            Next ➡
          </button>
        </div>
      </div>

      {/* Chat content for selected user */}
      <div style={{ flex: "2 1 600px", borderLeft: "1px solid #ccc", paddingLeft: "1rem" }}>
        <Outlet />
      </div>
    </div>
  );
}

export default ChatPage;