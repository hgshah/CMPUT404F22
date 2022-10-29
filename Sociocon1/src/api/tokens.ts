/**
 * Django equivalent is in mysocial/tokens
 */
import {Dispatch} from "redux";
import axiosService from "../utils/axios";
import authSlice from "../store/slices/auth";
import {Author} from "./authors";


export type LoginErrorCallback = (error: any) => void;
export type PostSuccessfulLoginCallback = (author: Author) => void;

export interface TokenRequest {
    username: string,
    password: string,
    dispatch: Dispatch;
    loginError?: LoginErrorCallback, // optional
    postSuccessfulLogin?: PostSuccessfulLoginCallback // optional
}

export interface TokenResponse {
    token: string;
    author: Author;
}

/**
 * Log the user in by calling the tokens endpoint
 * @param args TokenRequest
 */
export const login = (args: TokenRequest) => {
    const {username, password, postSuccessfulLogin, loginError, dispatch} = args;
    axiosService.post<TokenResponse>('/tokens/',
        {username, password},
        {withCredentials: true})
        .then((response) => {
            if (response.data?.token) {
                dispatch(authSlice.actions.setTokens(response.data));
                // todo(turnip): refresh????
                postSuccessfulLogin?.(response.data.author);
            } else {
                // todo(turnip): how do you properly log react?
                console.log("Missing token from server");
            }
        }).catch((error) => {
            console.log(`Error: ${error}`)
            loginError?.(error); // if loginError not null, call it!
        }
    )
}