import subprocess
import boto3
import os
import datetime

# Database connection settings
server_name = ''
database_name = ''
# No username and password needed for authentication

# AWS S3 credentials
aws_access_key_id = ''
aws_secret_access_key = ''
s3_bucket_name = ''
s3_key_prefix = ''

# Customizable backup location
backup_directory = r'C:\Program Files'

# Backup file name
backup_file_name = f'db_backup_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.bak'

# Location where the backup will be stored locally
backup_location = os.path.join(backup_directory, backup_file_name)

# Step 1: Backup the database (no authentication needed)
backup_command = f'sqlcmd -S {server_name} -d {database_name} -Q "BACKUP DATABASE {database_name} TO DISK = N\'{backup_location}\'"'
subprocess.run(backup_command, shell=True)

# Step 2: Upload to S3
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
s3.upload_file(backup_location, s3_bucket_name, os.path.join(s3_key_prefix, backup_file_name))

# Step 3: Clean up local backup file (optional)
#os.remove(backup_location)

print(f'Backup {backup_file_name} uploaded to S3 successfully.')
print(f'Backup file location: {backup_location}')
