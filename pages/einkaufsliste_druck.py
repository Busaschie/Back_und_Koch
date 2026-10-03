from datetime import datetime
from urllib import response

import pandas as pd
import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

# --- Page Setup for Printing ---
st.set_page_config(
    page_title="Wareneinkaufszettel",
    layout="wide",
    #initial_sidebar_state="collapsed",
)

# --- A4 Print & Screen Beautified Styling ---
st.html(
    """
<style>
    /* 1. DRUCK-MODUS (STRG + P) */
    @media print {
        @page {
            size: A4 portrait;
            margin-top: 1cm !important;
            margin-bottom: 1.5cm !important;
            margin-left: 0mm !important;
            margin-right: 0mm !important;
        }

        header, 
        footer, 
        .stButton, 
        div[data-testid="stSidebar"], 
        section[data-testid="stSidebar"],
        nav[data-testid="stSidebarNav"],
        div[data-testid="stHeader"], 
        .no-print, 
        .stAlert,
         hr {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
        }

        html, body,
        div[data-testid="stAppViewContainer"],
        div[data-testid="stAppViewBlockContainer"],
        div[data-testid="stMainBlockContainer"],
        .main,
        .main, .block-container {
            background-color: #ffffff !important;
            margin: 0 !important;
            padding: 0 !importan;
            width: 100% !importan;
            max-width: 100% !important;
            min-width: 100% !important;
        }
    
        .print-container {
            margin-top -2000px !important;
            width: 100% !important;
            max-width: 21cm !important;
            margin: 0 auto !important;
            padding: 0 auto !important;
            box-shadow: none !important;
            borders: none !important;
            box-sizing: border-box !important;
        }
         /* Abstand von Oben */
        .header-table {
            margin-top: -100px;
        }

        tr {
            page-brake-inside: avoid !important;
            break-inside: avoid !important;
        }
        
        thead {
            display: table-header-group !important;
        }
        
        /* Verhindert das Abschneiden der Tabelle auf Seite 2 */
        thead th {
            padding-top: 10px !important;
        }
        
        .footer-section {
            margin-top: 30px;
            width: 100%;
        }
    
        .small {
            font-size: 10px;
        }
  }
  
 /*  2. BILDSCHIRM-VORSCHAU */
 div[data-test-id="stMainBlockContainer"],
 .main .block-container {
    max-width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
 }
 
.print-container {
    max-width: 21cm;
    margin: 20px auto;
    background-color: #ffffff;
    padding: 1.5cm;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
    border-radius: 4px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #000000;
    box-sizing: border-box;
}

.header-table {
    width: 100%;
    margin-bottom: 20px;
    border-bottom: 2px solid #000000;
    padding-bottom: 10px;
}

.header-title {
    font-size: 22px;
    font-weight: bold;
    text-transform: uppercase;
    margin: 0;
}

.header-sub {
    font-size: 13px;
    color: #444444;
    margin-top: 5px;
}

.items-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

.items-table th {
    background-color: #f2f2f2 !important;
    color: #000000;
    font-weight: bold;
    font-size: 12px;
    padding: 8px 6px;
    border: 1px solid #000000 !important;
    text-align: left;
    -webkit-print-color-adjust: exact;
}

.items-table td {
    padding: 5px;
    font-size: 11px;
    border: 1px solid #000000 !important;
    vertical-align: middle;
}

.col-stueck { width: 6%; text-align: center; }
.col-leer1 { width: 6%; text-align: center; }
.col-leer2 { width: 6%; text-align: center; }
.col-bezeichnung { width: 34%; font-weight: 600; }
.col-einheit { width: 10%; text-align: center; }
.col-ep { width: 11%; text-align: right; }
.col-gp { width: 11%; text-align: right; }
.col-korrektur { width: 16%; text-align: center; }

.total-row td {
    font-weight: bold;
    background-color: #fafafa !important;
    font-size: 13px;
    -webkit-print-color-adjust: exact;
}

.footer-section {
    margin-top: 30px;
    width: 100%;
}

.small {
    font-size: 10px;
}
.info-row td {
    font-size:11px;
}
.notes-box {
    border: 1px solid #000000;
    height: 60px;
    margin-top: 5px;
    padding: 5px;
    font-size: 11px;
    color: #555555;
}

.signature-table {
    width: 100%;
    margin-top: 40px;
}

.sig-line {
    border-top: 1px solid #000000;
    text-align: center;
    font-size: 11px;
    padding-top: 5px;
} 
</style>
"""
)

