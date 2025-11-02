import sys
# Exemplo usando PostgreSQL. Ajuste para a sua biblioteca (ex: pymysql, cx_oracle, etc.)
try:
    import psycopg2 
except ImportError:
    # Se você não usa psycopg2, comente ou substitua pelo seu SGBD
    print("Aviso: psycopg2 não encontrado. Assumindo que você usa outro SGBD.")

# ----------------------------------------------------
# ⚠️ ATENÇÃO: SUBSTITUA COM SUAS CREDENCIAIS REAIS DA FASE 2
# Idealmente, carregue isso de variáveis de ambiente para segurança!
# ----------------------------------------------------
DB_HOST = "SEU_HOST_AWS_RDS_OU_LOCAL"
DB_NAME = "SEU_NOME_DO_BANCO_DE_DADOS"
DB_USER = "SEU_USUARIO_DB"
DB_PASS = "SUA_SENHA_DB"
# DB_PORT = 5432 # Ajuste a porta se necessário

def get_connection():
    """Tenta estabelecer e retornar uma nova conexão com o Banco de Dados (Fase 2)."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
            # port=DB_PORT # Descomente se precisar de porta específica
        )
        return conn
    except Exception as e:
        print(f"ERRO: Não foi possível conectar ao banco de dados. Detalhes: {e}")
        return None

def check_connection():
    """Verifica rapidamente o status da conexão para a Dashboard."""
    conn = get_connection()
    if conn:
        conn.close()
        return True
    return False

def fetch_data(query):
    """Executa uma query SELECT e retorna os dados como DataFrame do Pandas."""
    conn = get_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            print(f"Erro ao executar query: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    return pd.DataFrame()

# Adicione outras funções (insert_data, update_data) conforme necessário
