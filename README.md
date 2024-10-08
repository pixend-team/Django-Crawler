# Dynamic Web Scraping App

This Django application allows users to dynamically scrape web pages using specified HTML XPaths and keys, and save the results in the database. Users can access, view, download, and delete their scraped data. The scraping functionality is powered by a Scrapy spider.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Using the Application](#using-the-application)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features
- Dynamic web scraping using user-specified HTML XPaths
- Save scraped data to the database
- View, download, and delete scraped data
- User authentication and management


## Installation
1. Clone the repository:
```sh
git clone https://github.com/pixend-team/Django-Crawler.git
cd Django-Crawler
```
2. Install the Required Packages:
```sh
pip install -r requirements.txt
```

4. Apply migrations to create a database and create a superuser:
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Usage

### Running the Application
1. Run the Server
```sh
python manage.py runserver
```

2. The application will be accessible at `http://localhost:8000`.

### Using the Application
1. **Sign Up**: Create a new account.
2. **Log In**: Log in to your account.
3. **Scrape Data**: Navigate to the scraper page, enter the URL, keys, and XPaths, and start scraping.
4. **View Data**: Go to your profile to view the scraped data.
5. **Download Data**: Download the data as CSV or JSON.
6. **Delete Data**: Delete any scraped data you no longer need.

## Screenshots
- **Home Page**: ![Screenshot from 2024-08-03 16-44-01](https://github.com/user-attachments/assets/4014dee3-6fab-4679-9057-60f70236f35f)
- **Scraper Page**: ![Screenshot from 2024-08-03 16-49-52](https://github.com/user-attachments/assets/f95784d4-e702-49b6-94ed-6cf7208e7b12)
- **Profile Page**: ![Screenshot from 2024-08-03 16-50-01](https://github.com/user-attachments/assets/1b9033e4-56eb-4b04-af9b-a10e82cec568)


## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
