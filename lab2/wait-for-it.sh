
host=$(echo $1 | cut -d: -f1); port=$(echo $1 | cut -d: -f2); timeout=${2:-60}
for ((i=0;i<timeout;i++)); do
  (echo > /dev/tcp/$host/$port) >/dev/null 2>&1 && exit 0
  sleep 1
done
echo "Timeout waiting for $host:$port"; exit 1
