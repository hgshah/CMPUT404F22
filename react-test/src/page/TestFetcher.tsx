import useEffectOnce from "../utils/usehooks";
import axiosService, {fetcher} from "../utils/axios";
import {Author, AuthorList} from "../utils/types";
import useSWR from "swr";
import {login} from "../utils/auth";
import store from "../store";
import React from "react";
import {useDispatch} from "react-redux";

// Use as reference how to call the backend!
export const TestFetcher = () => {
    const dispatch = useDispatch();

    // how to call to backend
    useEffectOnce(() => {
        // how to call it directly
        // axiosService.get<AuthorList>('/authors/').then((response) => {
        //     console.log(response.data?.items);

        let postSuccessfulLogin = (author: Author) => {
            // don't use axiosService here! this is functional programming!
        }

        // how to login
        login({username: 'super', password: 'super', dispatch, postSuccessfulLogin});
    });

    const {token} = store.getState().auth;
    if (token) {
        // let's try getting their follow requests
        console.log("Getting follows/incoming");
        axiosService.get<AuthorList>('/follows/incoming')
            .then(response => {
                console.log(response.data);
            });
    } else {
        console.log("No token!");
    }

    // How to constantly call the endpoint every update in a non-verbose way
    // I forgot how to cache the results
    // Tip: use deep in the components tree!
    const {data} = useSWR<AuthorList>('/authors/', fetcher);
    console.log(data);
    return null;
}