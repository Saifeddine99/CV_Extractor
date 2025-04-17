import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the evaluation data
with open("src/evaluation/evaluation.json", "r") as f:
    evaluation_data = json.load(f)

# Helper to parse metrics
def collect_metrics(data):
    rows = []
    for file_path, evaluations in data.items():
        cv_type = "image_based" if "image_based" in file_path else "text_based"
        file_name = file_path.split("/")[-1]
        for eval in evaluations:
            for model, metrics in eval.items():
                if metrics:
                    rows.append({
                        "File": file_name,
                        "Type": cv_type,
                        "Model": model,
                        "Precision": metrics.get("precision", 0),
                        "Recall": metrics.get("recall", 0),
                        "F1 Score": metrics.get("f1_score", 0)
                    })
    return pd.DataFrame(rows)

# Streamlit App
st.title("📊 CV Extraction Accuracy Comparison")
st.markdown("Compare Precision, Recall, and F1 Score for 3 LLMs across 10 CVs.")

df = collect_metrics(evaluation_data)

# Summary Table
st.subheader("Model Performance Table")
st.dataframe(df.style.format({"Precision": "{:.2f}", "Recall": "{:.2f}", "F1 Score": "{:.2f}"}))

# Aggregated Metrics
st.subheader("Average Performance by Model")
avg_df = df.groupby("Model")[["Precision", "Recall", "F1 Score"]].mean().round(3)
st.dataframe(avg_df)

# Visualization
st.subheader("📈 Performance Comparison (Bar Chart)")
metric_choice = st.selectbox("Select metric to visualize", ["Precision", "Recall", "F1 Score"])
fig, ax = plt.subplots()
df_box = df.pivot_table(index="File", columns="Model", values=metric_choice)
df_box.plot(kind="bar", ax=ax, figsize=(10, 5))
plt.title(f"{metric_choice} Comparison Across CVs")
plt.ylabel(metric_choice)
plt.xlabel("CV File")
st.pyplot(fig)