#!/bin/python
import os
import subprocess
import getpass

def get_current_user_idle_time():
  current_user = getpass.getuser()
  idle_time = None

  terminal = os.ttyname(0)

  # Run the 'w' command to get the list of logged-in users and their idle times
  w_output = subprocess.check_output(['w']).decode().strip().split('\n')

  for i, line in enumerate(w_output):
    if i > 1:
      parts = line.split()
      if len(parts) >= 5 and parts[0] == current_user and \
        terminal.endswith(parts[1]):
        idle_time = parts[4]
  return idle_time

if __name__ == "__main__":
  idle_time = get_current_user_idle_time()
  if idle_time is not None:
    print(f"Current user's idle time: {idle_time}")
  else:
    print("User not found or not idle.")
