export PYTHONV=$(python -V 2>&1 | awk '{print $2}' | cut -f1,2 -d.)
