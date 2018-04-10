import os
import time
import tinys3

# Getting current datetime to create seprate backup folder like "12012013-071334".
DATETIME = time.strftime('%d%m%Y-%H%M%S')
BACKUP_PATH = 'backup/dbbackup/'
TODAYBACKUPPATH = BACKUP_PATH + DATETIME

# Checking if backup folder already exists or not. If not exists will create it.
#print "creating backup folder"
if not os.path.exists(TODAYBACKUPPATH):
    os.makedirs(TODAYBACKUPPATH)

dumpcmd = "mysqldump --add-drop-database -h XXXX.XXXX.ap-south-1.rds.amazonaws.com -P 3306 -u dbname -p'password'  dbname > " + TODAYBACKUPPATH + "/" + "dbname"+DATETIME + ".sql"
os.system(dumpcmd)

print "Backup script completed"

# conn = tinys3.Connection('S3_ACCESS_KEY','S3_SECRET_KEY',tls=True)

# f = open('some_file.zip','rb')
# conn.upload('some_file.zip',f,'my_bucket')