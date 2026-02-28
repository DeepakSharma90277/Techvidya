import axios from "axios";
import { store } from "../reducer/store";

export const axiosInstance = axios.create({});

export const apiConnector = (method, url, bodyData, headers, params) => {
  const token = store.getState().auth.token; // get token from redux

  return axiosInstance({
    method,
    url,
    data: bodyData || null,
    headers: {
      Authorization: token ? `Bearer ${token}` : "",
      ...headers,
    },
    params: params || null,
  });
};
