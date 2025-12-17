import streamlit as st
import pandas as pd
import io

# import your stages
from services.identification import Stage1
from services.enrichment import stage2
from services.scoring import Stage3

st.set_page_config(
    page_title="Lead Generation Agent",
    layout="wide"
)

st.title("Lead Generation Agent")

# Sidebar – Inputs
st.sidebar.header("Identification Filters")

title_filter = st.sidebar.text_input(
    "Title keywords (optional)",
    placeholder="toxicology, safety"
)

company_filter = st.sidebar.text_input(
    "Company (optional)"
)

name_filter = st.sidebar.text_input(
    "Name (optional)"
)

run_button = st.sidebar.button("Run Lead Generation")

# Run Pipeline
if run_button:
    st.info("Running identification → enrichment → scoring pipeline...")

    # identification
    stage1 = Stage1(
        name=name_filter if name_filter else None,
        title=title_filter if title_filter else None,
        company=company_filter if company_filter else None
    )

    identified_df = stage1.identification("C:/Users/hp333/Desktop/lead_generator/data/people_pool.csv")

    if identified_df is None or identified_df.empty:
        st.warning("No leads identified with current filters.")
        st.stop()

    st.success(f"Identified {len(identified_df)} potential leads")

    #enrichment
    stage2 = stage2()
    enriched_df, not_found = stage2.find_more_details(
        identified_df,
        "C:/Users/hp333/Desktop/lead_generator/data/leads.csv"
    )
    enriched_df.dropna(axis = 1, how = "all", inplace = True)
    enriched_df.reset_index(inplace=True)

    #scoring
    stage3 = Stage3()
    scored_df = stage3.scoring(enriched_df)

    # Sort by probability
    scored_df = scored_df.sort_values(
        "probability_score",
        ascending=False
    )

    # Search inside results
    st.subheader("Search Results")
    search_query = st.text_input(
        "Search by name, title, company, or location"
    )

    if search_query:
        mask = scored_df.astype(str).apply(
            lambda col: col.str.contains(search_query, case=False, na=False)
        ).any(axis=1)
        display_df = scored_df[mask]
    else:
        display_df = scored_df
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        display_df.to_excel(
            writer,
            index=False,
            sheet_name="Ranked Leads"
        )

    excel_buffer.seek(0)

    # Display Table
    st.subheader("Ranked Leads")

    st.dataframe(
        display_df,
        use_container_width=True
    )

    # Download CSV
    csv_data = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="ranked_leads.csv",
        mime="text/csv"
    )

    st.download_button(
    label="Download Excel (.xlsx)",
    data=excel_buffer,
    file_name="ranked_leads.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Not Found Info
    if not_found:
        st.warning(
            f"No enrichment data found for {len(not_found)} leads"
        )
        st.write(not_found)

else:
    st.info("Set filters and click **Run Lead Generation**.")
