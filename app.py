import streamlit as st

# ตั้งค่าหน้าจอให้เหมือนแอปมือถือ
st.set_page_config(page_title="NeoDose Emergency 2026", layout="centered")

st.title("🚨 NeoDose Emergency")
st.subheader("โปรแกรมคำนวณยาช่วยชีวิตทารก (NeoFax 2026)")

# 1. ส่วนรับข้อมูลคนไข้
with st.container():
    st.write("---")
    weight = st.number_input("น้ำหนักตัวทารก (kg)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    st.write(f"**คำนวณสำหรับน้ำหนัก:** {weight} kg")
    st.write("---")

# 2. ฐานข้อมูลยาช่วยชีวิต (Logic จาก NeoFax 2026)
drugs = {
    "Epinephrine (1:10,000)": {
        "dose_range": "0.01 - 0.03 mg/kg",
        "calc": lambda w: (w * 0.01, w * 0.03),
        "conc": "0.1 mg/mL",
        "vol_calc": lambda w: (w * 0.1, w * 0.3), # ml
        "note": "ให้ทาง IV/IO. สามารถให้ซ้ำได้ทุก 3-5 นาที"
    },
    "Adenosine": {
        "dose_range": "0.1 mg/kg",
        "calc": lambda w: (w * 0.1, w * 0.1),
        "conc": "3 mg/mL",
        "vol_calc": lambda w: (w * 0.1 / 3, w * 0.1 / 3),
        "note": "Rapid IV push (1-2 sec) ตามด้วย Saline flush ทันที"
    },
    "Sodium Bicarbonate (4.2%)": {
        "dose_range": "1 - 2 mEq/kg",
        "calc": lambda w: (w * 1, w * 2),
        "conc": "0.5 mEq/mL",
        "vol_calc": lambda w: (w * 2, w * 4),
        "note": "ฉีดช้าๆ อย่างน้อย 2 นาที. ห้ามผสมกับ Calcium"
    },
    "Naloxone": {
        "dose_range": "0.1 mg/kg",
        "calc": lambda w: (w * 0.1, w * 0.1),
        "conc": "0.4 mg/mL",
        "vol_calc": lambda w: (w * 0.25, w * 0.25),
        "note": "ให้ทาง IV, IM, หรือ ET"
    }
}

# 3. ส่วนแสดงผล
selected_drug = st.selectbox("เลือกยาที่ต้องการ:", list(drugs.keys()))

if selected_drug:
    data = drugs[selected_drug]
    low_mg, high_mg = data["calc"](weight)
    low_ml, high_ml = data["vol_calc"](weight)
    
    st.info(f"**Indication:** {selected_drug}")
    
    # แสดงผลขนาดใหญ่เพื่อความชัดเจน
    col1, col2 = st.columns(2)
    with col1:
        st.metric("ขนาดยา (mg)", f"{low_mg:.3f} mg")
    with col2:
        st.error(f"ดูดยามา (mL): {low_ml:.2f} mL")
    
    if low_mg != high_mg:
        st.write(f"ช่วงขนาดยา: {low_mg:.3f} - {high_mg:.3f} mg ({low_ml:.2f} - {high_ml:.2f} mL)")
    
    st.warning(f"**วิธีใช้:** {data['note']}")
    st.caption(f"ความเข้มข้นมาตรฐาน: {data['conc']}")

st.write("---")
st.caption("⚠️ อ้างอิงข้อมูลจาก NeoFax 2026 | ใช้เพื่อประกอบการตัดสินใจของแพทย์เท่านั้น")
