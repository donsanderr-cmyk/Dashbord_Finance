import streamlit as st
import pandas as pd
import plotly.express as px
import io

from database import (
    create_table,
    insert_data,
    get_all_data,
    insert_dataframe,
    delete_all_data
)

# =====================
# INIT DATABASE
# =====================

create_table()

# =====================
# PAGE CONFIG
# =====================

st.set_page_config(
    page_title="Econo Shield: Bankruptcy Predictor",
    page_icon="🛡️",
    layout="wide"
)

# =====================
# FUNCTIONS
# =====================

def calculate_risk_score(
    pemasukan,
    pengeluaran,
    aset,
    hutang,
    tabungan
):

    score = 0

    profit = pemasukan - pengeluaran

    if profit < 0:
        score += 30

    if aset > 0:

        debt_ratio = hutang / aset

        if debt_ratio > 0.8:
            score += 40

        elif debt_ratio > 0.5:
            score += 20

    if tabungan <= 0:
        score += 30

    return min(score, 100)


def risk_category(score):

    if score < 30:
        return "🟢 Rendah"

    elif score < 60:
        return "🟡 Sedang"

    return "🔴 Tinggi"


def bankruptcy_probability(score):
    return min(score, 100)


# =====================
# SIDEBAR
# =====================

st.sidebar.markdown("""
# 🛡️ Econo Shield

### Bankruptcy Predictor

Prediksi Risiko Kebangkrutan Individu
""")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Finansial",
        "Upload Data",
        "Prediksi",
        "Laporan"
    ]
)

# =====================
# DASHBOARD
# =====================

if menu == "Dashboard":

    st.title("🛡️ Econo Shield")

    data = get_all_data()

    if len(data) > 0:

        df = pd.DataFrame(
            data,
            columns=[
                "ID",
                "Nama",
                "Pemasukan",
                "Pengeluaran",
                "Aset",
                "Hutang",
                "Tabungan"
            ]
        )

        total_pemasukan = df["Pemasukan"].sum()
        total_pengeluaran = df["Pengeluaran"].sum()
        total_profit = total_pemasukan - total_pengeluaran

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Pemasukan",
            f"${total_pemasukan:,.0f}"
        )

        col2.metric(
            "Pengeluaran",
            f"${total_pengeluaran:,.0f}"
        )

        col3.metric(
            "Net Profit",
            f"${total_profit:,.0f}"
        )

        col4.metric(
            "Data",
            len(df)
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.divider()

        st.subheader("Pemasukan vs Pengeluaran")

        fig1 = px.bar(
            df,
            x="Nama",
            y=["Pemasukan", "Pengeluaran"],
            barmode="group",
            title="Pemasukan vs Pengeluaran"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        st.subheader("Aset vs Hutang")

        fig2 = px.bar(
            df,
            x="Nama",
            y=["Aset", "Hutang"],
            barmode="group",
            title="Aset vs Hutang"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    else:

        st.info(
            "Tidak Ada Data Tersedia."
        )


    st.divider()

    with st.expander("⚠️ Danger Zone"):

        st.warning("Tindakan ini akan menghapus SEMUA data secara permanen!")

        confirm = st.checkbox("Saya mengerti dan ingin melanjutkan reset data")

        if confirm:

            if st.button("🧨 RESET ALL DATA", type="primary"):

                delete_all_data()

            st.success("Semua data berhasil dihapus!")

            st.cache_data.clear()  # clear cache biar dashboard refresh

            st.rerun()

# =====================
# FINANCIAL INPUT
# =====================

elif menu == "Finansial":

    st.title("Finansial")

    col1, col2 = st.columns(2)

    with col1:

        nama_name = st.text_input(
            "Nama"
        )

        pemasukan = st.number_input(
            "Pemasukan",
            min_value=0.0
        )

        pengeluaran = st.number_input(
            "Pengeluaran",
            min_value=0.0
        )

    with col2:

        aset = st.number_input(
            "Aset",
            min_value=0.0
        )

        hutang = st.number_input(
            "Hutang",
            min_value=0.0
        )

        tabungan = st.number_input(
            "Tabungan",
            value=0.0
        )

    if st.button("Save Data"):

        insert_data(
            nama_name,
            pemasukan,
            pengeluaran,
            aset,
            hutang,
            tabungan
        )

        score = calculate_risk_score(
            pemasukan,
            pengeluaran,
            aset,
            hutang,
            tabungan
        )

        st.success(
            "Data Berhasil Disimpan!"
        )

        st.metric(
            "Skor Resiko",
            f"{score}%"
        )

        st.progress(score / 100)

        probability = bankruptcy_probability(score)

        st.metric(
            "Kemungkinan Kebangkrutan",
            f"{probability}%"
        )

        st.write(
            risk_category(score)
        )

# =====================
# EXCEL UPLOAD
# =====================

elif menu == "Upload Data":

    st.title("📊 Impor Data Finansial")

    st.info(
        "Upload beberapa data sekaligus."
    )

    uploaded_file = st.file_uploader(
        "Upload File Data",
        type=["xlsx"]
    )

    if uploaded_file:

        df_excel = pd.read_excel(
            uploaded_file
        )

        st.subheader(
            "Preview"
        )

        st.dataframe(
            df_excel,
            use_container_width=True
        )

        required_columns = [
            "nama_name",
            "pemasukan",
            "pengeluaran",
            "aset",
            "hutang",
            "tabungan"
        ]

        if all(
            col in df_excel.columns
            for col in required_columns
        ):

            if st.button(
                "Import Data"
            ):

                insert_dataframe(
                    df_excel
                )

                st.success(
                    f"{len(df_excel)} rows imported successfully!"
                )

        else:

            st.error(
                "Excel columns must be:"
            )

            st.code(
                """
nama_name
pemasukan
pengeluaran
aset
hutang
tabungan
"""
            )

# =====================
# PREDICTION
# =====================

elif menu == "Prediksi":

    st.title("Prediksi")

    data = get_all_data()

    if len(data) > 0:

        df = pd.DataFrame(
            data,
            columns=[
                "ID",
                "Nama",
                "Pemasukan",
                "Pengeluaran",
                "Aset",
                "Hutang",
                "Tabungan"
            ]
        )

        result = []

        for _, row in df.iterrows():

            score = calculate_risk_score(
                row["Pemasukan"],
                row["Pengeluaran"],
                row["Aset"],
                row["Hutang"],
                row["Tabungan"]
            )

            result.append([
                row["Nama"],
                score,
                bankruptcy_probability(score),
                risk_category(score)
            ])

        prediction_df = pd.DataFrame(
            result,
            columns=[
                "Nama",
                "Skor Resiko",
                "Probabilitas",
                "Kategori"
            ]
        )

        st.dataframe(
            prediction_df,
            use_container_width=True
        )

        st.divider()

        risk_counts = prediction_df[
            "Kategori"
        ].value_counts()

        fig = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Resiko Distribusi"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning(
            "Tidak Ada Data Tersedia."
        )

# =====================
# REPORTS
# =====================

elif menu == "Laporan":

    st.title("Laporan")

    data = get_all_data()

    if len(data) > 0:

        df = pd.DataFrame(
            data,
            columns=[
                "ID",
                "Nama",
                "Pemasukan",
                "Pengeluaran",
                "Aset",
                "Hutang",
                "Tabungan"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download Laporan Data",
            data=csv,
            file_name="econoshield_report.csv",
            mime="text/csv"
        )

    else:

        st.warning(
            "Tidak Ada Data Laporan Tersedia."
        )