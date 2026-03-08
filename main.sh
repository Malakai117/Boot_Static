echo "Starting python script..."

python3 src/main.py

echo "Starting HTML Server on localhost:8888"

cd public && python3 -m http.server 8888

