# FestList v1.0

FestList is a web application that allows users to create, manage, and explore music festivals. Festival organizers can add festivals and their respective lineups, while users can browse festivals and RSVP make a collection of festivals they're interested in attending.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
      - [Back End Dependencies](#back-end-dependencies)
      - [Front End Dependencies](#front-end-dependencies)
    - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **User Authentication:** Users can register an account, log in, and manage their session.
- **Festival Management:** Organizers can create new festivals, edit details, and manage artist lineups.
- **RSVP Functionality:** Users can RSVP to festivals, and view a list of festivals they're attending.
- **Festival Browsing:** Explore a list of upcoming festivals and view details about each one, including their artist lineups.
- **OAuth Linking with Spotify:** Integrates authorization through a user's spotify account to pull artist data.
- **Playlist Generation (Coming Soon):** Future versions will allow users to generate a playlist through the spotify developers API from a festival lineup of each artist's top songs, and export them to their personal spotify account.

## Getting Started

FestList relies on a number of dependencies, all of which are included in the installation package.

### Prerequisites

#### Back End Dependencies:

- Python (v3.8.13)
- Node.js (v16.20.0)
- Flask
  - Flask-SQLAlchemy
  - Flask-Migrate
  - Flask-Restful
  - Flask-CORS
  - Flask-bcrypt
  - Flask-marshmallow
- Faker
- requests
- authlib
- Alive-Progress
- Marshmallow-SQLAlchemy

#### Front End Dependencies

- Formik
- Yup
- React
  - React-Bootstrap
  - React-Datepicker
  - React-dom
  - React-router-dom
  - React-Scripts

### Installation

1. Fork and/or clone the repository:
    ```bash
    git clone https://github.com/yourusername/FestList.git
    ```

2. Navigate to the project directory and install the required packages:
    ```bash
    # Install Pipenv and dependencies, generate migrations, populate databases
    pipenv install && pipenv shell
    cd FestList/server
    flask db upgrade head
    python3 seed.py
    ```

3. Start the backend server:
    ```bash
    # from the server directory in pipenv shell
    python3 app.py
    ```


5. Start the frontend server:
    ```bash
    # In a separate terminal, run
    npm install
    npm start --prefix client
    ```

## Usage

1. **Register/Login:** Begin by registering an account or logging in if you already have one.
2. **Link Spotify account:** after redirect, you'll see a blue button on the home splash page to link your spotify account (While not necessary, this is highly reccommended.)
3. **Creating a Festival:** Navigate to "Festivals" via the nav bar to browse festival lineups or create a new one.
4. **RSVP to a Festival:** When viewing a festival, click the RSVP button to indicate your interest in going
5. **View My Festivals:** Navigate to the "My Festivals" section to see a list of festivals you're attending and the ones you've created.
6. **Editing a Festival:** From the "My Festivals" page, click on either "Edit Festival Details" or "Edit Lineup".

## Contributing

If you wish to contribute to FestList, please first discuss the change you wish to make via an issue, email, or pull request before making a change.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to the incredible group of instructors at [Flatiron School](https://flatironschool.com/) for any and all assistance provided in the creation of this capstone project.
  - A special shoutout in particular to Tom Tobar, who helped me tackle OAuth with no prior knowledge with 3 hours of uninterrupted support on a weekend!
- Thanks to my wife for putting up with me typing away at my keyboard for 2 weeks straight to get this project where it is today.