# sns_publisher.py

import boto3
import sys

# Importa as configurações da AWS
from config.config_aws import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, SNS_TOPIC_ARN

def publicar_alerta(titulo_assunto: str, mensagem_completa: str):
    """
    Publica uma mensagem no Tópico SNS da AWS.
    
    Esta função simula o envio do alerta por E-mail/SMS para os funcionários.
    """
    if AWS_ACCESS_KEY_ID == "SEU_ACCESS_KEY_AQUI" or SNS_TOPIC_ARN == "arn:aws:sns:us-east-1:123456789012:AlertasAgroFazenda":
        print("⚠️ Configurações da AWS não são válidas. Alerta de teste simulado.")
        return False
        
    try:
        # Inicializa o cliente SNS
        sns_client = boto3.client(
            'sns',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

        # Publica a mensagem no tópico
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=mensagem_completa,
            Subject=titulo_assunto
        )
        
        # Exibe o ID da mensagem para confirmação
        message_id = response['MessageId']
        print(f"✅ Alerta publicado com sucesso! ID da Mensagem: {message_id}")
        return True

    except Exception as e:
        print(f"❌ ERRO ao publicar no SNS: {e}")
        return False