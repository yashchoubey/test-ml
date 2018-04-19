import os,glob
import time
import boto

AWS_ACCESS_KEY_ID= os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

DATETIME = time.strftime('%Y%m%d-%H%M%S')
BACKUP_PATH = './backup/xxxxxxbackup/'

if not os.path.exists(BACKUP_PATH):
    os.makedirs(BACKUP_PATH)

dumpcmd = "mysqldump --add-drop-database -h xxxxx.xxxxxxx.ap-south-1.rds.amazonaws.com -P 3306 -u xxxxxx -p"+os.environ["ACCESS_KEY_DATABASE"]+"  xxxxxx > " +BACKUP_PATH + "/" + "xxxxxx"+DATETIME + ".sql"
os.system(dumpcmd)

files = glob.glob(BACKUP_PATH + "/" + "xxxxxx"+DATETIME  +"*.sql")

s3_connection = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,host='s3-ap-south-1.amazonaws.com')
bucket = s3_connection.get_bucket('xxxxxx-data')

k = boto.s3.key.Key(bucket)
k.key = '/data-dump/dump_'+DATETIME+'.sql'
k.set_contents_from_filename(files[0])
