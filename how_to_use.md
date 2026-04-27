In order to properly use this repository, do the following:
1. Create database using the create_db.sql file
2. Load data into the database using dataload.py. 

   -> Be use to put in database credentials so that way the data is able to be bulk loaded.
   
  -> All of the data has already been preprocessed and should insert smoothly, if any problems arise,
     run preprocess.py to ensure that the files were preprocessed as intended, and then try again.
     
4. While in app.py, put in database credentials and then run the file using streamlit run app.py.
  -> If streamlit isn't already installed in program, install using the instructions at the top of the file
