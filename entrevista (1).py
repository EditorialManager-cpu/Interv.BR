import streamlit as st
import csv
import pandas as pd
import os

st.set_page_config(page_title="Entrevista Corpo Editorial", page_icon="📝")

st.title("📝 Entrevista para Corpo Editorial de Pesquisas em Saúde")
st.write("**Esta entrevista é anônima. Responda com atenção, o envio só poderá ser feito uma única vez.**")

CSV_PERGUNTAS = "perguntas.csv"
CSV_RESPOSTAS = "respostas_entrevista.csv"

nome = st.text_input("Para controle interno, digite um codinome (pode ser um apelido ou número):")

if nome:
    df = pd.read_csv(CSV_PERGUNTAS)
    respostas = []

    for idx, row in df.iterrows():
        st.subheader(f"Pergunta {idx+1} de {len(df)}")

        if row["tipo"] == "MC":
            opcoes = [str(row[f"opcao{i}"]) for i in range(1, 5) if pd.notna(row[f"opcao{i}"])]
            resposta = st.radio(row["pergunta"], opcoes, key=idx)
        else:
            resposta = st.text_area(row["pergunta"], key=idx)

        respostas.append(resposta)

    if st.button("Enviar respostas"):
        novo_arquivo = not os.path.isfile(CSV_RESPOSTAS)
        with open(CSV_RESPOSTAS, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if novo_arquivo:
                cabecalho = ["Codinome"] + [f"P{i+1}" for i in range(len(respostas))]
                writer.writerow(cabecalho)
            writer.writerow([nome] + respostas)

        st.success("✅ Respostas enviadas com sucesso! Obrigado por participar.")
        st.stop()