// From https://dev.to/koladev/django-rest-authentication-cmh
// todo(turnip): add link to backend
import {Author} from "./utils/types";

export interface TokenResponse {
    token: string;
    author: Author;
}