# Inbox

## Remote Documentation
ENDPOINT: `POST author/{AUTHOR_ID}/inbox`

Liking a post:
```python
{
    "type": "like",
    "object": "http://127.0.0.1:8080/authors/f4af2492-e84f-4d4d-87fa-3832bc17b953/posts/4e7adec8-0ed5-48fc-ad75-058a349c0fd4",
    "actor": "http://127.0.0.1:8000/authors/44248451-2deb-421c-b5f6-db0c214b68ea"
}
```

Liking a comment:
```python
{
    "type": "like",
    "object": "http://127.0.0.1:8080/authors/f4af2492-e84f-4d4d-87fa-3832bc17b953/posts/4e7adec8-0ed5-48fc-ad75-058a349c0fd4/comments/98b5a822-6e09-4b4d-af9e-466d99137774"",
    "actor": "http://127.0.0.1:8000/authors/44248451-2deb-421c-b5f6-db0c214b68ea"
}
```
Note: the actor should be *YOU* with your host!

Adding a post:
```python 
{
    "type": "post",
    "title": "mytitle",
    "id": "aa292f41-90b2-4b0f-af4e-fc4cdfaabcc4",
    "source": "www.default.com",
    "origin": "www.default.com",
    "description": "mydesc",
    "contentType": "text/plain",
    "author": {
        "type": "author",
        "id": "44248451-2deb-421c-b5f6-db0c214b68ea",
        "url": "http://127.0.0.1:8000/authors/44248451-2deb-421c-b5f6-db0c214b68ea",
        "host": "127.0.0.1:8000",
        "displayName": "amanda",
        "github": "",
        "profileImage": ""
    },
    "categories": [],
    "count": 4,
    "comments": "aa292f41-90b2-4b0f-af4e-fc4cdfaabcc4/comments",
    "published": "2022-11-17T21:07:41.803434Z",
    "visibility": "public",
    "unlisted": false,
    "url": "http://127.0.0.1:8000/authors/44248451-2deb-421c-b5f6-db0c214b68ea/posts/aa292f41-90b2-4b0f-af4e-fc4cdfaabcc4"
}
```
Unrequired fields: categories

Adding a comment:
```python
{
    "type": "comment",
    "author": {
        "type": "author",
        "id": "44248451-2deb-421c-b5f6-db0c214b68ea",
        "url": "http://127.0.0.1:8000/authors/44248451-2deb-421c-b5f6-db0c214b68ea",
        "host": "127.0.0.1:8000",
        "displayName": "amanda",
        "github": "",
        "profileImage": ""
    },
    "comment": "hahahahah",
    "contentType": "text/plain",
    "published": "2022-11-19T03:47:35.831322Z",
    "id": "7bae9bbb-d26a-46d0-9345-3710db936692",
    "url": "http://127.0.0.1:8000/authors/44248451-2deb-421c-b5f6-db0c214b68ea/posts/aa292f41-90b2-4b0f-af4e-fc4cdfaabcc4/comments/7bae9bbb-d26a-46d0-9345-3710db936692"
}
```
Every field is required!

PS I can only validate that the general JSON body is correct, not the author JSON so please make sure the author object is correct before sending it to our inbox!

Create a comment: `POST authors/{AUTHOR_ID}/posts/{POST_ID/comments
```python
{
    "comment": "this is my comment",
    "contentType": "text/plain",
    "actor": "http://127.0.0.1:8000/authors/44248451-2deb-421c-b5f6-db0c214b68ea"
}
```

## Local Documentation
Liking a post:
```python
{
    "type": "like",
    "object": "http://127.0.0.1:8080/authors/f4af2492-e84f-4d4d-87fa-3832bc17b953/posts/4e7adec8-0ed5-48fc-ad75-058a349c0fd4"
}
```

Liking a comment:
```python
{
    "type": "like",
    "object": "http://127.0.0.1:8080/authors/f4af2492-e84f-4d4d-87fa-3832bc17b953/posts/4e7adec8-0ed5-48fc-ad75-058a349c0fd4/comments/98b5a822-6e09-4b4d-af9e-466d99137774""
}
```
