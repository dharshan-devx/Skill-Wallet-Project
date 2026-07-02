import urllib.request
import urllib.parse
import threading
import time
import subprocess
import sys

def test_prediction():
    # Wait for server to start
    time.sleep(4)
    print("Testing /result endpoint...")
    
    # 30 features
    features = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
    
    # Mock data
    data = {f: "0.5" for f in features}
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    
    try:
        req = urllib.request.Request("http://127.0.0.1:5000/result", data=encoded_data)
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            print(f"Status Code: {response.status}")
            
            if "Prediction Result" in html:
                print("SUCCESS: Endpoint responded with Prediction Result HTML!")
                if "Credit Card Approved" in html or "Credit Card Rejected" in html:
                    print("SUCCESS: Found valid status in response.")
                else:
                    print("FAILED: Could not find Approved/Rejected text.")
                    sys.exit(1)
            else:
                print("FAILED: 'Prediction Result' not found in response HTML.")
                sys.exit(1)
            
    except Exception as e:
        print(f"FAILED: Exception occurred during test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Running end-to-end verification...")
    
    # Start the server as a subprocess
    server_process = subprocess.Popen([sys.executable, "app.py"])
    
    try:
        test_prediction()
    finally:
        print("Terminating server...")
        server_process.terminate()
        server_process.wait()
    
    print("Verification completed successfully.")
