import useEffectOnce from "../utils/usehooks";
import axiosService, {fetcher} from "../utils/axios";
import {AuthorList} from "../utils/types";
import useSWR from "swr";

export const TestFetcher = () => {
    // how to call to backend
    useEffectOnce(() => {
        // how to call it directly
        // axiosService.get<AuthorList>('/authors/').then((response) => {
        //     console.log(response.data?.items);
        // })
        axiosService.get<AuthorList>(
            '/follows/incoming/',
            {withCredentials: true}
        ).then((response) => {
            console.log(response.data?.items);
        })
    })

    // How to constantly call the endpoint every update in a non-verbose way
    // I forgot how to cache the results
    // Tip: use deep in the components tree!
    // const {data} = useSWR<AuthorList>('/authors/', fetcher);
    // console.log(data?.items);
    return null;
}