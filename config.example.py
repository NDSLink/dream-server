class Config:
    DEBUG = True
    USE_REDIS = True
    FLAGSMITH_KEY = ":)"
    SQLALCHEMY_DATABASE_URI = "sqlite:///victini.db"
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    DEV_USER_GSID = 0 # Don't allow GSIDs that decode to this to be interacted with
    DEV_USER_PASSWORD = "capybaras are cool"
    SECRET_KEY = """According to all known laws of aviation, there is no way a bee should be able to fly.
Its wings are too small to get its fat little body off the ground.
The bee, of course, flies anyway because bees don't care what humans think is impossible.
Yellow, black. Yellow, black. Yellow, black. Yellow, black.
Ooh, black and yellow!
Let's shake it up a little.
Barry! Breakfast is ready!"""  # yes that's the bee movie script. don't ask
