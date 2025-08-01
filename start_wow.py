import argparse
from os import environ
import subprocess

from server_code import start_server

REQUIRED_ENVVARS = [
    'SERVER_BIN_PATH',
    'WOW_EXE_PATH'
]

"""
There are three key types of creatures being set here:
    - Normal
    - Elite
    - WORLDBOSS
we set multipliers for their different stats such as Damage, SpellDamage, HP
"""
PROFILES = {
    'solo': {
        'Mangosd_Rate_Creature_Normal': "1",
        'Mangosd_Rate_Creature_Elite_Elite': ".2",
        'Mangosd_Rate_Creature_Elite_RAREELITE': ".25",
        'Mangosd_Rate_Creature_Elite_WORLDBOSS': "1"
    },

    '5-man': {
        'Mangosd_Rate_Creature_Normal': ".25",
        'Mangosd_Rate_Creature_Elite_Elite': ".25",
        'Mangosd_Rate_Creature_Elite_WORLDBOSS': "1"
    },

    '10-man': {
        'Mangosd_Rate_Creature_Normal': ".1",
        'Mangosd_Rate_Creature_Elite_Elite': ".125",
        'Mangosd_Rate_Creature_Elite_WORLDBOSS': ".12"
    },

    '20-man': {
        'Mangosd_Rate_Creature_Normal': ".04",
        'Mangosd_Rate_Creature_Elite_Elite': ".04",
        'Mangosd_Rate_Creature_Elite_WORLDBOSS': ".04"
    },

    '40-man': {
        'Mangosd_Rate_Creature_Normal': ".025",
        'Mangosd_Rate_Creature_Elite_Elite': ".025",
        'Mangosd_Rate_Creature_Elite_WORLDBOSS': ".025"
    }
}

def check_envvar_set(v):
    try:
        environ[v]

    except KeyError:
        print(f"ERROR: Make sure to set env var {v}.")
        exit(1)

def parse_args():
    parser = argparse.ArgumentParser(description="Mode to set up server with.")
    parser.add_argument(
        "-m", "--mode",
        type=str,
        required=True,
        help="Specify the mode ('solo', '5-man', '10-man', '20-man', '40-man')"
    )
    return parser.parse_args().mode

def configure_mangosd(mode: str) -> dict:
    # returns dict representing envvars to use for server
    env = environ.copy()

    for (k, v) in PROFILES[mode].items():
        for stat in ("Damage", "SpellDamage", "HP"):
            env[f"{k}.{stat}"] = v

    return env

def start_wow_client():
    return subprocess.Popen(
        ["wine", f"{environ['WOW_EXE_PATH']}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

if __name__ == '__main__':
    map(check_envvar_set, REQUIRED_ENVVARS)
    mode = parse_args()
    env = configure_mangosd(mode)
    realmd_proc, mangos_proc = start_server(env)
    start_wow_client()
