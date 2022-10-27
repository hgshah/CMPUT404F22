import useEffectOnce from "../utils/usehooks";
import axiosService, {fetcher} from "../utils/axios";
import {AuthorList} from "../utils/types";
import useSWR from "swr";
import auth from "../store/slices/auth";

export const TestFetcher = () => {
    // how to call to backend
    useEffectOnce(() => {
        // how to call it directly
        // axiosService.get<AuthorList>('/authors/').then((response) => {
        //     console.log(response.data?.items);
        // })
        // fetch('http://127.0.0.1:8000/tokens/', {
        //     credentials: 'include',
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({username: 'super', password: 'super'})
        // }).then((data) => {
        //         console.log('Success:', data);
        //     })
        //     .catch((error) => {
        //         console.error('Error:', error);
        //     });
        axiosService.post(
            '/tokens/',
            {username: 'super', password: 'super'},
            {
                withCredentials: true,
                // auth: {
                //     username: 'super',
                //     password: 'super',
                // }
            },
        ).then((response) => {
            console.log(response.data);
            var token = response.data?.token;

            axiosService.get<AuthorList>(
                '/follows/incoming/',
                {
                    withCredentials: true,
                    headers: {
                        "Authorization": `Token ${token}`,
                    }
                }
            ).then((response) => {
                console.log(response.data?.items);
            })
        }).catch((err) => {
            console.log(`Cry: ${err}`);
        })
    })

    // How to constantly call the endpoint every update in a non-verbose way
    // I forgot how to cache the results
    // Tip: use deep in the components tree!
    // const {data} = useSWR<AuthorList>('/authors/', fetcher);
    // console.log(data?.items);
    return null;
}