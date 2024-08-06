from pathlib import Path
import sqlite3
import streamlit as st
import altair as alt
import pandas as pd

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='96-Well Plate Tracker',
    page_icon=':test_tube:',  # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

def connect_db():
    '''Connects to the sqlite database.'''

    DB_FILENAME = Path(__file__).parent / '96_well_plate.db'
    db_already_exists = DB_FILENAME.exists()

    conn = sqlite3.connect(DB_FILENAME)
    db_was_just_created = not db_already_exists

    return conn, db_was_just_created


def initialize_data(conn):
    '''Initializes the 96-well plate table with some data.'''
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS wells (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT UNIQUE,
            name TEXT,
            volume REAL,
            lipid_structure TEXT
        )
        '''
    )

    # Sample data
    data = [
        ("A1", "A1", -560.0, "Amines"),
        ("B1", "None", 0.0, "None"),
        ("C1", "None", 0.0, "None"),
        ("D1", "None", 0.0, "None"),
        ("E1", "None", 0.0, "None"),
        ("F1", "None", 0.0, "None"),
        ("G1", "D13", 880.0, "Lipid Carboxylic Acid"),
        ("H1", "None", 0.0, "None"),
        ("A2", "A2", 240.0, "Amines"),
        ("B2", "None", 0.0, "None"),
        ("C2", "None", 0.0, "None"),
        ("D2", "None", 0.0, "None"),
        ("E2", "None", 0.0, "None"),
        ("F2", "None", 0.0, "None"),
        ("G2", "None", 0.0, "None"),
        ("H2", "D26", 880.0, "Lipid Carboxylic Acid"),
        ("A3", "None", 0.0, "None"),
        ("B3", "None", 0.0, "None"),
        ("C3", "None", 0.0, "None"),
        ("D3", "B7", 400.0, "Isocyanide"),
        ("E3", "None", 0.0, "None"),
        ("F3", "None", 0.0, "None"),
        ("G3", "None", 0.0, "None"),
        ("H3", "D27", 880.0, "Lipid Carboxylic Acid"),
        ("A4", "A4", 2000.0, "Amines"),
        ("B4", "None", 0.0, "None"),
        ("C4", "None", 0.0, "None"),
        ("D4", "None", 0.0, "None"),
        ("E4", "None", 0.0, "None"),
        ("F4", "None", 0.0, "None"),
        ("G4", "None", 0.0, "None"),
        ("H4", "None", 0.0, "None"),
        ("A5", "A5", 2000.0, "Amines"),
        ("B5", "None", 0.0, "None"),
        ("C5", "None", 0.0, "None"),
        ("D5", "None", 0.0, "None"),
        ("E5", "C9", 920.0, "Lipid Aldehyde"),
        ("F5", "None", 0.0, "None"),
        ("G5", "None", 0.0, "None"),
        ("H5", "None", 0.0, "None"),
        ("A6", "None", 0.0, "None"),
        ("B6", "None", 0.0, "None"),
        ("C6", "None", 0.0, "None"),
        ("D6", "None", 0.0, "None"),
        ("E6", "C10", 920.0, "Lipid Aldehyde"),
        ("F6", "None", 0.0, "None"),
        ("G6", "None", 0.0, "None"),
        ("H6", "None", 0.0, "None"),
        ("A7", "None", 0.0, "None"),
        ("B7", "None", 0.0, "None"),
        ("C7", "None", 0.0, "None"),
        ("D7", "B11", 400.0, "Isocyanide"),
        ("E7", "None", 0.0, "None"),
        ("F7", "None", 0.0, "None"),
        ("G7", "None", 0.0, "None"),
        ("H7", "None", 0.0, "None"),
        ("A8", "None", 0.0, "None"),
        ("B8", "None", 0.0, "None"),
        ("C8", "None", 0.0, "None"),
        ("D8", "B12", 880.0, "Isocyanide"),
        ("E8", "None", 0.0, "None"),
        ("F8", "None", 0.0, "None"),
        ("G8", "None", 0.0, "None"),
        ("H8", "None", 0.0, "None"),
        ("A9", "None", 0.0, "None"),
        ("B9", "None", 0.0, "None"),
        ("C9", "None", 0.0, "None"),
        ("D9", "None", 0.0, "None"),
        ("E9", "None", 0.0, "None"),
        ("F9", "None", 0.0, "None"),
        ("G9", "None", 0.0, "None"),
        ("H9", "None", 0.0, "None"),
        ("A10", "None", 0.0, "None"),
        ("B10", "None", 0.0, "None"),
        ("C10", "None", 0.0, "None"),
        ("D10", "None", 0.0, "None"),
        ("E10", "None", 0.0, "None"),
        ("F10", "None", 0.0, "None"),
        ("G10", "None", 0.0, "None"),
        ("H10", "None", 0.0, "None"),
        ("A11", "None", 0.0, "None"),
        ("B11", "None", 0.0, "None"),
        ("C11", "None", 0.0, "None"),
        ("D11", "None", 0.0, "None"),
        ("E11", "C15", 920.0, "Lipid Aldehyde"),
        ("F11", "None", 0.0, "None"),
        ("G11", "None", 0.0, "None"),
        ("H11", "None", 0.0, "None"),
        ("A12", "None", 0.0, "None"),
        ("B12", "None", 0.0, "None"),
        ("C12", "None", 0.0, "None"),
        ("D12", "None", 0.0, "None"),
        ("E12", "C16", 920.0, "Lipid Aldehyde"),
        ("F12", "D12", 1040.0, "Lipid Carboxylic Acid"),
        ("G12", "None", 0.0, "None"),
        ("H12", "None", 0.0, "None")
    ]

    # Insert initial data
    cursor.executemany(
        '''
        INSERT OR IGNORE INTO wells (location, name, volume, lipid_structure)
        VALUES (?, ?, ?,
        ''', data
    )

    # Ensure all wells are initialized
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    cols = list(range(1, 13))
    all_wells = [f"{r}{c}" for r in rows for c in cols]

    for well in all_wells:
        cursor.execute(
            '''
            INSERT OR IGNORE INTO wells (location, name, volume, lipid_structure)
            VALUES (?, ?, ?, ?)
            ''', (well, 'None', 0.0, 'None')
        )

    conn.commit()


def load_data(conn):
    '''Loads the 96-well plate data from the database.'''
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM wells')
        data = cursor.fetchall()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

    df = pd.DataFrame(data,
                      columns=['id', 'location', 'name', 'volume', 'lipid_structure'])

    return df


def update_data(conn, df, changes):
    '''Updates the 96-well plate data in the database.'''
    cursor = conn.cursor()

    if changes['edited_rows']:
        deltas = st.session_state.well_table['edited_rows']
        rows = []

        for i, delta in deltas.items():
            row_dict = df.iloc[i].to_dict()
            row_dict.update(delta)
            rows.append(row_dict)

        cursor.executemany(
            '''
            UPDATE wells
            SET
                location = :location,
                name = :name,
                volume = :volume,
                lipid_structure = :lipid_structure
            WHERE id = :id
            ''',
            rows,
        )

    if changes['added_rows']:
        # Prepare data for insertion
        new_rows = []
        for row in changes['added_rows']:
            # Ensure all keys are present with default values if missing
            row_dict = {key: row.get(key, None) for key in ['location', 'name', 'volume', 'lipid_structure']}
            row_dict['volume'] = row_dict.get('volume', 0.0)
            new_rows.append(row_dict)

        cursor.executemany(
            '''
            INSERT INTO wells
                (location, name, volume, lipid_structure)
            VALUES
                (:location, :name, :volume, :lipid_structure)
            ''',
            new_rows
        )

    if changes['deleted_rows']:
        cursor.executemany(
            'DELETE FROM wells WHERE id = :id',
            ({'id': int(df.loc[i, 'id'])} for i in changes['deleted_rows'])
        )

    conn.commit()


# -----------------------------------------------------------------------------
# Draw the actual page, starting with the inventory table.

# Set the title that appears at the top of the page.
'''
# :test_tube: 96-Well Plate Tracker

**Welcome to the 96-Well Plate Tracker!**
This page reads and writes directly from/to our database.
'''

st.info('''
    Use the table below to add, remove, and edit wells.
    And don't forget to commit your changes when you're done.
    ''')

# Connect to database and create table if needed
conn, db_was_just_created = connect_db()

# Initialize data.
if db_was_just_created:
    initialize_data(conn)
    st.toast('Database initialized with some sample data.')

# Load data from database
df = load_data(conn)

# Display data with editable table
edited_df = st.data_editor(
    df,
    disabled=['id'],  # Don't allow editing the 'id' column.
    num_rows='dynamic',  # Allow appending/deleting rows.
    key='well_table')

has_uncommitted_changes = any(len(v) for v in st.session_state.well_table.values())

st.button(
    'Commit changes',
    type='primary',
    disabled=not has_uncommitted_changes,
    # Update data in database
    on_click=update_data,
    args=(conn, df, st.session_state.well_table))

# -----------------------------------------------------------------------------
# Visualization of 96-Well Plate

# Add some space
''
''
''

st.subheader('96-Well Plate Visualization', divider='red')

# Visualization using Altair
chart = alt.Chart(edited_df).mark_circle(size=60).encode(
    x=alt.X('location:O', title='Location'),
    y=alt.Y('volume:Q', title='Volume'),
    color=alt.Color('volume:Q', scale=alt.Scale(scheme='blues')),
    tooltip=['name', 'volume', 'lipid_structure']
).properties(
    width=800,
    height=300
)

st.altair_chart(chart, use_container_width=True)

st.caption('The size and color of each dot represent the volume in each well.')

# -----------------------------------------------------------------------------

st.subheader('Volume Updates', divider='orange')

# Sidebar for updating volumes
location = st.selectbox("Select Well Location", options=df['location'].unique())
volume_change = st.number_input("Volume Change", value=0.0)

if st.button("Update Volume"):
    # Update the volume in the session state and database
    current_volume = df.loc[df['location'] == location, 'volume'].values[0]
    new_volume = current_volume + volume_change
    df.loc[df['location'] == location, 'volume'] = new_volume
    
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE wells
        SET volume = ?
        WHERE location = ?
        ''',
        (new_volume, location)
    )
    conn.commit()

    st.success(f"Volume at {location} updated to {new_volume:.2f}")

# -----------------------------------------------------------------------------
# Closing the database connection
conn.close()