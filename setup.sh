#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# docker
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg --yes
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# setup
chmod +x $SCRIPT_DIR/setup.sh
chmod +x $SCRIPT_DIR/start.sh
chmod +x $SCRIPT_DIR/restart.sh
chmod +x $SCRIPT_DIR/stop.sh

ln -s "$SCRIPT_DIR/start.sh" /usr/bin/start_im_productive_bot
ln -s "$SCRIPT_DIR/restart.sh" /usr/bin/restart_im_productive_bot
ln -s "$SCRIPT_DIR/stop.sh" /usr/bin/stop_im_productive_bot
