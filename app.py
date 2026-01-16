import streamlit as st
import pandas as pd

st.title("Personalized Workout & Diet Planner with AI")

st.write("Enter your details to generate a customized plan")

# ---------- USER INPUTS ----------

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


# ---------- FUNCTIONS ----------

def calculate_bmi(w, h):
    h = h / 100
    return round(w / (h * h), 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal Weight"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"


def calorie_requirement(weight, height, age, goal):
    bmr = 10 * weight + 6.25 * height - 5 * age + 5

    if goal == "Weight Loss":
        return bmr - 300
    elif goal == "Muscle Gain":
        return bmr + 300
    else:
        return bmr


# ---------- WEEKLY WORKOUT PLANS ----------

weekly_plans = {
    "Weight Loss": [
        "Monday - 30 min Cardio",
        "Tuesday - Light Strength Training",
        "Wednesday - 30 min Brisk Walk",
        "Thursday - Cardio + Abs",
        "Friday - Full Body Workout",
        "Saturday - Yoga or Stretching",
        "Sunday - Rest"
    ],

    "Muscle Gain": [
        "Monday - Chest and Triceps",
        "Tuesday - Back and Biceps",
        "Wednesday - Legs",
        "Thursday - Shoulders",
        "Friday - Full Body Strength",
        "Saturday - Core Training",
        "Sunday - Rest"
    ],

    "General Fitness": [
        "Monday - Jogging",
        "Tuesday - Yoga",
        "Wednesday - Strength Training",
        "Thursday - Cardio",
        "Friday - Mixed Workout",
        "Saturday - Outdoor Activity",
        "Sunday - Rest"
    ]
}


# ---------- MAIN PROCESS ----------

if st.button("Generate Plan"):

    bmi = calculate_bmi(weight, height)

    st.subheader("Your Health Analysis")

    st.write("BMI Value:", bmi)
    st.write("BMI Category:", bmi_category(bmi))

    calories = calorie_requirement(weight, height, age, goal)

    st.subheader("Daily Calorie Requirement")
    st.write(round(calories), "kcal per day")

    # Load datasets
    diet_data = pd.read_csv("diet_data.csv")
    workout_data = pd.read_csv("workout_data.csv")

    diet_plan = diet_data[
        (diet_data["goal"] == goal) &
        (diet_data["diet_type"] == diet) &
        (diet_data["budget"] == budget)
    ]

    st.subheader("Recommended Diet Plan")

    if not diet_plan.empty:
        st.write(diet_plan["meal_plan"].values[0])
    else:
        st.write("Balanced healthy diet recommended")

    st.subheader("Weekly Workout Schedule")

    plan = weekly_plans.get(goal)

    for day in plan:
        st.write(day)

    st.success("Your Personalized Plan is Ready")
