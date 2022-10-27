// from https://github.com/koladev32/django-react-auth-app/blob/main/src/utils/types.ts
export interface Author {
    displayName: string;
    github: string;
    host: string;
    id: string;
    profileImage: string;
    type: string;
    url: string;
}

export interface AuthorList {
    type: string;
    items: Author[];
}