import streamlit as st
import requests
# Main function for the Streamlit app
# Set the layout to wide
st.set_page_config(layout="wide")
st. title ("SDL Checklist")

# 定义步骤和描述
steps = {
    "feeders": [
        "≥ 12 300 ul racks in feeder_0",
        "≥ 10 20 ul racks in feeder_1",
        "≥ 2 DW and ≥ 2 covered DW in feeder_2",
        "≥ 4 reading plates in feeder_3"
    ],
    "stock_solution": [
        "empty the stock solution deep well",
        "resealing the mat",
        "put it in the opentron 0 pos 0"
    ],
    "reagent_deep_well": [
        "empty the reagent deep well",
        "refill MC3, one glow, mRNA aqua master mix, ethanol master mix",
        "resealing the mat",
        "put it in the opentron 1 pos 6"
    ],
    "incubator": ["put four new plates of cells in incubator"],
    "bin": ["Empty the bin"]
}

# 初始化checkbox状态
checkbox_states = {step: [False] * len(tasks) for step, tasks in steps.items()}

# 显示checkbox并更新状态
for step, tasks in steps.items():
    st.header(step.capitalize())
    for i, task in enumerate(tasks):
        checkbox_states[step][i] = st.checkbox(task, key=f"{step}_{i}")

# 检查是否所有步骤都已完成
all_steps_completed = all(all(state) for state in checkbox_states.values())

# 显示激活按钮
if all_steps_completed:
    if st.button("Send API to System and Resume the experiment"):
        # 发送API请求
        response = requests.post("https://example.com/api/activate")
        
        if response.status_code == 200:
            st.success("API请求成功发送并恢复实验!")
        else:
            st.error("API请求失败，请重试。")
else:
    st.warning("请完成所有步骤。")