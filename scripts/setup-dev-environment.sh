#!/usr/bin/env bash
source scripts/utils.sh
echo ""
echo "Creating virtual environment and installing dependencies:"
echo ""

app=$(parse_app_option "$@")
app_post_string="_requirements.txt"
app_requirements="${app}${app_post_string}"
echo "App requirements: $app_requirements"

dnf list installed "libnsl" &> /dev/null || (echo "Installerer 'libnsl'" && sudo dnf install libnsl --assumeyes)

rm -rf .venv/* && \
  python3.11 -m venv .venv && \
  source .venv/bin/activate && \
  pip3 install pip --upgrade && \
  pip3 install -r $app_requirements &&

source .venv/bin/activate
echo ""
echo "Done creating dev-environment."
