
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SaaS Tenant Portal",
    page_icon="🏢",
    layout="wide"
)

# Demo data lives in this app session only.
if "tenants" not in st.session_state:
    st.session_state.tenants = [
        {
            "Customer": "Acme Technologies",
            "Model": "Shared",
            "Plan": "Professional",
            "Status": "Active"
        },
        {
            "Customer": "Northstar Enterprise",
            "Model": "Dedicated",
            "Plan": "Enterprise",
            "Status": "Pending"
        }
    ]

st.title("SaaS Tenant Management Portal")
st.caption("Learning project | Demo data only")

tenants = st.session_state.tenants

# Dashboard metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total tenants", len(tenants))
col2.metric(
    "Active tenants",
    sum(t["Status"] == "Active" for t in tenants)
)
col3.metric(
    "Pending / failed",
    sum(t["Status"] in ["Pending", "Failed"]
        for t in tenants)
)

st.divider()
st.subheader("Provision a new tenant")

with st.form("tenant_form"):
    customer = st.text_input("Customer organization")

    model = st.selectbox(
        "Tenant model",
        ["Shared", "Dedicated"]
    )

    plan = st.selectbox(
        "Subscription plan",
        ["Starter", "Professional", "Enterprise"]
    )

    submitted = st.form_submit_button(
        "Create tenant"
    )

    if submitted:
        if not customer.strip():
            st.error("Enter a customer name.")
        elif any(
            t["Customer"].casefold() == customer.strip().casefold()
            for t in tenants
        ):
            st.error("This customer already exists.")
        else:
            tenants.append({
                "Customer": customer.strip(),
                "Model": model,
                "Plan": plan,
                "Status": "Pending"
            })
            st.success(
                "Tenant record created with Pending status."
            )

st.divider()
st.subheader("Tenant inventory")

if tenants:
    st.dataframe(
        pd.DataFrame(tenants),
        use_container_width=True,
        hide_index=True
    )

    customer_names = [t["Customer"] for t in tenants]
    selected = st.selectbox(
        "Select a tenant to update",
        customer_names
    )

    action = st.selectbox(
        "Simulate provisioning result",
        ["Active", "Failed"]
    )

    if st.button("Update tenant status"):
        for tenant in tenants:
            if tenant["Customer"] == selected:
                tenant["Status"] = action
                break
        st.rerun()
else:
    st.info("No tenants created yet.")

st.caption(
    "Demo only: provisioning is simulated; "
    "no real cloud resources are created."
)
