import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv # <-- Tambahkan ini

# Wajib dipanggil agar bisa membaca .env
load_dotenv() 

def send_otp_email(user_email, otp_code):
    sender_email = "batik.flyyy@gmail.com"
    # Pastikan di dalam .env nama variabelnya adalah EMAIL_PASSWORD (huruf besar semua)
    sender_password = os.getenv("EMAIL_PASSWORD") 

    msg = MIMEMultipart()
    msg['From'] = "BatikFly Support <batik.flyyy@gmail.com>"
    msg['To'] = user_email
    msg['Subject'] = "Kode Verifikasi OTP BatikFly"
    msg['X-Mailer'] = "BatikFly-System"

    body = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
        <h2>Halo User BatikFly,</h2>
        <p>Gunakan kode verifikasi berikut untuk menyelesaikan pendaftaran Anda:</p>
        <h1 style="color: #2e6c80; font-size: 36px;">{otp_code}</h1>
        <p>Kode ini hanya berlaku selama 5 menit. Jangan berikan kepada siapa pun.</p>
    </div>
    """
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error mengirim email: {e}")
        return False