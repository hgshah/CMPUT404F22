# API README

- `follows.ts` has examples of authenticated calls to the backend
- To make unauthenticated or anonymous calls to the backend, don't use the config option of axios or leave
    `withCredentials = false;`
- to check out how to use the API, look at `src/page/TestFetcher.tsx`

## Testing
- You can test by commenting out `TestFetcher()` in `News.js`
- To test out authenticated calls, like making a post, you have to login. uncomment the useEffectOnce
  with the login calls and put your password and username in it (not advisable to commit that when we're now
  using a remote heroku server!)
- Put your own calls in `TestFetcher()`
- Remember to run your Django server too!
- To monitor calls to the backend, use the Network and Console in your browser's developer tools

## Issues
- csrf authentication is broken due to conflicts with basic auth token so simply going to the address
  like `127.0.0.1/follows/incoming/` will not work, even if you're logged in admin in `127.0.0.1/admin/`