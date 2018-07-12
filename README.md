# mv-scraper

This script generates a music video dataset.

The goal is to provide a list of:

Title, Artist, Billboard Rankings & Date, Lyrics, Youtube Link, Likes, Dislikes, Views, Date Uploaded, Number of Comments, Date Updated

# Installation

This project requires the following dependencies to be installed:

[PyLyrics fork](https://github.com/charlesverdad/PyLyrics) - This fork has better chance of returning lyrics
[Billboard-charts fork](https://github.com/charlesverdad/billboard-charts) - This fork can parse year-end charts.

To install the dependencies, run

```
pip install -r requirements.txt
```

# Using the script

```
python scraper.py
```
