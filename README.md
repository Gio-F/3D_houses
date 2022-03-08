# 3D_houses

##### Description

Provided with a postal address address, using LIDAR data available online , build a 3D model of the area

The project is executed using the following resources:
- *LIDAR data* of "Digitaal Hoogtemodel Vlaanderen II" available at the following links:
    - [DSM](https://www.geopunt.be/download?container=dhm-vlaanderen-ii-dsm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DSM,%20raster,%201m)
    - [DTM](https://www.geopunt.be/download?container=dhm-vlaanderen-ii-dtm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DTM,%20raster,%201m)
- *AGIV Geolocation API* [v4](http://loc.geopunt.be/)

##### Pre-requisites
      
     - Python            3.8.1
   
     - Numpy             1.22.2
   
     - Rasterio          1.2.10
   
     - Plotly            5.6.0
   
     - Streamlit         1.7.0
   
     - Internet Connection
      
     
##### Installation and Usage
 
*Jupyter Notebook* : the program can be ran directly in Jupyter Notebook using the file "API to plot.ipynb". It allows to visualize the 3D model of the area selected based on the input address directly on your browser.
  
*Terminal* : use `$ streamlit run 'API to plot w Streamlit.py'` (file available in this repo) to run the program from your terminal and visualize the plot on browser thanks to Streamlit. You will see the message "You can now view your Streamlit app in your browser." followed by the http address you need to copy in your browser address bar.


In both cases:

- The file paths are hardcoded. Before running the program, please:

  - Change the path for new_j_all_bounds.json to match the location on your machine (file available in this repo);
  - Change the paths for "file_path_dtm" and "file_path_dsm" to match the folder where you want to download the files on your machine.
  
- Ensure to type full address includng ZIP code in French or Dutch (ex. "Zeedijk 261, 8370 Blankenberge" )


   
##### Visuals

Example of a 3D plot visualization. The image can be rotated, zoomed in and out, etc.

![newplot(5)](https://user-images.githubusercontent.com/90340959/157256017-407efde0-a8d3-448d-b8af-4b2fc3e96562.png)
![newplot(4)](https://user-images.githubusercontent.com/90340959/157256020-1b6f49fd-b234-4b2e-840e-dcc9cce77ed1.png)


##### ToDo
 
 Remove hardcoded paths;
 Error handling (ex. file already downloaded, timeout, ...);
 Account for edge cases (e.g. property is between 2 files).
 
 
##### Context

This project is part of my training as Junior AI developer at BeCode (Belgium)


