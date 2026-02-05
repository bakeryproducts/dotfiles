#!/bin/bash
# Install Alacritty on Debian/Ubuntu

set -e

echo "Installing Alacritty..."
sudo apt-get update
sudo apt-get install -y alacritty

echo "Done. Alacritty installed."
echo ""
echo "Config location: ~/.config/alacritty/alacritty.toml"
