# Introduction
This project uses Graham's formula to calculate an intrinsic value for various company tickers based on the current yield, 
earnings per share for the company and its predicted growth rate over the next 5 years. 
We compare this to the current value of the stock (at opening) to understand whether the stock is overpriced, underpriced 
or accurately priced. 
Our software is programmed to fetch relevant numbers, calculate the intrinsic value and send an email with the ticker 
symbols, current values, intrinsic values, and difference every day 5 minutes after opening. 

We get the necessary values from the Yahoo Finance website. Our project is made using an AWS EC2 instance linux server,
AWS SES, python and crontab. 

# Instructions
To run this project we need to make a couple installations. Run the following commands to have the project up and running!

1. Install Python 3.11.4

2. Download all folders from this repository. 

3. Install Python Packages:
You need to install some packaged to run the python code. Use this command to run the installation. 

   > pip install -r requirements.txt

4. Create email template: 
Assuming you are using an AWS EC2 instance linux server, to send a templated email via AWS SES you need to create a template using the AWS CLI. Run the following command to create the template.

   > aws ses create-template --cli-input-json  file://dynamictabletemplate.json

5. Set up a cronjob. 