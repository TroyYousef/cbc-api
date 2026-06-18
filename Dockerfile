FROM python:3.10-slim

# تثبيت poppler-utils لمعالجة ملفات PDF
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# تحديد مجلد العمل
WORKDIR /app

# إنشاء مجلد الرفع وإعطاؤه الصلاحيات
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

# نسخ وتثبيت الاعتماديات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# تشغيل التطبيق على بورت 7860 (الخاص بـ Hugging Face)
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
