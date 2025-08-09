// src/features/usersSlice.js
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

export const fetchUsers = createAsyncThunk(
  "users/fetchUsers",
  async ({ page = 1, perPage = 10 }, { getState, rejectWithValue }) => {
    try {
      const token = getState().auth.token;
      const res = await fetch(
        `http://127.0.0.1:8000/users?page=${page}&perPage=${perPage}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!res.ok) {
        const errorData = await res.json();
        return rejectWithValue(errorData.detail || "Failed to fetch users");
      }

      return await res.json(); // { total, page, perPage, users: [...] }
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
);

const usersSlice = createSlice({
  name: "users",
  initialState: {
    list: [],
    loading: false,
    error: null,
    total: 0,
    page: 1,
    perPage: 10,
    hasNext: false,
    hasPrev: false,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        const { users, total, page, perPage } = action.payload;
        state.loading = false;
        state.list = users;
        state.total = total;
        state.page = page;
        state.perPage = perPage;
        state.hasPrev = page > 1;
        state.hasNext = page * perPage < total;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default usersSlice.reducer;
