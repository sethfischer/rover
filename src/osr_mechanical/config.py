"""Configuration."""

from datetime import datetime

now = datetime.today()


COPYRIGHT_OWNER = "Seth Fischer"
DOCUMENTATION_URL = "https://osr.fischer.nz/"
LICENCE = "MIT License"
PROJECT_HOST = "osr.fischer.nz"
PROJECT_NAME = "sethfischer-osr"
PROJECT_URL = f"https://{PROJECT_HOST}"
REPO_URL = "https://github.com/sethfischer/osr"
SHORT_DESCRIPTION = "Alternative body for the NASA JPL Open Source Rover."
LONG_DESCRIPTION = (
    f"Final assembly of {PROJECT_NAME}, a quarter-scale Mars rover. "
    f"See <{PROJECT_URL}>. "
    "Based on NASA-JPL's Perseverance Mars Rover."
)

COPYRIGHT_NOTICE = f"(c) {now.strftime('%Y')} {COPYRIGHT_OWNER}; Licence: {LICENCE}"
