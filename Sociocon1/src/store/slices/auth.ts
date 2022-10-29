// from https://dev.to/koladev/django-rest-authentication-cmh
import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {Author} from "../../api/authors";
import {TokenResponse} from "../../api/tokens";

type State = {
    token: string | null;
    author: Author | null;
};

const initialState: State = { token: null, author: null };

const authSlice = createSlice({
    name: "auth",
    initialState,
    reducers: {
        setTokens(state: State, action: PayloadAction<TokenResponse>) {
            state.author = action.payload.author;
            state.token = action.payload.token;
        },
        setLogout(state: State) {
            state.author = null;
            state.token = null;
        },
    },
});

export default authSlice;