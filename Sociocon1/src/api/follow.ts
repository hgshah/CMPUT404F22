/**
 * Django equivalent is in mysocial/authors
 * Tip: to understand what's supposed to be in the request and response interface,
 * Check out the view.py and serializers.py
 * Tip: check out TestFetcher.tsx
 * Tip: casing for the fields should match the JSON sent back by Django
 */
import {Author, AUTHORS_BASE_PATH} from "./authors";
import axiosService from "../utils/axios";
import {AxiosResponse} from "axios";

export const FOLLOWS_BASE_PATH = "/follows/";

export interface Follow {
    type: string,
    id: string,
    summary: string,
    has_accepted: boolean,
    object: Author,
    actor: Author,
}

// todo: outgoing GET

// =============================================
// Get all follow requests: follows/incoming GET
// =============================================
// import useSWR from "swr";
// import {FOLLOWS_INCOMING_PATH, IncomingFollowsResponse} from "../api/follow";
// const {data, error} = useSWR<IncomingFollowsResponse>(`${FOLLOWS_INCOMING_PATH}`, fetcher);
export const FOLLOWS_INCOMING_PATH = `${FOLLOWS_BASE_PATH}incoming`

export interface IncomingFollowsResponse {
    type: string;
    items: Follow[];
}

// todo: follows/id GET

// todo: follows/id PUT #

// todo: follows/id DELETE #

// todo: authors/author_id/followers GET

// todo: authors/author_id/followers POST #
// =========================================================
// Create a follow request: authors/author_id/followers POST
// =========================================================
/**
 * @param authorId of account to follow with the current account
 *
 * @example
 * createFollowRequest('')
 *     .then((response) => {
 *         console.log(response.data); // <- successful follow!
 *     })
 *     .catch((error) => {
 *         // catch error here! check out error code!
 *         console.log(error);
 *     });
 */
export const createFollowRequest = (authorId: string): Promise<AxiosResponse<Follow>> => {
    const path = `${AUTHORS_BASE_PATH}${authorId}/followers/`
    return axiosService.post<Follow>(path, {withCredentials: true});
}

// todo: authors/author_id/friends GET