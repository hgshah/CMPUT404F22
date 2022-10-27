import useEffectOnce from "../utils/usehooks";
import axiosService, {fetcher} from "../utils/axios";
import {Author, AuthorList} from "../utils/types";
import useSWR from "swr";
import {login} from "../utils/auth";
import store from "../store";
import {useDispatch} from "react-redux";
import {useEffect} from "react";

// Use as reference how to call the backend!
export const TestFetcher = () => {
    const dispatch = useDispatch();
    const {token} = store.getState().auth;
    const {data} = useSWR<AuthorList>('/authors/', fetcher);

    // How to constantly call the endpoint every update in a non-verbose way
    // I forgot how to cache the results
    // Tip: use deep in the components tree!
    if (data) {
        console.log(data);
    }

    // how to call to backend
    useEffectOnce(() => {
        // how to call it directly
        // axiosService.get<AuthorList>('/authors/').then((response) => {
        //     console.log(response.data?.items);

        let postSuccessfulLogin = (_: Author) => {
            // don't use axiosService here! this is functional programming!
        }

        // how to login
        login({username: 'super', password: 'super', dispatch, postSuccessfulLogin});
    });

    useEffect(() => {
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
    })

    return null;
}