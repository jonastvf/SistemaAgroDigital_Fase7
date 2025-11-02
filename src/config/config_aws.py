#configs da aws

import os

# Acess Key e Secret Key para o boto3
# Tenta carregar de variáveis de ambiente, se não encontrar, usa placeholders.
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "SEU_ACCESS_KEY_AQUI")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "SUA_SECRET_KEY_AQUI")

# Região da AWS onde você configurou o SNS (Fase 5)
AWS_REGION = "us-east-1"  # Exemplo: Verifique a região do seu SNS

# O Nome do Recurso da Amazon (ARN) do Tópico SNS para o envio de alertas
# Substitua pelo ARN real criado na AWS
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:AlertasAgroFazenda" 

# Lista de emails ou números para testes (opcional, para referência)
DESTINATARIOS_TESTE = [
    {"protocol": "email", "endpoint": "seu_email_para_teste@example.com"},
    # {"protocol": "sms", "endpoint": "+5511999999999"} # Exemplo de SMS
]
