# Purrfect Companions
## Video Demo: https://youtu.be/lUz-MKkcFyE
## Description:
Purrfect Companions is a website designed for the final project of CS50x. It serves as a platform where users can either upload cat adoption posts or find and adopt a cat.

The project is made with HTML, CSS, JavaScript, Python (Flask) and a little bit of SQL.
When a user enters the website for the first time he is redirected to a sign up page where the user needs to fill in a username and password. If any field is empty, the username is taken or the password does not match the confirmation, an error is displayed accordingly.
The password is hashed using a bcrypt libray and will be stored in database.

After the sign up is completed, the user is redirected to the log in section where as well, if any field is empty or the password does not match the set password, an error is displayed.
Next, the home page is shown where the user can select one or more filters for location, age and gender. Each filter option is generated automatically using an SQL querry.

After the filters are set an SQL querry is made based on the user's selection and a page with all the cat adoption posts is displayed.
The user can add cats to the favourites section by pressing the "Add to favourites" button. Using JavaScript an array is made and the cats' IDs are added to it if it is not already there.
By pressing the "View details" a querry is run and the cat information is fetched using the cat's ID.
If the "Adopt" button is pressed the user is notified that he adopted the cat and a querry is made to remove the cat info from the database.

The Favourites page is generated by the IDs that are stored in the favourites IDs. To remove the ID from the array the "Remove from favourites" button needs to be pressed and the ID will be deleted.

The user can then log out.

## Personal Info
Boerescu Constantin [costi.boerescu14@gmail.com](costi.boerescu14@gmail.com)
