/**
 * Django equivalent is in mysocial/authors
 */

export const AUTHORS_BASE_PATH = "/authors/";

export interface Author {
    display_name: string;
    github: string;
    host: string;
    id: string;
    profile_image: string;
    type: string;
    url: string;
}

export interface AuthorList {
    type: string;
    items: Author[];
}

// To get all authors:
// import useSWR from "swr";
// import {AuthorList, AUTHOR_BASE_PATH} from "../api/authors";
// const {data, error} = useSWR<AuthorList>(`${BASE_PATH}`, fetcher);

// To get a specific author
// import useSWR from "swr";
// import {Author, AUTHOR_BASE_PATH} from "../api/authors";
// const {data, error} = useSWR<AuthorList>(`${BASE_PATH}${author_id}`, fetcher);
// Note: to do the string interpolation `${author_id}`, use backtick ` NOT single quote '
