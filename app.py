import streamlit as st
import pandas as pd
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Fitness Planner", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title("🏋 AI Fitness Planner")

st.sidebar.markdown("### Enter Your Details")

age = st.sidebar.number_input("Age", 10, 60)
weight = st.sidebar.number_input("Weight (kg)", 20, 120)
height = st.sidebar.number_input("Height (cm)", 100, 200)

goal = st.sidebar.selectbox(
    "Fitness Goal",
    ["Weight Loss", "Muscle Gain", "General Fitness"]
)

diet = st.sidebar.selectbox("Diet Preference", ["Veg", "Non-Veg"])

budget = st.sidebar.selectbox("Budget Level", ["Low", "Medium"])

time_available = st.sidebar.selectbox(
    "Daily Available Time",
    ["15 min", "30 min", "45 min", "60 min"]
)

generate = st.sidebar.button("Generate My Plan")

# ---------- TITLE ----------
st.title("💪 Personalized Workout & Diet Planner with AI")

st.markdown("""
Welcome to the **AI Powered Student Fitness Planner**  
Your personal smart assistant for healthy living!
""")

st.markdown("---")

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
        return 12000
    elif goal == "Muscle Gain":
        return 9000
    else:
        return 10000

# ---------- WORKOUT PLANS ----------
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

# ---------- MAIN LOGIC ----------
if generate:

    with st.spinner("Analyzing your details..."):
        time.sleep(2)

    st.success("Analysis Complete!")

    # Animation effect
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    bmi = calculate_bmi(weight, height)
    calories = calorie_requirement(weight, height, age, goal)

    st.header("📊 Health Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("BMI Value", bmi)
    col2.metric("BMI Category", bmi_category(bmi))
    col3.metric("Daily Calories", f"{round(calories)} kcal")

    st.markdown("---")

    st.subheader("🎯 Fitness Indicators")

    col1, col2 = st.columns(2)

    with col1:
        st.write("BMI Progress")
        st.progress(min(int((bmi / 40) * 100), 100))

    with col2:
        steps = step_suggestion(goal)
        st.write("Step Goal Progress")
        st.progress(int((steps / 15000) * 100))

    st.markdown("---")

    # Animated Counter
    st.subheader("💧 Lifestyle Suggestions")

    water = water_intake(weight)

    counter = st.empty()

    for i in range(1, int(water * 10) + 1):
        counter.write(f"Recommended Water Intake: {i/10} liters")
        time.sleep(0.05)

    st.info(f"Final Recommendation: {water} liters of water daily")
    st.info(f"Daily Step Target: {steps} steps")

    st.markdown("---")

    st.subheader("🍎 Personalized Diet Plan")

    diet_data = pd.read_csv("diet_data.csv")

    diet_plan = diet_data[
        (diet_data["goal"] == goal) &
        (diet_data["diet_type"] == diet) &
        (diet_data["budget"] == budget)
    ]

    with st.expander("View Diet Recommendation"):
        if not diet_plan.empty:
            st.table(diet_plan[["meal_plan", "protein", "carbs", "fats"]])
        else:
            st.write("Balanced healthy diet recommended")

    st.markdown("---")

    st.subheader("🏋 Weekly Workout Plan")

    plan = weekly_plans.get(goal)

    workout_table = pd.DataFrame({
        "Day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        "Workout": plan
    })

    with st.expander("View Workout Schedule"):
        st.table(workout_table)

    st.markdown("---")

    st.subheader("📈 Nutrition Breakdown Chart")

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

    st.markdown("---")

    # Final Celebration Animation
    st.subheader("🎉 Plan Ready!")

    st.balloons()

    st.success("Your AI Personalized Fitness Plan is Ready to Follow!")

    st.download_button(
        label="Download My Fitness Report",
        data="Your AI Generated Fitness Plan is Ready!",
        file_name="fitness_report.txt"
    )

    st.markdown("---")

    st.write("Built with ❤️ using Python, Streamlit and AI")

else:
    st.info("Fill details in sidebar and click 'Generate My Plan'")
