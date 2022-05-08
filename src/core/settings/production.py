import os
from .base import *

# For security and performance reasons, DEBUG is turned off
DEBUG = env.bool("DEBUG", default=False)

# Amazon S3
USE_S3 = env.bool("USE_S3", default=False)

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    # s3 static settings
    STATIC_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
    STATICFILES_STORAGE = "api_base.services.storage.StaticStorage"
    # s3 public media settings
    MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "api_base.services.storage.MediaStorage"
else:
    # Static file
    STATIC_ROOT = join(BASE_DIR, "static")
    STATIC_URL = "/static/"
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "dist", "static"),
    ]
    # Media files
    MEDIA_ROOT = join(BASE_DIR, "media")
    MEDIA_URL = "/media/"
    MEDIA_IMAGE = f"{CUSTOM_DOMAIN}"

    # Upload storage
    DEFAULT_FILE_STORAGE = "binary_database_files.storage.DatabaseStorage"
    DB_FILES_AUTO_EXPORT_DB_TO_FS = False
    DATABASE_FILES_URL_METHOD = "URL_METHOD_2"

# Webpack
WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "dist/",
        "STATS_FILE": os.path.join(BASE_DIR, "webpack-stats.json"),
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}