# Task-ID aus Session State laden
task_id = st.session_state.get("print_task_id")

# Helper zum Berechnung der Summe aus Wallet
def get_wallet_sum_schritt_zwei(task_id: int) -> float:
    if not task_id:
        return 0.0
    try:
        response = requests.get(f"{BASE_URL}/wallets/wallet_task", params={"task_id": task_id, "schritt": "zwei"}, timeout=5)
        if response.status_code == 200:
            wallet = response.json()
            if isinstance(wallet, list):
                total_abbuchung = sum(float(w.get("betrag", 0.0)) for w in wallet if w.get("betrag") is not None)
                total_old = sum(float(w.get("old_amount", 0.0)) for w in wallet if w.get("old_amount") is not None)
                total_sum = [total_abbuchung, total_old]
                return total_sum
    except Exception as e:
        st.warning(f"Konnte Wallet-Summer für Schritt 2 nicht laden: {e}")
    return 0.0


if task_id:
    task_id = int(task_id)
else:
    st.error(
        "Keine aktive Vorgangs-ID gefunden! Bitte wähle zuerst auf der"
        " Hauptseite einen Vorgang aus."
    )
    if st.button("🔙 Zurück zur Hauptseite"):
        st.switch_page("pages/vorgang.py")
    st.stop()

# Oberer Hinweisbereich
st.html(
    f"""
    <div class="no-print" style="background-color: #e8f4f8; padding: 12px; border-radius: 6px; margin-bottom: 15px;">
        <h4 style="margin:0; color: #1e3d59;">🖨️ Einkaufsliste Druckansicht (Vorgang #{task_id})</h4>
        <p style="margin: 5px 0 0 0; font-size: 13px;">💡 <strong>Tipp:</strong> Drücke <code>STRG + P</code> zum Drucken.</p>
    </div>
"""
)

if st.button("🔄 Daten frisch synchronisieren", key="sync_btn"):
    st.rerun()

# --- Gecachte Ladefunktion für schnelle Ladezeiten ---
@st.cache_data(ttl=60)
def load_data(current_task_id: int):
    try:
        res = requests.get(
            f"{BASE_URL}/bestellung/{current_task_id}/bestellung_task",
            timeout=5,
        )

        if res.status_code == 200:
            items = res.json()
            if not items:
                return None, f"Für den Vorgang #{current_task_id} wurde noch keine Einkaufsliste gefunden."

            data = {
                "task": {"id": current_task_id, "created_at": None},
                "items": items,
            }
            return data, None

        elif res.status_code == 404:
            return None, f"Für den Vorgang #{current_task_id} wurde noch keine Einkaufsliste gefunden."

        return None, f"Fehler beim Laden der Einkaufsliste (Status: {res.status_code})"
    except Exception as e:
        return None, f"Verbindung zur API fehlgeschlagen: {e}"


data, error = load_data(task_id)

if error:
    st.error(error)
elif not data:
    st.warning("Keine Daten für diese Einkaufsliste vorhanden.")
