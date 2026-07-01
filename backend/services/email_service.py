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
    
def send_reset_password_email(user_email, token):
    sender_email = "batik.flyyy@gmail.com"
    sender_password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = "BatikFly Support <batik.flyyy@gmail.com>"
    msg["To"] = user_email
    msg["Subject"] = "Reset Password BatikFly"
    msg["X-Mailer"] = "BatikFly-System"

    body = f"""
    <div style="
        font-family: Arial, sans-serif;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fafafa;
    ">

        <h2 style="color:#2e6c80;">
            Reset Password BatikFly
        </h2>

        <p>
            Kami menerima permintaan untuk mengatur ulang password akun Anda.
        </p>

        <p>
            Gunakan <b>Token Reset Password</b> berikut pada aplikasi BatikFly:
        </p>

        <div style="
            background:#F4B400;
            color:#000;
            font-size:28px;
            font-weight:bold;
            text-align:center;
            padding:18px;
            border-radius:8px;
            letter-spacing:2px;
            margin:20px 0;
        ">
            {token}
        </div>

        <p>
            Token ini hanya berlaku selama <b>15 menit</b>.
        </p>

        <p>
            Buka aplikasi BatikFly, kemudian masuk ke halaman
            <b>Reset Password</b> dan masukkan token di atas.
        </p>

        <hr>

        <small>
            Jika Anda tidak meminta reset password,
            abaikan email ini.
        </small>

    </div>
    """

    msg.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print(f"Error mengirim email reset password: {e}")
        return False