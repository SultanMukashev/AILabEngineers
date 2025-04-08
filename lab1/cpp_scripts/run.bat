@echo off
cmake --build build
echo Running load_postgres.exe...
.\build\Debug\load_postgres.exe
echo Running s3_uploads.exe...
.\build\Debug\s3_uploader.exe
pause