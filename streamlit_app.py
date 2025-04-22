import streamlit as st

def round_weight(w):
    return int(round(w / 5.0)) * 5

def get_me_lower(week, auto_reg):
    if week in [1, 2, 3]:
        return "Pin Pulls (below knee), work up to a heavy single" if not auto_reg else "Pin Pulls, heavy triple"
    elif week in [4, 5, 6]:
        return "Dimel Deadlifts: 2–3x20 @ ~30%" if not auto_reg else "Dimel Deads: 1–2x15, lower RPE"
    else:
        return "SSB Good Morning to Low Box: work up to a heavy triple" if not auto_reg else "SSB Good Morning: Top set of 5"

def get_me_upper(week, auto_reg):
    if week in [1, 2, 3]:
        return "Close-Grip Incline Press, work up to a heavy single" if not auto_reg else "Close-Grip Incline, work up to 90% single"
    elif week in [4, 5, 6]:
        return "Floor Press, work up to a heavy single" if not auto_reg else "Floor Press, top set of 3"
    else:
        return "2-Board Press, work up to a heavy single" if not auto_reg else "2-Board Press, single at RPE 8"

def get_dynamic_lower(week, auto_reg):
    squat_1rm = 550
    dl_1rm = 635
    base_pct = 45 + (week - 1) * 2
    squat_pct = min(60, base_pct)
    squat_sets = 8 if not auto_reg else 6
    squat_weight = round_weight(squat_1rm * squat_pct / 100)
    dl_pct = 0.55 if not auto_reg else 0.50
    dl_weight = round_weight(dl_1rm * dl_pct)
    return f"Box Squats: {squat_sets}x2 @ {squat_pct}% = {squat_weight} lbs\nSpeed Pulls: 6x1 @ ~{int(dl_pct*100)}% = {dl_weight} lbs"

def get_dynamic_upper(auto_reg):
    bench_1rm = 315
    bench_pct = 0.55 if not auto_reg else 0.50
    bench_weight = round_weight(bench_1rm * bench_pct)
    sets = 8 if not auto_reg else 6
    return f"Speed Bench: {sets}x3 @ 50–60% = {bench_weight} lbs average, rotate grips"

def get_gpp(week, auto_reg):
    base = ["Sled Drag x3", "Pushups x10", "Band Pullaparts x20"]
    if week >= 3:
        base += ["GHR x5", "Situps x10"]
    if week >= 5:
        base += ["Chins x5", "Neck Raises x15"]
    if auto_reg:
        base = base[:3]  # trim for lower fatigue
    return base

def get_assistance(day, auto_reg):
    def mod(reps):
        return reps if not auto_reg else f"{int(int(reps.split('x')[0])*0.75)}x{int(int(reps.split('x')[1])*0.8)}"

    if day == 1:
        return [
            f"GHR: {mod('3x10')}",
            f"Reverse Hypers: {mod('3x12')}",
            f"Pulldown Abs: {mod('5x15')}",
            f"Hanging Leg Raises: {mod('3x15')}"
        ]
    elif day == 2:
        return [
            f"JM Press: {mod('4x8')}",
            f"Lateral Raises: {mod('3x15')}",
            f"Face Pulls: {mod('4x15')}",
            f"DB Rows: {mod('4x8')}"
        ]
    elif day == 3:
        return [
            f"Single Leg RDL: {mod('3x10')}",
            f"Band Abductions: {mod('3x30') + 's hold'}",
            f"Incline Sit-Ups or Pulldown Abs: {mod('4x15')}"
        ]
    elif day == 4:
        return [
            f"DB Triceps Extensions: {mod('4x10')}",
            f"Front Raises: {mod('3x12')}",
            f"Rear Delt Flyes: {mod('3x12')}",
            f"Chest Supported Rows: {mod('4x8')}"
        ]
    return []

def display_workout(week, day, auto_reg):
    titles = {
        1: "Max Effort Lower",
        2: "Max Effort Upper",
        3: "Dynamic Effort Lower",
        4: "Dynamic Effort Upper"
    }
    title = titles.get(day, "Invalid Day")

    if day == 1:
        main = get_me_lower(week, auto_reg)
    elif day == 2:
        main = get_me_upper(week, auto_reg)
    elif day == 3:
        main = get_dynamic_lower(week, auto_reg)
    elif day == 4:
        main = get_dynamic_upper(auto_reg)
    else:
        main = "Invalid day selection."

    st.subheader(f"{title} — Day {day} — Week {week}")
    st.markdown(f"**Main Lift:**\n{main}")

    st.markdown("**Assistance Work:**")
    for move in get_assistance(day, auto_reg):
        st.write(f"- {move}")

    st.markdown("**GPP / Warmup:**")
    for move in get_gpp(week, auto_reg):
        st.write(f"- {move}")

# === App UI ===

st.title("Conjugate Training Cheat Sheet")

week = st.selectbox("Select Week", list(range(1, 10)))
day = st.selectbox(
    "Select Training Day",
    [(1, "1 — Max Effort Lower"), (2, "2 — Max Effort Upper"),
     (3, "3 — Dynamic Effort Lower"), (4, "4 — Dynamic Effort Upper")],
    format_func=lambda x: x[1]
)
auto_reg = st.checkbox("Enable Auto-Regulation Mode")

display_workout(week, day[0], auto_reg)