else:
    items = data.get("items", [])
    created_at_fmt = datetime.now().strftime("%d.%m.%Y / %H:%M")
    df_items = pd.DataFrame(items)

    if df_items.empty:
        table_rows_html = """
            <tr>
                <td colspan="8" style="text-align: center; color: #666; font-style: italic;">Keine Artikel in dieser Einkaufsliste.</td>
            </tr>
        """
    else:
        df_filtered = df_items[df_items["bestellmenge"] > 0]
        gesamtsumme = df_filtered["gesamt_preis"].sum()
        gesamt_artikel = df_filtered["bestellmenge"].sum()

        summe_schritt_zwei = get_wallet_sum_schritt_zwei(task_id)
        bar_gesamt = summe_schritt_zwei[0] + summe_schritt_zwei[1]
        bar_ueber = bar_gesamt - gesamtsumme

        rows = []
        for _, row in df_filtered.iterrows():
            bezeichnung = row.get("bezeichnung", "")
            bestellmenge = int(row.get("bestellmenge", 0))
            preis = float(row.get("preis", 0.0))
            gesamt = float(row.get("gesamt_preis", 0.0))
            art = row.get("art", "")
            menge = row.get("menge", "")

            rows.append(f"""
            <tr>
                <td class="col-stueck">{bestellmenge}</td>
                <td class="col-leer1">   </td>
                <td class="col-leer2">   </td>
                <td class="col-bezeichnung">{bezeichnung}</td>
                <td class="col-einheit">{menge} {art}</td>
                <td class="col-ep">{preis:,.2f} €</td>
                <td class="col-gp">{gesamt:,.2f} €</td>
                <td class="col-korrektur">   </td>
            </tr>
            """)

        rows.append(f"""
            <tr class="total-row">
                <td class="col-stueck">{gesamt_artikel}</td>
                <td class="col-leer1">   </td>
                <td class="col-leer2">   </td>
                <td class="col-bezeichnung">Bestellung Gesamt</td>
                <td class="col-einheit"></td>
                <td class="col-ep"></td>
                <td class="col-gp">{gesamtsumme:,.2f} €</td>
                <td class="col-korrektur">   </td>
            </tr>
            <tr class="info-row">
                <td></td>
                <td colspan="3">Bar ausgezahlt für aktuellen Einkauf</td>
                <td></td>
                <td></td>
                <td class="col-gp">{summe_schritt_zwei[0]:,.2f} €</td>
                <td></td>
            </tr>
            <tr class="info-row">
                <td></td>
                <td colspan="3">Alter Kontostand</td>
                <td></td>
                <td></td>
                <td class="col-gp">{summe_schritt_zwei[1]:,.2f} €</td>
                <td></td>
            </tr>
            <tr class="info-row">
                <td></td>
                <td colspan="3">Neuer / Aktueller Kontostand / Bar gesamt</td>
                <td></td>
                <td></td>
                <td class="col-gp">{bar_gesamt:,.2f} €</td>
                <td></td>
            </tr>
            <tr class="info-row">
                <td></td>
                <td colspan="3">Überschuß / Bar für aktuellen Einkauf*</td>
                <td></td>
                <td></td>
                <td class="col-gp">{bar_ueber:,.2f} €</td>
                <td></td>
            </tr>
        """)

        table_rows_html = "".join(rows)

    html_content = f"""
    <div class="a4-page">
    <div class="print-container">
        <table class="header-table">
            <tr>
                <td>
                    <div class="header-sub">Vorgang #{task_id} | Erstellt am: {created_at_fmt}</div>
                </td>
                <td style="text-align: right; vertical-align: bottom;">
                    <div style="font-size: 12px; font-weight: bold;">Viel Spaß beim Einkaufen!</div>
                </td>
            </tr>
        </table>

        <table class="items-table">
            <thead>
                <tr>
                    <th class="col-stueck">Stk</th>
                    <th class="col-leer1"></th>
                    <th class="col-leer2"></th>
                    <th class="col-bezeichnung">Bezeichnung</th>
                    <th class="col-einheit">Einheit</th>
                    <th class="col-ep">Einzelpreis</th>
                    <th class="col-gp">Gesamtpreis</th>
                    <th class="col-korrektur">Korrektur</th>
                </tr>
            </thead>
            <tbody>
                {table_rows_html}
            </tbody>
        </table>
        <div class="small">* Rechnerischer Betrag, bei vorhandensein aller Artikel und aktuellen Warenwert</div>

        <div class="footer-section">
        </div>
    </div>
    </div>
    """

    st.html(html_content)