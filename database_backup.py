import os,glob
import time
import tinys3

# Getting current datetime to create seprate backup folder like "12012013-071334".
DATETIME = time.strftime('%Y%m%d-%H%M%S')
BACKUP_PATH = '/home/yash/backup/dbbackup/'
# 
# Checking if backup folder already exists or not. If not exists will create it.
# print "creating backup folder"
# if not os.path.exists(BACKUP_PATH):
#     os.makedirs(BACKUP_PATH)

# dumpcmd = "mysqldump --add-drop-database -h xxxxxxxxxxxxxxx.ccxxxxxxxtfjxcp81.ap-south-1.rds.amazonaws.com -P 3306 -u xxxxxx -p'xxxxxxxx'  xxxxxxxxxxx > " +BACKUP_PATH + "/" + "xxxxxxxxx"+DATETIME + ".sql"
# os.system(dumpcmd)

# print "Backup script completed"

# AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxxxxx'
# AWS_SECRET_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
conn = tinys3.Connection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY, default_bucket="bucket_name", tls=True,endpoint='s3.us-east-1.amazonaws.com')


#files = glob.glob(BACKUP_PATH + "/" + "discovery"+DATETIME  +"*.sql")
files = glob.glob('/home/yash/backup/dbbackup/20180410-182848.sql')

# for folder in glob.glob(BACKUP_PATH):
# 	print "folder =", folder
# 	for file in glob.glob(folder + '/*.*'):
# 		# retrieves the stats for the current file as a tuple
# 		# (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)
# 		# the tuple element mtime at index 8 is the last-modified-date
# 		#stats = os.stat(file
# 		print file
 
print files[0]
#print files[0]
# print("\n".join(files))
f = open(files[0],'w')
conn.upload('dump'+DATETIME+'.sql',f)
#conn.get(files[0],'discovery-nlp-data')



# import boto


# bucket_name = 'bucket'
# conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY, host='s3-us-east-1.amazonaws.com')

# bucket = conn.get_bucket('/bucket')

# print '-'#'Uploading %s to Amazon S3 bucket %s' % \ 	(filename, bucket_name)

# k = Key(bucket)
# k.key = files[0]
# k.set_contents_from_filename(files[0],cb=percent_cb, num_cb=10)