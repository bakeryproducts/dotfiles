#!/bin/bash
# Install Iosevka Nerd Font

FONT_DIR="$HOME/.local/share/fonts"
FONT_URL="https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/Iosevka.zip"
TMP_FILE="/tmp/Iosevka.zip"

mkdir -p "$FONT_DIR"

echo "Downloading Iosevka Nerd Font..."
wget -q --show-progress "$FONT_URL" -O "$TMP_FILE"

echo "Installing fonts..."
unzip -o "$TMP_FILE" -d "$FONT_DIR"

echo "Updating font cache..."
fc-cache -fv "$FONT_DIR"

rm "$TMP_FILE"

echo "Done. Iosevka Nerd Font installed."
echo ""
echo "Add to alacritty.toml:"
echo '  [font.normal]'
echo '  family = "Iosevka Nerd Font"'
