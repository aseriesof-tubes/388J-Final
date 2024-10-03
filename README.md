# Song Review

# Q1 
## Description of your final project idea:
Essentially, we will be making a music discussion forum site which will allow for people to rate songs and leave reviews about it. We also include a Spotify embed that will allow for people to hear a short sample of the song.
# Q2
## Describe what functionality will only be available to logged-in users:
Users will be able to rate and comment on songs, and these comments can be seen by everyone and will have their username, profile pic, and the time posted on the comments.
# Q3 
## List and describe at least 4 forms:
Register form: Information that will be used for the user next time they log in to use the site
Login form: Information/credentials which will be checked to gain access to data in MongoDB
SongReviewform: User and their rating for a specific song
SearchForm: User's inputted text which will be used to parse for related songs

# Q4 
## List and describe your routes/blueprints (don’t need to list all routes/blueprints you may have–just enough for the requirement):
1. Auth blueprint which would handle all authentication-related routes like login, registration, and logout.
2. song blueprint for routes such as viewing song details, rating, and commenting.
3. user blueprint for user profile and user-specific interactions such as viewing and updating preferences and accessing personalized recommendations.
# Q5 
## Describe what will be stored/retrieved from MongoDB:
Login information such as username and password will be kept. Profile pics will be included as well. Reviews will also be included which will include the time and content of the review.
# Q6 
## Describe what Python package or API you will use and how it will affect the user experience:
Spotify API, allow for catalog of information such as songs and genre information. # 388J-Final
