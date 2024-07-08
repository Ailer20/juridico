import pandas as pd
import sqlite3

# TESTES PARA O SQL =========================
# Criando o Conn

    

    

    
conn = sqlite3.connect('sistema.db')
c = conn.cursor()
c.execute('''
        CREATE TABLE IF NOT EXISTS reunioes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            processo TEXT,
            data DATE,
            hora TEXT,
            descricao TEXT
        )
    ''')
c.execute('''
        CREATE TABLE IF NOT EXISTS processos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            "No Processo" TEXT,
            Unidade TEXT,
            Tipo TEXT,
            Ação TEXT,
            Contrato TEXT,
            Cidade TEXT,
            Vara TEXT,
            Fase TEXT,
            Instância INTEGER,
            "Data julgamento" TEXT,
            "Data Inicial" TEXT,
            "Data Final" TEXT,
            "Processo Tramite" number,
            "Processo Extinto" number,
            "Transito julgado" number,
            Advogado TEXT,
            Cliente TEXT,
            "Cpf Cliente" INTEGER,
            Descrição TEXT
        )
    ''')
c.execute("""CREATE TABLE IF NOT EXISTS advogados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Advogado text,
            OAB number)""")




df_proc = pd.read_sql("SELECT * FROM processos", conn)
df_reu = pd.read_sql("SELECT * FROM reunioes", conn)
df_adv = pd.read_sql("SELECT * FROM advogados", conn)
conn.commit()
conn.close()


