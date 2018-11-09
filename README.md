# austin-projects

Miscellaneous personal programming/data projects done on my free time

## Kaggle

### PUBG Finish Placement Prediction

My current version of the Jupyter notebook used as a submission for the 'PUBG Finish Placement Prediction' Kaggle competition. Used over 5 million entries of game data to predict player placement given their game statistics. Used a LightGBM model to achieve a Mean Absolute Error score of 0.0432 (for targets from 0-1). Currently placed in top 37% (ongoing competition).

## Melee

### StreamFriend.py

A python file to continuously check a tournament on smash.gg for its stream queue, then export the currently streamed tournament round and player names to text files. These text files can be easily used by OBS for stream overlay purposes.

### basedpy.py

A python file to scrape smash.gg API data to compile a comprehensive set history for any given player on smash.gg. Enter your tag and the URL extension of any tourney you have entered (e.g. waveshine-infinite-12), and the script will export 2 csv files. One with singles results and one with doubles results. Details included are date, tournament, opponent, set count, and round.
