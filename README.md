BookFinder
1.	Background 
Many people find it difficult to find books that suit their taste, especially when the information is scattered among different sources such as online bookstores, libraries and personal recommendations. Today, users have to go through many websites to find a book that suits them, read reviews or find out more details about books.
 A central web system can provide an efficient solution, make it easier for users to search for books, and enable a rich and intuitive user experience.
2.	The purpose of the project
The goal of Book finder is to create an interactive website that brings together information about books from different sources. The website will allow users to: find books quickly and easily according to parameters such as the book's name, author, genre or year of publication.
 In addition, the website will be able to display detailed information about books including a summary, image, ratings and reviews. Saving books to a personal reading list and sharing site recommendations will also provide site administrators with tools to manage data quality and track user activity.
       3.     System description
3.1 The nature of the application
3.1.1. The website application will be developed using Web technologies (Django).
3.1.2. Information sources: integration of external APIs such as Google Books, in addition, the option of manually entering books by users or administrators will be provided
3.1.3 Database: Using MySQL to manage books, users and reviews data.
3.2 System users
3.2.1 Regular user - Only registered users will be able to view book details, add opinions, view ratings, reviews and save favorite books.
One will also be able to search for books according to various parameters such as book name, author and genre and will be able to see ratings and review
3.2.2 Manager - adding, editing or removing books entered by users, user management (blocking, deleting) and tracking user activity reports.
3.2.3 Bot - will collect information from external sources (websites, etc.), will be able to enter new books and will also be able to analyze and organize the data to create an up-to-date and reliable database.
Each participant will be identified by: e-mail and password.
3.3 List of website capabilities
3.3.1 The basic component of the website will be a book search engine
3.3.2 The website will allow users to register and connect to the system, it will also allow unregistered users to view the site.
3.3.3 The website will allow users to add book data by book name, author, abstract, genre, year of publication and a picture of the cover (up to 15 MG).
3.3.4 The website will authorize unregistered users to view the books in a detailed manner: book name, author, summary, genre, rating, year of publication, image of the cover and reviews .
3.3.5 The website will allow users to query the database and display it on the website according to the following parameters:
3.3.5.1 Name of the book.
3.3.5.2 Author 
3.3.5.4 Genre.
3.3.6 The website will allow the administrator to delete information from the database and manage the users. (deletion, blocking, etc.) In addition, he will be able to track user reports.
3.3.7 The website will allow the bot to enter new books (by searching the Internet) and it will also analyze and organize the data to create an up-to-date and reliable database. The bot will analyze the information, filter duplicate books, and enter accurate data into the system.
3.3.8 The website will allow the user to see his data such as: favorite books (only for registered users).


3.6.1.5 Saving special data
The database will also have the option of saving links to images of the book covers (URL to the image on an external or internal server).
Ability to save genres or categories of books. and information about the availability of the books.
(optional): for example, books that are in stores, public libraries or available online
Optional - option to tag books (for example: "bestseller", "classic book", or "award winner") to facilitate filtering and searching.
3.6.1.5 Special values
Book categories: categories by genre (for example: fantasy, novel, children's literature, non-fiction, etc.). 
Rating: values from 1 to 5. 
Publication year: Publication year format: Saving the publication year in. YYYY format
Format of abstract: The abstract of the book will be kept in short text up to 500 words.


 Yuval Betito 
