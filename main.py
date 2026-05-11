import streamlit as st
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Premium RSS Assistant", page_icon="🌿", layout="centered")

# 2. Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 25px; height: 3.5em; 
        background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%); 
        color: white; font-weight: bold; border: none;
    }
    .report-card { 
        background-color: white; padding: 15px; border-radius: 12px; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 10px; 
        border-left: 6px solid #e53935; 
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #2e7d32;'>🌿 RSS Premium Check</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>เครื่องมือวิเคราะห์และเปรียบเทียบเกรดยางพรีเมียม (Prototype)</p>", unsafe_allow_html=True)

# 3. Input Section
st.markdown("### 📝 ระบุผลการทดสอบ")
col1, col2 = st.columns(2)
with col1:
    dirt_val = st.number_input("Dirt (%)", min_value=0.0, step=0.001, format="%.2f")
    ash_val = st.number_input("Ash (%)", min_value=0.0, step=0.01, format="%.2f")
    vm_val = st.number_input("VM ความชื้น (%)", min_value=0.0, step=0.1, format="%.2f")
    n_val = st.number_input("Nitrogen (%)", min_value=0.0, step=0.01, format="%.2f")
    
with col2:
    po_val = st.number_input("Po Index", min_value=0.0, step=0.1, format="%.1f")
    pri_val = st.number_input("PRI Index", min_value=0.0, step=0.1, format="%.1f")
    mv_val = st.number_input("Mooney (MV)", min_value=0.0, step=0.1, format="%.1f")

# 4. วิเคราะห์ผล
if st.button("🚀 ตรวจสอบและแสดงกราฟเปรียบเทียบ"):
    st.divider()
    
    # ข้อมูลสำหรับกราฟ
    labels = ['Nitrogen', 'Ash', 'Dirt', 'VM']
    user_values = [n_val, ash_val, dirt_val, vm_val]
    standards = [0.40, 0.30, 0.02, 0.50] 
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='ผลทดสอบของคุณ', x=labels, y=user_values, marker_color='#81c784'))
    fig.add_trace(go.Scatter(name='เกณฑ์พรีเมียม (ห้ามเกิน)', x=labels, y=standards, mode='lines+markers', line=dict(color='red', width=3, dash='dash')))
    
    # ตรงนี้แหละครับที่แก้ไข!
    fig.update_layout(title='เปรียบเทียบผลทดสอบกับเกณฑ์มาตรฐานเกรดพรีเมียม', barmode='group', height=350)
    st.plotly_chart(fig, use_container_width=True)

    # ตรวจสอบเงื่อนไข
    fails = []
    if n_val > 0.40: fails.append(("Nitrogen", n_val, 0.40, "ล้างน้ำเซรุ่มไม่สะอาด / ใส่กรดมากเกินไป"))
    if ash_val > 0.30: fails.append(("Ash", ash_val, 0.30, "มีฝุ่น/ทรายปนเปื้อน หรือน้ำที่ใช้ล้างไม่สะอาด"))
    if dirt_val > 0.02: fails.append(("Dirt", dirt_val, 0.02, "การกรองน้ำยางสดไม่ละเอียดพอ"))
    if vm_val > 0.50: fails.append(("VM", vm_val, 0.50, "ยางยังแห้งไม่สนิท ควรเพิ่มเวลารมควัน"))
    if pri_val < 80.0 and pri_val > 0: fails.append(("PRI", pri_val, 80.0, "ยางเสื่อมสภาพจากความร้อนสูงเกินไป"))

    if not fails and n_val > 0:
        st.success("### ✅ ยางของคุณอยู่ในเกณฑ์ PREMIUM RSS")
        st.balloons()
    elif n_val > 0:
        st.error("### ⚠️ ผลการวิเคราะห์: ไม่ผ่านเกณฑ์พรีเมียม")
        for name, val, limit, advice in fails:
            st.markdown(f"""<div class="report-card"><b>{name}</b>: ปัจจุบัน {val} (เกณฑ์ต้อง ≤ {limit})<br><small>💡 วิธีแก้: {advice}</small></div>""", unsafe_allow_html=True)
    else:
        st.info("กรุณากรอกข้อมูลเพื่อเริ่มการวิเคราะห์")