# audio-sharing

Simple Python Django + HTML + vanilla JS application for recording and sharing audio

- This project is configured to be deployed on *Heroku*: https://www.heroku.com/
- Audio recording is done by using https://github.com/higuma/web-audio-recorder-js



# Some environment variables we should pay attention to

- `SECRET_KEY`: make sure it's different between development and production
- `DJANGO_SETTINGS_MODULE`: for this project, it should be `commons.settings.dev` for development and `commons.settings.prod` for production
- `ALLOWED_HOSTS`: Read Django's Doc: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts