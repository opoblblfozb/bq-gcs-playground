# - 手元の画像を.jpgとしてGCSに保存する処理
# - 保存した画像のURLをまた手元に持ってくる処理
### bucket_name　と destination_blob_nameがわかれば
### https://storage.cloud.google.com/　と組み合わせて，URLは特定可能．
# https://cloud.google.com/storage/docs/reference/libraries?hl=ja
# https://dev.classmethod.jp/articles/gcs-python-client-libraries-how2/#delete_bucket
# https://googleapis.dev/python/storage/latest/blobs.html

# %%
from google.cloud import storage

BACKET_NAME = "images-for-study"


# %%
# create bucket
storage_client = storage.Client()
bucket = storage_client.create_bucket(BACKET_NAME)

print("Bucket {} created".format(bucket.name))

# %%
filename = "sample.jpeg"
### ローカルのファイルをアップロード
### destination_blob_nameに送ろうとするとエラーはでずに，PUT処理になる．
def upload_blob_from_filename(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

upload_blob_from_filename(BACKET_NAME, source_file_name=filename, destination_blob_name="sample1/" + filename)

# %%
#### binaryの文字列をcontent-type指定してアップロード
def upload_blob_from_string(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    with open(source_file_name, "br")as f:
        content = f.read()
    blob.upload_from_string(content, content_type="image/jpeg")
    print(blob.bucket)
    print(blob.name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
upload_blob_from_filename(BACKET_NAME, source_file_name=filename,
destination_blob_name="sample2/" + filename)




# %%
## requests
import requests
from PIL import Image
import io
import matplotlib.pyplot as plt
import numpy as np

def download_blob(bucket_name, source_blob_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    img_br = blob.download_as_bytes()

    print(
        "Downloaded storage object {} from bucket {} to local file.".format(
            source_blob_name, bucket_name
        )
    )

    return img_br

d = download_blob(BACKET_NAME, source_blob_name="sample2/" + filename, )
img_arr = np.array(Image.open(io.BytesIO(d)))
plt.imshow(img_arr)
# %%
