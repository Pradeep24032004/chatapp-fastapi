import axios from 'axios';

const API = 'http://localhost:8000';

export const api = axios.create({
  baseURL: API,
});

export const signup = (data) => api.post('/signup', data);
export const signin = (data) =>
  api.post('/signin', new URLSearchParams(data), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
export const postMessage = (token, data) =>
  api.post('/message', data, { headers: { Authorization: `Bearer ${token}` } });
export const getMessages = (token) =>
  api.get('/messages', { headers: { Authorization: `Bearer ${token}` } });
export const deleteMessage = (token, id) =>
  api.delete(`/delete_message/${id}`, { headers: { Authorization: `Bearer ${token}` } });
/*
export const getCurrentUser = (token) =>
  api.get('/user/me', { headers: { Authorization: `Bearer ${token}` } }); */
