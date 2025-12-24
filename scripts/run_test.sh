#!/bin/bash

# Find all test files
TEST_FILES=($(find tests -name "test_*.py" -o -name "*_test.py" | sort))

if [ ${#TEST_FILES[@]} -eq 0 ]; then
    echo "No test files found."
    exit 0
fi

echo "Available test files:"
for i in "${!TEST_FILES[@]}"; do
    echo "$((i+1)). ${TEST_FILES[$i]}"
done

echo ""
read -p "Enter the number of the test file to run: " choice

if [[ ! "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt "${#TEST_FILES[@]}" ]; then
    echo "Invalid selection."
    exit 1
fi

SELECTED_FILE=${TEST_FILES[$((choice-1))]}
echo "Running: pytest $SELECTED_FILE -v -s"
python -m pytest "$SELECTED_FILE" -v -s
