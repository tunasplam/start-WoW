"""
Everything that has to do with starting the server
"""

from os import environ, setsid
import subprocess
import time

def start_server(env: dict):

    if not db_service_active():
        start_db_service()

    realmd_proc = subprocess.Popen(
        ["./realmd"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=environ['SERVER_BIN_PATH'],
        env=env,
        preexec_fn=setsid
    )

    mangos_proc = subprocess.Popen(
        ["./mangosd"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=environ['SERVER_BIN_PATH'],
        env=env,
        preexec_fn=setsid
    )

    print("Waiting to give mangosd some time. You may need to wait longer if you have playerbots enabled.")
    time.sleep(120)
    return (realmd_proc, mangos_proc)

def start_db_service(timeout=10):
    print("Starting MariaDB service...")
    result = subprocess.run(
        ["systemctl", "start", "mariadb"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False
    )
    time.sleep(2)

    if result.returncode != 0:
        print("ERROR: Failed to start mariadb service:")
        exit(1)

    wait_for_service_start()

def wait_for_service_start(timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        if db_service_active():
            return True
    print("ERROR: Mariadb service timed out!")
    exit()

def db_service_active() -> bool:
    # returns True if mariadb service is running
    try:
        result = subprocess.run(
            ["systemctl", "is-active", "mariadb"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        return result.stdout.strip() == "active"

    except Exception as e:
        print(f"Error checking service status: {e}")
        return False

