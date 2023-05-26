import os, subprocess

PYTHON_NAME = "python3.11" if os.name == "posix" else \
    "python"
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS", "0.0.0.0")
SERVER_PORT = os.getenv("SERVER_PORT", 8000)


def call_django_command(args: object, post_args: list) -> None:
    local_args = args[:]
    local_args += post_args
    process = subprocess.Popen(local_args)
    process.communicate()


def check_db(args, post_args: list, database: str, seconds: int = None, attempts: int = None):
    local_args = args[:]

    local_args += post_args
    local_args += [database]

    if seconds:
        local_args += ["--seconds", seconds]
    if attempts:
        local_args += ["--attempts", attempts]

    process = subprocess.Popen(local_args)
    process.communicate()

    exit_code = process.returncode

    print(f"The task has returned exit code {exit_code}")

    if exit_code > 0:
        return False

    return True


if __name__ == '__main__':
    pre_args = [PYTHON_NAME, os.path.join(os.getenv('APP_HOME', os.getcwd()), "manage.py")]

    check_db_result = check_db(pre_args, post_args=["checkdb", "--database"], database="default")

    if check_db_result or bool(int(os.getenv('DEBUG', 1))):
        call_django_command(pre_args, ["migrate"])
        call_django_command(pre_args, ["createsuperuser",
                                       "--username",
                                       os.getenv('DJANGO_SUPERUSER_USERNAME', "admin"),
                                       "--noinput", "--email",
                                       os.getenv('DJANGO_SUPERUSER_EMAIL', "admin@example.com")])
        call_django_command(pre_args, ["collectstatic", "--noinput", "--clear"])
        call_django_command(pre_args, ["createtasks"])
        call_django_command(pre_args, ["addlocations"])
        call_django_command(pre_args, ["addcars"])

        run_server = subprocess.Popen(
            ("gunicorn", "core.wsgi:application",
             f"--bind={SERVER_ADDRESS}:{SERVER_PORT}", "--workers=6", "--threads=6")
        )
        run_server.communicate()
