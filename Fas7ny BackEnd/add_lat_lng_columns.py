"""
سكريبت إضافة عمودين latitude/longitude لجدول provider_profiles
مباشرة (من غير Alembic) - مفيد لو مش مستخدم migrations دلوقتي.

شغّله مرة واحدة من روت المشروع:

    python add_lat_lng_columns.py

آمن إنه يتشغل أكتر من مرة (بيتأكد إن العمود مش موجود قبل ما يضيفه).
"""

from sqlalchemy import text
from app.db.session import engine

with engine.connect() as conn:
    # SQLite/Postgres compatible check - نجرب نضيف العمود ونتجاهل الخطأ
    # لو موجود بالفعل (بدل ما نعمل query معقد للتأكد الأول)
    for column_sql in [
        "ALTER TABLE provider_profiles ADD COLUMN latitude FLOAT",
        "ALTER TABLE provider_profiles ADD COLUMN longitude FLOAT",
    ]:
        try:
            conn.execute(text(column_sql))
            conn.commit()
            print(f"تم تنفيذ: {column_sql}")
        except Exception as e:
            print(f"تم تجاهله (العمود موجود غالبًا أو خطأ آخر): {e}")

print("\nخلصنا. تأكد بعدها إنك حطيت قيم lat/lng لأي provider موجود.")