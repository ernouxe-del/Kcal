import streamlit as st
import pandas as pd
import plotly.express as px
from database import init_db, log_meal, log_exercise, get_weekly_data
from utils import get_nutrition, calculate_bmr

st.set_page_config(page_title="NutriTrack Perso", layout="wide")
init_db()

st.title("🥗 Mon Coach Diététique Perso")

# Sidebar - Profil
st.sidebar.header("Mon Profil")
poids = st.sidebar.number_input("Poids (kg)", value=70)
taille = st.sidebar.number_input("Taille (cm)", value=175)
age = st.sidebar.number_input("Âge", value=30)
genre = st.sidebar.selectbox("Genre", ["Homme", "Femme"])
objectif = st.sidebar.number_input("Objectif Kcal/jour", value=2000)

bmr = calculate_bmr(poids, taille, age, genre)
st.sidebar.info(f"Votre métabolisme de base (BMR) : **{int(bmr)} kcal**")

# Tabs principales
tab1, tab2, tab3 = st.tabs(["Suivi Journalier", "Dépense Physique", "Rapports Hebdo"])

with tab1:
    st.subheader("Ajouter un plat")
    food_query = st.text_input("Qu'avez-vous mangé ? (ex: '2 eggs and 100g chicken')")
    if st.button("Analyser et Enregistrer"):
        nutri = get_nutrition(food_query)
        if nutri:
            log_meal(food_query, nutri)
            st.success(f"Enregistré : {nutri['calories']} kcal | P: {nutri['protein_g']}g")
        else:
            st.error("Erreur d'analyse. Essayez en anglais pour de meilleurs résultats.")

with tab2:
    st.subheader("Dépense énergétique")
    col1, col2 = st.columns(2)
    with col1:
        activity = st.text_input("Activité (ex: Running)")
    with col2:
        kcal_lost = st.number_input("Calories brûlées", min_value=0)
    if st.button("Enregistrer l'effort"):
        log_exercise(activity, kcal_lost)
        st.info("Sport enregistré !")

with tab3:
    st.subheader("Analyse des progrès")
    df_meals, df_exercise = get_weekly_data()
    
    if not df_meals.empty:
        df_meals['date'] = pd.to_datetime(df_meals['date'])
        daily_kcal = df_meals.groupby('date')['kcal'].sum().reset_index()
        
        fig = px.bar(daily_kcal, x='date', y='kcal', title="Consommation de Calories par Jour")
        fig.add_hline(y=objectif, line_dash="dot", line_color="red", annotation_text="Objectif")
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("📊 **Récapitulatif Hebdomadaire**")
        avg_kcal = daily_kcal['kcal'].mean()
        st.metric("Moyenne Kcal", f"{int(avg_kcal)} kcal", delta=f"{int(avg_kcal - objectif)}")
    else:
        st.write("Aucune donnée pour le moment.")
