import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:5000';
// const BASE_URL = 'https://cs6474-trendsetters-app.onrender.com';


export const fetchTopPosts = () => axios.get(`${BASE_URL}/top-engagement`);
// export const fetchClusterNames = () => axios.get(`${BASE_URL}/cluster-names`);
// export const fetchForecastForCluster = (id) =>
//   axios.get(`${BASE_URL}/forecast-multi/${id}`);

export const fetchClusterNames = (subreddit) =>
  axios.get(`${BASE_URL}/cluster-names`, {
    params: { subreddit },
  });
export const fetchForecastForCluster = (clusterId, subreddit) =>
  axios.get(`${BASE_URL}/forecast-multi/${subreddit}/${clusterId}`);
