# AnimeDownloader

It consists of 2 files: **anime.py** and **anime.db**.
The first one is the Python script that performs the anime downloading, the second one is the database (SQLite3) that contains the anime's download links. You can easily access it and add new animes by using *SQLiteStudio. There are 3 columns in it:

- *name*: is the name of the anime (since it has to be typed, abbreviations are used, i.e. *Mob Psycho 100* is ```mob```).
- *num*: is the episode number counter.
- *link*: is the link. Links must be of the following pattern: ```https://www.someting_1.something_2/something_3/..../animename_animenumber.extension```. And ```something_i``` must be constant throughout all the episodes.

To download an anime you have to open the command prompt inside the directory where *animedl.py* and *anime.db*, and then you have 3 options:

- if you want to download a new episode (or new episodes) after the last one you've already downloaded (for example the last *One Piece* episode):

      animedl.py name number
    
  For example:

      animedl.py onepiece 1

  downloads ```1``` new episode of One Piece after the last one you've already downloaded (of course you can download more than one episode, actually it was the main purpose of this code).

- if you want to download a specific episode but you don't want to update it on the database:

      animedl.py .name number

  For example:

      animedl.py .onepiece 125

- if you want to download a specific episode and you want to update it on the database:

      animedl.py !name number

  For example:

      animedl.py !onepiece 125
