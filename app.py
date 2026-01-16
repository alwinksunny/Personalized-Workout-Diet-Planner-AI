import streamlit as st
import pandas as pd

st.title("Personalized Workout & Diet Planner with AI")

# -------- SIDEBAR INFORMATION --------
st.sidebar.title("Fitness AI Planner")
st.sidebar.write("Generate personalized workout and diet plans")
st.sidebar.write("Designed especially for students")

st.write("Enter your details to generate a customized fitness and diet plan")

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


def water_intake(weight):
    return round(weight * 0.033, 2)


def step_suggestion(goal):
    if goal == "Weight Loss":
        return "10,000 - 12,000 steps per day"
    elif goal == "Muscle Gain":
        return "7,000 - 9,000 steps per day"
    else:
        return "8,000 - 10,000 steps per day"


# ---------- WEEKLY WORKOUT PLANS ----------

weekly_plans = {
    "Weight Loss": [
        "30 min Cardio",
        "Light Strength Training",
        "30 min Brisk Walk",
        "Cardio + Abs",
        "Full Body Workout",
        "Yoga or Stretching",
        "Rest"
    ],

    "Muscle Gain": [
        "Chest and Triceps",
        "Back and Biceps",
        "Legs Workout",
        "Shoulders",
        "Full Body Strength",
        "Core Training",
        "Rest"
    ],

    "General Fitness": [
        "Jogging",
        "Yoga",
        "Strength Training",
        "Cardio",
        "Mixed Workout",
        "Outdoor Activity",
        "Rest"
    ]
}


# ---------- MAIN PROCESS ----------

if st.button("Generate Plan"):

    bmi = calculate_bmi(weight, height)

    st.subheader("Health Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**BMI Value:**", bmi)

    with col2:
        st.write("**BMI Category:**", bmi_category(bmi))

    calories = calorie_requirement(weight, height, age, goal)

    st.subheader("Daily Calorie Requirement")
    st.write(f"Approximately **{round(calories)} kcal per day**")

    # Extra Recommendations
    st.subheader("Additional Health Recommendations")

    st.write("**Daily Water Intake:**", water_intake(weight), "liters")
    st.write("**Recommended Step Count:**", step_suggestion(goal))

    # Load datasets
    diet_data = pd.read_csv("diet_data.csv")

    diet_plan = diet_data[
        (diet_data["goal"] == goal) &
        (diet_data["diet_type"] == diet) &
        (diet_data["budget"] == budget)
    ]

    st.subheader("Personalized Diet Recommendation")

    if not diet_plan.empty:
        st.table(diet_plan[["meal_plan", "protein", "carbs", "fats"]])
    else:
        st.write("Balanced healthy diet recommended")

    st.subheader("Weekly Workout Schedule")

    plan = weekly_plans.get(goal)

    workout_table = pd.DataFrame({
        "Day": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "Workout Plan": plan
    })

    st.table(workout_table)

    # ---- SIMPLE VISUALIZATION ----

    st.subheader("Nutrition Distribution Visualization")

    if not diet_plan.empty:
        values = [
            int(diet_plan["protein"].values[0].replace("g","")),
            int(diet_plan["carbs"].values[0].replace("g","")),
            int(diet_plan["fats"].values[0].replace("g",""))
        ]

        chart_data = pd.DataFrame({
            "Nutrient": ["Protein", "Carbs", "Fats"],
            "Grams": values
        })

        st.bar_chart(chart_data.set_index("Nutrient"))

    st.info("Follow this plan consistently for best results")

    st.success("Your Advanced Personalized Plan is Ready")

    # Download option
    st.download_button(
        label="Download Plan Summary",
        data="Personalized Plan Generated Successfully",
        file_name="fitness_plan.txt"
    )
