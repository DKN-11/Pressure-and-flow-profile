import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

st.title("Radial Flow: Pressure & Velocity vs. Distance (Linear Scale)")

st.markdown("""
This app shows **pressure** and **flow velocity** profiles from the wellbore out into the reservoir,  
using **Darcy’s steady-state radial flow** equation.

✅ Use either **sliders** or **precise keyboard input** to change values.
""")

# Helper function to create dual input (slider + number input)
def dual_input(label, min_val, max_val, slider_val, step, format="%f", key=None):
    col1, col2 = st.columns([2, 1])
    slider_val = col1.slider(label, min_value=min_val, max_value=max_val, value=slider_val, step=step, key=f"{key}_slider")
    num_val = col2.number_input(" ", value=slider_val, step=step, format=format, label_visibility="collapsed", key=f"{key}_number")
    return num_val

#st.sidebar.header("Reservoir & Fluid Properties")
st.header("Reservoir & Fluid Properties")
# Dual Inputs
P_r = dual_input("Reservoir Pressure (psi)", 1000.0, 5000.0, 3000.0, 100.0,key="reservoir pressure")
q = dual_input("Flow Rate (STB/day)", 100.0, 5000.0, 500.0, 50.0,key="flow rate")
mu = dual_input("Viscosity (cp)", 0.1, 10.0, 1.0, 0.1,key="viscosity")
k = dual_input("Permeability (mD)", 1.0, 1000.0, 100.0, 10.0,key="permeability")
h = dual_input("Reservoir Thickness (ft)", 10.0, 200.0, 50.0, 5.0,key="res thickness")
r_w = dual_input("Wellbore Radius (ft)", 0.1, 1.0, 0.25, 0.01,key="rw")
r_e = dual_input("Drainage Radius (ft)", 100.0, 2000.0, 500.0, 50.0,key="re")

# Distance array (LINEAR)
r = np.linspace(r_w, r_e, 300)

# Pressure and velocity
pressure = P_r - (q * mu) / (2 * np.pi * k * h) * np.log(r_e / r)
velocity = q / (2 * np.pi * r * h)

# Plotting
fig, axs = plt.subplots(2, 1, figsize=(8, 10))
plt.subplots_adjust(hspace=0.4)

axs[0].plot(r, pressure, color='blue')
axs[0].set_title("Pressure Profile")
axs[0].set_xlabel("Distance from Wellbore (ft)")
axs[0].set_ylabel("Pressure (psi)")
axs[0].grid(True)

axs[1].plot(r, velocity, color='green')
axs[1].set_title("Flow Velocity Profile")
axs[1].set_xlabel("Distance from Wellbore (ft)")
axs[1].set_ylabel("Velocity (ft³/day/ft²)")
axs[1].grid(True)

st.pyplot(fig)

# Summary values
st.subheader("Output Summary")
st.markdown(f"""
- **Pressure at wellbore ({r_w} ft)**: {pressure[0]:.2f} psi  
- **Pressure at outer radius ({r_e} ft)**: {pressure[-1]:.2f} psi  
- **Velocity at wellbore ({r_w} ft)**: {velocity[0]:.2f} ft³/day/ft²  
- **Velocity at outer radius ({r_e} ft)**: {velocity[-1]:.2f} ft³/day/ft²
""")
