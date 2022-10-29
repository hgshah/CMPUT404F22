import {fetcher} from "../utils/axios";
import useSWR from "swr";
import store from "../store";
import {useDispatch} from "react-redux";
import {AUTHORS_BASE_PATH, Author} from "../api/authors";
import {createFollowRequest, FOLLOWS_INCOMING_PATH, IncomingFollowsResponse} from "../api/follow";
import {useEffect} from "react";
import useEffectOnce from "../utils/usehooks";

// Use as reference how to call the backend!
export const TestFetcher = () => {
    const dispatch = useDispatch();
    const {token} = store.getState().auth;
    const id = "f20a28a6-23be-46a0-a42d-f4fd6c1a5ddd"
    const {data, error} = useSWR<IncomingFollowsResponse>(`${FOLLOWS_INCOMING_PATH}`, fetcher);

    // How to constantly call a GET endpoint every update in a non-verbose way
    // I forgot how to cache the results
    // Tip: use deep in the components tree!
    if (data) {
        data.items?.forEach((item) => {
            console.log(item.actor);
        })
    }

    if (error) {
        // todo: handle error!
    }

    // // how to call to backend in non-GET ways
    // useEffectOnce(() => {
    //     // how to call it directly
    //     // axiosService.get<AuthorList>('/authors/').then((response) => {
    //     //     console.log(response.data?.items);
    //
    //     let postSuccessfulLogin = (_: Author) => {
    //         // don't use axiosService here! this is functional programming!
    //     }
    //
    //     // how to login
    //     login({username: 'super', password: 'super', dispatch, postSuccessfulLogin});
    // });

    // useEffect(() => {
    //     if (token) {
    //         // let's try getting their follow requests
    //         console.log("Getting follows/incoming");
    //         axiosService.get<AuthorList>('/follows/incoming')
    //             .then(response => {
    //                 console.log(response.data);
    //             });
    //     } else {
    //         console.log("No token!");
    //     }
    // })

    // sample how to make a follow request
    useEffectOnce(() => {
        if (token) {
            // let's try getting their follow requests
            createFollowRequest('f20a28a6-23be-46a0-a42d-f4fd6c1a5ddd')
                .then((response) => {
                    console.log(response.data); // <- successful follow!
                })
                .catch((error) => {
                    // catch error here!
                    console.log(error);
                });
        } else {
            console.log("No token!");
        }
    })

    return null;
}