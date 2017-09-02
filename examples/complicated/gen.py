import sys
import json
import time

for i in range(5):
    print(json.dumps({"message": "stderr", "i": i}), file=sys.stderr)
    sys.stderr.flush()
    print(json.dumps({"message": "stdout", "i": i}))
    sys.stdout.flush()
    time.sleep(0.05)
