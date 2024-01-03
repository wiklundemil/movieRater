# MovieRater

## Product Summary
MovieRater is a social platform where users can create posts about movies,
the community can then rate or comment on the particular movie that the post 
is about. Further there is a voting system (upvote/downvote) to promote posts.

## Installation 

1. Dependencies 
   1. Django
   2. Rest Framework
   3. Oath authentication 
2. Running the system
   1. Clone the project : `` put clone link ``
   2. Navigate to project root folder and run : `` python manage.py makemigrations ``
   3. Run : `` python manage.py migrate ``
   4. start the server : `` python manage.py runserver ``
   5. follow the api endpoint description below to interact with the system.

## API endpoints
1. /api/signup/ <br/> User sign up, use the following json body as payload: ``{ "username" : "x" , "password" : "pwd" , "email" : "x@gmail.com" }``.
2. /api/login/ <br/> User login : `` {"username": "UserTest", "password": "pwdTest"} ``
3. /api/logout/ <br/> User log out.
3. /api/createpost/ <br/> Text search query to TMDB that stores the key for a certain movie: ``{"moviequery" : "Moneyball"}``
4. /api/searchpost/ <br/> Text search for movies titles of users posts. 
5.  /api/updatepost/ <br/> Change the movie of one of your own posts.
6. /api/deletepost/ <br/> Deletes one of your own posts.
7. /api/post/upvote <br/> Upvote a certain post, negation included.
8. /api/post/downvote <br/> Downvote a certain post, negation included.