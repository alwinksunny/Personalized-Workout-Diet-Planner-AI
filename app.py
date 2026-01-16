import streamlit as st
import pandas as pd

st.title("Personalized Workout & Diet Planner with AI")

st.write("Enter your details to generate a customized plan")

age = st.number_input("Age", 10, 60)
weight = st.number_input("Weight (kg)", 20, 120)
height = st.number_input("Height (cm)", 100, 200)

goal = st.selectbox("Select Fitness Goal",
                    ["Weight Loss", "Muscle Gain", "General Fitness"])

diet = st.selectbox("Diet Preference",
                    ["Veg", "Non-Veg"])

budget = st.selectbox("Budget Level",
                      ["Low", "Medium"])

time = st.selectbox("Daily Available Time",
                    ["15 min", "30 min", "45 min", "60 min"])


def calculate_bmi(w, h):
    h = h / 100
    return round(w / (h * h), 2)


if st.button("Generate Plan"):

    bmi = calculate_bmi(weight, height)

    st.subheader("Your Health Details")
    st.write("BMI:", bmi)

    diet_data = pd.read_csv("diet_data.csv")
    workout_data = pd.read_csv("workout_data.csv")

    diet_plan = diet_data[
        (diet_data["goal"] == goal) &
        (diet_data["diet_type"] == diet) &
        (diet_data["budget"] == budget)
    ]

    workout_plan = workout_data[
        workout_data["goal"] == goal
    ]

    st.subheader("Recommended Workout Plan")

    if not workout_plan.empty:
        st.write(workout_plan["plan"].values[0])
    else:
        st.write("Default workout plan")

    st.subheader("Recommended Diet Plan")

    if not diet_plan.empty:
        st.write(diet_plan["meal_plan"].values[0])
    else:
        st.write("Balanced healthy diet recommended")

    st.success("Personalized Plan Generated Successfully")
