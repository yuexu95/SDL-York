import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("./sdl-lnp-firebase-adminsdk-5tax5-75f56b0882.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

# Set the layout to wide
st.set_page_config(layout="wide")
st. title ("LNP formulation calculator")

def log_to_firebase(data):
    """
    Log the data to Firebase Firestore
    """
    try:
        doc_ref = db.collection("lnp_logs").document()
        doc_ref.set(data)
        st.success("Data logged to Firebase successfully!")
    except Exception as e:
        st.error(f"Failed to log data to Firebase: {e}")


def make_lnp_formulation(rna_scale, rna_stock_concentration, ionizable_lipid_to_rna_ratio, aqueous_to_ethanol_ratio, ionizable_lipid_mw, helper_lipid_mw, cholesterol_mw, pegdmg2000_mw, ionizable_lipid_concentration, helper_lipid_concentration, cholesterol_concentration, pegdmg2000_concentration, ionizable_lipid_ratio, helper_lipid_ratio, cholesterol_ratio, pegdmg2000_ratio):
    """
    Calculates the composition and prepares an LNP formulation.

    Returns:
    A DataFrame containing the calculated values for the LNP composition and preparation.
    """ 
    # Calculate moles of ionizable lipid using the correct formula
    ionizable_lipid_moles = (rna_scale * ionizable_lipid_to_rna_ratio) / ionizable_lipid_mw
    
    # Calculate moles of each lipid based on their molar ratios
    helper_lipid_moles = ionizable_lipid_moles * helper_lipid_ratio / ionizable_lipid_ratio
    cholesterol_moles = ionizable_lipid_moles * cholesterol_ratio / ionizable_lipid_ratio
    pegdmg2000_moles = ionizable_lipid_moles * pegdmg2000_ratio / ionizable_lipid_ratio

    # Calculate mass of each lipid
    ionizable_lipid_mass = ionizable_lipid_moles * ionizable_lipid_mw
    helper_lipid_mass = helper_lipid_moles * helper_lipid_mw
    cholesterol_mass = cholesterol_moles * cholesterol_mw
    pegdmg2000_mass = pegdmg2000_moles * pegdmg2000_mw

    # Calculate final LNP volume
    final_lnp_volume = rna_scale / 0.1
    
    # Calculate ethanol phase volume
    ionizable_lipid_volume = ionizable_lipid_mass / ionizable_lipid_concentration
    helper_lipid_volume = helper_lipid_mass / helper_lipid_concentration
    cholesterol_volume = cholesterol_mass / cholesterol_concentration
    pegdmg2000_volume = pegdmg2000_mass / pegdmg2000_concentration
    ethanol = final_lnp_volume / (aqueous_to_ethanol_ratio + 1) - ionizable_lipid_volume - helper_lipid_volume - cholesterol_volume - pegdmg2000_volume
    ethanol_phase_volume = ionizable_lipid_volume + helper_lipid_volume + cholesterol_volume + pegdmg2000_volume + ethanol

    # Calculate aqueous phase volume
    aqueous_phase_volume = final_lnp_volume * (aqueous_to_ethanol_ratio / (aqueous_to_ethanol_ratio + 1))
    rna_volume = rna_scale / rna_stock_concentration
    citrate_volume = 0.1 * aqueous_phase_volume
    water_volume = aqueous_phase_volume - rna_volume - citrate_volume

    # Create DataFrame for the results
    data = {
        'Component': ['Ionizable Lipid', 'Helper Lipid', 'Cholesterol', 'PEG-DMG2000', 'Ethanol', 'RNA', 'Citrate', 'Water'],
        'Volume (mL)': [ionizable_lipid_volume, helper_lipid_volume, cholesterol_volume, pegdmg2000_volume, ethanol, rna_volume, citrate_volume, water_volume]
    }

    df = pd.DataFrame(data)
    
    volumes = {
        "Ionizable Lipid": ionizable_lipid_volume,
        "helper_lipid_volume": helper_lipid_volume,
        "cholesterol_volume": cholesterol_volume,
        "pegdmg2000_volume": pegdmg2000_volume,
        "ethanol": ethanol,
        "ethanol_phase_volume": ethanol_phase_volume,
        "rna_volume": rna_volume,
        "citrate_volume": citrate_volume,
        "water_volume": water_volume,
        "aqueous_volume": aqueous_phase_volume
    }

    return df, volumes

def prepare_bulk_lnp_volumes(volumes, times):
    """
    Prepares the volumes for any times the LNP with extra.

    Returns:
    A DataFrame containing the bulk volumes.
    """
    bulk_volumes = {
        "Component": ['Ionizable Lipid', "Helper Lipid", "Cholesterol", "PEG-DMG2000", "Ethanol", "RNA", "Citrate", "Water"],
        "Volume (μL)": [
            volumes["Ionizable Lipid"] * times * 1.5,
            volumes["helper_lipid_volume"] * times * 1.5,
            volumes["cholesterol_volume"] * times * 1.5,
            volumes["pegdmg2000_volume"] * times * 1.5,
            volumes["ethanol"] * times * 1.5,
            volumes["rna_volume"] * times * 1.2,
            volumes["citrate_volume"] * times * 1.2,
            volumes["water_volume"] * times * 1.2,
        ]
    } 
    bulk_df = pd.DataFrame(bulk_volumes)
    return bulk_df

def main():

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        rna_scale = st.number_input("RNA Scale (μg)", min_value=0.0, step=1.0, value=3.0)
    with col2:
        rna_stock_concentration = st.number_input("RNA Stock (μg/μL)", min_value=0.0, step=0.1, value=1.0)
    with col3:
        ionizable_lipid_to_rna_ratio = st.number_input("Ionizable Lipid to RNA Ratio", min_value=0.0, max_value=100.0, step=0.1, value=10.0)
    with col4:
        aqueous_to_ethanol_ratio = st.number_input("Aqueous to Ethanol Ratio", min_value=0.0, step=0.1, value=3.0)

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        ionizable_lipid_mw = st.number_input("Ionizable Lipid Molecular Weight (μg/μmol)", min_value=0.0, step=1.0, value=1000.0)
    with col6:
        helper_lipid_mw = st.number_input("Helper Lipid Molecular Weight (μg/μmol)", min_value=0.0, step=1.0, value=744.034)
    with col7:
        cholesterol_mw = st.number_input("Cholesterol Molecular Weight (μg/μmol)", min_value=0.0, step=1.0, value=386.654)
    with col8:
        pegdmg2000_mw = st.number_input("PEG-DMG2000 Molecular Weight (μg/μmol)", min_value=0.0, step=1.0, value=2509.2)

    col9, col10, col11, col12 = st.columns(4)
    with col9:
        ionizable_lipid_concentration = st.number_input("Ionizable Lipid Concentration (μg/μL)", min_value=0.0, step=0.1, value=40.0)
    with col10:
        helper_lipid_concentration = st.number_input("Helper Lipid Concentration (μg/μL)", min_value=0.0, step=0.1, value=10.0)
    with col11:
        cholesterol_concentration = st.number_input("Cholesterol Concentration (μg/μL)", min_value=0.0, step=0.1, value=10.0)
    with col12:
        pegdmg2000_concentration = st.number_input("PEG-DMG2000 Concentration (μg/μL)", min_value=0.0, step=0.1, value=10.0)
    
    col13, col14, col15, col16 = st.columns(4)
    with col13:
        ionizable_lipid_ratio = st.number_input("Ionizable Lipid Molar Ratio", min_value=0.0, step=0.1, value=35.0)
    with col14:
        helper_lipid_ratio = st.number_input("Helper Lipid Molar Ratio", min_value=0.0, step=0.1, value=16.0)
    with col15:
        cholesterol_ratio = st.number_input("Cholesterol Molar Ratio", min_value=0.0, step=0.1, value=46.5)
    with col16:
        pegdmg2000_ratio = st.number_input("PEG-DMG2000 Molar Ratio", min_value=0.0, step=0.1, value=2.5)
    
    col17, col18 = st. columns(2)
    with col17:
        bulk_times = st.number_input("Bulk Preparation Times", min_value=1, step=1, value=1)
    
    if "result_df" not in st.session_state:
        st.session_state.result_df = None
        st.session_state.volumes = None
        st.session_state.checkboxes_col2 = {}
        st.session_state.checkboxes_col4 = {}

    if st.button("Calculate"):
        result_df, volumes = make_lnp_formulation(
            rna_scale, rna_stock_concentration, ionizable_lipid_to_rna_ratio, aqueous_to_ethanol_ratio,
            ionizable_lipid_mw, helper_lipid_mw, cholesterol_mw, pegdmg2000_mw, ionizable_lipid_concentration,
            helper_lipid_concentration, cholesterol_concentration, pegdmg2000_concentration, ionizable_lipid_ratio,
            helper_lipid_ratio, cholesterol_ratio, pegdmg2000_ratio
        )
        st.session_state.result_df = result_df
        st.session_state.volumes = volumes
        
        # Convert DataFrame to list of dictionaries
        result_dict = result_df.to_dict('records')

        # Log data to Firebase
        log_data = {
            "rna_scale": rna_scale,
            "rna_stock_concentration": rna_stock_concentration,
            "ionizable_lipid_to_rna_ratio": ionizable_lipid_to_rna_ratio,
            "aqueous_to_ethanol_ratio": aqueous_to_ethanol_ratio,
            "ionizable_lipid_mw": ionizable_lipid_mw,
            "helper_lipid_mw": helper_lipid_mw,
            "cholesterol_mw": cholesterol_mw,
            "pegdmg2000_mw": pegdmg2000_mw,
            "ionizable_lipid_concentration": ionizable_lipid_concentration,
            "helper_lipid_concentration": helper_lipid_concentration,
            "cholesterol_concentration": cholesterol_concentration,
            "pegdmg2000_concentration": pegdmg2000_concentration,
            "ionizable_lipid_ratio": ionizable_lipid_ratio,
            "helper_lipid_ratio": helper_lipid_ratio,
            "cholesterol_ratio": cholesterol_ratio,
            "pegdmg2000_ratio": pegdmg2000_ratio,
            "result_df": result_dict,
            "volumes": volumes
        }

        log_to_firebase(log_data)
        
        # 初始化复选框状态
        st.session_state.checkboxes_col2 = {index: False for index in result_df.index}
        st.session_state.checkboxes_col4 = {index: False for index in result_df.index}

    if st.session_state.result_df is not None:
        st.header('', divider='rainbow')
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("Single LNP")
            
            st.dataframe(st.session_state.result_df)

        with col2:
            st.markdown("Checklist")
            for index, row in st.session_state.result_df.iterrows():
                st.session_state.checkboxes_col2[index] = st.checkbox(
                    f"{row['Component']}", 
                    value=st.session_state.checkboxes_col2[index],
                    key=f"col2_{index}"
                )               
        with col3:
            st.markdown("EtOH Phasex1.5, Aqueous Phasex1.2")
            
            # 确保 volumes 已初始化
            if st.session_state.volumes is not None:
                bulk_volumes = prepare_bulk_lnp_volumes(st.session_state.volumes, bulk_times)
                st.dataframe(bulk_volumes)

        with col4:
            st.markdown("Checklist")
            for index, row in st.session_state.result_df.iterrows():
                st.session_state.checkboxes_col4[index] = st.checkbox(
                    f"{row['Component']}", 
                    value=st.session_state.checkboxes_col4[index],
                    key=f"col4_{index}"
                )

if __name__ == "__main__":
    main()
