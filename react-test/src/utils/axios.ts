import axios from 'axios';
import store from '../store';

// from
const baseURL = process.env.NODE_ENV === "development"
    ? "http://127.0.0.1:8000/"
    : "http://example.com" // todo: change with heroku!

const axiosService = axios.create({
    // baseURL: process.env.REACT_APP_API_URL,
    baseURL: baseURL, // todo: make this dynamic!!
    headers: {
        'Content-Type': 'application/json',
    },
});

axiosService.interceptors.request.use(async (config) => {
    const { token } = store.getState().auth;

    if (token !== null) {
        config.headers.Authorization = 'Token ' + token;
        // @ts-ignore
        console.debug('[Request]', config.baseURL + config.url, JSON.stringify(token));
    }
    return config;
});

// todo(turnip): don't know what this is; we might use it later?
// axiosService.interceptors.response.use(
//     (res) => {
//         // @ts-ignore
//         console.debug('[Response]', res.config.baseURL + res.config.url, res.status, res.data);
//         return Promise.resolve(res);
//     },
//     (err) => {
//         console.debug(
//             '[Response]',
//             err.config.baseURL + err.config.url,
//             err.response.status,
//             err.response.data
//         );
//         return Promise.reject(err);
//     }
// );

export function fetcher<T = any>(url: string) {
    return axiosService.get<T>(url).then((res) => res.data);
}

export default axiosService;
