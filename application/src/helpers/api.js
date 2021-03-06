/*
    Contains all URLs and ApiFunctions
 */
import axios from "axios";
import {reactLocalStorage} from "reactjs-localstorage";

import {API_TOKENS} from "../data/storage";
import {errorGettingUserInfoNotification, signINAgainNotification} from "./notifications";


const BASE_URL = "http://localhost:8000";
axios.defaults.baseURL = BASE_URL;
axios.defaults.headers.get['Content-Type'] = 'application/x-www-urlencoded';


const GET_TOKEN_PAIR = '/auth/token/';
const CREATE_ACCOUNT = '/auth/sign-up/';
const USERNAME_AVAILABLE = '/auth/username/available/';
const REFRESH_ACCESS_TOKEN = '/auth/token/refresh/';
const USER_DETAILS = "/user/meta/";


const getAccessToken = () => {
    return new Promise(async (resolve, reject) => {
        const data = reactLocalStorage.getObject(API_TOKENS);

        if (!data)
            return resolve('No User found');

        let access_token = '';
        const expires = new Date(data.expires * 1000);
        const currentTime = new Date();

        if (expires > currentTime) {
            access_token = data.tokens.access;
        } else {
            try {
                const new_token = await loadOpenUrl(REFRESH_ACCESS_TOKEN, {
                    method: 'post',
                    data: {
                        refresh: data.tokens.refresh,
                    }
                });
                access_token = new_token.access;
                const expires = new_token.expires;

                reactLocalStorage.setObject(API_TOKENS, {
                    tokens: {
                        ...data.tokens,
                        access: access_token
                    },
                    expires: expires
                });

            } catch (e) {
                try {
                    if (e.data.code === "token_not_valid")
                        signINAgainNotification();
                    else
                        errorGettingUserInfoNotification();
                } catch (e) {
                    // pass
                }

                return reject('Error refreshing token', e);
            }
        }

        return resolve(access_token);
    });
};

export const loadOpenUrl = async (url, config = {}) => {
    return new Promise((resolve, reject) => {
        axios(url, config)
            .then((res) => resolve(res.data))
            .catch(err => reject(err.response))
    });
};

export const loadSecureUrl = (url, config) => {
    return new Promise(async (resolve, reject) => {
        try {
            const data = await loadOpenUrl(url, {
                ...config,
                headers: {
                    'Authorization': `Bearer ${await getAccessToken()}`
                }
            });
            return resolve(data)
        } catch (e) {
            return reject(e)
        }
    })
};

export const getAPITokens = async (username, password) => {
    return loadOpenUrl(GET_TOKEN_PAIR, {
        data: {
            username: username,
            password: password
        },
        method: "post"
    })
};

export const getUserDetails = () => {

    //TODO: Show loading screen
    const data = loadSecureUrl(USER_DETAILS);

    //TODO: hide loading screen
    return data;
};


export const isUsernameAvailable = async (username) => {
    try {
        return await loadOpenUrl(USERNAME_AVAILABLE, {
            params: {
                username: username
            }
        })
    } catch (e) {
        console.log(e);
        return false
    }

};

export const signUpUser = async (data) => {
    return loadOpenUrl(CREATE_ACCOUNT, {
        method: 'post',
        data: data
    })
};
