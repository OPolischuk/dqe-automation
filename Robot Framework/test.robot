*** Settings ***
Documentation     End-to-End DQE test: Validating BI report accuracy against Parquet storage.
Library           SeleniumLibrary
Library           helper.py
Test Teardown     Close Browser

*** Variables ***
${REPORT_URL}        file:///C:/polishchuk1/Studying/DQE%20Automation/dqe-automation/Robot%20Framework/report.html
${PARQUET_FOLDER}    C:/polishchuk1/Studying/DQE Automation/dqe-automation/results/parquet_data/facility_type_avg_time_spent_per_visit_date

# Defining the synchronization window to align Parquet data with the BI Report UI
${START_DATE}        2026-03-10
${END_DATE}          2026-03-16

*** Test Cases ***
Compare BI Report With Parquet
    [Documentation]    Extracts reporting data via JavaScript execution and compares it with filtered Parquet datasets.
    
    Open Browser    ${REPORT_URL}    chrome
    Maximize Browser Window
    Sleep    5s

    # Accessing Plotly data object directly from the DOM to avoid complex HTML parsing
    ${plotly_json}=    Execute Javascript    
    ...    return JSON.stringify(document.getElementsByClassName('plotly-graph-div')[0].data.find(trace => trace.type === 'table'));

    # Loading extracted JSON into a Pandas DataFrame
    ${df_html}=       Read Plotly Json      ${plotly_json}

    # Reading Parquet data with targeted date filtering for precise validation
    ${df_parquet}=    Read Parquet Data     ${PARQUET_FOLDER}    ${START_DATE}    ${END_DATE}

    # Executing the comparison logic and capturing the validation status
    ${status}    ${diff}=    Compare Dataframes    ${df_html}    ${df_parquet}

    # Assertion fails with detailed mismatch log if status is False
    Should Be True    ${status}    ${diff}