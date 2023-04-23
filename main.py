import pickle
from pathlib import Path

import streamlit_authenticator as stauth

# names = ["Aishworyann", "Khushal", "Shrey", "Vibhor"]
# usernames = ["aish", "kjain", "skansal", "bhurr"]
# passwords = ["gaandbhai", "kirthbkl", "bhoshrey", "bhurr@123"]

hashed_passwords = stauth.Hasher(['aish', 'bhoshrey']).generate()
print(hashed_passwords)
# file_path = Path(__file__).parent / "hashed_pw.pkl"
# with file_path.open("wb") as file:
#     pickle.dump(hashed_passwords, file)