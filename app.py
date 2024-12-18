from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
import logging
from datetime import datetime
import schedule
import time
from calendar import month_name
from dateutil.relativedelta import relativedelta
import argparse

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_next_months():
    current_date = datetime.now()
    next_month = current_date + relativedelta(months=1)
    two_months = current_date + relativedelta(months=2)
    return current_date, next_month, two_months


def create_month_mapping(current, next_month, following_month):
    months_full = {
        month_name[current.month]: month_name[next_month.month],
        month_name[next_month.month]: month_name[following_month.month],
    }

    months_short = {
        month_name[current.month][:3]: month_name[next_month.month][:3],
        month_name[next_month.month][:3]: month_name[following_month.month][:3],
    }

    return {**months_full, **months_short}


def get_month_replacements():
    current, next_month, following_month = get_next_months()
    return create_month_mapping(current, next_month, following_month)


def load_credentials(token_path):
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            return pickle.load(token)
    return None


def save_credentials(creds, token_path):
    with open(token_path, 'wb') as token:
        pickle.dump(creds, token)


def refresh_credentials(creds, token_path):
    try:
        creds.refresh(Request())
        save_credentials(creds, token_path)
        return creds
    except:
        return None


def get_new_credentials(scopes, token_path):
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
    creds = flow.run_local_server(port=0)
    save_credentials(creds, token_path)
    return creds


def authenticate():
    token_path = 'token.pickle'
    scopes = ['https://www.googleapis.com/auth/documents']

    creds = load_credentials(token_path)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds = refresh_credentials(creds, token_path)

        if not creds:
            creds = get_new_credentials(scopes, token_path)

    return creds


def create_replace_request(old_word, new_word):
    return {
        'replaceAllText': {
            'containsText': {'text': old_word, 'matchCase': True},
            'replaceText': new_word,
        }
    }


def process_text_element(text, replacements):
    requests = []
    for old_word, new_word in replacements.items():
        if old_word in text:
            requests.append(create_replace_request(old_word, new_word))
    return requests


def get_document_content(service, document_id):
    document = service.documents().get(documentId=document_id).execute()
    return document.get('body', {}).get('content', [])


def update_google_doc(document_id, replacements):
    try:
        creds = authenticate()
        service = build('docs', 'v1', credentials=creds)
        content = get_document_content(service, document_id)

        requests = []
        for item in content:
            if 'paragraph' not in item:
                continue

            for element in item['paragraph'].get('elements', []):
                if 'textRun' not in element:
                    continue

                text = element['textRun'].get('content', '')
                requests.extend(process_text_element(text, replacements))

        if requests:
            service.documents().batchUpdate(
                documentId=document_id, body={'requests': requests}
            ).execute()
            logging.info(f"Updated {len(requests)} instances in document")
            return True

        logging.info("No matching words found")
        return True

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return False


def parse_arguments():
    parser = argparse.ArgumentParser(description='Google Docs Month Updater')
    parser.add_argument('--doc-id', required=True, help='Google Document ID')
    parser.add_argument('--run-once', action='store_true', help='Run once and exit')
    parser.add_argument(
        '--schedule-day', type=int, default=15, help='Day of month to run'
    )
    parser.add_argument(
        '--schedule-time', default='00:00', help='Time to run in HH:MM format'
    )
    return parser.parse_args()


def run_task(document_id):
    replacements = get_month_replacements()
    logging.info(f"Replacing months with: {replacements}")
    return update_google_doc(document_id, replacements)


def main():
    args = parse_arguments()

    if args.run_once:
        success = run_task(args.doc_id)
        exit(0 if success else 1)

    schedule.every().month.at(args.schedule_time).do(run_task, args.doc_id)
    logging.info(
        f"Scheduler started. Running on day {args.schedule_day} at {args.schedule_time}"
    )

    while True:
        if datetime.now().day == args.schedule_day:
            schedule.run_pending()
        time.sleep(3600)


if __name__ == '__main__':
    main()
