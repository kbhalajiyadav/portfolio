---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
lastmod: {{ .Date }}
draft: true
summary: ""
tags: []
# Add the public copies only after syndication succeeds.
# syndication:
#   - name: LinkedIn
#     url: https://www.linkedin.com/posts/...
#   - name: Bluesky
#     url: https://bsky.app/profile/.../post/...
---

Write the canonical note here. Publish this URL first; syndicate only after it is live.
