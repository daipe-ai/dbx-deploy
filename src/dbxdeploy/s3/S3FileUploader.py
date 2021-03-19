import boto3
from urllib.parse import urlparse
from botocore.exceptions import ClientError
from dbxdeploy.package.PackageUploaderInterface import PackageUploaderInterface

class S3FileUploader(PackageUploaderInterface):

    def __init__(
        self,
        awsAccessKeyId: str,
        awsSecretAccessKey: str,
    ):
        self.__awsAccessKeyId = awsAccessKeyId
        self.__awsSecretAccessKey = awsSecretAccessKey
        self.__s3Client = boto3.client(
            service_name='s3',
            aws_access_key_id=self.__awsAccessKeyId,
            aws_secret_access_key=self.__awsSecretAccessKey
        )

    def upload(self, content: bytes, filePath: str, overwrite: bool = False):
        bucket, key = self.__parseS3Path(filePath)

        if not overwrite and self.__fileExists(bucket, key):
            raise Exception(f'File {filePath} already exist')

        response = self.__s3Client.put_object(
            Bucket=bucket,
            Key=key,
            Body=content
        )

        statusCode = response['ResponseMetadata']['HTTPStatusCode']

        if statusCode != 200:
            raise Exception(f'S3 API call failed, status code: {statusCode}')

    def exists(self, filePath: str):
        bucket, key = self.__parseS3Path(filePath)

        return self.__fileExists(bucket, key)

    def __fileExists(self, bucket, key):
        try:
            self.__s3Client.head_object(Bucket=bucket, Key=key)
        except ClientError as e:
            if e.response['Error']['Code'] != '404':
                raise

            return False

        return True

    def __parseS3Path(self, filePath: str):
        parsedS3Path = urlparse(filePath, allow_fragments=False)

        if parsedS3Path.scheme != 's3':
            raise Exception('File path must start with s3://')

        bucket = parsedS3Path.netloc
        key = parsedS3Path.path.lstrip('/')

        return (bucket, key)
