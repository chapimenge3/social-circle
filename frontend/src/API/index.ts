import Axios from "axios";

export const tweetsAPI = async () =>
  await Axios.get("http://localhost:8000/timeline/");

export const recomendationsAPI = async () =>
  await Axios.get("http://localhost:8000/recomendations/");

export const trendingAPI = async () =>
  await Axios.get("http://localhost:8000/trending/");

export const notificationAPI = async () =>
  await Axios.get("http://localhost:8000/notifications");
