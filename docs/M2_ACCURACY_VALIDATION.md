
# Milestone 2 – Accuracy Validation and Testing

## 1. Objective

The objective of Milestone 2 is to validate the Triage Agent, Log Analysis Agent, and Multi-Agent Orchestrator of the Intelligent Bug Diagnosis Platform.

Testing was performed using predefined bug reports with expected outputs. Actual agent outputs were compared against these expected values.

The agents currently use rule-based logic and regular-expression-based extraction. Confidence scores are heuristic values and should not be interpreted as statistical probabilities.

---

## 2. Triage Agent Validation

### 2.1 Test Coverage

The Triage Agent was tested using 10 predefined bug reports.

The test cases covered:

- Critical production outage
- High authentication failure
- Medium network timeout
- Low user-interface alignment issue
- Performance issue
- Search failure
- Payment failure
- Database query failure
- File upload failure
- Memory failure

### 2.2 Expected Outputs

Each test checked three fields:

- Severity
- Priority
- Affected software component

### 2.3 Results

| Metric | Result |
|---|---:|
| Test cases | 10 |
| Total field checks | 30 |
| Passed checks | 30 |
| Failed checks | 0 |
| Field-level accuracy | 100% |

The Triage Agent successfully classified all 10 test cases according to their predefined expected labels.

---

## 3. Log Analysis Agent Validation

### 3.1 Test Coverage

The Log Analysis Agent was tested using 8 test cases.

The test cases covered:

1. Java NullPointerException
2. Java ArrayIndexOutOfBoundsException
3. Python ValueError
4. JavaScript TypeError
5. Logs without a stack trace
6. Logs without a bug description
7. Messy Python logs
8. Empty bug report

### 3.2 Validation Fields

Each test checked:

- Exception or error type
- Failure-point file name
- Failure-point line number
- Analysis status

Code-path extraction and heuristic confidence scores were also observed.

### 3.3 Results

| Metric | Result |
|---|---:|
| Test cases | 8 |
| Total field checks | 32 |
| Passed checks | 32 |
| Failed checks | 0 |
| Field-level accuracy | 100% |

### 3.4 Observations

- Java exception types and stack frames were extracted successfully.
- Python exception types, file names, and line numbers were extracted successfully.
- JavaScript error type, file name, and line number were extracted successfully.
- Logs without stack traces were processed without failure.
- Reports containing logs but no description were analysed successfully.
- Empty reports returned an Incomplete status.

### 3.5 Known Limitations

- JavaScript stack frames are not currently included in the extracted code path.
- Logs without stack traces cannot provide a reliable failure-point location.
- The parser supports selected common formats and may not recognise every logging format.
- Confidence scores are rule-based heuristic values.

---

## 4. Multi-Agent Orchestrator Validation

### 4.1 Objective

The orchestrator coordinates the Triage Agent and Log Analysis Agent. It passes the submitted bug report to both agents, collects their outputs, and determines the overall analysis status.

### 4.2 Test Coverage

Five scenarios were tested:

1. Complete bug report containing description, stack trace, and logs.
2. Report without logs.
3. Logs without a description.
4. Empty bug report.
5. Invalid report input.

### 4.3 Results

| Metric | Result |
|---|---:|
| Test cases | 5 |
| Total field checks | 15 |
| Passed checks | 15 |
| Failed checks | 0 |
| Field-level accuracy | 100% |

### 4.4 Observations

- Both agents completed successfully for a complete report.
- Missing logs resulted in a Partial overall status.
- Logs without a description were analysed successfully.
- Empty reports were handled without crashing.
- Invalid input caused the Triage Agent to fail while the Log Analysis Agent returned an Incomplete result.
- The orchestrator continued execution when one agent failed.

---

## 5. Overall Validation Summary

| Component | Test Cases | Total Checks | Passed | Failed |
|---|---:|---:|---:|---:|
| Triage Agent | 10 | 30 | 30 | 0 |
| Log Analysis Agent | 8 | 32 | 32 | 0 |
| Agent Orchestrator | 5 | 15 | 15 | 0 |
| **Total** | **23** | **77** | **77** | **0** |

Overall field-level accuracy on the defined validation checks:

**100% (77 out of 77 checks passed).**

This result applies only to the predefined test cases. It does not represent general real-world accuracy or performance on unseen bug reports.

---

## 6. Known System Limitations

1. The agents currently use predefined rules and regular expressions rather than trained machine-learning classifiers.
2. Severity, priority, and component predictions depend on keyword matching.
3. Confidence scores are heuristic and are not calibrated probabilities.
4. Log extraction supports selected Java, Python, and JavaScript formats but does not cover every possible stack-trace format.
5. Historical defect retrieval can return unrelated results for some queries.
6. Retrieved similarity scores should be treated as ranking scores, not verified diagnosis confidence.
7. Root-cause hypotheses and remediation suggestions require developer verification.

---

## 7. Historical Mozilla Triage Validation – Final Results

The Triage Agent was additionally evaluated using 20 historical Mozilla bug reports.

**Input fields:** Title and Description only.

### 7.1 Severity Validation

- Comparable records: 18
- Correct predictions: 18
- Incorrect predictions: 0
- Agreement: 100%

Provisional source-label mapping:

- normal → Medium
- minor → Low
- S3 → Medium

Records with unavailable or unsupported severity labels were excluded from comparison.

### 7.2 Component Validation

- Comparable records: 10
- Correct predictions: 10
- Incorrect predictions: 0
- Agreement: 100%

Only historical File Handling labels were directly mapped to the implemented component category. Other source-specific component labels were not compared.

### 7.3 Improvements Made

1. Refined component keywords to reduce false matches.
2. Added URI Loader recognition for URILoader.
3. Added feature-request keywords to identify minor enhancement requests.
4. Re-ran predefined and historical validation after the changes.

### 7.4 Limitations

- The historical dataset contains only 20 Mozilla records.
- Label mappings are provisional and may not exactly represent the original severity definitions.
- Component agreement covers only records with a directly comparable mapped label.
- Results should not be interpreted as general real-world accuracy.
- The agent uses keyword-based rules rather than a trained classification model.

---

## 8. Conclusion

The Triage Agent, Log Analysis Agent, and Multi-Agent Orchestrator passed all 77 predefined validation checks.

The Triage Agent also achieved 100% agreement on 18 comparable historical severity labels and 10 comparable historical component labels.

The testing confirmed that the agents can process representative bug reports, extract selected error information, classify predefined issue categories, and handle missing or invalid inputs without stopping the entire orchestration workflow.

The current implementation provides a rule-based prototype for intelligent bug diagnosis. Further improvements are required to increase retrieval relevance, broaden log-format support, and evaluate performance on larger and independently labelled datasets.
