import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from data_loader import load_all_data

# ==============================================================================
# KONFIGURASI HALAMAN & CUSTOM CSS (CORPORATE TELECOM: DARK SLATE & DEEP RED)
# ==============================================================================
st.set_page_config(
    page_title="Executive Financial & Subsidiary Tracker | Telkom 2025",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    /* Tema Utama Dark Slate & Deep Red Accent */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    section[data-testid="stSidebar"] {
        background-color: #1E293B;
        border-right: 1px solid #334155;
    }
    h1, h2, h3, h4 {
        color: #F8FAFC !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    /* Header Banner */
    .exec-header {
        background: linear-gradient(90deg, #7F1D1D 0%, #1E293B 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        border-left: 6px solid #EF4444;
        margin-bottom: 1.5rem;
    }
    .exec-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .exec-header p {
        margin: 0.3rem 0 0 0;
        color: #CBD5E1;
        font-size: 0.95rem;
    }
    /* KPI Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-size: 1.5rem !important;
        font-weight: 700;
    }
    /* Card Container */
    .custom-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .badge-sehat {
        background-color: #064E3B;
        color: #34D399;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .badge-anomali {
        background-color: #7F1D1D;
        color: #FCA5A5;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.8rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# FUNGSI RENDERING MODUL
# ==============================================================================
def render_header():
    st.markdown(
        """
        <div class="exec-header">
            <h1>📡 Executive Financial & Subsidiary Tracker</h1>
            <p>TelkomGroup Consolidated Performance & Anomaly Detection Dashboard (FY 2024 vs 2025)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_executive_summary(df_cons: pd.DataFrame, df_sub: pd.DataFrame):
    st.subheader("📊 Executive Summary: Kinerja Konsolidasi 2024 vs 2025")

    # Ambil nilai metrik
    rev_25 = df_cons.loc[df_cons["Metrik"] == "Pendapatan Konsolidasi", "2025"].values[0]
    rev_chg = df_cons.loc[df_cons["Metrik"] == "Pendapatan Konsolidasi", "YoY_Change_Pct"].values[0]

    ebitda_25 = df_cons.loc[df_cons["Metrik"] == "EBITDA", "2025"].values[0]
    ebitda_chg = df_cons.loc[df_cons["Metrik"] == "EBITDA", "YoY_Change_Pct"].values[0]

    ni_25 = df_cons.loc[df_cons["Metrik"] == "Laba Bersih Parent", "2025"].values[0]
    ni_chg = df_cons.loc[df_cons["Metrik"] == "Laba Bersih Parent", "YoY_Change_Pct"].values[0]

    net_margin_25 = (ni_25 / rev_25) * 100
    net_margin_24 = (22403.0 / 149967.0) * 100
    net_margin_diff = net_margin_25 - net_margin_24

    ecl_25 = df_cons.loc[df_cons["Metrik"] == "Cadangan Kerugian Piutang (ECL)", "2025"].values[0]
    ecl_chg = df_cons.loc[df_cons["Metrik"] == "Cadangan Kerugian Piutang (ECL)", "YoY_Change_Pct"].values[0]

    # Top KPI Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Revenue 2025", f"Rp{rev_25:,.0f} M", f"{rev_chg:.1f}% YoY")
    with c2:
        st.metric("EBITDA 2025", f"Rp{ebitda_25:,.0f} M", f"{ebitda_chg:.1f}% YoY")
    with c3:
        st.metric("Net Income (Parent)", f"Rp{ni_25:,.0f} M", f"{ni_chg:.1f}% YoY")
    with c4:
        st.metric("Net Margin", f"{net_margin_25:.1f}%", f"{net_margin_diff:.1f}% pts")
    with c5:
        st.metric(
            "Cadangan Piutang (ECL)",
            f"Rp{ecl_25:,.0f} M",
            f"+{ecl_chg:.1f}% YoY",
            delta_color="inverse",
        )

    st.markdown("---")

    # Alert Callout Anomali Utama
    col_alert1, col_alert2 = st.columns(2)
    with col_alert1:
        st.error(
            "🚨 **ANOMALI ANAK PERUSAHAAN TERDETEKSI:**\n\n"
            "- **PT Sigma Cipta Caraka (Sigma):** Rugi bersih **-Rp363,6 M** (membengkak 64,3% akibat *Clean Sheet Strategy*).\n"
            "- **PT Telkom Satelit Indonesia (Telkomsat):** Rugi bersih **-Rp249,5 M** akibat tekanan persaingan satelit & beban bunga."
        )
    with col_alert2:
        st.warning(
            "⚠️ **TEKANAN PROFITABILITAS KONSOLIDASI:**\n\n"
            "- **Operating Margin** turun dari **28,7%** (2024) menjadi **23,6%** (2025).\n"
            "- **Cadangan Kerugian Piutang (ECL)** naik **+14,7%** menjadi **Rp6.955 M**.\n"
            "- **Unrealized Loss Investasi (GOTO/MDI)** tercatat sebesar **Rp242 M**."
        )

    # Chart Perbandingan Konsolidasi 2024 vs 2025 (Bar & Line)
    st.subheader("📈 Perbandingan Kinerja Keuangan Konsolidasi (2024 vs 2025)")
    df_plot = df_cons[
        df_cons["Metrik"].isin(
            ["Pendapatan Konsolidasi", "EBITDA", "Laba Bersih Parent", "Cadangan Kerugian Piutang (ECL)"]
        )
    ].copy()

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="2024",
            x=df_plot["Metrik"],
            y=df_plot["2024"],
            marker_color="#475569",
            hovertemplate="<b>%{x}</b><br>2024: Rp%{y:,.0f} M<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            name="2025",
            x=df_plot["Metrik"],
            y=df_plot["2025"],
            marker_color="#EF4444",
            hovertemplate="<b>%{x}</b><br>2025: Rp%{y:,.0f} M<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            name="YoY Change (%)",
            x=df_plot["Metrik"],
            y=df_plot["YoY_Change_Pct"],
            yaxis="y2",
            mode="lines+markers+text",
            text=[f"{v:+.1f}%" for v in df_plot["YoY_Change_Pct"]],
            textposition="top center",
            line=dict(color="#FBBF24", width=3),
            marker=dict(size=9, color="#FBBF24"),
            hovertemplate="<b>%{x}</b><br>YoY: %{y:+.1f}%<extra></extra>",
        )
    )

    fig.update_layout(
        barmode="group",
        template="plotly_dark",
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        height=430,
        yaxis=dict(title="Nilai (Rp Miliar)", gridcolor="#334155"),
        yaxis2=dict(
            title="Perubahan YoY (%)",
            overlaying="y",
            side="right",
            showgrid=False,
            zeroline=True,
            zerolinecolor="#64748B",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=50, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_subsidiary_anomaly(df_sub: pd.DataFrame):
    st.subheader("🚨 Subsidiary Anomaly Tracker")

    # Filter Threshold Anomali
    with st.expander("⚙️ Filter Threshold Deteksi Anomali", expanded=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            loss_threshold = st.slider(
                "Batas Kerugian Bersih (Net Loss > Rp Miliar)",
                min_value=0,
                max_value=400,
                value=100,
                step=25,
                help="Entitas dengan kerugian melebihi nilai ini akan ditandai sebagai ANOMALI / RUGI.",
            )
        with col_f2:
            margin_threshold = st.slider(
                "Batas Minimum Net Margin (%)",
                min_value=-20.0,
                max_value=20.0,
                value=0.0,
                step=1.0,
                help="Entitas dengan Net Margin di bawah batas ini akan ditandai sebagai ANOMALI / RUGI.",
            )

    # Evaluasi status dinamis berdasarkan filter
    df_disp = df_sub.copy()
    df_disp["Status"] = df_disp.apply(
        lambda r: "[ANOMALI / RUGI]"
        if (r["Laba_Bersih"] < -loss_threshold or r["Net_Margin_Pct"] < margin_threshold)
        else "[SEHAT]",
        axis=1,
    )

    # Tabel Datar Anak Perusahaan dengan styling warna
    def style_status(val):
        if "ANOMALI" in val:
            return "background-color: #7F1D1D; color: #FCA5A5; font-weight: bold;"
        return "background-color: #064E3B; color: #34D399; font-weight: bold;"

    df_table = df_disp[
        ["Entitas", "Pendapatan", "EBITDA", "Laba_Bersih", "EBITDA_Margin_Pct", "Net_Margin_Pct", "Status"]
    ].copy()
    df_table.columns = [
        "Entitas",
        "Pendapatan (Rp M)",
        "EBITDA (Rp M)",
        "Laba Bersih (Rp M)",
        "EBITDA Margin (%)",
        "Net Margin (%)",
        "Status",
    ]

    st.dataframe(
        df_table.style.format(
            {
                "Pendapatan (Rp M)": "{:,.1f}",
                "EBITDA (Rp M)": "{:,.1f}",
                "Laba Bersih (Rp M)": "{:,.1f}",
                "EBITDA Margin (%)": "{:.1f}%",
                "Net Margin (%)": "{:.1f}%",
            }
        ).map(style_status, subset=["Status"]),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")
    st.subheader("🔍 Deep-Dive Anomali: PT Sigma Cipta Caraka & Telkomsat")

    anomaly_entities = df_sub[
        df_sub["Entitas"].isin(
            ["PT Sigma Cipta Caraka (Sigma)", "PT Telkom Satelit Indonesia (Telkomsat)"]
        )
    ]

    col_a1, col_a2 = st.columns(2)
    for idx, (_, row) in enumerate(anomaly_entities.iterrows()):
        target_col = col_a1 if idx == 0 else col_a2
        with target_col:
            st.markdown(
                f"""
                <div class="custom-card">
                    <h4 style="margin-top:0; color:#FCA5A5;">{row['Entitas']}</h4>
                    <p style="color:#CBD5E1; font-size:0.9rem;"><b>Driver Kerugian:</b> {row['Catatan_Driver']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            fig_sub = go.Figure(
                data=[
                    go.Bar(
                        name="Pendapatan",
                        x=["Pendapatan", "Total Beban & Pajak", "Laba/Rugi Bersih"],
                        y=[row["Pendapatan"], row["Total_Beban_dan_Pajak"], row["Laba_Bersih"]],
                        marker_color=["#38BDF8", "#F59E0B", "#EF4444"],
                        text=[
                            f"Rp{row['Pendapatan']:,.1f} M",
                            f"Rp{row['Total_Beban_dan_Pajak']:,.1f} M",
                            f"Rp{row['Laba_Bersih']:,.1f} M",
                        ],
                        textposition="auto",
                        hovertemplate="<b>%{x}</b><br>Nilai: Rp%{y:,.1f} M<extra></extra>",
                    )
                ]
            )
            fig_sub.update_layout(
                template="plotly_dark",
                paper_bgcolor="#1E293B",
                plot_bgcolor="#1E293B",
                height=320,
                showlegend=False,
                yaxis=dict(title="Rp Miliar", gridcolor="#334155"),
                margin=dict(l=30, r=20, t=20, b=30),
            )
            st.plotly_chart(fig_sub, use_container_width=True)


def render_segment_breakdown(df_seg: pd.DataFrame):
    st.subheader("🏢 Segment Breakdown Analysis (FY 2025)")

    col_s1, col_s2 = st.columns([1.3, 1])

    with col_s1:
        st.markdown("**Treemap Kontribusi Pendapatan & Operating Margin Segmen**")
        fig_tree = px.treemap(
            df_seg,
            path=["Segmen"],
            values="Pendapatan_2025",
            color="Operating_Margin_Pct",
            color_continuous_scale="RdYlGn",
            color_continuous_midpoint=0,
            custom_data=["Result_2025", "Operating_Margin_Pct", "Kontribusi_Pendapatan_Pct"],
        )
        fig_tree.update_traces(
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Pendapatan: Rp%{value:,.0f} M (%{customdata[2]:.1f}%)<br>"
                "Result: Rp%{customdata[0]:,.0f} M<br>"
                "Operating Margin: %{customdata[1]:.1f}%<extra></extra>"
            ),
            textinfo="label+value+percent root",
        )
        fig_tree.update_layout(
            template="plotly_dark",
            paper_bgcolor="#1E293B",
            height=420,
            margin=dict(l=10, r=10, t=20, b=10),
        )
        st.plotly_chart(fig_tree, use_container_width=True)

    with col_s2:
        st.markdown("**Perbandingan Margin Operasi Antar Segmen**")
        fig_bar = go.Figure(
            go.Bar(
                x=df_seg["Operating_Margin_Pct"],
                y=df_seg["Segmen"],
                orientation="h",
                marker_color=[
                    "#10B981" if v >= 0 else "#EF4444" for v in df_seg["Operating_Margin_Pct"]
                ],
                text=[f"{v:.1f}%" for v in df_seg["Operating_Margin_Pct"]],
                textposition="auto",
                hovertemplate="<b>%{y}</b><br>Operating Margin: %{x:.1f}%<extra></extra>",
            )
        )
        fig_bar.update_layout(
            template="plotly_dark",
            paper_bgcolor="#1E293B",
            plot_bgcolor="#1E293B",
            height=420,
            xaxis=dict(title="Operating Margin (%)", gridcolor="#334155", zeroline=True),
            yaxis=dict(autorange="reversed"),
            margin=dict(l=20, r=20, t=20, b=30),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Tabel Ringkasan Segmen
    df_seg_tbl = df_seg[
        [
            "Segmen",
            "Pendapatan_2025",
            "Kontribusi_Pendapatan_Pct",
            "Result_2025",
            "Operating_Margin_Pct",
            "YoY_Result_Growth_Pct",
            "Deskripsi",
        ]
    ].copy()
    df_seg_tbl.columns = [
        "Segmen",
        "Pendapatan (Rp M)",
        "Kontribusi (%)",
        "Result (Rp M)",
        "Operating Margin (%)",
        "YoY Result (%)",
        "Keterangan",
    ]
    st.dataframe(
        df_seg_tbl.style.format(
            {
                "Pendapatan (Rp M)": "{:,.0f}",
                "Kontribusi (%)": "{:.1f}%",
                "Result (Rp M)": "{:,.0f}",
                "Operating Margin (%)": "{:.1f}%",
                "YoY Result (%)": "{:+.1f}%",
            },
            na_rep="-",
        ),
        use_container_width=True,
        hide_index=True,
    )


def render_what_if_simulator(df_cons: pd.DataFrame, df_sub: pd.DataFrame):
    st.subheader("🧮 Executive What-If Simulator")
    st.markdown(
        "Simulasikan dampak efisiensi operasional, pemulihan piutang, dan perbaikan kinerja anak perusahaan "
        "terhadap **Laba Bersih Konsolidasi (Parent) 2025** secara *real-time*."
    )

    # Baseline 2025
    base_ni = 17814.0
    base_rev = 146742.0
    base_ebitda = 72240.0
    # Estimasi Opex non-D&A = Revenue - EBITDA
    base_opex = base_rev - base_ebitda  # 74.502 M
    base_ecl = 6955.0
    sigma_telkomsat_loss = abs(-249.5) + abs(-363.6)  # 613.1 M

    col_sim1, col_sim2, col_sim3 = st.columns(3)
    with col_sim1:
        opex_red_pct = st.slider(
            "% Penurunan Beban Operasional (Opex)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.5,
        )
    with col_sim2:
        ecl_eff_pct = st.slider(
            "% Efisiensi Cadangan Piutang (ECL)",
            min_value=0.0,
            max_value=50.0,
            value=15.0,
            step=2.5,
        )
    with col_sim3:
        sub_rec_pct = st.slider(
            "% Pemulihan Rugi Sigma & Telkomsat",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=5.0,
        )

    # Kalkulasi Dampak (Asumsi tarif pajak efektif ~22% untuk penghematan opex & ECL)
    tax_shield = 0.78
    gain_opex = base_opex * (opex_red_pct / 100.0) * tax_shield
    gain_ecl = base_ecl * (ecl_eff_pct / 100.0) * tax_shield
    gain_sub = sigma_telkomsat_loss * (sub_rec_pct / 100.0)

    total_gain = gain_opex + gain_ecl + gain_sub
    projected_ni = base_ni + total_gain
    ni_uplift_pct = (total_gain / base_ni) * 100

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Baseline Laba Bersih 2025", f"Rp{base_ni:,.0f} M")
    m2.metric(
        "Potensi Tambahan Laba Bersih",
        f"+Rp{total_gain:,.1f} M",
        f"+{ni_uplift_pct:.1f}% Uplift",
    )
    m3.metric(
        "Proyeksi Laba Bersih Baru",
        f"Rp{projected_ni:,.1f} M",
        f"vs Rp22.403 M (2024)",
    )

    # Waterfall Chart Dampak Simulasi
    fig_wf = go.Figure(
        go.Waterfall(
            name="Simulasi Laba Bersih",
            orientation="v",
            measure=["absolute", "relative", "relative", "relative", "total"],
            x=[
                "Baseline 2025",
                "Efisiensi Opex",
                "Efisiensi Piutang (ECL)",
                "Pemulihan Sigma & Telkomsat",
                "Proyeksi Laba Bersih",
            ],
            textposition="outside",
            text=[
                f"Rp{base_ni:,.0f} M",
                f"+Rp{gain_opex:,.0f} M",
                f"+Rp{gain_ecl:,.0f} M",
                f"+Rp{gain_sub:,.0f} M",
                f"Rp{projected_ni:,.0f} M",
            ],
            y=[base_ni, gain_opex, gain_ecl, gain_sub, projected_ni],
            connector={"line": {"color": "#64748B"}},
            increasing={"marker": {"color": "#10B981"}},
            totals={"marker": {"color": "#EF4444"}},
            hovertemplate="<b>%{x}</b><br>Nilai: Rp%{y:,.1f} M<extra></extra>",
        )
    )
    fig_wf.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        height=400,
        yaxis=dict(title="Laba Bersih (Rp Miliar)", gridcolor="#334155"),
        margin=dict(l=40, r=40, t=40, b=40),
    )
    st.plotly_chart(fig_wf, use_container_width=True)


# ==============================================================================
# MAIN APPLICATION
# ==============================================================================
def main():
    render_header()
    data = load_all_data()

    # Sidebar Navigation
    st.sidebar.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Telkom_Indonesia_2013.svg/512px-Telkom_Indonesia_2013.svg.png",
        width=160,
    )
    st.sidebar.markdown("### 🧭 Navigasi Dashboard")
    menu = st.sidebar.radio(
        "Pilih Halaman:",
        [
            "📊 Executive Summary",
            "🚨 Subsidiary Anomaly Tracker",
            "🏢 Segment Breakdown Analysis",
            "🧮 Executive What-If Simulator",
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        "**Sumber Data:**\n"
        "Profil Keuangan Konsolidasi & Anak Perusahaan TelkomGroup FY 2024–2025.\n\n"
        "Seluruh nilai dalam **Miliar Rupiah (Rp M)** kecuali dinyatakan lain."
    )

    if menu == "📊 Executive Summary":
        render_executive_summary(data["consolidated"], data["subsidiaries"])
    elif menu == "🚨 Subsidiary Anomaly Tracker":
        render_subsidiary_anomaly(data["subsidiaries"])
    elif menu == "🏢 Segment Breakdown Analysis":
        render_segment_breakdown(data["segments"])
    elif menu == "🧮 Executive What-If Simulator":
        render_what_if_simulator(data["consolidated"], data["subsidiaries"])


if __name__ == "__main__":
    main()
