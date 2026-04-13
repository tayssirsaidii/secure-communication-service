import uvicorn
from pathlib import Path# نستعملو Path باش نتعاملو مع مسارات الفايلات بطريقة سهلة
# نحددو مسار ملفات الشهادة والمفتاح
CERT_FILE = Path("certs/cert.pem")
KEY_FILE = Path("certs/key.pem")
# دالة باش تتأكد إلي الفايلات موجودين وماهمش فارغين
def check_certificates(cert_file: Path, key_file: Path):
    if not cert_file.exists() or not key_file.exists():
          # إذا واحد من الملفين مش موجود، نرمي خطأ ونوقّف الكود
        raise FileNotFoundError("TLS certificate or key file not found.")
    if cert_file.stat().st_size == 0 or key_file.stat().st_size == 0:
         # إذا واحد منهم فارغ، زادة نرمي خطأ
        raise ValueError("Certificate or key file is empty.")
# ننفذو التحقق قبل ما نبدؤو السيرفر
check_certificates(CERT_FILE, KEY_FILE)
# نجهزو إعدادات الـ SSL باش نعطيوها للسيرفر
ssl_options = {
    "ssl_certfile": str(CERT_FILE), # ملف الشهادة (cert.pem)
    "ssl_keyfile": str(KEY_FILE)# المفتاح الخاص (key.pem)
}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # <import path
        host="0.0.0.0",
        port=8443,
        reload=True,
        **ssl_options# نمررو الإعدادات متاع TLS للسيرفر
    )
