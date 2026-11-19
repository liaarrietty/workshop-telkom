import pandas as pd
import numpy as np


def load_consolidated_data() -> pd.DataFrame:
    """
    Memuat data kinerja keuangan konsolidasi Telkom Indonesia 2024 vs 2025.
    Satuan nilai dalam Miliar Rupiah (Rp M), kecuali Margin (%).
    """
    data = {
        "Metrik": [
            "Pendapatan Konsolidasi",
            "EBITDA",
            "Laba Bersih Parent",
            "Operating Margin (%)",
            "Cadangan Kerugian Piutang (ECL)",
            "Unrealized Loss Investasi (GOTO/MDI)",
        ],
        "2024": [149967.0, 75029.0, 22403.0, 28.7, 6064.0, 0.0],
        "2025": [146742.0, 72240.0, 17814.0, 23.6, 6955.0, 242.0],
        "YoY_Change_Pct": [-2.2, -3.7, -20.5, -5.1, 14.7, np.nan],
        "Satuan": ["Rp M", "Rp M", "Rp M", "%", "Rp M", "Rp M"],
    }
    df = pd.DataFrame(data)
    df["Selisih_Absolut"] = df["2025"] - df["2024"]
    return df


def load_segment_data() -> pd.DataFrame:
    """
    Memuat data kinerja segmen bisnis Telkom Indonesia tahun 2025.
    Satuan nilai dalam Miliar Rupiah (Rp M).
    """
    data = {
        "Segmen": ["B2C", "B2B ICT", "B2B Infra", "International", "Others"],
        "Pendapatan_2025": [105898.0, 15300.0, 8929.0, 10673.0, 5942.0],
        "Result_2025": [27793.0, 1759.0, 10487.0, 961.0, -4491.0],
        "YoY_Result_Growth_Pct": [np.nan, 25.5, -36.3, -20.2, np.nan],
        "Deskripsi": [
            "Segmen ritel & seluler (Telkomsel, IndiHome)",
            "Layanan solusi ICT korporasi & enterprise",
            "Infrastruktur menara, jaringan & data center",
            "Layanan telekomunikasi internasional & carrier",
            "Lainnya & eliminasi/beban korporat",
        ],
    }
    df = pd.DataFrame(data)
    df["Operating_Margin_Pct"] = (df["Result_2025"] / df["Pendapatan_2025"]) * 100
    df["Kontribusi_Pendapatan_Pct"] = (
        df["Pendapatan_2025"] / df["Pendapatan_2025"].sum()
    ) * 100
    return df


def load_subsidiary_data() -> pd.DataFrame:
    """
    Memuat data kinerja anak perusahaan kunci TelkomGroup tahun 2025.
    Satuan nilai dalam Miliar Rupiah (Rp M).
    """
    data = {
        "Entitas": [
            "Telkomsel",
            "Mitratel",
            "Telin",
            "PT Telkom Infrastruktur Indonesia (TIF)",
            "PT Telkom Akses",
            "PT Telkom Satelit Indonesia (Telkomsat)",
            "PT Sigma Cipta Caraka (Sigma)",
        ],
        "Pendapatan": [109307.0, 9534.0, 12169.0, 4455.0, 6083.0, 1844.0, 2613.0],
        "EBITDA": [49624.0, 7835.0, 1682.0, 612.0, 454.0, 557.0, 45.0],
        "Laba_Bersih": [19687.0, 2119.0, 944.0, 541.0, 174.0, -249.5, -363.6],
        "Status_Awal": [
            "Normal",
            "Normal",
            "Normal",
            "Normal",
            "Normal",
            "Anomali",
            "Anomali",
        ],
        "Catatan_Driver": [
            "Kontributor utama pendapatan & laba konsolidasi",
            "Margin EBITDA sangat kuat (82,2%) dari bisnis menara",
            "Kinerja stabil pada segmen internasional",
            "Entitas infrastruktur baru dengan profitabilitas sehat",
            "Ekspansi jaringan FTTH dengan margin tipis",
            "Rugi akibat persaingan satelit & beban bunga tinggi",
            "Rugi membengkak 64,3% akibat Clean Sheet Strategy",
        ],
    }
    df = pd.DataFrame(data)
    df["EBITDA_Margin_Pct"] = (df["EBITDA"] / df["Pendapatan"]) * 100
    df["Net_Margin_Pct"] = (df["Laba_Bersih"] / df["Pendapatan"]) * 100
    # Estimasi Beban Operasional & Lainnya = Pendapatan - Laba Bersih (untuk visualisasi breakdown)
    df["Total_Beban_dan_Pajak"] = df["Pendapatan"] - df["Laba_Bersih"]
    return df


def load_all_data() -> dict:
    """Mengembalikan seluruh dataset dalam satu dictionary."""
    return {
        "consolidated": load_consolidated_data(),
        "segments": load_segment_data(),
        "subsidiaries": load_subsidiary_data(),
    }
