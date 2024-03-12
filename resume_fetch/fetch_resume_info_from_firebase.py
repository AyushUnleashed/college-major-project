import firebase_admin
from firebase_admin import credentials, firestore
import os
from firebase_admin import credentials, initialize_app
from firebase_admin import auth
# Initialize Firebase Admin SDK
absolute_path = "serviceAccountKey.json"
# absolute_path = os.path.join(os.getcwd(), relative_path)
cred = credentials.Certificate(absolute_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_uid_from_email(email):
    try:
        user = auth.get_user_by_email(email)
        uid = user.uid
        return uid
    except auth.UserNotFoundError:
        print("User with email {} not found.".format(email))
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def fetch_resume_data(email):
    uid = get_uid_from_email(email)
    
    if uid is None:
        raise Exception(f"User with email {email} not found.")
    
    try:
        resume_ref = db.collection('resume').document(uid).get()
    except Exception as e:
        raise Exception(f"Failed to retrieve resume document for UID {uid}: {e}")

    if not resume_ref.exists:
        raise Exception(f"Resume not found for user with email {email}")

    resume_data = resume_ref.to_dict()
    print(f"Resume data for user with email {email}: {resume_data}")

    generations_folder = 'generations'
    if not os.path.exists(generations_folder):
        try:
            os.makedirs(generations_folder)
        except OSError as e:
            raise Exception(f"Failed to create directory {generations_folder}: {e}")

    resume_filename = f"generations/{email}_resume.txt"

    try:
        with open(resume_filename, 'w', encoding='utf-8') as file:
            file.write(str(resume_data))
            print(f"Resume data for {email} saved to {resume_filename}")
    except IOError as e:
        raise Exception(f"Failed to write resume data to file {resume_filename}: {e}")
    
    return resume_data

if __name__ == "__main__":
    # Example usage:
    email = 'ayushyadavcodes@gmail.com'

    fetch_resume_data(email)

