import psycopg2


conn_str = "postgresql://postgres.mvqdgkctdhaonejfarbc:31gRVKhVkgNN5K57VFmNRLVQw74DJ1lt@aws-0-us-east-1.pooler.supabase.com:5432/postgres"

conn_str = "postgresql://postgres.mvqdgkctdhaonejfarbcpass:31gRVKhVkgNN5K57VFmNRLVQw74DJ1lt@aws-0-us-east-1.pooler.supabase.com:5432/postgres"

conn = psycopg2.connect(conn_str)

conn = psycopg2.connect(
    host="aws-0-us-east-1.pooler.supabase.com",
    port="5432",  # padrão do PostgreSQL
    database="public",
    user="postgres.mvqdgkctdhaonejfarbc",
    password="31gRVKhVkgNN5K57VFmNRLVQw74DJ1lt"
)

def consulta_ce_supabase():

    # Dados da conexão
    conn = psycopg2.connect(
        host="aws-0-us-east-1.pooler.supabase.com",
        port="5432",  # padrão do PostgreSQL
        database="public",
        user="postgres.mvqdgkctdhaonejfarbc",
        password="31gRVKhVkgNN5K57VFmNRLVQw74DJ1lt"
    )

    #conn = psycopg2.connect(conn_str)

    # Cria um cursor para executar comandos SQL
    cur = conn.cursor()

    # Executa um SELECT
    cur.execute("select bl_master, quantidade_house, cnpj_desconsolidador, codigo_nvocc  FROM processos where ce_mercante = '182505155788958'")

    # Pega os resultados
    resultados = cur.fetchall()

    # Exibe os dados
    for linha in resultados:
        print(linha)

    # Fecha a conexão
    cur.close()
    conn.close()
