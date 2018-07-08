#!/bin/bash

source $HOME/.nix-profile/etc/profile.d/nix.sh
echo "Starting subshell with Nix Python packages enabled, exit when done."

nix-shell -p python27Packages.matplotlib \
          -p python27Packages.virtualenv \
          -p python27Packages.jsonnet \
          -p python27Packages.click 

echo "Exiting Nix Python enabled subshell"

