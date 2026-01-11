import streamlit as st
import os

st.set_page_config(page_title="Hyponatremia Simulator", layout="wide")

# ===============================
# SESSION STATE
# ===============================
if "step" not in st.session_state:
    st.session_state.step = 0
if "case_choice" not in st.session_state:
    st.session_state.case_choice = None
if "answered" not in st.session_state:
    st.session_state.answered = False
if "visible_labs" not in st.session_state:
    st.session_state.visible_labs = ["Na⁺"]

# ===============================
# IMAGE PATH CONFIGURATION
# ===============================
DESKTOP_PATH = "" 

# ===============================
# LAB DATA DISPLAY LOGIC
# ===============================
LAB_VALUES = {
    "case1": {"Na⁺": "121", "Serum Osm": "258", "Urine Osm": "520", "Urine Na": "7", "BUN/Cr": "48 / 1.5"},
    "case2": {"Na⁺": "124", "Serum Osm": "265", "Urine Osm": "470", "Urine Na": "9"},
    "case3": {"Na⁺": "118", "Serum Osm": "255", "Urine Osm": "410", "Urine Na": "38"},
    "case4": {"Na⁺": "119", "Serum Osm": "260", "Urine Osm": "55", "Urine Na": "14"}
}

def display_dynamic_labs():
    case = st.session_state.case_choice
    labs = LAB_VALUES[case]
    current_display = [f"{k} {labs[k]}" for k in st.session_state.visible_labs if k in labs]
    st.markdown("### 🧪 Labs")
    st.code(" | ".join(current_display))

# ===============================
# CASE CONTENT FUNCTIONS
# ===============================
def show_case_1():
    st.markdown("### 📋 Clinical Vignette")
    st.info("""A 45-year-old woman presents with four days of persistent nausea and repeated non-bloody vomiting. She reports that she has barely been able to keep down fluids and feels lightheaded when standing. She notes her urine has become dark and infrequent. She has had no diarrhea, fevers, or new medications. She mentions that she has been trying to “push water” to stay hydrated, but admits she mostly sips small amounts because she feels constantly nauseated.
On exam, she appears fatigued with dry mucous membranes, cool extremities, and delayed capillary refill. Her blood pressure is 92/58 sitting and 84/50 standing, with a pulse of 120. Lungs are clear, and there is no edema.""")
    display_dynamic_labs()

def show_case_2():
    st.markdown("### 📋 Clinical Vignette")
    st.info("""A 72-year-old man with a history of congestive heart failure presents with worsening shortness of breath over the past week. He reports that he needs multiple pillows to sleep, has difficulty walking short distances without stopping to catch his breath, and feels his legs are “puffy and tight.” He denies diarrhea, vomiting, fevers, or new medications, though he admits missing several doses of his prescribed diuretic. He has been drinking more fluids because he “feels thirsty all the time,” but says this thirst is not helped by drinking.
On exam, he appears fatigued and mildly dyspneic. His blood pressure is 142/85 and his pulse is 102. You observe elevated jugular venous pressure, bibasilar crackles on lung auscultation, and 2+ pitting edema in both lower extremities. His abdomen is soft, and there is no guarding or tenderness. He has gained six pounds since his last appointment a week ago.""")
    display_dynamic_labs()

def show_case_3():
    st.markdown("### 📋 Clinical Vignette")
    st.info("""A 63-year-old man with recently diagnosed small cell lung cancer presents with increasing confusion, difficulty concentrating, and a new unsteady gait. His wife states that he has become progressively forgetful over the past week and has seemed “off.” He denies vomiting, diarrhea, or increased water intake. He has been eating normally and reports no pain, fevers, or medication changes.
On exam, he is alert but disoriented to time. His vital signs are stable, and physical exam reveals moist mucous membranes, no edema, and normal skin turgor. Lung and cardiac exams are unremarkable. Neurologically, he has mild confusion but no focal deficits. There are no signs of dehydration or volume overload.""")
    display_dynamic_labs()

def show_case_4():
    st.markdown("### 📋 Clinical Vignette")
    st.info("""A 37-year-old man with schizophrenia presents with nausea, dizziness, and intermittent confusion. His caregiver reports that he has been drinking “gallons of water” daily, sometimes filling up sinks or bathtubs to drink from. His diet has consisted mostly of crackers and juice for the past week. He denies alcohol use, vomiting, diarrhea, or diuretics.
On exam, he appears calm with normal vital signs. Skin turgor is normal, mucous membranes are moist, and he has no edema. His cardiopulmonary and abdominal exams are unremarkable. He does not appear dehydrated or fluid overloaded.""")
    display_dynamic_labs()

