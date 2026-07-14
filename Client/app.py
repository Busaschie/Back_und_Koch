import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://localhost:8000"  # uvicorn -> restapi

# Seite auf weites Layout stellen, damit links und rechts genug Platz ist
st.set_page_config(layout="wide")


# API-Abfrage (wird von Streamlit gecacht)
@st.cache_data
def get_api_data():
    try:
        response = requests.get(f"{BASE_URL}/users")
        df = pd.DataFrame(response.json())
        return df[['vorname', 'nachname']].copy()

    except Exception as e:
        # Falls die API mal offline ist, stürzt die App nicht ab
        st.error(f"Fehler beim Laden der API: {e}")
        return pd.DataFrame(columns=['vorname', 'nachname'])


# !!! WICHTIG: Hier rufen wir die Funktion auf, um die Daten bereitzustellen !!!
df_gefiltert = get_api_data()

# ==========================================
# 1. NAVIGATION (Ganz oben über die volle Breite)
# ==========================================
with st.container(border=True):
    nav_col1, nav_col2, nav_col3, nav_spacer = st.columns([1, 1, 1, 7])
    with nav_col1:
        st.button("Home", use_container_width=True)
    with nav_col2:
        st.button("Dashboard", use_container_width=True)
    with nav_col3:
        st.button("Einstellungen", use_container_width=True)

st.write("---")  # Trennlinie

# ==========================================
# MAIN LAYOUT (Aufteilung in Links und Rechts)
# ==========================================
# 20% Breite für Links (Einkäufe), 80% Breite für Rechts (Übersichten)
col_links, col_rechts = st.columns([2, 8])

# --- LINKE SEITE: Container für Einkäufe ---
with col_links:
    with st.container(border=True):
        st.subheader("📋 Einkäufe")

        tasks = [
            {"id": 1, "task": "15.07.2026", "status": "Offen"},
            {"id": 2, "task": "19.06.2026", "status": "Erledigt"},
            {"id": 3, "task": "25.05.2026", "status": "Erledigt"}
        ]

        for t in tasks:
            with st.container(border=True):
                st.markdown(f"**{t['task']}**")

# --- RECHTE SEITE: Die 4 aufklappbaren Übersichten ---
with col_rechts:
    with st.container(border=True):
        st.subheader("Übersichten")

        # Expander 1
        with st.expander("Gruppe 1: Nutzerübersicht", expanded=True):
            # Kopie erstellen und die Status-Spalte für das Dropdown hinzufügen
            df_mit_status = df_gefiltert.copy()
            df_mit_status["Status"] = "Bitte wählen..."

            # Der Data Editor
            df_editiert = st.data_editor(
                df_mit_status,
                column_config={
                    "Status": st.column_config.SelectboxColumn(
                        "Status",  # Spaltenüberschrift in der Tabelle
                        help="Wähle einen Status für den Nutzer",
                        width="medium",
                        options=["Bitte wählen...", "Aktiv", "Inaktiv"],
                        required=True,
                    )
                },
                disabled=["vorname", "nachname"],  # Namen sind schreibgeschützt
                hide_index=True,
                use_container_width=True,
                key="nutzer_editor"  # Eindeutiger Key für Streamlit
            )

        # Expander 2
        with st.expander("Gruppe 2: Ausstehende Genehmigungen"):
            st.dataframe(df_gefiltert, hide_index=True, use_container_width=True)

        # Expander 3
        with st.expander("Gruppe 3: Archivierte Daten"):
            st.dataframe(df_gefiltert, hide_index=True, use_container_width=True)

        # Expander 4
        with st.expander("Gruppe 4: Sonstige Listen"):
            st.dataframe(df_gefiltert, hide_index=True, use_container_width=True)