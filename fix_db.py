import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tropicana_backend.settings')
django.setup()

from django.db import connection

sql_commands = [
    "ALTER TABLE api_configsite ADD COLUMN IF NOT EXISTS telephone_raw varchar(20) DEFAULT '+22901000000'",
    "ALTER TABLE api_configsite ADD COLUMN IF NOT EXISTS tiktok_url varchar(200) DEFAULT ''",
    "ALTER TABLE api_configsite ADD COLUMN IF NOT EXISTS facebook_url varchar(200) DEFAULT ''",
    "ALTER TABLE api_configsite ADD COLUMN IF NOT EXISTS description_footer text DEFAULT ''",
    "ALTER TABLE api_configsite ADD COLUMN IF NOT EXISTS prix_affiche varchar(50) DEFAULT 'des 1000 FCFA'",
    "ALTER TABLE api_configsite ADD COLUMN IF NOT EXISTS prix_mini varchar(50) DEFAULT '1000 FCFA'",
    "ALTER TABLE api_configsite ADD COLUMN IF NOT EXISTS paiements varchar(200) DEFAULT 'MTN Money'",
    "ALTER TABLE api_configsite ADD COLUMN IF NOT EXISTS email varchar(254) DEFAULT ''",
]

with connection.cursor() as cursor:
    for sql in sql_commands:
        try:
            cursor.execute(sql)
            print(f"OK: {sql[:60]}")
        except Exception as e:
            print(f"SKIP: {e}")

print("Done!")
