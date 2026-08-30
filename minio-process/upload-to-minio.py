# import minio
# import glob
# import os
# import json
# from minio import Minio
# import urllib3
# from minio.error import S3Error
# import pandas as pd

import os

from minio.error import S3Error

from minio import Minio

print(os.getenv('MINIO_SERVER_NAME'))
# import pandas as pd
# import json

try:
    minio_client = Minio(
        "172.19.0.6:9000",
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=False
    )

    buckets = minio_client.list_buckets()
    for bucket in buckets:
        print(bucket.name, bucket.creation_date)
except S3Error as error:
    print("Error occured. ", error)

# df = pd.read_csv(f"")
# df.to_parquet(f"")
# client.make_bucket(f"")
# client.fput_object(
#     f"dataset.pq", f"/dataset.pq"
# )
# policy_read_only = {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Principal": {"AWS": "*"},
#             "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
#             "Resource": f"arn:aws:s3:::dataset",
#         },
#         {
#             "Effect": "Allow",
#             "Principal": {"AWS": "*"},
#             "Action": "s3:GetObject",
#             f"Resource": f"arn:aws:s3:::dataset/*",
#         },
#     ],
# }

# client.set_bucket_policy(f'dataset{}', json.dumps(policy_read_only))
# print(f'dataset uploaded')
print("Test")
