import json
import sys
from datetime import datetime

import requests

URL = sys.argv[1]
IMAGE_PATHS = sys.argv[2:]
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJuZXR6YmV3ZWlzLmNvbSIsImF1ZCI6ImFwaS5uZXR6YmV3ZWlzLmNvbSIsIm5hbWUiOiJqdXJ4cGVydC1leHRlbnNpb24tY29kZSIsInR5cGUiOiJwcm9kIiwianRpIjoianVyeHBlcnQtY29kZS0wMSIsImlhdCI6MTY2MjA3MTk3NiwiZXhwIjoxNjc3NjIzOTc2LCJyZWZlcnJlciI6WyJjaHJvbWUtZXh0ZW5zaW9uOi8vbmxtam5sb2VsaGJmYXBmaWRhcGFqanBpZGJhaG9vcGIiLCJjaHJvbWUtZXh0ZW5zaW9uOi8vamtma2prZmlnbWFpZGhjYW1kam9jYmhvbmtta21kYWQiXSwiZW1haWwiOiJ5b3VyQG1vbS55ZWV0Iiwib25seUNvZGVzIjp0cnVlfQ.idcL5Womu_YVYgwNr3-TCM5V_eOveEiy25W7_TkVs9k"

now = datetime.now()
registerPayload = {
    "url": URL,
    "extensionVersion": "1.4.4",
    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "dto": now.isoformat(),
    "clientLanguage": "de-DE",
    "clientTime": now.isoformat(),
    "extensions": []
}

resp = requests.post(
    "https://api.netzbeweis.com/v1/extension/registerEvidenceCollection",
    headers={
        "Authorization": "Bearer " + TOKEN,
        "Origin": "chrome-extension://nlmjnloelhbfapfidapajjpidbahoopb"
    },
    data=json.dumps(registerPayload),
)
resp.raise_for_status()

collection_id = resp.json()["uuid"]

for i, image_path in enumerate(IMAGE_PATHS):
    resp = requests.post(
        f"https://api.netzbeweis.com/v1/extension/{collection_id}/submitEvidence",
        headers={
            "Authorization": "Bearer " + TOKEN,
            "Accept": "application/json",
            "Origin": "chrome-extension://nlmjnloelhbfapfidapajjpidbahoopb"
        },
        files={
            "image": ("blob", open(image_path, "rb").read(), "image/png"),
        },
        data={
            "evidenceData": json.dumps({
                "numY": i,
                "numX": 0,
                "totalY": len(IMAGE_PATHS),
                "totalX": 1,
                "evidenceType": "partOfPageScreenshot"
            }),
        }
    )
    resp.raise_for_status()

resp = requests.post(
    f"https://api.netzbeweis.com/v1/extension/{collection_id}/finishSubmission",
    headers={
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/json",
        "Origin": "chrome-extension://nlmjnloelhbfapfidapajjpidbahoopb"
    },
    data=json.dumps({})
)
resp.raise_for_status()

submission_code = resp.json()["code"]

print(f"Images submitted successfully with code: {submission_code}")
