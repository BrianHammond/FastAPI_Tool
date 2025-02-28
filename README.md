I'm still learning Python and using these as reference guides for any employment opportunities and future projects.

I'm experimenting with FastAPI.

For documentation run the program and go to 127.0.0.1:8000/docs

If you want to run this on your local machine just click on run.bat to run the program, the bat file will install fastapi and uvicorn if they are not already installed on your system and start the application.

Redis is used as a database, this FastAPI tool is configured to use 127.0.0.1 but you can just change the IP depending on your system.

Tested working with [Redis Cloud](https://redis.io/cloud/)

The docker-compose.yaml builds the FastAPI tool and includes Redis for easy testing.
```bash
docker-compose up
```

Best Regards,<br/>
Brian
