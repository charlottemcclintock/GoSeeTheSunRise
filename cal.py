from pyicloud import PyiCloudService
from dotenv import load_dotenv
import os

if __name__=="__main__":
  load_dotenv('.env')
  
  USERNAME = os.environ.get("USERNAME")
  PASSWORD = os.environ.get("PASSWORD")
  api = PyiCloudService('rohit.musti.rm@gmail.com', '9n3n7m%$mzbbf87PL#PVmdnk$I3^&wf')
  if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input("Enter the code you received of one of your approved devices: ")
        result = api.validate_2fa_code(code)
        print(f"Code validation result: {result}")

