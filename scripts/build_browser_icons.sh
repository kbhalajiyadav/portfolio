#!/usr/bin/env bash
set -euo pipefail

source_svg="static/media/bk-monogram-canonical-20260730.svg"
output_dir="static/media"

command -v rsvg-convert >/dev/null 2>&1 || {
  echo "librsvg is required to build browser icons." >&2
  exit 1
}
command -v convert >/dev/null 2>&1 || {
  echo "ImageMagick is required to build the ICO file." >&2
  exit 1
}

temporary_dir="$(mktemp -d)"
trap 'rm -rf "$temporary_dir"' EXIT

render_png() {
  local size="$1"
  local destination="$2"
  rsvg-convert --width "$size" --height "$size" \
    --output "$destination" "$source_svg"
}

mkdir -p "$output_dir"
for size in 16 32 48 64; do
  render_png "$size" "$temporary_dir/icon-${size}.png"
done
cp "$temporary_dir/icon-32.png" "$output_dir/bk-browser-32-20260730-v6.png"
render_png 180 "$output_dir/bk-apple-touch-20260730-v6.png"
render_png 192 "$output_dir/bk-app-192-20260730-v6.png"
render_png 512 "$output_dir/bk-app-512-20260730-v6.png"

convert \
  "$temporary_dir/icon-16.png" \
  "$temporary_dir/icon-32.png" \
  "$temporary_dir/icon-48.png" \
  "$temporary_dir/icon-64.png" \
  "$output_dir/bk-browser-20260730-v6.ico"
