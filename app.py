import os
import tempfile
from typing import List

import numpy as np
import pandas as pd
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings


st.set_page_config(page_title="AI Report Narration Studio", page_icon="📊", layout="wide")


@st.cache_data(show_spinner=False)
def make_synthetic_data(months: int = 12, seed: int = 17) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=months, freq="ME")
    regions = ["North America", "Europe", "APAC"]
    products = ["Core", "Premium", "Enterprise"]

    rows = []
    for dt in dates:
        for region in regions:
            for product in products:
                trend = 15000 + (dt.month * 130)
                seasonality = 2200 * np.sin((dt.month / 12) * 2 * np.pi)
                region_bias = {"North America": 4200, "Europe": 2800, "APAC": 3500}[region]
                product_bias = {"Core": 0, "Premium": 1700, "Enterprise": 3100}[product]
                noise = rng.normal(0, 950)
                revenue = max(trend + seasonality + region_bias + product_bias + noise, 200)
                target = revenue * rng.uniform(0.9, 1.08)
                margin = rng.uniform(0.17, 0.42)
                rows.append(
                    {
                        "month": dt,
                        "region": region,
                        "product": product,
                        "revenue": round(revenue, 2),
                        "target": round(target, 2),
                        "margin": round(margin, 4),
                    }
                )

    return pd.DataFrame(rows)


def build_documents(df: pd.DataFrame) -> List[Document]:
    docs: List[Document] = []
    grouped = (
        df.groupby(["month", "region"], as_index=False)
        .agg(revenue=("revenue", "sum"), target=("target", "sum"), margin=("margin", "mean"))
        .sort_values("month")
    )

    for _, row in grouped.iterrows():
        gap = row["revenue"] - row["target"]
        content = (
            f"Month: {row['month'].strftime('%Y-%m')}; Region: {row['region']}; "
            f"Revenue: ${row['revenue']:,.0f}; Target: ${row['target']:,.0f}; "
            f"Gap: ${gap:,.0f}; Avg margin: {row['margin']*100:.1f}%"
        )
        docs.append(Document(page_content=content, metadata={"region": row["region"]}))

    return docs


def get_embeddings(model_name: str) -> OllamaEmbeddings:
    return OllamaEmbeddings(model=model_name)


def get_vector_store(documents: List[Document], embeddings: OllamaEmbeddings, backend: str):
    if backend == "Chroma":
        persist_dir = tempfile.mkdtemp(prefix="chroma_narration_")
        return Chroma.from_documents(documents=documents, embedding=embeddings, persist_directory=persist_dir)
    return FAISS.from_documents(documents=documents, embedding=embeddings)


def build_kpi_snapshot(df: pd.DataFrame) -> str:
    monthly = df.groupby("month", as_index=False).agg(revenue=("revenue", "sum"), target=("target", "sum"))
    latest = monthly.iloc[-1]
    previous = monthly.iloc[-2]
    mom = ((latest["revenue"] - previous["revenue"]) / previous["revenue"]) * 100
    gap = latest["revenue"] - latest["target"]

    best_region = (
        df[df["month"] == latest["month"]]
        .groupby("region", as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
        .iloc[0]
    )

    return (
        f"Latest month: {latest['month'].strftime('%B %Y')} | Revenue ${latest['revenue']:,.0f} | "
        f"MoM {mom:+.1f}% | Target gap ${gap:,.0f} | Best region {best_region['region']} "
        f"(${best_region['revenue']:,.0f})"
    )


def generate_narration(df: pd.DataFrame, backend: str, llm_model: str, embed_model: str, question: str) -> str:
    docs = build_documents(df)
    embeddings = get_embeddings(embed_model)
    vector_store = get_vector_store(docs, embeddings, backend)
    retrieved_docs = vector_store.similarity_search(question, k=6)

    context = "\n".join([d.page_content for d in retrieved_docs])
    kpi_snapshot = build_kpi_snapshot(df)

    prompt = PromptTemplate(
        input_variables=["kpi_snapshot", "context", "question"],
        template=(
            "You are a business analytics narrator. Write a concise, factual report narration in bullet points.\n"
            "Include: summary, key drivers, anomalies/risks, and recommended actions.\n"
            "Do not invent numbers.\n\n"
            "KPI Snapshot:\n{kpi_snapshot}\n\n"
            "Retrieved Evidence:\n{context}\n\n"
            "User ask: {question}\n"
        ),
    )

    llm = ChatOllama(model=llm_model, temperature=0.2)
    chain_input = prompt.format(kpi_snapshot=kpi_snapshot, context=context, question=question)
    return llm.invoke(chain_input).content


st.title("📊 AI Report Narration Studio")
st.caption("LangChain + Chroma/FAISS + Ollama LLM for analytics storytelling.")

with st.sidebar:
    st.header("Controls")
    months = st.slider("Months of synthetic data", min_value=6, max_value=36, value=12)
    seed = st.number_input("Random seed", min_value=1, max_value=9999, value=17)
    vector_backend = st.selectbox("Vector DB", options=["Chroma", "FAISS"], index=0)
    llm_model = st.text_input("Ollama LLM model", value="llama3.2")
    embed_model = st.text_input("Ollama embedding model", value="nomic-embed-text")

if "data" not in st.session_state:
    st.session_state["data"] = make_synthetic_data(months=months, seed=seed)

if st.button("Regenerate synthetic dataset"):
    st.session_state["data"] = make_synthetic_data(months=months, seed=seed)

df = st.session_state["data"]

c1, c2 = st.columns(2)
with c1:
    st.subheader("Revenue by Month")
    monthly = df.groupby("month", as_index=False).agg(revenue=("revenue", "sum"), target=("target", "sum"))
    st.line_chart(monthly.set_index("month")[["revenue", "target"]])

with c2:
    st.subheader("Regional mix (latest month)")
    latest_month = df["month"].max()
    pie_data = (
        df[df["month"] == latest_month]
        .groupby("region", as_index=False)
        .agg(revenue=("revenue", "sum"))
        .set_index("region")
    )
    st.bar_chart(pie_data)

st.subheader("Data Preview")
st.dataframe(df, use_container_width=True)

question = st.text_area(
    "Narration request",
    value="Create an executive summary for the latest report and suggest 3 actions.",
)

if st.button("Generate AI narration"):
    try:
        narration = generate_narration(
            df=df,
            backend=vector_backend,
            llm_model=llm_model,
            embed_model=embed_model,
            question=question,
        )
        st.success(narration)
    except Exception as exc:  # keep app useful if local models are not pulled yet
        st.error(
            "Generation failed. Ensure Ollama is running and models are pulled. "
            f"Technical details: {exc}"
        )
