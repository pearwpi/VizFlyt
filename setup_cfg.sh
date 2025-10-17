#!/bin/bash

# Check if VIZFLYT_PATH is set
if [ -z "$VIZFLYT_PATH" ]; then
    echo "❌ Error: VIZFLYT_PATH is not set."
    exit 1
fi

# Define the full Python path
PYTHON_EXEC="$VIZFLYT_PATH/.vizflyt/bin/python"

# Generate setup.cfg
cat > $VIZFLYT_PATH/vizflyt_ws/src/vizflyt/setup.cfg <<EOF
[develop]
script_dir=\$base/lib/vizflyt
[install]
install_scripts=\$base/lib/vizflyt
[build_scripts]
executable = $PYTHON_EXEC
EOF

echo "✅ setup.cfg generated with:"
echo "executable = $PYTHON_EXEC"
