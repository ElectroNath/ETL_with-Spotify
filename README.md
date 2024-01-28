# Spotify Data ETL Project

## Overview

This project is designed to extract recently played tracks from your Spotify account, transform the data into a structured format, and load it into a SQLite database for further analysis. It uses the Spotify API for data extraction and SQLAlchemy for database interaction.

## Table of Contents

- [Background](#background)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Background

This project is part of my journey in data engineering, where I encountered challenges with Spotify authentication. The use of the Authorization Code PKCE method adds an extra layer of security, ensuring a safe and reliable authentication process. Additionally, a Chrome driver is utilized to automate the authorization steps.

## Prerequisites

Before you begin, ensure you have the following prerequisites:

- Python 3.x installed
- Chrome browser installed
- Spotify Developer account with a registered application

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your_username/spotify-data-etl.git


2. Navigate to the project directory:

    ```bash
    cd spotify-data-etl

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt

## Usage

1. Obtain your Spotify Developer credentials (Client ID, Redirect URI) and create a .env file in the project directory:

    ```env
    CLIENT_ID=your_client_id
    REDIRECT_URI=http://localhost:8080

2. Run the ETL process:

    ```bash
    python main.py

3. Follow the instructions to perform the authorization in your browser.

4. Once authorized, the data will be extracted, transformed, and loaded into a SQLite database.

## Troubleshooting

If you encounter any issues during the authorization process or data extraction, refer to the following resources:

- For Spotify-related issues, consult the [Spotify API Documentation](https://developer.spotify.com/documentation/).
- For Selenium and Chrome driver-related issues, check the [Selenium Documentation](https://www.selenium.dev/documentation/en/) and [ChromeDriver Documentation](https://sites.google.com/chromium.org/driver/).


## Contributing

Contributions are welcome! If you find any improvements or issues, please open an [issue](https://github.com/your_username/spotify-data-etl/issues) or submit a [pull request](https://github.com/your_username/spotify-data-etl/pulls).

## Acknowledgments

- **Karolina Sowinka**: Project inspiration and insights from the Data Appreciation Society [YouTube Channel](https://www.youtube.com/c/DataAppreciationSociety).
- **Imdad Ahad**: Demystifying OAuth concepts on the Imdad Codes [YouTube Channel](https://www.youtube.com/c/ImdadCodes).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

