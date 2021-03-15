For my CS50W final project, I made a website that is similar to Yelp, on which one can search for restaurants in any city. To do so, I used APIs from a company called TomTom in order to receive the information about the restaurants and in order to geocode the city name into a latitude and longitude, which are required parameters for some of the APIs I used. To call the APIs, I used Python, and specifically used the requests.get() function, which is from the requests library. I also made a feature for users who are logged in to add restaurants to a saved list.

I believe my final project satisfies the distinctiveness and complexity requirements for several reasons. First of all, it utilizes Django (including two DJango models) on the back-end and JavaScript on the front-end, and is mobile-responsive. Second, it is not based on the old CS50W Pizza project, nor is it a social network/e-commerce site. Third, I believe my project is sufficiently distinct and more complex than the other projects, because 1) it has far more CSS than was needed for any of the other projects, 2) the APIs used are as a whole more complex, 3) the JavaScript is more complex, 4) is is built from scratch, without using Bootstrap, thus making the task more difficult. 

The following is a list of files I created for this project and what’s contained in each.

- api_key.txt: the API key
- secret_key.txt: the Django secret key
- Restaurant_Photos, Restaurants_Photos, Saved_Restaurants_Photos: folders to hold pictures for the restaurants

- layout.html and layout.css: the basic layout for each page of the website
- index.html and index.css: the homepage
- register.html, login,html, and register&login.css: the register and login pages
- profile.html and profile.css: the profile page for a signed in user
- results.html and results.css: the page that lists the restaurants returned by the API
- restaurant.html and restaurant_page.css: the page for one restaurant (after clicking on it on the results/profile page)
- about.html and about.css: the about page for the website

- add_or_remove.js: to add or remove a restaurant from a user's list
- change_nav_bar.js: to change the style of the nav bar when scrolling past or above a certain point
- index.js: to slide in the side nav bar on mobile
- results.js: to style the results.html page when there are no results from the API, and to activate the filters bar on mobile or on the no results page

- LogoMakr...pngs: for the logo
- no_image.png: for restaurants that don’t have an image

- admin.py: for registering the models for the Django admin interface
- models.py: the Django models
- urls.py: all the urls for the website
- views.py: all the Django views, and the Django Form classes

- .gitignore: files I wanted git to ignore and not upload to my github repository.

To run the website, one types in “python3 manage.py runserver” in the terminal, in the “finalproject” directory of my project.
(By the way, my project isn’t done yet, but I wanted to submit it early. I plan on continuing to work on it.)



