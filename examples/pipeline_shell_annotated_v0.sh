#!/usr/bin/env bash
set -euo pipefail

# Example: annotated shell import for AutoAppDev.
# Only "# AAPS:" comment lines are extracted; normal shell code is ignored.

echo "hello from shell (ignored by importer)"

# AAPS: AUTOAPPDEV_PIPELINE 1
# AAPS:
# AAPS: TASK {"id":"t1","title":"Annotated shell import demo"}
# AAPS:
# AAPS: STEP {"id":"s1","title":"Plan","block":"plan"}
# AAPS: ACTION {"id":"a1","kind":"note","params":{"text":"Imported from # AAPS: comments."}}
# AAPS:
# AAPS: STEP {"id":"s2","title":"Work","block":"work"}
# AAPS: ACTION {"id":"a1","kind":"run","params":{"cmd":"echo work"}}

echo "done (ignored by importer)"

