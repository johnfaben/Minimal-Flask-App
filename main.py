from app import app

app.run(
      host = "0.0.0.0", # or 127.0.0.1 (DONT USE LOCALHOST)
      port = 8080,
      debug = True
)

