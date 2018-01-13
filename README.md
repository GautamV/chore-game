A text-message based Heroku / Twilio app to track and display chore data (who's doing what and how often) in a house/apartment. 

To use, deploy this code to a new Heroku project. Provision a Heroku Postgres database for the project. Sign up for a free Twilio account, purchase a number (free trials available), and set your Twilio webhooks to your Heroku urls.

Currently available commands (executed by texting your Twilio number):

add user <user_name> : adds a new user with the phone number used to send the text

add chore <chore_name> : adds a new chore category

add instance <chore_name> : records that the user associated with the phone number used to send the text did the specified chore


stats all [<num_days>] : returns stats for all chores for the past num_days days. if num_days is not given, returns stats for all time
stats <chore_name> [<num_days>] : returns stats for the specified chore for the past num_days days. if num_days is not given, returns stats for all time
