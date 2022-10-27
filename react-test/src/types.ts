// From https://dev.to/koladev/django-rest-authentication-cmh
export interface AccountResponse {
    user: {
        id: string;
        email: string;
        username: string;
        is_active: boolean;
        created: Date;
        updated: Date;
    };
    access: string;
    refresh: string;
}