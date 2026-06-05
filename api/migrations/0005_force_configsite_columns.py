from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0004_alter_alertestock_options_alter_articleblog_options_and_more'),
    ]
    operations = [
        migrations.RunSQL(
            sql="""
            DO $$ BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='api_configsite' AND column_name='telephone_raw') THEN
                    ALTER TABLE api_configsite ADD COLUMN telephone_raw varchar(20) DEFAULT '+22901000000' NOT NULL;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='api_configsite' AND column_name='tiktok_url') THEN
                    ALTER TABLE api_configsite ADD COLUMN tiktok_url varchar(200) DEFAULT '' NOT NULL;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='api_configsite' AND column_name='facebook_url') THEN
                    ALTER TABLE api_configsite ADD COLUMN facebook_url varchar(200) DEFAULT '' NOT NULL;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='api_configsite' AND column_name='description_footer') THEN
                    ALTER TABLE api_configsite ADD COLUMN description_footer text DEFAULT '' NOT NULL;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='api_configsite' AND column_name='prix_affiche') THEN
                    ALTER TABLE api_configsite ADD COLUMN prix_affiche varchar(50) DEFAULT 'dès 1 000 FCFA' NOT NULL;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='api_configsite' AND column_name='prix_mini') THEN
                    ALTER TABLE api_configsite ADD COLUMN prix_mini varchar(50) DEFAULT '1 000 FCFA' NOT NULL;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='api_configsite' AND column_name='paiements') THEN
                    ALTER TABLE api_configsite ADD COLUMN paiements varchar(200) DEFAULT 'MTN Money,Moov Money' NOT NULL;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='api_configsite' AND column_name='email') THEN
                    ALTER TABLE api_configsite ADD COLUMN email varchar(254) DEFAULT '' NOT NULL;
                END IF;
            END $$;
            """,
            reverse_sql="",
        ),
    ]
