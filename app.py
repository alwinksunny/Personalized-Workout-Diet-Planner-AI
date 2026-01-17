import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Fitness Planner", layout="wide")

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.title("🏋 Fitness Planner")

st.sidebar.write("Enter your details below")

age = st.sidebar.number_input("Age", 10, 60)
weight = st.sidebar.number_input("Weight (kg)", 20, 120)
height = st.sidebar.number_input("Height (cm)", 100, 200)

goal = st.sidebar.selectbox(
    "Select Fitness Goal",
    ["Weight Loss", "Muscle Gain", "General Fitness"]
)

diet = st.sidebar.selectbox(
    "Diet Preference",
    ["Veg", "Non-Veg"]
)

budget = st.sidebar.selectbox(
    "Budget Level",
    ["Low", "Medium"]
)

time = st.sidebar.selectbox(
    "Daily Available Time",
    ["15 min", "30 min", "45 min", "60 min"]
)

st.sidebar.write("Click below to generate your plan")
generate = st.sidebar.button("Generate Plan")

# ---------------- MAIN TITLE ----------------
st.title("💪 Personalized Workout & Diet Planner with AI")
st.markdown(
    "An intelligent system that creates customized fitness and diet plans "
    "based on your personal goals, budget, and lifestyle."
)

st.markdown("---")

# ---------------- FUNCTIONS ----------------
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

# ---------------- WEEKLY PLANS ----------------
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

# ---------------- MAIN PROCESS ----------------
if generate:

    st.header("📊 Your Health Summary")

    bmi = calculate_bmi(weight, height)
    calories = calorie_requirement(weight, height, age, goal)

    col1, col2, col3 = st.columns(3)

    col1.metric("BMI Value", bmi)
    col2.metric("BMI Category", bmi_category(bmi))
    col3.metric("Daily Calories", f"{round(calories)} kcal")

    st.markdown("---")

    st.header("💧 Lifestyle Recommendations")

    col1, col2 = st.columns(2)

    col1.info(f"**Daily Water Intake:** {water_intake(weight)} liters")
    col2.info(f"**Recommended Steps:** {step_suggestion(goal)}")

    st.markdown("---")

    # Load dataset
    diet_data = pd.read_csv("diet_data.csv")

    diet_plan = diet_data[
        (diet_data["goal"] == goal) &
        (diet_data["diet_type"] == diet) &
        (diet_data["budget"] == budget)
    ]

    st.header("🍎 Personalized Diet Plan")

    with st.expander("View Diet Details"):
        if not diet_plan.empty:
            st.table(diet_plan[["meal_plan", "protein", "carbs", "fats"]])
        else:
            st.write("Balanced healthy diet recommended")

    st.markdown("---")

    st.header("🏋 Weekly Workout Schedule")

    plan = weekly_plans.get(goal)

    workout_table = pd.DataFrame({
        "Day": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "Workout Plan": plan
    })

    with st.expander("View Workout Plan"):
        st.table(workout_table)

    st.markdown("---")

    st.header("📈 Nutrition Visualization")

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

    st.success("Your Personalized Plan is Generated Successfully")

    st.download_button(
        label="Download Plan Summary",
        data="Personalized Fitness Plan Generated Successfully",
        file_name="fitness_plan.txt"
    )

    st.markdown("---")

    st.write(
        "Developed using Python & Streamlit | AI Powered Student Fitness Planner"
    )

else:
    st.info("Please enter details in the sidebar and click 'Generate Plan'")
