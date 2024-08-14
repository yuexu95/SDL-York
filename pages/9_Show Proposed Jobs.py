import streamlit as st
import requests

st.title("SDL Checklist")

# Define steps and descriptions
steps = {
    "feeders": [
        "≥ 12 300 ul racks in feeder_0",
        "≥ 10 20 ul racks in feeder_1",
        "≥ 2 DW and ≥ 2 covered DW in feeder_2",
        "≥ 4 reading plates in feeder_3",
    ],
    "stock_solution": [
        "empty the stock solution deep well",
        "resealing the mat",
        "put it in the opentron 0 pos 0",
    ],
    "reagent_deep_well": [
        "empty the reagent deep well",
        "refill MC3, one glow, mRNA aqua master mix, ethanol master mix",
        "resealing the mat",
        "put it in the opentron 1 pos 6",
    ],
    "incubator": ["put four new plates of cells in incubator"],
    "bin": ["Empty the bin"],
}

# Step 1: Select Job ID
base_url = "http://192.168.1.11:12001"
get_api_url = f"{base_url}/proposed_jobs"
response = requests.get(get_api_url)
job_ids = []
experiment_data = {}

if response.status_code == 200:
    data = response.json()
    job_ids = [job["job_id"] for job in data]
    experiment_data = {
        job["job_id"]: list(job.get("experiment_input_dict", {}).keys()) for job in data
    }
else:
    st.error(
        f"Failed to fetch job data from the API. Status code: {response.status_code}"
    )

selected_job_id = st.selectbox("Select a Job ID", job_ids)

if selected_job_id:
    # Initialize checkbox states
    checkbox_states = {step: [False] * len(tasks) for step, tasks in steps.items()}

    # Display checkboxes and update states
    for step, tasks in steps.items():
        st.header(step.capitalize())
        for i, task in enumerate(tasks):
            checkbox_states[step][i] = st.checkbox(task, key=f"{step}_{i}")

    # Check if all steps are completed
    all_steps_completed = all(all(state) for state in checkbox_states.values())

    if all_steps_completed:
        # Display activation buttons only if all checkboxes are checked
        st.header("Actions")

        post_base_url = f"{base_url}/start"
        get_details_url = f"{base_url}/experiment_details"
        pause_experiment_url = f"{base_url}/pause_experiment"
        resume_experiment_url = f"{base_url}/resume_experiment"
        stop_all_experiments_url = f"{base_url}/stop_all"

        # Step 2: Select Experiment ID based on the selected Job ID
        experiment_ids = experiment_data.get(selected_job_id, [])
        selected_experiment_id = st.selectbox("Select an Experiment ID", experiment_ids)

        # Optional: Include functionality to start a job
        if st.button("Start Job"):
            if selected_job_id:
                post_url = f"{post_base_url}/{selected_job_id}"
                post_response = requests.post(post_url)
                if post_response.status_code == 200:
                    st.success(f"Job {selected_job_id} has been started successfully!")
                else:
                    st.error(
                        f"Failed to start the job. Status code: {post_response.status_code}"
                    )

        # GET request: Fetch experiment details
        if st.button("Get Experiment Details"):
            if selected_experiment_id:
                get_response = requests.get(
                    f"{get_details_url}/{selected_experiment_id}"
                )
                if get_response.status_code == 200:
                    st.subheader(f"Details for Experiment ID: {selected_experiment_id}")
                    st.json(get_response.json())
                else:
                    st.error(
                        f"Failed to get experiment details. Status code: {get_response.status_code}"
                    )
            else:
                st.error("Please select a valid Experiment ID.")

        # POST request: Pause experiment
        if st.button("Pause Experiment"):
            if selected_experiment_id:
                pause_response = requests.post(
                    pause_experiment_url, json={"experiment_id": selected_experiment_id}
                )
                if pause_response.status_code == 200:
                    st.success(
                        f"Experiment {selected_experiment_id} has been paused successfully!"
                    )
                else:
                    st.error(
                        f"Failed to pause the experiment. Status code: {pause_response.status_code}"
                    )
            else:
                st.error("Please select a valid Experiment ID.")

        # POST request: Resume experiment
        if st.button("Resume Experiment"):
            if selected_experiment_id:
                resume_response = requests.post(
                    resume_experiment_url,
                    json={"experiment_id": selected_experiment_id},
                )
                if resume_response.status_code == 200:
                    st.success(
                        f"Experiment {selected_experiment_id} has been resumed successfully!"
                    )
                else:
                    st.error(
                        f"Failed to resume the experiment. Status code: {resume_response.status_code}"
                    )
            else:
                st.error("Please select a valid Experiment ID.")

        # GET request: Stop All Experiments
        if st.button("Stop All Experiments"):
            stop_all_response = requests.get(stop_all_experiments_url)
            if stop_all_response.status_code == 200:
                st.success("All experiments have been stopped successfully!")
            else:
                st.error(
                    f"Failed to stop all experiments. Status code: {stop_all_response.status_code}"
                )
