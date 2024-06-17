import streamlit as st
import pandas as pd

def make_lnp_formulation(rna_scale, rna_stock_concentration, ionizable_lipid_to_rna_ratio, aqueous_to_ethanol_ratio, ionizable_lipid_mw, helper_lipid_mw, cholesterol_mw, pegdmg2000_mw, ionizable_lipid_concentration, helper_lipid_concentration, cholesterol_concentration, pegdmg2000_concentration, ionizable_lipid_ratio, helper_lipid_ratio, cholesterol_ratio, pegdmg2000_ratio):
    """
    Calculates the composition and prepares an LNP formulation.

    Returns:
    A DataFrame containing the calculated values for the LNP composition and preparation.
    """
    # Calculate total molar ratio
    total_molar_ratio = ionizable_lipid_ratio + helper_lipid_ratio + cholesterol_ratio + pegdmg2000_ratio
    
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

    # Calculate ethanol phase volume
    ionizable_lipid_volume = ionizable_lipid_mass / ionizable_lipid_concentration
    helper_lipid_volume = helper_lipid_mass / helper_lipid_concentration
    cholesterol_volume = cholesterol_mass / cholesterol_concentration
    pegdmg2000_volume = pegdmg2000_mass / pegdmg2000_concentration
    ethanol_phase_volume = ionizable_lipid_volume + helper_lipid_volume + cholesterol_volume + pegdmg2000_volume

    # Calculate aqueous phase volume
    aqueous_phase_volume = ethanol_phase_volume * aqueous_to_ethanol_ratio
    rna_volume = rna_scale / rna_stock_concentration
    citrate_volume = 0.1 * aqueous_phase_volume
    water_volume = aqueous_phase_volume - rna_volume - citrate_volume

    # Calculate final LNP volume and RNA concentration
    final_lnp_volume = aqueous_phase_volume + ethanol_phase_volume
    final_rna_concentration = rna_scale / final_lnp_volume

    data = {
        "Component": ["Ionizable Lipid", "Helper Lipid", "Cholesterol", "PEG-DMG2000", "Ethanol Phase", "Aqueous Phase", "Citrate", "Water", "Final LNP Volume", "Final RNA Concentration"],
        "Moles": [f"{ionizable_lipid_moles:.2f}", f"{helper_lipid_moles:.2f}", f"{cholesterol_moles:.2f}", f"{pegdmg2000_moles:.2f}", "", "", "", "", "", ""],
        "Mass (μg)": [f"{ionizable_lipid_mass:.2f}", f"{helper_lipid_mass:.2f}", f"{cholesterol_mass:.2f}", f"{pegdmg2000_mass:.2f}", "", "", "", "", "", ""],
        "Volume (μL)": [f"{ionizable_lipid_volume:.2f}", f"{helper_lipid_volume:.2f}", f"{cholesterol_volume:.2f}", f"{pegdmg2000_volume:.2f}", f"{ethanol_phase_volume:.2f}", f"{aqueous_phase_volume:.2f}", f"{citrate_volume:.2f}", f"{water_volume:.2f}", f"{final_lnp_volume:.2f}", ""],
        "Concentration (μg/μL)": ["", "", "", "", "", "", "", "", "", f"{final_rna_concentration:.2f}"]
    }
    volumes = {
        "ionizable_lipid_volume": ionizable_lipid_volume,
        "helper_lipid_volume": helper_lipid_volume,
        "cholesterol_volume": cholesterol_volume,
        "pegdmg2000_volume": pegdmg2000_volume,
        "ethanol_phase_volume": ethanol_phase_volume,
        "rna_volume": rna_volume,
        "citrate_volume": citrate_volume,
        "water_volume": water_volume
    }
    return pd.DataFrame(data), volumes

def prepare_bulk_lnp_volumes(volumes, times):
    """
    Prepares the volumes for any times the LNP with extra.

    Returns:
    A list of dictionaries containing the bulk volumes.
    """
    return [
        {"Component": "Bulk Helper Lipid", "Volume (μL)": volumes["helper_lipid_volume"] * times * 1.5},
        {"Component": "Bulk Cholesterol", "Volume (μL)": volumes["cholesterol_volume"] * times * 1.5},
        {"Component": "Bulk PEG-DMG2000", "Volume (μL)": volumes["pegdmg2000_volume"] * times * 1.5},
        {"Component": "Bulk Ethanol Phase", "Volume (μL)": volumes["ethanol_phase_volume"] * times * 1.5},
        {"Component": "Bulk RNA", "Volume (μL)": volumes["rna_volume"] * times * 1.2},
        {"Component": "Bulk Citrate", "Volume (μL)": volumes["citrate_volume"] * times * 1.2},
        {"Component": "Bulk Water", "Volume (μL)": volumes["water_volume"] * times * 1.2}
    ]

def main():
    st.title("LNP Formulation Calculator")
    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        rna_scale = st.number_input("RNA Scale (μg)", min_value=0.0, step=1.0, value=3.0)
    with col2:
        rna_stock = st.number_input("RNA Stock (μg/μL)", min_value=0.0, step=0.1, value=1.0)
    with col3:
        ionizable_lipid_to_rna_ratio = st.number_input("Ionizable Lipid to RNA Ratio", min_value=0.0, max_value=100.0, step=0.1, value=10.0)
    with col4:
        aqueous_to_ethanol_ratio = st.number_input("Aqueous to Ethanol Ratio", min_value=0.0, step=0.1, value=3.0)

    col5, col6 = st.columns(2)
    with col5:
        ionizable_lipid_mw = st.number_input("Ionizable Lipid Molecular Weight (μg/μmol)", min_value=0.0, step=1.0, value=1000.0)
    with col6:
        helper_lipid_mw = st.number_input("Helper Lipid Molecular Weight (μg/μmol)", min_value=0.0, step=1.0, value=744.034)
        
    col7, col8 = st.columns(2)
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
    
    col17, col18 = st.columns(2)
    with col17:
        bulk_times = st.number_input("Bulk Preparation Times", min_value=1, step=1, value=1)

    if st.button("Calculate"):
        # Use the make_lnp_formulation function to calculate the values
        result_df, volumes = make_lnp_formulation(rna_scale, rna_stock, ionizable_lipid_to_rna_ratio, aqueous_to_ethanol_ratio, ionizable_lipid_mw, helper_lipid_mw, cholesterol_mw, pegdmg2000_mw, ionizable_lipid_concentration, helper_lipid_concentration, cholesterol_concentration, pegdmg2000_concentration, ionizable_lipid_ratio, helper_lipid_ratio, cholesterol_ratio, pegdmg2000_ratio)
    
        # Display the results
        st.dataframe(result_df)
    
        # Calculate and display bulk volumes
        bulk_volumes = prepare_bulk_lnp_volumes(volumes, bulk_times)
        bulk_df = pd.DataFrame(bulk_volumes)
        st.dataframe(bulk_df)

if __name__ == "__main__":
    main()