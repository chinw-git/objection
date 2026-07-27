import json
import pandas as pd
import streamlit as st
from utils.bucket_mapper import BucketMapper

from crews.objection_assessment_crew import (
    create_objection_assessment_crew
)

mapper = BucketMapper()


st.set_page_config(
    page_title="Property Objection Assessment",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Property Objection Assessment")

st.write(
    "Enter the grounds of objection below to assess the case "
    "using historical precedents."
)

objection = st.text_area(
    "Grounds of Objection",
    height=250
)


if st.button("Assess Objection"):

    if objection.strip() == "":
        st.warning("Please enter an objection.")
        st.stop()

    with st.spinner("Assessing objection..."):

        crew = create_objection_assessment_crew()

        response = crew.kickoff(
            inputs={
                "objection": objection
            }
        )

    # CrewAI usually returns a CrewOutput object
    try:
        result = json.loads(str(response))
    except Exception:
        result = response

    result = mapper.enrich(result)

    st.divider()
    st.header("Assessment Summary")

    col1, col2, col3 = st.columns(3)

    

    col1.metric(
        "Primary Bucket",
        result.get("primary_bucket", "-")
    )

    col2.metric(
        "Complexity",
        result.get("complexity", "-")
    )

    col3.metric(
        "Urgency",
        result.get("urgency", "-")
    )

    st.divider()

    st.header("Reasoning")

    st.write(result.get("reasoning", "No reasoning returned."))

    st.divider()

    st.header("Supporting Historical Cases")

    supporting_cases = result.get(
        "supporting_cases",
        []
    )

    if len(supporting_cases) > 0:

        rows = []

        for i, case in enumerate(supporting_cases, start=1):

            rows.append({

                "Case": i,

                "Primary Bucket": case.get(
                    "primary_bucket",
                    "-"
                ),

                "Complexity": case.get(
                    "complexity",
                    "-"
                ),

                "Urgency": case.get(
                    "urgency",
                    "-"
                ),

                "Grounds Preview":
                    case.get(
                        "grounds_of_objection",
                        ""
                    )[:100] + "..."
            })

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Case Details")

        for i, case in enumerate(supporting_cases, start=1):

            with st.expander(f"Case {i}"):

                st.markdown("**Grounds of Objection**")

                st.text(
                    case.get(
                        "grounds_of_objection",
                        "-"
                    )
                )

                st.markdown("**Primary Bucket**")

                st.text(
                    case.get(
                        "primary_bucket",
                        "-"
                    )
                )

                st.markdown("**Complexity**")

                st.text(
                    case.get(
                        "complexity",
                        "-"
                    )
                )

                st.markdown("**Urgency**")

                st.write(
                    case.get(
                        "urgency",
                        "-"
                    )
                )

                if "distance" in case:

                    st.markdown("**Similarity Distance**")

                    st.write(case["distance"])

    else:

        st.info("No supporting cases were returned.")

    with st.expander("Developer Output"):

        st.json(result)