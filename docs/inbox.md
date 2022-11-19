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


## Local Documentation
Liking a post:
```python
{
    "type": "like",
    "object": "http://127.0.0.1:8080/authors/f4af2492-e84f-4d4d-87fa-3832bc17b953/posts/4e7adec8-0ed5-48fc-ad75-058a349c0fd4"
}
```
