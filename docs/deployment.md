# Deployment

Build the image and run:

```bash
docker build -t opspilot:0.1 .
docker run --rm -p 8000:8000 opspilot:0.1
```

The container runs the CLI health check by default; run the FastAPI app when developing.
