from kace import kace
import os
import sys
import redis
import time
import subprocess
import json
import argparse
import requests




def runme(command):
  commandlist = command.split(" ")
  result = subprocess.run(commandlist, capture_output=True)
  payload = {"returncode": result.returncode, "stdout": result.stdout.decode(), "stderr": result.stderr }
  return payload

def main():
    parser = argparse.ArgumentParser(description="Eat your Kace", usage="kace <action> \n\n \
                                     options:\n  \
                                     netbox    Run kace to update netbox  \n  \
                                     ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup netbox')
    args = parser.parse_args()
    token=os.getenv("NBTOKEN")
    url=os.getenv("NBURL")

    if args.action[0] == "netbox":
      kace.kace()



   





