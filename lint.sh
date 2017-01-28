#!/usr/bin/bash

# remove trailing whitespace
find . -name "*.py" | xargs sed -i '' -e's/[ ^I]*$//'

# lint project
pylint monopoly > linting_report.txt

echo "project linted"
