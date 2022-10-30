#! /bin/sh

curl --header "Content-Type:application/json" --request POST --data '{"context": "like1", "summary": "i liked your post", "type": "like", "author": {"type": "author", "id": "http://localhost/authors/abefc574-d6a9-4e20-bd65-931da4c0521a", "url": "http://localhost/authors/abefc574-d6a9-4e20-bd65-931da4c0521a", "host": "localhost", "displayName": "", "github": "", "profileImage": ""}, "objectURL": "http://12312/authors/f49bce07-1139-42a2-841b-27c4dd62c334/posts/b55722dd-7311-4242-a552-4aa00e18941b"}' http://127.0.0.1:8000/authors/abefc574-d6a9-4e20-bd65-931da4c0521a/inbox


# curl -v -H 'Content-Type: application/json' -X POST http://127.0.0.1:8000/authors/abefc574-d6a9-4e20-bd65-931da4c0521a/inbox -d '{
#             "context": "like",
#             "summary": "like POST test,
#             "type": "like",
#             "author": {
#                 "type": "author",
#                 "id": "http://localhost/authors/abefc574-d6a9-4e20-bd65-931da4c0521a",
#                 "url": "http://localhost/authors/abefc574-d6a9-4e20-bd65-931da4c0521a",
#                 "host": "localhost",
#                 "displayName": "",
#                 "github": "",
#                 "profileImage": ""
#             },
#             "objectURL": "http://12312/authors/f49bce07-1139-42a2-841b-27c4dd62c334/posts/b55722dd-7311-4242-a552-4aa00e18941b"
#         }'
