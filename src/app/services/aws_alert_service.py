import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError

class AwsAlertService:
    @staticmethod
    def publish_alert(subject: str, message: str) -> bool:
        try:
            sns_client = boto3.client(
                "sns",
                region_name=os.getenv("AWS_REGION"),
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )

            response = sns_client.publish(
                TopicArn=os.getenv("AWS_SNS_TOPIC_ARN"),
                Subject=subject,
                Message=message,
            )

            print(f"[SNS] Sucesso! MessageId: {response.get('MessageId')}")
            return True

        except (BotoCoreError, ClientError) as e:
            print(f"[SNS] ERRO ao publicar: {e}")
            return False
