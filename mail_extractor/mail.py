import os
import email
from email import policy
from email.parser import BytesParser

mail_path = "mail.eml"
output_path = "attachments/"

def main():
    with open(mail_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    for part in msg.iter_attachments():
        if part.get_content_type() == "application/pdf":
            data = part.get_payload(decode=True)
            pdf_filename = part.get_filename()
            
            if pdf_filename is None:
                pdf_filename = "data.pdf"

            with open(os.path.join(output_path, pdf_filename), "wb") as pdf_file:
                pdf_file.write(data)

            print(f"PDF file extracted: {os.path.join(output_path, pdf_filename)}")

if __name__ == "__main__":
    main()