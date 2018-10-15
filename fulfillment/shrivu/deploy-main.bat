@echo off
gcloud functions deploy get_time_open --runtime python37 --trigger-http
gcloud functions describe get_time_open
pause