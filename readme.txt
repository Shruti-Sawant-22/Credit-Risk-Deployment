# create conda enviroment
> conda create --name deployment python=3.6

# activate the conda env and install libraries 
> conda activate deployment
> pip install -r requirements.txt 

# deactivate the enviroment
> conda deactivate 



### Heroku deployment steps

1.	Activate the environment and install all the libraries 
2.	Cd to project repositories 
3.	Create Heroku account
4.	Install gunicorn and Heroku cls
	https://devcenter.heroku.com/articles/heroku-cli#download-and-install
5.	Install and setup git
6.	Create Heroku application
7.	Restart the computer 
8.	Make sure you have install gunicorn==20.0.4
9.	Create requirements.txt file 
10.	Create Procfile 
11.	Create new app on Heroku
12.	Use Heroku cli command from browser
13.	Push and install to Heroku app 
14. wait till you get the verify msg 


