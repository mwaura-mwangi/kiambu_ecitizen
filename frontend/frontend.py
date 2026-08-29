import streamlit as st
import requests
import random

API = "http://backend:8001"
st.set_page_config(page_title="Kiambu eCitizen")
st.title("Kiambu eCitizen")

if st.button("Home/New Payment"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

name = st.text_input("Name")
id_no = st.text_input("ID Number")
phone = st.text_input("Phone", placeholder="07xxxxxxxx")

try:
    services = requests.get(f"{API}/services").json()
except:
    st.error("Backend not running on :8001 - run `uvicorn main:app --reload --port 8001`")
    st.stop()

service_names = {f"{s['name']} - Ksh {s['amount']}": s for s in services}
choice = st.selectbox("What are you paying for?", list(service_names.keys()))
selected = service_names[choice]

st.divider()
st.subheader(f"Pay {selected['name']}")
st.metric("Amount to Pay", f"Ksh {selected['amount']}")
# FIX for None display
if selected.get('description'):
    st.caption(selected['description'])

if st.button("Pay via MPESA", type="primary", use_container_width=True):
    if not name or not id_no or not phone:
        st.error("Fill Name, ID and Phone first")
        st.stop()

    phone_254 = "254" + phone.strip()[1:] if phone.startswith("0") else phone.strip()

    with st.spinner("Processing..."):
        u_res = requests.post(f"{API}/users", json={"id_number": id_no, "name": name, "phone": phone_254})
        u = u_res.json()

        a = requests.post(f"{API}/applications",
            json={"user_id": u["id"], "service_id": selected["id"], "amount_billed": selected['amount']}
        ).json()

        stk_resp = requests.post(f"{API}/payments/stk",
            json={"phone": phone_254, "amount": selected['amount']}
        ).json()

        # Optional: auto mark as paid for demo
        requests.post(f"{API}/payments", json={
            "application_id": a['id'],
            "mpesa_code": f"MOCK{random.randint(100000,999999)}",
            "amount": selected['amount']
        })

    st.success(f"Application #{a['id']} created for {selected['name']}")
    st.info(f"Prompt sent to {phone_254} for Ksh {selected['amount']}. Check your phone.")
