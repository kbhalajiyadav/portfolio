#!/usr/bin/env bash
set -euo pipefail

root_dir="static"
source_svg="$root_dir/favicon.svg"
output_dir="$root_dir/media"

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

# Stable root-level files are intentionally unversioned. Search engines cache
# favicon URLs independently, so keeping these paths fixed avoids stale icons.
cp "$temporary_dir/icon-48.png" "$root_dir/favicon-48.png"
render_png 180 "$root_dir/apple-touch-icon.png"
render_png 192 "$root_dir/icon-192.png"
render_png 512 "$root_dir/icon-512.png"
convert \
  "$temporary_dir/icon-16.png" \
  "$temporary_dir/icon-32.png" \
  "$temporary_dir/icon-48.png" \
  "$temporary_dir/icon-64.png" \
  "$root_dir/favicon.ico"

# Retain the previously published versioned files so existing browser caches
# and installed shortcuts continue to resolve while the stable URLs propagate.
cp "$temporary_dir/icon-32.png" "$output_dir/bk-browser-32-20260730-v6.png"
cp "$root_dir/apple-touch-icon.png" "$output_dir/bk-apple-touch-20260730-v6.png"
cp "$root_dir/icon-192.png" "$output_dir/bk-app-192-20260730-v6.png"
cp "$root_dir/icon-512.png" "$output_dir/bk-app-512-20260730-v6.png"
cp "$root_dir/favicon.ico" "$output_dir/bk-browser-20260730-v6.ico"
