import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8002, reload=True)
