import imaplib
import logging
import email
from email.header import decode_header

def connect_to_gmail_imap(user="sovintomaailmassa@gmail.com", password="nyax yhqt nbln iyxw"):
    imap_url = 'imap.gmail.com'
    try:
        with imaplib.IMAP4_SSL(imap_url) as imap:
            imap.login(user, password)
            status, messages = imap.select('inbox')
            typ, nums = imap.search(None, "FROM no-reply@senko.digital")
            print(nums)
            nums_list = nums[0].split()
            if not nums_list:
                print("Нет писем в папке")
                return
            msgs = []
            for num in nums_list:
                typ, data = imap.fetch(num, '(RFC822)')
                msgs.append(data)
            for msg_id in msgs:
                msg = email.message_from_bytes(msg_id[0][1])

                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes) and encoding is not None:
                    subject = subject.decode(encoding)

                print("Subject:", subject)
                print("From:", msg["From"])
                print(msg.get_payload(decode=True).decode('utf-8',errors='replace'))
                print("Date:", msg["Date"], '\n')
    except Exception as e:
        logging.error("Connection failed: {}".format(e))
        raise

connect_to_gmail_imap()

