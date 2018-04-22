# CSE6242Team13
**CSE6242 Group Project for Team13**


**Description:**

This is the repository for Team 13 for Data Visualization CSE6242 at the Georgia Institue of Technology. All code in this repository deals with analyzing and visualizing pediatric prevalence and cost data in the United States.

**Installation:**

Our code does not require any installation to run. All dependencies should be in the repository.

**Execution:**

To run the regression, simply open a terminal and naviagate to the folder containing the script "regression_code.py" (it should be the head folder of the repository), and type the command:

<p align="center"> <b>python regression_code.py</b> </p>

To run the visualization, navigate to the src folder and run 'pediatric_disease_map.html'


**If you wish to contribute:**

If you wish to contribute data to enhance our analysis and visualization, navigate to the data folder. 

Rename the directory with the data you wish to add to the year of the claims from the data and place it in either the Cost or Prevalence directory depending on what type of data you are contributing. (For example, if you have a directory with cost data for 2013 for all 25 diseases, rename the directory to 2013 and place this directory in the Data/Cost directory.) 

After you have added the data, you simply need to rerun the regression file using the same command as above. 

To update the visualization with the new dataset, you can use the "Data Prep.xlsx" file (instructions included in the file) to generate the input csv files for the visualization code. Now navigate to the src folder and open the 'pediatric_disease_map.html'. Add the year to the array named 'yearNum' on line 54 so that our visualization knows to display that year.
