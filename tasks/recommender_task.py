from crewai import Task

def create_recommender_task(recommender_agent, classifier_task):
    return Task(

            description="""
            You are advising a property tax valuer on the next steps for a property tax objection that has already been assessed.

            <definitions>

            - RFI (Request for Information): A request issued to the taxpayer to obtain
            additional documents or clarification required to assess the objection.
            - Comparable properties: Similar properties that can be used as valuation
            evidence.

            </definitions>

            <inputs>

            You are provided with:
            1. The current objection.
            2. The complexity assessment from the previous task, including:
            - complexity category
            - triggered rubric criteria
            - relevant Property Tax Act sections
            - reasoning

            </inputs>

            <instructions>
            
            - You have access to the complexity assessment produced by the previous classifier task.
            - Do NOT modify, reinterpret or recompute the classification.
            - Preserve the previous task's classification exactly as provided.
            - Your responsibility is only to recommend SPECIFIC and ACTIONABLE next steps for the valuer.
            - Base your recommendations only on:
                - the user's objection,
                - the assigned complexity assessment,
                - the relevant Property Tax Act sections.
            - Adhere to the decision rules below when determining the next steps.
            - Return a single JSON object containing BOTH the classification and the recommendation.
        
            </instructions>
            
            <decision rules>
            If the category is **EASY – DISALLOW**:
            - Recommend finding suitable comparable properties.
            - Recommend disallowing the objection.
            - State exactly:
                - "Find comparables"
                - "Disallow the objection"
            - Briefly describe the type of comparables that should be reviewed
            (e.g. similar units within the same development or nearby comparable properties).
        
            If the category is **EASY – RFI (minimal)**:
            - Recommend only the minimum supporting documents required.
            - Specify the exact document(s) to request.
            - Examples include:
                - tenancy agreement
                - rental invoices
                - floor plans
                - photographs
            - Avoid generic statements such as "request more information".
        
            If the category is **MEDIUM – RFI (extensive)**:
            - Recommend all supporting documents required.
            - Name the exact document types.
            - Include any valuation evidence or additional information needed.
        
            If the category is **DIFFICULT**:
            - Recommend escalation to a senior valuer or appropriate specialist.
            - Explain why escalation is necessary.
            - State what expertise is required
            (for example engineering assessment, valuation expertise, or legal interpretation of the Property Tax Act).
            
            <decision rules>
            """,
        
            expected_output="""
            Return ONLY valid JSON.
        
            {
                "classification": {
                    "complexity": "",
                    "rubric_criteria": [
                        ""
                    ],
                    "relevant_pta_sections": [
                        {
                            "section": "",
                            "content": "",
                            "reason": ""
                        }
                    ],
                    "reasoning": ""
                },
        
                "recommendation": {
                    "rfi_needed": true | false,
                    "next_steps": [
                        ""
                    ],
                    "escalation_needed": true | false,
                    "escalation_reason": "Reason if escalation_needed is true, otherwise an empty string."
                }
            }
        
            Where:
            - rfi_needed must be either true or false.
            - escalation_needed must be either true or false.
            - escalation_reason must contain a reason only if escalation_needed is true; otherwise return an empty string ("").
            - next_steps must contain one or more specific, actionable recommendations.
        
            Do not include markdown, code fences, or any additional text outside the JSON object.
            """,
        
            agent=recommender_agent,
            context=[classifier_task],
        )