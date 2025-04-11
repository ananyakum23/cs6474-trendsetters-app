import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:5000';

export const fetchTopPosts = () => axios.get(`${BASE_URL}/top-engagement`);
export const fetchClusterNames = () => axios.get(`${BASE_URL}/cluster-names`);
export const fetchForecastForCluster = (id) =>
  axios.get(`${BASE_URL}/forecast-multi/${id}`);