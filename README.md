# Ionos Python test Challenge
## Intro:
### Objective
- The idea of this project is to create a command line application to run some tests, extract  data about the run and store it in a Database.

### Motivation
- The test is a challenge of a selection process and was proposed to the position of python test.

## Documentation:  
  
- To run the tests you first need to start the database:  
```docker-compose up -d```

- To make it easier for the program to run, change the permissions levels on the file:  
```chmod 755 main.py```

- After that you are Ready to Go! 
- To use the application, run on the terminal:  
```./main.py --run```
- If you need to query the info from the database, just run:  
```./main.py --query```