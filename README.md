# autotake-food24

Automate process calculation of Intake24 data with the HEIFA scoring.
Purpose of this project is to reduce the time taken to calculate the recal
of a single survey.

## Steps involved

**Uploading files**: Upload and clean the raw files of Intake24 and HEIFA-related files.

**Processing files**: Extract the important pieces of information required for the calculations.

**Calculating the serves**: Calculate the serves, per survey ID, for each of the food groups involved. \
In addition, find the total of the main groups and sub-groups. \
Example of main group: Vegetables \
Example of sub-groups: Vegetables/Green, Vegetables/Cruciferous

**Conversion to HEIFA scores**: Convert the serves to the respective HEIFA scores, based on range and gender. \
In addition, sum up all the HEIFA scores, based on gender.

**Writing to CSV file**: Write the HEIFA scores and serve sizes to a CSV file for further analysis.

## Website

Website link: https://autotake-food24.streamlit.app/
