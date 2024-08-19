from datetime import datetime, timedelta

import altair as alt
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
from streamlit_extras.colored_header import colored_header


def convert_target_to_dataframe(targets):
    """
    targets is like this:
    [
      {
        "lipid": {
          "amines": "A1",
          "isocyanide": "B4",
          "lipid_carboxylic_acid": "D19",
          "lipid_aldehyde": "C15"
        }
      },
      {
        "lipid": {
          "amines": "A1",
          "isocyanide": "B6",
          "lipid_carboxylic_acid": "D15",
          "lipid_aldehyde": "C9"
        }
      },
    ]
    """
    lipid_data = [data.get("lipid", {}) for data in targets]
    df = pd.DataFrame(lipid_data)
    return df


# Main function for the Streamlit app
def example() -> None:
    st.set_page_config(
        page_title="SDL Dashboard",
        page_icon="🦾",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Display the current date and time
    current_datetime = datetime.now()

    # Use colored_header to display a header with the current system time
    colored_header(
        label="SDL-LNP",
        description=f"The current system time: {current_datetime.strftime('%H:%M:%S')}",
        color_name="green-100",
    )

    # Define steps and descriptions
    steps = {
        "feeders": [
            "≥ 6 300 ul racks in feeder_0",
            "≥ 10 20 ul racks in feeder_1",
            "≥ 4 DeepWells in feeder_2",
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
        "shaker": ["Ensure latch is open"],
        "camera": ["Check the camera"],
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
            job["job_id"]: list(job.get("experiment_input_dict", {}).keys())
            for job in data
        }
    else:
        st.error(
            f"Failed to fetch job data from the API. Status code: {response.status_code}"
        )

    selected_job_id = st.selectbox("Select a Job ID", job_ids, index=None)

    if selected_job_id:
        # get the refillment data from the proposal
        usage_and_refills_data_list = data[job_ids.index(selected_job_id)].get(
            "usage_and_refills", {}
        )
        refill_list = [item.get("refill") for item in usage_and_refills_data_list]
        merged_refill = {}
        for refill in refill_list:
            for key, value in refill.items():
                if key in merged_refill:
                    merged_refill[key] += value
                else:
                    merged_refill[key] = value

        # Initialize checkbox states
        checkbox_states = {step: [False] * len(tasks) for step, tasks in steps.items()}

        # Show the experiment_data for the selected job_id
        st.subheader("Job experiments")
        job_data = data[job_ids.index(selected_job_id)]
        for exp_id, exp_data in job_data.get("experiment_input_dict", {}).items():
            st.write(f"Experiment ID: {exp_id}")
            # st.json(exp_data)
            df = convert_target_to_dataframe(exp_data.get("targets", []))
            st.dataframe(df, use_container_width=True)

        # Display the refillment data as checkbox in the table
        st.subheader("Refillment Data")
        st.write(
            "Refillment Data from the proposal, check the box to confirm the refillment"
        )

        # cols: well name (key), volume (value), checked (new, bool)
        well_name, volume, checked = [], [], []
        for key, value in merged_refill.items():
            well_name.append(key)
            volume.append(value)
            checked.append(False)
        refill_df = pd.DataFrame(
            {"Well Name": well_name, "Volume": volume, "Confirm": checked}
        )
        edited_df = st.data_editor(
            refill_df,
            column_config={
                "Confirm": st.column_config.CheckboxColumn(
                    "Check",
                    help="Confirm the refillment",
                    default=False,
                )
            },
            disabled=["widgets"],
            hide_index=True,
        )

        # Display checkboxes and update states
        for step, tasks in steps.items():
            st.header(step.capitalize())
            for i, task in enumerate(tasks):
                checkbox_states[step][i] = st.checkbox(task, key=f"{step}_{i}")

        # have a button to check all
        st.subheader("Check All")
        if st.button("Check All"):
            for step, tasks in steps.items():
                for i, task in enumerate(tasks):
                    checkbox_states[step][i] = True
            for i in range(len(refill_df)):
                edited_df.loc[i, "Confirm"] = True

        # Check if all steps are completed and refillments are confirmed

        all_steps_completed = all(all(state) for state in checkbox_states.values())

        all_refill_confirmed = edited_df["Confirm"].all()

        if all_steps_completed and all_refill_confirmed:
            # Display activation buttons only if all checkboxes are checked and all refillments are confirmed (if any)
            st.header("Actions")

            post_base_url = f"{base_url}/start"
            get_details_url = f"{base_url}/experiment_details"
            pause_experiment_url = f"{base_url}/pause_experiment"
            resume_experiment_url = f"{base_url}/resume_experiment"
            stop_all_experiments_url = f"{base_url}/stop_all"

            # Step 2: Select Experiment ID based on the selected Job ID
            experiment_ids = experiment_data.get(selected_job_id, [])
            selected_experiment_id = st.selectbox(
                "Select an Experiment ID", experiment_ids
            )

            # Optional: Include functionality to start a job
            if st.button("Start Job"):
                if selected_job_id:
                    post_url = f"{post_base_url}/{selected_job_id}"
                    post_response = requests.post(post_url)
                    if post_response.status_code == 200:
                        st.success(
                            f"Job {selected_job_id} has been started successfully!"
                        )
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
                        st.subheader(
                            f"Details for Experiment ID: {selected_experiment_id}"
                        )
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
                        pause_experiment_url,
                        json={"experiment_id": selected_experiment_id},
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


if __name__ == "__main__":
    example()
