@echo off
echo [INFO] Starting NHS ETL Automation with Conda...

REM Initialize Conda (this is required for bat files)
CALL C:\UoS_Lab\Anaconda\Scripts\activate.bat

REM Activate your Conda environment
cd C:\UoS_Lab\Jobs\Projects\NHS_Data_Projects\NHSAandE_Performance_Analysis_and_Forecasting
CALL conda activate ./nhs_env

REM Start Docker container
cd C:\UoS_Lab\Jobs\Projects\NHS_Data_Projects\NHSAandE_Performance_Analysis_and_Forecasting\notebooks
docker-compose up -d

REM Wait for PostgreSQL to be ready
echo [INFO] Waiting for PostgreSQL to initialize...
timeout /t 10 > nul

REM Run the Python ETL script
cd C:\UoS_Lab\Jobs\Projects\NHS_Data_Projects\NHSAandE_Performance_Analysis_and_Forecasting\notebooks
python NHSAandE_data_ETL.py > etl_log.txt 2>&1

REM Stop Docker container after ETL is complete
cd C:\UoS_Lab\Jobs\Projects\NHS_Data_Projects\NHSAandE_Performance_Analysis_and_Forecasting\notebooks
docker-compose down

echo [INFO] ETL process completed successfully!
pause

exit