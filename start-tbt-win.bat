@echo off

rem Installing the tbt project in your environment
echo “Installing the tbt project in your environment”
pip install -e .

rem Check if the database directory (instance) exists
if exist instance\ (
  echo "Database already exists, skipping initialization."
) else (
  rem Initializing the database
  echo “Initializing the database”
  flask --app tbt init-db
)

rem Starting the tbt application
echo “Starting the tbt application”
flask --app tbt run

rem Application access information
echo “To access the application, navigate to http://127.0.0.1:5000”

rem Installing the tbt project in your environment
echo “To shut your server down, use the 'fg' command to bring the flask application process into the foreground.”
echo “Press CTRL+C to quit.”
echo "You can also close and terminate your terminal window."

pause