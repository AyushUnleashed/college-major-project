import firebase_admin
from firebase_admin import credentials, firestore
import os
from firebase_admin import credentials, initialize_app
from firebase_admin import auth
# Initialize Firebase Admin SDK
relative_path = "credentials/serviceAccountKey.json"
absolute_path = os.path.join(os.getcwd(), relative_path)
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

def fetch_resume_data(email, role, company_name):
    try:
        # Step 1: Get the UID associated with the email
        uid = get_uid_from_email(email)
        
        if uid is None:
            print("User with email {} not found.".format(email))
            return
        
        # Step 2: Retrieve the resume document using the UID
        resume_ref = db.collection('resume').document(uid).get()
        if resume_ref.exists:
            resume_data = resume_ref.to_dict()
            # Process the retrieved resume data here
            print("Resume data for user with email {}: {}".format(email, resume_data))
        else:
            print("Resume not found for user with email {}".format(email))
    except Exception as e:
        print("An error occurred:", e)

# Example usage:
email = 'gate2024rank2@gmail.com'
role = 'Software Engineer'
company_name = 'Example Company'

fetch_resume_data(email, role, company_name)

