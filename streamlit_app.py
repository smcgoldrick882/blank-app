import streamlit as st

def round_weight(w):
    return int(round(w / 5.0)) * 5

def get_me_lower(week):
    if week in [1, 2, 3]:
        return "Pin Pulls (below knee), work up to a heavy single"
    elif week in [4, 5, 6]:
        return "Dimel Deadlifts: 2–3 sets x 20 reps @ ~30% DL (~190 lbs)"
    else:
        return "SSB Good Morning to Low Box: work up to a heavy triple"

def get_me_upper(week):
    if week in [1, 2, 3]:
        return "Close-Grip Incline Press, work up to a heavy single"
    elif week in [4, 5, 6]:
        return "Floor Press, work up to a heavy single"
    else:
        return "2-Board Press, work up to a heavy single"

def get_dynamic_lower(week):
    squat_1rm = 550
    dl_1rm = 635
    squat_pct = min(60, 45 + (week - 1) * 2)
    squat_weight = round_weight(squat_1rm * squat_pct / 100)
    dl_weight = round_weight(dl_1rm * 0.55)
    return f"Box Squats: 8x2 @ {squat_pct}% = {squat_weight} lbs\nSpeed Pulls: 6x1 @ ~55% = {dl_weight} lbs"

def get_dynamic_upper():
    bench_1rm = 315
    bench_weight = round_weight(bench_1rm * 0.55)
    return f"Speed Bench: 8x3 @ 50–60% = {bench_weight} lbs average, rotate grips"

def get_gpp(week):
    base = ["Sled Drag x3", "Pushups x10", "Band Pullaparts x20"]
    if week >= 3:
        base += ["GHR x5", "Situps x10"]
    if week >= 5:
        base += ["Chins x5", "Neck Raises x15"]
    return base

def get_assistance(day):
    if day == 1:
        return ["GHR: 3x5–10", "Reverse Hypers: 3x8–12", "Pulldown Abs: 5x15", "Hanging Leg Raises: 3x15"]
    elif day == 2:
        return ["JM Press: 4x6–8", "Lateral Raises: 3x10–15", "Face Pulls: 4x15", "DB Rows: 4x8"]
    elif day == 3:
        return ["Single Leg RDL: 3x10/leg", "Band Abductions: 3x30s holds", "Incline Sit-Ups or Pulldown Abs: 4x15"]
    elif day == 4:
        return ["DB Triceps Extensions: 4x10", "Front Raises: 3x12", "Rear Delt Flyes: 3x12", "Chest Supported Rows: 4x8"]
    return []

def display_workout(week, day, auto_reg):
    titles = {1: "Max Effort Lower", 2: "Max Effort Upper", 3: "Dynamic Effort Lower", 4: "Dynamic Effort Upper"}
    title = titles.get(day, "Invalid Day")

    if day == 1:
        main = get_me_lower(week)
    elif day == 2:
        main = get_me_upper(week)
    elif day == 3:
        main = get_dynamic_lower(week)
    elif day == 4:
        main = get_dynamic_upper()
    else:
        main = "Invalid day selection."

    st.subheader(f"{title} - Week {week}")
    st.markdown(f"**Main Lift:** {main}")

    st.markdown("**Assistance Work:**")
    for move in get_assistance(day):
        st.write(f"- {move}")

    st.markdown("**GPP/Warmup Suggestions:**")
    for move in get_gpp(week):
        st.write(f"- {move}")

    if auto_reg:
        st.markdown("**Auto-Regulation Enabled:** Use heavy triples, reduce sets to 6, or extend rest.")

# === App UI ===

st.title("Conjugate Training Cheat Sheet")

week = st.selectbox("Select Week", list(range(1, 10)))
day = st.selectbox(
    "Select Training Day",
    [(1, "Max Effort Lower"), (2, "Max Effort Upper"), (3, "Dynamic Effort Lower"), (4, "Dynamic Effort Upper")],
    format_func=lambda x: x[1]
)
auto_reg = st.checkbox("Enable Auto-Regulation")

display_workout(week, day[0], auto_reg)
