from flask_apscheduler import APScheduler
import os

sched = APScheduler()


@sched.authenticate
def authenticate(auth: dict) -> bool:
    """Check auth."""
    return auth["username"] == os.getenv(
        "SCHEDULER_USERNAME", "admin"
    ) and auth["password"] == os.getenv("SCHEDULER_PASSWORD", "admin")
