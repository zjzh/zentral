# Generated by Django 2.2.18 on 2021-05-30 07:17

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid
import zentral.contrib.mdm.models


def delete_all_dep_enrollment_sessions(apps, schema_editor):
    DEPEnrollmentSession = apps.get_model("mdm", "DEPEnrollmentSession")
    DEPEnrollmentSession.objects.all().delete()


def set_enrollments_push_certificates(apps, schema_editor):
    PushCertificate = apps.get_model("mdm", "PushCertificate")
    DEPEnrollment = apps.get_model("mdm", "DEPEnrollment")
    OTAEnrollment = apps.get_model("mdm", "OTAEnrollment")
    UserEnrollment = apps.get_model("mdm", "UserEnrollment")
    try:
        push_certificate = PushCertificate.objects.all().order_by("-pk")[0]
    except IndexError:
        DEPEnrollment.objects.all().delete()
        OTAEnrollment.objects.all().delete()
        UserEnrollment.objects.all().delete()
    else:
        DEPEnrollment.objects.all().update(push_certificate=push_certificate)
        OTAEnrollment.objects.all().update(push_certificate=push_certificate)
        UserEnrollment.objects.all().update(push_certificate=push_certificate)


class Migration(migrations.Migration):

    dependencies = [
        ('realms', '0006_realmgroupmapping'),
        ('inventory', '0056_machine_snapshot_program_instances_on_delete_cascade'),
        ('mdm', '0034_auto_20200305_2328'),
    ]

    operations = [
        migrations.RunPython(delete_all_dep_enrollment_sessions),
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('type', models.CharField(choices=[('EnterpriseApp', 'Enterprise App'), ('Profile', 'Profile')], editable=False, max_length=64)),
                ('channel', models.CharField(choices=[('Device', 'Device'), ('User', 'User')], editable=False, max_length=64)),
                ('platforms', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('iOS', 'iOS'), ('iPadOS', 'iPadOS'), ('macOS', 'macOS'), ('tvOS', 'tvOS')], default=zentral.contrib.mdm.models.Platform.all_values, max_length=64), size=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('trashed_at', models.DateTimeField(editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArtifactVersion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('version', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('artifact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mdm.Artifact')),
            ],
        ),
        migrations.CreateModel(
            name='Blueprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlueprintArtifact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('install_before_setup_assistant', models.BooleanField(default=False)),
                ('auto_update', models.BooleanField(default=True)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('artifact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mdm.Artifact')),
                ('blueprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mdm.Blueprint')),
            ],
        ),
        migrations.CreateModel(
            name='DEPEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False, unique=True)),
                ('use_realm_user', models.BooleanField(default=False)),
                ('realm_user_is_admin', models.BooleanField(default=True)),
                ('admin_full_name', models.CharField(blank=True, max_length=80, null=True)),
                ('admin_short_name', models.CharField(blank=True, max_length=32, null=True)),
                ('admin_password_hash', django.contrib.postgres.fields.jsonb.JSONField(editable=False, null=True)),
                ('name', models.CharField(max_length=125, unique=True)),
                ('allow_pairing', models.BooleanField(default=False)),
                ('auto_advance_setup', models.BooleanField(default=False)),
                ('await_device_configured', models.BooleanField(default=False)),
                ('department', models.CharField(blank=True, max_length=125)),
                ('is_mandatory', models.BooleanField(default=True)),
                ('is_mdm_removable', models.BooleanField(default=False)),
                ('is_multi_user', models.BooleanField(default=True)),
                ('is_supervised', models.BooleanField(default=True)),
                ('language', models.CharField(blank=True, choices=[('aa', 'Afar'), ('ab', 'Abkhazian'), ('ae', 'Avestan'), ('af', 'Afrikaans'), ('ak', 'Akan'), ('am', 'Amharic'), ('an', 'Aragonese'), ('ar', 'Arabic'), ('as', 'Assamese'), ('av', 'Avaric'), ('ay', 'Aymara'), ('az', 'Azerbaijani'), ('ba', 'Bashkir'), ('be', 'Belarusian'), ('bg', 'Bulgarian'), ('bh', 'Bihari languages'), ('bi', 'Bislama'), ('bm', 'Bambara'), ('bn', 'Bengali'), ('bo', 'Tibetan'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan, Valencian'), ('ce', 'Chechen'), ('ch', 'Chamorro'), ('co', 'Corsican'), ('cr', 'Cree'), ('cs', 'Czech'), ('cu', 'Church Slavic, Old Slavonic, Church Slavonic, Old Bulgarian, Old Church Slavonic'), ('cv', 'Chuvash'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('dv', 'Divehi, Dhivehi, Maldivian'), ('dz', 'Dzongkha'), ('ee', 'Ewe'), ('el', 'Greek, Modern (1453-)'), ('en', 'English'), ('eo', 'Esperanto'), ('es', 'Spanish, Castilian'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('ff', 'Fulah'), ('fi', 'Finnish'), ('fj', 'Fijian'), ('fo', 'Faroese'), ('fr', 'French'), ('fy', 'Western Frisian'), ('ga', 'Irish'), ('gd', 'Gaelic, Scottish Gaelic'), ('gl', 'Galician'), ('gn', 'Guarani'), ('gu', 'Gujarati'), ('gv', 'Manx'), ('ha', 'Hausa'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('ho', 'Hiri Motu'), ('hr', 'Croatian'), ('ht', 'Haitian, Haitian Creole'), ('hu', 'Hungarian'), ('hy', 'Armenian'), ('hz', 'Herero'), ('ia', 'Interlingua (International Auxiliary Language Association)'), ('id', 'Indonesian'), ('ie', 'Interlingue, Occidental'), ('ig', 'Igbo'), ('ii', 'Sichuan Yi, Nuosu'), ('ik', 'Inupiaq'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('iu', 'Inuktitut'), ('ja', 'Japanese'), ('jv', 'Javanese'), ('ka', 'Georgian'), ('kg', 'Kongo'), ('ki', 'Kikuyu, Gikuyu'), ('kj', 'Kuanyama, Kwanyama'), ('kk', 'Kazakh'), ('kl', 'Kalaallisut, Greenlandic'), ('km', 'Central Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('kr', 'Kanuri'), ('ks', 'Kashmiri'), ('ku', 'Kurdish'), ('kv', 'Komi'), ('kw', 'Cornish'), ('ky', 'Kirghiz, Kyrgyz'), ('la', 'Latin'), ('lb', 'Luxembourgish, Letzeburgesch'), ('lg', 'Ganda'), ('li', 'Limburgan, Limburger, Limburgish'), ('ln', 'Lingala'), ('lo', 'Lao'), ('lt', 'Lithuanian'), ('lu', 'Luba-Katanga'), ('lv', 'Latvian'), ('mg', 'Malagasy'), ('mh', 'Marshallese'), ('mi', 'Maori'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('ms', 'Malay'), ('mt', 'Maltese'), ('my', 'Burmese'), ('na', 'Nauru'), ('nb', 'Bokmål, Norwegian, Norwegian Bokmål'), ('nd', 'Ndebele, North, North Ndebele'), ('ne', 'Nepali'), ('ng', 'Ndonga'), ('nl', 'Dutch, Flemish'), ('nn', 'Norwegian Nynorsk, Nynorsk, Norwegian'), ('no', 'Norwegian'), ('nr', 'Ndebele, South, South Ndebele'), ('nv', 'Navajo, Navaho'), ('ny', 'Chichewa, Chewa, Nyanja'), ('oc', 'Occitan (post 1500)'), ('oj', 'Ojibwa'), ('om', 'Oromo'), ('or', 'Oriya'), ('os', 'Ossetian, Ossetic'), ('pa', 'Panjabi, Punjabi'), ('pi', 'Pali'), ('pl', 'Polish'), ('ps', 'Pushto, Pashto'), ('pt', 'Portuguese'), ('qu', 'Quechua'), ('rm', 'Romansh'), ('rn', 'Rundi'), ('ro', 'Romanian, Moldavian, Moldovan'), ('ru', 'Russian'), ('rw', 'Kinyarwanda'), ('sa', 'Sanskrit'), ('sc', 'Sardinian'), ('sd', 'Sindhi'), ('se', 'Northern Sami'), ('sg', 'Sango'), ('si', 'Sinhala, Sinhalese'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sm', 'Samoan'), ('sn', 'Shona'), ('so', 'Somali'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('ss', 'Swati'), ('st', 'Sotho, Southern'), ('su', 'Sundanese'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('tg', 'Tajik'), ('th', 'Thai'), ('ti', 'Tigrinya'), ('tk', 'Turkmen'), ('tl', 'Tagalog'), ('tn', 'Tswana'), ('to', 'Tonga (Tonga Islands)'), ('tr', 'Turkish'), ('ts', 'Tsonga'), ('tt', 'Tatar'), ('tw', 'Twi'), ('ty', 'Tahitian'), ('ug', 'Uighur, Uyghur'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('uz', 'Uzbek'), ('ve', 'Venda'), ('vi', 'Vietnamese'), ('vo', 'Volapük'), ('wa', 'Walloon'), ('wo', 'Wolof'), ('xh', 'Xhosa'), ('yi', 'Yiddish'), ('yo', 'Yoruba'), ('za', 'Zhuang, Chuang'), ('zh', 'Chinese'), ('zu', 'Zulu')], max_length=3)),
                ('org_magic', models.CharField(blank=True, max_length=256)),
                ('region', models.CharField(blank=True, choices=[('AD', 'Andorra'), ('AE', 'United Arab Emirates'), ('AF', 'Afghanistan'), ('AG', 'Antigua and Barbuda'), ('AI', 'Anguilla'), ('AL', 'Albania'), ('AM', 'Armenia'), ('AO', 'Angola'), ('AQ', 'Antarctica'), ('AR', 'Argentina'), ('AS', 'American Samoa'), ('AT', 'Austria'), ('AU', 'Australia'), ('AW', 'Aruba'), ('AX', 'Åland Islands'), ('AZ', 'Azerbaijan'), ('BA', 'Bosnia and Herzegovina'), ('BB', 'Barbados'), ('BD', 'Bangladesh'), ('BE', 'Belgium'), ('BF', 'Burkina Faso'), ('BG', 'Bulgaria'), ('BH', 'Bahrain'), ('BI', 'Burundi'), ('BJ', 'Benin'), ('BL', 'Saint Barthélemy'), ('BM', 'Bermuda'), ('BN', 'Brunei Darussalam'), ('BO', 'Bolivia, Plurinational State of'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BR', 'Brazil'), ('BS', 'Bahamas'), ('BT', 'Bhutan'), ('BV', 'Bouvet Island'), ('BW', 'Botswana'), ('BY', 'Belarus'), ('BZ', 'Belize'), ('CA', 'Canada'), ('CC', 'Cocos (Keeling) Islands'), ('CD', 'Congo, Democratic Republic of the'), ('CF', 'Central African Republic'), ('CG', 'Congo'), ('CH', 'Switzerland'), ('CI', "Côte d'Ivoire"), ('CK', 'Cook Islands'), ('CL', 'Chile'), ('CM', 'Cameroon'), ('CN', 'China'), ('CO', 'Colombia'), ('CR', 'Costa Rica'), ('CU', 'Cuba'), ('CV', 'Cabo Verde'), ('CW', 'Curaçao'), ('CX', 'Christmas Island'), ('CY', 'Cyprus'), ('CZ', 'Czechia'), ('DE', 'Germany'), ('DJ', 'Djibouti'), ('DK', 'Denmark'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('DZ', 'Algeria'), ('EC', 'Ecuador'), ('EE', 'Estonia'), ('EG', 'Egypt'), ('EH', 'Western Sahara'), ('ER', 'Eritrea'), ('ES', 'Spain'), ('ET', 'Ethiopia'), ('FI', 'Finland'), ('FJ', 'Fiji'), ('FK', 'Falkland Islands (Malvinas)'), ('FM', 'Micronesia, Federated States of'), ('FO', 'Faroe Islands'), ('FR', 'France'), ('GA', 'Gabon'), ('GB', 'United Kingdom of Great Britain and Northern Ireland'), ('GD', 'Grenada'), ('GE', 'Georgia'), ('GF', 'French Guiana'), ('GG', 'Guernsey'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GL', 'Greenland'), ('GM', 'Gambia'), ('GN', 'Guinea'), ('GP', 'Guadeloupe'), ('GQ', 'Equatorial Guinea'), ('GR', 'Greece'), ('GS', 'South Georgia and the South Sandwich Islands'), ('GT', 'Guatemala'), ('GU', 'Guam'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HK', 'Hong Kong'), ('HM', 'Heard Island and McDonald Islands'), ('HN', 'Honduras'), ('HR', 'Croatia'), ('HT', 'Haiti'), ('HU', 'Hungary'), ('ID', 'Indonesia'), ('IE', 'Ireland'), ('IL', 'Israel'), ('IM', 'Isle of Man'), ('IN', 'India'), ('IO', 'British Indian Ocean Territory'), ('IQ', 'Iraq'), ('IR', 'Iran, Islamic Republic of'), ('IS', 'Iceland'), ('IT', 'Italy'), ('JE', 'Jersey'), ('JM', 'Jamaica'), ('JO', 'Jordan'), ('JP', 'Japan'), ('KE', 'Kenya'), ('KG', 'Kyrgyzstan'), ('KH', 'Cambodia'), ('KI', 'Kiribati'), ('KM', 'Comoros'), ('KN', 'Saint Kitts and Nevis'), ('KP', "Korea, Democratic People's Republic of"), ('KR', 'Korea, Republic of'), ('KW', 'Kuwait'), ('KY', 'Cayman Islands'), ('KZ', 'Kazakhstan'), ('LA', "Lao People's Democratic Republic"), ('LB', 'Lebanon'), ('LC', 'Saint Lucia'), ('LI', 'Liechtenstein'), ('LK', 'Sri Lanka'), ('LR', 'Liberia'), ('LS', 'Lesotho'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('LV', 'Latvia'), ('LY', 'Libya'), ('MA', 'Morocco'), ('MC', 'Monaco'), ('MD', 'Moldova, Republic of'), ('ME', 'Montenegro'), ('MF', 'Saint Martin (French part)'), ('MG', 'Madagascar'), ('MH', 'Marshall Islands'), ('MK', 'North Macedonia'), ('ML', 'Mali'), ('MM', 'Myanmar'), ('MN', 'Mongolia'), ('MO', 'Macao'), ('MP', 'Northern Mariana Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MS', 'Montserrat'), ('MT', 'Malta'), ('MU', 'Mauritius'), ('MV', 'Maldives'), ('MW', 'Malawi'), ('MX', 'Mexico'), ('MY', 'Malaysia'), ('MZ', 'Mozambique'), ('NA', 'Namibia'), ('NC', 'New Caledonia'), ('NE', 'Niger'), ('NF', 'Norfolk Island'), ('NG', 'Nigeria'), ('NI', 'Nicaragua'), ('NL', 'Netherlands'), ('NO', 'Norway'), ('NP', 'Nepal'), ('NR', 'Nauru'), ('NU', 'Niue'), ('NZ', 'New Zealand'), ('OM', 'Oman'), ('PA', 'Panama'), ('PE', 'Peru'), ('PF', 'French Polynesia'), ('PG', 'Papua New Guinea'), ('PH', 'Philippines'), ('PK', 'Pakistan'), ('PL', 'Poland'), ('PM', 'Saint Pierre and Miquelon'), ('PN', 'Pitcairn'), ('PR', 'Puerto Rico'), ('PS', 'Palestine, State of'), ('PT', 'Portugal'), ('PW', 'Palau'), ('PY', 'Paraguay'), ('QA', 'Qatar'), ('RE', 'Réunion'), ('RO', 'Romania'), ('RS', 'Serbia'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('SA', 'Saudi Arabia'), ('SB', 'Solomon Islands'), ('SC', 'Seychelles'), ('SD', 'Sudan'), ('SE', 'Sweden'), ('SG', 'Singapore'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('SI', 'Slovenia'), ('SJ', 'Svalbard and Jan Mayen'), ('SK', 'Slovakia'), ('SL', 'Sierra Leone'), ('SM', 'San Marino'), ('SN', 'Senegal'), ('SO', 'Somalia'), ('SR', 'Suriname'), ('SS', 'South Sudan'), ('ST', 'Sao Tome and Principe'), ('SV', 'El Salvador'), ('SX', 'Sint Maarten (Dutch part)'), ('SY', 'Syrian Arab Republic'), ('SZ', 'Eswatini'), ('TC', 'Turks and Caicos Islands'), ('TD', 'Chad'), ('TF', 'French Southern Territories'), ('TG', 'Togo'), ('TH', 'Thailand'), ('TJ', 'Tajikistan'), ('TK', 'Tokelau'), ('TL', 'Timor-Leste'), ('TM', 'Turkmenistan'), ('TN', 'Tunisia'), ('TO', 'Tonga'), ('TR', 'Turkey'), ('TT', 'Trinidad and Tobago'), ('TV', 'Tuvalu'), ('TW', 'Taiwan, Province of China'), ('TZ', 'Tanzania, United Republic of'), ('UA', 'Ukraine'), ('UG', 'Uganda'), ('UM', 'United States Minor Outlying Islands'), ('US', 'United States of America'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VA', 'Holy See'), ('VC', 'Saint Vincent and the Grenadines'), ('VE', 'Venezuela, Bolivarian Republic of'), ('VG', 'Virgin Islands, British'), ('VI', 'Virgin Islands, U.S.'), ('VN', 'Viet Nam'), ('VU', 'Vanuatu'), ('WF', 'Wallis and Futuna'), ('WS', 'Samoa'), ('XK', 'Kosovo'), ('YE', 'Yemen'), ('YT', 'Mayotte'), ('ZA', 'South Africa'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')], max_length=2)),
                ('skip_setup_items', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('Accessibility', 'Accessibility'), ('Android', 'Android'), ('Appearance', 'Appearance'), ('AppleID', 'AppleID'), ('Biometric', 'Biometric'), ('DeviceToDeviceMigration', 'DeviceToDeviceMigration'), ('Diagnostics', 'Diagnostics'), ('DisplayTone', 'DisplayTone'), ('FileVault', 'FileVault'), ('HomeButtonSensitivity', 'HomeButtonSensitivity'), ('iCloudDiagnostics', 'iCloudDiagnostics'), ('iCloudStorage', 'iCloudStorage'), ('iMessageAndFaceTime', 'iMessageAndFaceTime'), ('Location', 'Location'), ('MessagingActivationUsingPhoneNumber', 'MessagingActivationUsingPhoneNumber'), ('OnBoarding', 'OnBoarding'), ('Passcode', 'Passcode'), ('Payment', 'Payment'), ('Privacy', 'Privacy'), ('Restore', 'Restore'), ('RestoreCompleted', 'RestoreCompleted'), ('ScreenSaver', 'ScreenSaver'), ('ScreenTime', 'ScreenTime'), ('SIMSetup', 'SIMSetup'), ('Siri', 'Siri'), ('SoftwareUpdate', 'SoftwareUpdate'), ('TapToSetup', 'TapToSetup'), ('TOS', 'TOS'), ('TVHomeScreenSync', 'TVHomeScreenSync'), ('TVProviderSignIn', 'TVProviderSignIn'), ('TVRoom', 'TVRoom'), ('UpdateCompleted', 'UpdateCompleted'), ('WatchMigration', 'WatchMigration'), ('Welcome', 'Welcome'), ('Zoom', 'Zoom')], max_length=64), editable=False, size=None)),
                ('support_email_address', models.EmailField(blank=True, max_length=250)),
                ('support_phone_number', models.CharField(blank=True, max_length=50)),
                ('include_tls_certificates', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('blueprint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mdm.Blueprint')),
                ('enrollment_secret', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='dep_enrollment', to='inventory.EnrollmentSecret')),
                ('push_certificate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mdm.PushCertificate')),
                ('realm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='realms.Realm')),
                ('virtual_server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mdm.DEPVirtualServer')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='DeviceArtifact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('artifact_version', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mdm.ArtifactVersion')),
            ],
        ),
        migrations.CreateModel(
            name='EnterpriseApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package', models.FileField(upload_to=zentral.contrib.mdm.models.enterprise_application_package_path)),
                ('bundle_identifier', models.TextField(db_index=True)),
                ('bundle_version', models.TextField()),
                ('manifest', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('artifact_version', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='enterprise_app', to='mdm.ArtifactVersion')),
            ],
            options={
                'unique_together': {('bundle_identifier', 'bundle_version')},
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.BinaryField()),
                ('filename', models.TextField()),
                ('payload_identifier', models.TextField(unique=True)),
                ('payload_uuid', models.TextField()),
                ('payload_display_name', models.TextField()),
                ('payload_description', models.TextField(null=True)),
                ('artifact_version', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='mdm.ArtifactVersion')),
            ],
        ),
        migrations.CreateModel(
            name='UserArtifact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('artifact_version', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mdm.ArtifactVersion')),
                ('enrolled_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='installed_artifacts', to='mdm.EnrolledUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserCommand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('kwargs', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('time', models.DateTimeField(null=True)),
                ('result_time', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('A', 'A'), ('E', 'E'), ('C', 'C'), ('N', 'N')], max_length=64, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('artifact_version', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mdm.ArtifactVersion')),
                ('enrolled_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commands', to='mdm.EnrolledUser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('blueprint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mdm.Blueprint')),
                ('enrollment_secret', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='user_enrollment', to='inventory.EnrollmentSecret')),
                ('push_certificate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mdm.PushCertificate')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='UserEnrollmentSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('STARTED', 'Started'), ('SCEP_VERIFIED', 'SCEP verified'), ('AUTHENTICATED', 'Authenticated'), ('COMPLETED', 'Completed')], max_length=64)),
                ('managed_apple_id', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='depprofile',
            name='enrollment_secret',
        ),
        migrations.RemoveField(
            model_name='depprofile',
            name='realm',
        ),
        migrations.RemoveField(
            model_name='depprofile',
            name='virtual_server',
        ),
        migrations.RemoveField(
            model_name='deviceartifactcommand',
            name='artifact_content_type',
        ),
        migrations.RemoveField(
            model_name='deviceartifactcommand',
            name='command',
        ),
        migrations.AlterUniqueTogether(
            name='installeddeviceartifact',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='installeddeviceartifact',
            name='artifact_content_type',
        ),
        migrations.RemoveField(
            model_name='installeddeviceartifact',
            name='enrolled_device',
        ),
        migrations.RemoveField(
            model_name='kernelextension',
            name='team',
        ),
        migrations.RemoveField(
            model_name='kernelextensionpolicy',
            name='allowed_kernel_extensions',
        ),
        migrations.RemoveField(
            model_name='kernelextensionpolicy',
            name='allowed_teams',
        ),
        migrations.RemoveField(
            model_name='kernelextensionpolicy',
            name='meta_business_unit',
        ),
        migrations.RemoveField(
            model_name='mdmenrollmentpackage',
            name='meta_business_unit',
        ),
        migrations.RemoveField(
            model_name='metabusinessunitpushcertificate',
            name='meta_business_unit',
        ),
        migrations.RemoveField(
            model_name='metabusinessunitpushcertificate',
            name='push_certificate',
        ),
        migrations.RenameField(
            model_name='devicecommand',
            old_name='request_type',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='depdevice',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='depenrollmentsession',
            name='dep_profile',
        ),
        migrations.RemoveField(
            model_name='depenrollmentsession',
            name='imei',
        ),
        migrations.RemoveField(
            model_name='depenrollmentsession',
            name='language',
        ),
        migrations.RemoveField(
            model_name='depenrollmentsession',
            name='meid',
        ),
        migrations.RemoveField(
            model_name='depenrollmentsession',
            name='product',
        ),
        migrations.RemoveField(
            model_name='depenrollmentsession',
            name='version',
        ),
        migrations.RemoveField(
            model_name='devicecommand',
            name='body',
        ),
        migrations.RemoveField(
            model_name='devicecommand',
            name='status_code',
        ),
        migrations.RemoveField(
            model_name='otaenrollmentsession',
            name='imei',
        ),
        migrations.RemoveField(
            model_name='otaenrollmentsession',
            name='language',
        ),
        migrations.RemoveField(
            model_name='otaenrollmentsession',
            name='meid',
        ),
        migrations.RemoveField(
            model_name='otaenrollmentsession',
            name='product',
        ),
        migrations.RemoveField(
            model_name='otaenrollmentsession',
            name='version',
        ),
        migrations.AddField(
            model_name='devicecommand',
            name='kwargs',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='devicecommand',
            name='status',
            field=models.CharField(choices=[('A', 'A'), ('E', 'E'), ('C', 'C'), ('N', 'N')], max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='enrolleddevice',
            name='bootstrap_token',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enrolleddevice',
            name='cert_fingerprint',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enrolleddevice',
            name='cert_not_valid_after',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enrolleddevice',
            name='platform',
            field=models.CharField(choices=[('iOS', 'iOS'), ('iPadOS', 'iPadOS'), ('macOS', 'macOS'), ('tvOS', 'tvOS')], default='macOS', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='otaenrollment',
            name='push_certificate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mdm.PushCertificate'),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='enrolled_device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commands', to='mdm.EnrolledDevice'),
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='uuid',
            field=models.UUIDField(editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='enrolleddevice',
            name='push_certificate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mdm.PushCertificate'),
        ),
        migrations.DeleteModel(
            name='ConfigurationProfile',
        ),
        migrations.DeleteModel(
            name='DEPProfile',
        ),
        migrations.DeleteModel(
            name='DeviceArtifactCommand',
        ),
        migrations.DeleteModel(
            name='InstalledDeviceArtifact',
        ),
        migrations.DeleteModel(
            name='KernelExtension',
        ),
        migrations.DeleteModel(
            name='KernelExtensionPolicy',
        ),
        migrations.DeleteModel(
            name='KernelExtensionTeam',
        ),
        migrations.DeleteModel(
            name='MDMEnrollmentPackage',
        ),
        migrations.DeleteModel(
            name='MetaBusinessUnitPushCertificate',
        ),
        migrations.AddField(
            model_name='userenrollmentsession',
            name='enrolled_device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mdm.EnrolledDevice'),
        ),
        migrations.AddField(
            model_name='userenrollmentsession',
            name='enrollment_secret',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='user_enrollment_session', to='inventory.EnrollmentSecret'),
        ),
        migrations.AddField(
            model_name='userenrollmentsession',
            name='realm_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='realms.RealmUser'),
        ),
        migrations.AddField(
            model_name='userenrollmentsession',
            name='scep_request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='inventory.EnrollmentSecretRequest'),
        ),
        migrations.AddField(
            model_name='userenrollmentsession',
            name='user_enrollment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mdm.UserEnrollment'),
        ),
        migrations.AddField(
            model_name='deviceartifact',
            name='enrolled_device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='installed_artifacts', to='mdm.EnrolledDevice'),
        ),
        migrations.AddField(
            model_name='depdevice',
            name='enrollment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mdm.DEPEnrollment'),
        ),
        migrations.AddField(
            model_name='depenrollmentsession',
            name='dep_enrollment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mdm.DEPEnrollment'),
        ),
        migrations.AddField(
            model_name='devicecommand',
            name='artifact_version',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mdm.ArtifactVersion'),
        ),
        migrations.AddField(
            model_name='enrolleddevice',
            name='blueprint',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mdm.Blueprint'),
        ),
        migrations.AddField(
            model_name='otaenrollment',
            name='blueprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mdm.Blueprint'),
        ),
        migrations.RunPython(set_enrollments_push_certificates),
        migrations.AlterField(
            model_name='depenrollmentsession',
            name='dep_enrollment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mdm.DEPEnrollment'),
        ),
        migrations.AlterField(
            model_name='enrolleddevice',
            name='push_certificate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mdm.PushCertificate'),
        ),
        migrations.AlterField(
            model_name='otaenrollment',
            name='push_certificate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mdm.PushCertificate'),
        ),
        migrations.AlterField(
            model_name='userenrollment',
            name='push_certificate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mdm.PushCertificate'),
        ),
    ]
