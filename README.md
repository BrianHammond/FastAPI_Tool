I'm still learning Python and using these as reference guides for any employment opportunities and future projects.

I'm experimenting with FastAPI.

For documentation run the program and go to 127.0.0.1:8000/docs

uvcorn.run is included in main.py so you don't have to run it separtely.

If you want to run this on your local machine just click on run.bat to run the program, the bat file will install fastapi and uvicorn if they are not already installed on your system and start the application.

Alternatively you can run this as a docker Container.
Build the docker image:
```bash
docker build -t fastapi .
```
Run the docker container in this example the name of the container will be fastapi:
```bash
docker run -d -p 8000:8000 --name fastapi fastapi

```

Best Regards,<br/>
Brian
