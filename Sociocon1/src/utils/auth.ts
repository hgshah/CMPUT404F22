import axiosService from "./axios";
import authSlice from "../store/slices/auth";
import {TokenResponse} from "../types";
import {Author} from "./types";
import {Dispatch} from "redux";

export type LoginErrorCallback = (error: any) => void;
export type PostSuccessfulLoginCallback = (author: Author) => void;

export interface LoginArguments {
    username: string,
    password: string,
    dispatch: Dispatch;
    loginError?: LoginErrorCallback,
    postSuccessfulLogin?: PostSuccessfulLoginCallback
}

export function login(args: LoginArguments) {
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