# ===============================
# MAIN NAVIGATION
# ===============================
st.title("🧠 Hyponatremia Clinical Reasoning Simulator")

if st.session_state.step == 0:
    st.session_state.visible_labs = ["Na⁺"]
    st.markdown("#### Select a case to begin the clinical simulation.")
    cols = st.columns(4)
    case_titles = ["Case A", "Case B", "Case C", "Case D"]
    case_keys = ["case1", "case2", "case3", "case4"]
    for i, col in enumerate(cols):
        if col.button(case_titles[i], key=f"btn_{i}", use_container_width=True):
            st.session_state.case_choice = case_keys[i]
            st.session_state.step = 1
            st.rerun()

else:
    cases = {"case1": show_case_1, "case2": show_case_2, "case3": show_case_3, "case4": show_case_4}
    show_case = cases[st.session_state.case_choice]

    # STEP 1: First Step (Selecting Lab)
    if st.session_state.step == 1:
        show_case()
        st.subheader("What is the FIRST step in evaluating this patient’s hyponatremia?")
        ans = st.radio("", ["Assess volume status", "Check serum osmolality", "Check urine sodium", "Restrict free water"], key="s1")
        if st.button("Submit"):
            if ans == "Check serum osmolality":
                st.success("Correct! When you see a low sodium level, the very first question you must ask is whether the sodium is truly low or whether something is artificially lowering it. Sodium concentration only becomes meaningfully low if the blood itself is diluted with excess free water — this is what “true hypotonic hyponatremia” means. Serum osmolality tells you whether the blood is actually diluted.")
                col_txt, col_img = st.columns([1, 1])
                with col_txt:
                    st.write("This is where we are in the algorithm provided in lecture. Determining serum osmolality is the first step in determining the etiology of the hyponatremia.")
                with col_img:
                    st.image(DESKTOP_PATH + "step1hyponatremia.PNG")
                
                if "Serum Osm" not in st.session_state.visible_labs:
                    st.session_state.visible_labs.append("Serum Osm")
                st.session_state.answered = True
            else:
                st.error("Incorrect. Remember, the evaluation must begin by confirming if the blood itself is actually diluted.")

    # STEP 2: Interpretation of Osmolality (SPOILER REVEALED HERE)
    elif st.session_state.step == 2:
        show_case()
        st.subheader("How do you interpret the serum osmolality?")
        ans = st.radio("", ["Low (Hypotonic)", "Normal (Isotonic)", "High (Hypertonic)"], key="s2")
        if st.button("Submit"):
            if "Low" in ans:
                explanations = {
                    "case1": "Correct! To determine whether this is “true” hyponatremia, we first look at the serum osmolality. Her serum osm of 258 mOsm/kg is significantly below 275, which means the blood is diluted — it contains more water relative to solute. This confirms hypotonic hyponatremia. This is a crucial step because sodium can appear artificially low in conditions like hyperglycemia or high triglycerides, but those conditions do not lower serum osm. By seeing a low serum osmolality, we know that the sodium value reflects a real physiologic problem — the patient has an excess of free water in relation to sodium.",
                    "case2": "Correct! His serum osmolality is 265 mOsm/kg, which is clearly below 275, confirming that this is true hypotonic hyponatremia. The sodium concentration is low because the plasma is diluted with excess free water. This tells us that the sodium value reflects a genuine physiologic problem, not an artifact or a shift caused by glucose, lipids, or proteins. Recognizing this is essential because heart failure does not cause pseudohyponatremia — it causes real dilution from water retention. This also lets you know that water-handling hormones (ADH and RAAS) will be behaving in predictable patterns based on perfusion status.",
                    "case3": "Correct! With a serum osmolality of 255, this patient clearly has true hypotonic hyponatremia.",
                    "case4": "Correct! His serum osmolality is 260, which confirms true dilutional hyponatremia. This means his blood is overwhelmed with water relative to solute."
                }
                st.success(explanations[st.session_state.case_choice])
                st.session_state.answered = True
            else: 
                st.error("Incorrect. Look at the patient's Serum Osm lab value. Is it below, within, or above 275-295?")

    # STEP 3: Next Lab (Urine Osm)
    elif st.session_state.step == 3:
        show_case()
        st.subheader("What is the NEXT step in finding the diagnosis?")
        ans = st.radio("", ["Check urine sodium", "Assess volume status", "Check urine osmolality"], key="s3")
        if st.button("Submit"):
            if ans == "Check urine osmolality":
                st.success("Correct! Urine osmolality shows whether ADH is turned on and how strongly. It helps us determine if ADH is appropriately suppressed or inappropriately active by looking at how concentrated the urine is.")
                
                col_txt, col_img = st.columns([1, 1])
                with col_txt:
                    st.write("This is where we are in the algorithm provided in lecture. Determining urine osmolality is the next step in determining the etiology of the hyponatremia.")
                with col_img:
                    st.image(DESKTOP_PATH + "step2hyponatremia.PNG")

                if "Urine Osm" not in st.session_state.visible_labs:
                    st.session_state.visible_labs.append("Urine Osm")
                st.session_state.answered = True
            else:
                st.error("Incorrect. Before checking volume or salt handling, we need to know if the brain is signalng the kidneys to hold water.")

    # STEP 4: ADH Status interpretation
    elif st.session_state.step == 4:
        show_case()
        st.subheader("Is ADH turned on or off?")
        options = ["ADH OFF (Dilute Urine)", "ADH ON (Concentrated Urine)"]
        ans = st.radio("", options, key="s4")
        correct = "ADH OFF" if st.session_state.case_choice == "case4" else "ADH ON"
        if st.button("Submit"):
            if correct in ans:
                explanations = {
                    "case1": "Correct! Her urine osm is 520, which is very high, meaning her urine is extremely concentrated. The only physiologic way the kidney can produce concentrated urine is when ADH is activated. ADH acts on the collecting ducts to reabsorb water back into the bloodstream, which is exactly what the body wants when blood volume is low.",
                    "case2": "Correct! His urine osmolality is 470, which is very high, meaning ADH is actively concentrating his urine. ADH only turns on when the body feels it must preserve water — usually due to high serum osmolality or low perfusion. In CHF, although the total body water is high, the effective arterial blood volume is low because the heart cannot pump blood forward properly. This low perfusion activates baroreceptors in the carotid sinus and kidney, which stimulate ADH release. ADH activation in CHF is therefore “appropriate” from the body’s perspective, even though it worsens hyponatremia. The kidneys are simply responding to signals of low circulation, not the actual fluid overload.",
                    "case3": "Correct! His urine osm is 410, which is elevated, indicating that ADH is ON. This should raise some confusion as the kidneys are holding onto water even though neither serum osmolality nor perfusion status would justify it. This leads to concentrated urine despite a diluted bloodstream.",
                    "case4": "Correct! ADH is OFF. His urine osm is 55, which is extremely dilute. The body is appropriately trying to get rid of excess water by suppressing ADH and allowing the kidneys to dump as much free water as possible. This is the key insight: the problem is not hormone activation — the problem is that his water intake far exceeds the kidney’s ability to excrete it, especially given his extremely low solute intake. This explains why ADH off does not correct the hyponatremia. Since you have reached this point, you can stop here as the reasoning of the hyponatremia must be ADH independent."
                }
                st.success(explanations[st.session_state.case_choice])
                st.session_state.answered = True
            else: 
                st.error("Incorrect. Check the Urine Osm value. Is it low (<100) or high (>285)?")

    # STEP 5: Next Step (Volume Status)
    elif st.session_state.step == 5:
        show_case()
        st.subheader("What is the NEXT step in diagnosis?")
        ans = st.radio("", ["Restrict Fluids", "Determine clinical volume status", "Check TSH"], key="s5")
        if st.button("Submit"):
            if "volume status" in ans:
                st.success("Correct! Once true hyponatremia is confirmed and ADH is found to be ON, the next critical step is evaluating volume status. This drives the response of the ADH and RAAS systems.")
                
                if st.session_state.case_choice in ["case1", "case2", "case3"]:
                    col_txt, col_img = st.columns([1, 1])
                    with col_txt:
                        st.write("This is where we are in the algorithm provided in lecture. Determining volume status is the next step in determining the etiology of the hyponatremia. Because we have high urine osmolality we do this. If the urine osmolality was low, we would not do this.")
                    with col_img:
                        st.image(DESKTOP_PATH + "step4hyponatremia.PNG")

                st.session_state.answered = True
            else: 
                st.error("Incorrect. We must determine if the patient is hypovolemic, euvolemic, or hypervolemic.")

    # STEP 6: Determine Volume Status Interpretation
    elif st.session_state.step == 6:
        show_case()
        st.subheader("What is the volume status?")
        vols = {"case1": "Hypovolemic", "case2": "Hypervolemic", "case3": "Euvolemic"}
        ans = st.radio("", ["Hypovolemic", "Euvolemic", "Hypervolemic"], key="s6")
        if st.button("Submit"):
            if ans == vols[st.session_state.case_choice]:
                explanations = {
                    "case1": "Correct! Her vital signs and physical exam show classic markers of hypovolemia. A blood pressure of 92/58 and a pulse of 120 strongly suggest that her body is struggling to maintain adequate blood flow — these are compensatory signs of low circulating volume. Dry mucous membranes, reduced urine output, and dark urine all reinforce that she is losing fluid faster than she is replacing it, mostly from vomiting and inadequate intake. Her BUN/Cr ratio is elevated, which indicates the kidneys are not being perfused well — this is another sign of volume depletion. Putting these together, we can confidently say she is truly hypovolemic. In hypovolemia, the body cares more about maintaining perfusion than correcting sodium levels. Even though her sodium is already low, her brain senses that circulation is threatened and prioritizes keeping water inside the body to support blood pressure. So ADH activation here is not only present — it is completely appropriate given her physiologic state.",
                    "case2": "This patient is clearly hypervolemic. He has JVD, peripheral edema, crackles, and rapid weight gain — all of which indicate excess total body sodium and water. However, the key concept is that although total fluid is high, his effective arterial blood volume (EABV) is low. Because blood isn’t being pumped forward efficiently, the kidneys believe the body is dehydrated, despite the obvious fluid overload. CHF is the perfect example of why volume status assessment must differentiate between total volume and perfusion.",
                    "case3": "This patient is clinically euvolemic. His vitals are normal, his mucous membranes are neither dry nor swollen, and he has no edema, crackles, or JVD elevations."
                }
                st.success(explanations[st.session_state.case_choice])
                st.session_state.answered = True
            else: 
                st.error("Incorrect. Re-read the physical exam findings carefully.")

    # STEP 7: RAAS Logic
    elif st.session_state.step == 7:
        show_case()
        st.subheader("How do we determine if RAAS is ON or OFF?")
        ans = st.radio("", ["Check TSH levels", "Check urine sodium levels", "Order a renal ultrasound", "Check urine osmolality"], key="s7")
        if st.button("Submit"):
            if "urine sodium" in ans:
                st.success("Correct! Urine sodium tells you whether the kidney is trying to hold onto sodium or is comfortable letting sodium go. This is the best marker of RAAS activity.")
                if "Urine Na" not in st.session_state.visible_labs:
                    st.session_state.visible_labs.append("Urine Na")
                if st.session_state.case_choice == "case1" and "BUN/Cr" not in st.session_state.visible_labs:
                    st.session_state.visible_labs.append("BUN/Cr")
                st.session_state.answered = True
            else: 
                st.error("Incorrect. We need to check if the kidneys are saving or losing sodium.")

    # STEP 8: Interpret RAAS (Urine Na)
    elif st.session_state.step == 8:
        show_case()
        st.subheader("Is RAAS activated?")
        raas_ans = "RAAS ON" if st.session_state.case_choice != "case3" else "RAAS OFF"
        ans = st.radio("", ["RAAS ON", "RAAS OFF"], key="s8")
        if st.button("Submit"):
            if ans == raas_ans:
                explanations = {
                    "case1": "Correct! Her urine sodium is 7 mEq/L, which is extremely low (<20 mEq/L). This tells us the kidney is actively conserving sodium. The only way this happens is if the RAAS system is turned on, specifically aldosterone, which instructs the kidneys to reabsorb sodium in exchange for potassium. This makes perfect physiologic sense: her kidneys sense low perfusion (because she is hypovolemic from vomiting), so they turn on renin → angiotensin → aldosterone. Aldosterone’s job is to rescue circulating volume by pulling sodium (and therefore water) back into the bloodstream. Low urine sodium is the hallmark sign that RAAS is activated. This is the body’s survival mechanism to fight volume loss.",
                    "case2": "Correct! His urine sodium is 9 mEq/L, which is extremely low (<20 mEq/L). This tells us the kidneys are aggressively conserving sodium — a direct indication that RAAS is activated. Aldosterone increases sodium reabsorption to salvage perfusion. In CHF, the kidney’s baroreceptors sense poor blood flow and assume the body is hypovolemic, which activates renin → angiotensin → aldosterone. This leads to sodium retention and further water retention, worsening his fluid overload. Low urine sodium in CHF is therefore the body’s attempt to correct what it misinterprets as low blood volume. This is quintessential RAAS-driven sodium conservation.",
                    "case3": "Correct! No — RAAS is not activated in this scenario. His urine sodium is 38, which is higher than 20 and indicates that the kidney is not trying to conserve sodium. This makes sense because his volume status is normal — his kidneys do not sense any threat to perfusion."
                }
                st.success(explanations[st.session_state.case_choice])
                st.session_state.answered = True
            else: 
                st.error("Incorrect. Look at the Urine Sodium lab value.")

    # FINAL STEP: Diagnosis
    elif st.session_state.step == 9:
        show_case()
        st.subheader("What is the most likely diagnosis?")
        options = ["Hypovolemic Hyponatremia", "SIADH", "Hypervolemic hyponatremia (CHF)", "Psychogenic polydipsia"]
        diag_map = {"case1": options[0], "case2": options[2], "case3": options[1], "case4": options[3]}
        
        ans = st.radio("", options, key="dx")
        if st.button("Submit Diagnosis"):
            if ans == diag_map[st.session_state.case_choice]:
                st.balloons()
                # Your specific document summaries for the final result
                final_explanations = {
                    "case1": "Correct! Putting all the reasoning together, this is hypovolemic hyponatremia caused by vomiting and inadequate intake. Her low serum osmolality shows true hyponatremia, her exam and labs reveal significant volume depletion, ADH is appropriately turned on to preserve water, and RAAS is activated to retain sodium. This hormonal pattern — ADH ON + RAAS ON + low urine sodium + high urine osm — is the classic pattern for hypovolemic hyponatremia. Her body is essentially fighting to survive dehydration, even though doing so worsens her sodium level.",
                    "case2": "Correct! This is classic hypervolemic hyponatremia secondary to congestive heart failure. The patient has fluid overload, low serum osmolality, high urine osmolality (ADH ON), and low urine sodium (RAAS ON). This combination — ADH ON + RAAS ON + volume overload + low EABV — is the hallmark of CHF-related hyponatremia. Even though the body is fluid-overloaded, its hormonal responses behave as though dehydration were occurring, leading to a dangerous cycle of water retention and worsening hyponatremia.",
                    "case3": "Correct! This is SIADH, most likely from small cell lung cancer. The hallmark combination is: normal exam, low serum osm, high urine osm, high urine sodium, ADH ON despite normal perfusion, and RAAS OFF.  This inappropriate activation stems from ectopic ADH secretion by small cell lung cancer. In this disease process, ADH secretion becomes autonomous and no longer responds to normal physiologic feedback, causing progressive dilutional hyponatremia. SIADH clue should be LOW serum osmolality with HIGH urine sodium.",
                    "case4": "Correct! This is ADH-independent hyponatremia due to psychogenic polydipsia and low solute intake. ADH is appropriately suppressed, RAAS is off, and the kidneys are trying to eliminate water — but cannot because solute intake is too low to carry water out of the body efficiently."
                }
                st.success(final_explanations[st.session_state.case_choice])
                st.write("here is how we can use the algorithim provided in lecture to find the etiologies of hyponatremia.")
                st.image(DESKTOP_PATH + "step5hyponatremia.PNG")
            else: 
                st.error("Incorrect. Review the path of your reasoning through the algorithm.")
        
        if st.button("Return to Menu"):
            st.session_state.step = 0
            st.session_state.answered = False
            st.rerun()

    # NAVIGATION LOGIC
    if st.session_state.answered and st.session_state.step < 9:
        if st.button("Next Step ➡️"):
            if st.session_state.case_choice == "case4" and st.session_state.step == 4:
                st.session_state.step = 9
            else:
                st.session_state.step += 1
            st.session_state.answered = False

            st.rerun()
