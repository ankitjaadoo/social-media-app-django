** Introduction **

This Project is all about building a Backend API for a Social Network site using Django REST Framework

** Functionalities **

- User Sign Up
- User Log In
- Create a Post
- Delete a Post
- Comment on a Post
- Like a Post
- Search for Post(s) using Hashtag(s)
- View all posts by a user

** API Endpoints **

1. User Sign Up - http://127.0.0.1:8000/signup?username=<username>&password=<password>
2. User Log In - http://127.0.0.1:8000/login?username=<username>&password=<password>
3. Create a Post - http://127.0.0.1:8000/post/create?username=<username>&post_text=<post_text>
4. Delete a Post - http://127.0.0.1:8000/post/1/delete?username=<username>
5. Comment on a Post - http://127.0.0.1:8000/post/10/comment?username=<username>&comment_text=<comment_text>
6. Like a Post - http://127.0.0.1:8000/post/1/like?username=<username>
7. Search for Post(s) using Hashtag(s) - http://127.0.0.1:8000/post/search?username=<username>&hashtag=<hashtag>
8. View all posts by a user - http://127.0.0.1:8000/post?username=<username>

