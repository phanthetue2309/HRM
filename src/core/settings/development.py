import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

STATIC_ROOT = join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "dist", "static"),
]

# MEDIA related settings
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
        "BUNDLE_DIR_NAME": "",
        "STATS_FILE": os.path.join(BASE_DIR, "webpack-stats.json"),
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}
