
from .base import * # noqa: F403


if ENVIRONMENT == "production":  # noqa: F405
    from .production import *  # noqa: F403
elif ENVIRONMENT == "test": # noqa: F405
    from .test import * # noqa: F403
else:
    from .dev import * # noqa: F403
