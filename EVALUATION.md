# Evaluation System Documentation

## Overview

The Courtroom AI system includes a comprehensive evaluation framework that measures and tracks the quality of legal simulations across multiple dimensions. This system automatically evaluates every case simulation and stores metrics for historical analysis and trend tracking.

## Key Features

### 1. **Automatic Evaluation**
After each simulation completes, the system automatically evaluates the case on standardized criteria and stores the results.

### 2. **Multi-Dimensional Scoring**
Evaluation happens across 8 core dimensions:

| Dimension | Weight | Measures |
|-----------|--------|----------|
| **Case Analysis** | 20% | Completeness of case extraction, fact accuracy, entity recognition |
| **Legal Research** | 25% | Relevance of cited sections and precedents, research completeness |
| **Argument Quality** | 25% | Coherence of prosecution/defense arguments, debate strength |
| **Verdict Quality** | 30% | Justification clarity, reasoning quality, confidence calibration |

### 3. **Performance Metrics**
Tracks execution time for each component:
- Case Manager processing time
- Legal Research generation time
- Debate execution time (both rounds)
- Judge deliberation time
- **Total execution time**

### 4. **Historical Analytics**
All metrics are stored in JSONL format for:
- Trend analysis over time
- Verdict distribution analysis
- Component performance comparison
- Quality improvement tracking

## Core Metrics

### Quality Scores (0-100)

#### Case Analysis Quality
- **Case Extraction Completeness**: How complete the case details extracted
- **Fact Accuracy**: Percentage of accurately identified facts
- **Entity Recognition Accuracy**: How well entities (accused, victim) are identified

#### Legal Research Quality
- **Applicable Sections Relevance**: Relevance of cited BNS/other law sections
- **Precedent Relevance**: Quality and applicability of cited precedents
- **Legal Research Completeness**: Overall coverage of legal analysis

#### Argument Quality
- **Prosecution Coherence**: Quality and consistency of prosecution arguments
- **Defense Coherence**: Quality and consistency of defense arguments
- **Argument Strength**: Overall debate quality score

#### Verdict Quality
- **Verdict Justification**: How well the verdict is justified by reasoning
- **Confidence Calibration**: How well the judge's confidence level matches verdict clarity
- **Reasoning Clarity**: How clear and well-articulated the reasoning is
- **Precedent Adherence**: Does verdict follow from cited legal precedents?

#### System Performance
- **Consistency Score**: How consistent is the verdict with presented arguments
- **Overall Quality Score**: Weighted average of all quality scores

## Data Storage

### File Structure
```
evaluation/
├── data/
│   ├── metrics_history.jsonl        # All recorded metrics (append-only)
│   ├── summary.json                  # Current summary statistics
│   └── metrics_export.csv            # Exported CSV for analysis
├── evaluator.py                      # Core evaluation logic
├── metrics.py                        # Metrics collection & storage
├── dashboard.py                      # Streamlit dashboard
└── __init__.py
```

### Metrics Record Format
Each metric record contains:

```python
{
    "timestamp": "2026-06-24T14:30:00",
    "case_id": "a1b2c3d4",
    "accused": "Malkhan Singh",
    "verdict": "Guilty",
    "confidence": 85,
    
    # Quality Scores
    "case_extraction_completeness": 92.5,
    "fact_accuracy": 88.0,
    "entity_recognition_accuracy": 95.0,
    "applicable_sections_relevance": 90.0,
    "precedent_relevance": 85.0,
    "legal_research_completeness": 87.5,
    "prosecution_coherence": 82.0,
    "defense_coherence": 78.0,
    "argument_strength": 80.0,
    "verdict_justification_quality": 88.0,
    "confidence_calibration": 75.0,
    "reasoning_clarity": 85.0,
    
    # Performance
    "total_execution_time": 45.3,
    "case_manager_time": 2.1,
    "legal_research_time": 8.5,
    "debate_time": 28.7,
    "judge_time": 6.0,
    
    # Consistency
    "consistency_score": 85.0,
    "precedent_adherence": 80.0,
    "overall_quality_score": 84.2
}
```

## Accessing Metrics

### 1. **In-App Dashboard**
- Navigate to the sidebar and check **"📈 View Evaluation Metrics"**
- View real-time quality trends
- Analyze component breakdown
- Review verdict distribution
- Export data to CSV

### 2. **Programmatic Access**

```python
from evaluation.metrics import MetricsCollector

collector = MetricsCollector()

# Get all metrics
all_metrics = collector.get_all_metrics()

# Get average scores
averages = collector.get_average_metrics()

# Get recent cases
recent = collector.get_recent_metrics(n=10)

# Export to CSV
collector.export_csv("my_export.csv")
```

### 3. **Direct File Access**
- **metrics_history.jsonl**: Raw JSONL file with one metric record per line
- **summary.json**: Current aggregated statistics

## Evaluation Criteria Details

### Case Analysis Evaluation

The system evaluates how well the Case Manager extracts and structures the case:

- ✅ Completeness: Are all required fields present? (Accused, Victim, Allegation, Facts)
- ✅ Accuracy: Are the extracted facts accurate and relevant?
- ✅ Entity Recognition: Are key entities (people, organizations) correctly identified?
- ⚠️ Missing Information: Are important gaps in the complaint noted?

**Score Impact**: 
- 25 points per required field present
- +10 bonus if 5+ detailed facts extracted
- Penalized 15 points per missing information item

### Legal Research Evaluation

Measures the quality of legal research and precedent analysis:

- ✅ Applicable Sections: Are relevant BNS/legal sections identified?
- ✅ Precedents: Are relevant court decisions cited?
- ✅ Evidentiary Notes: Are evidentiary considerations noted?
- ✅ Unsettled Questions: Are open legal questions identified?

**Score Impact**:
- 20 points per applicable section (max 100)
- 25 points per relevant precedent (max 100)
- 10 points per evidentiary note
- Overall capped at 100

### Argument Quality Evaluation

Evaluates the strength and coherence of legal arguments:

- ✅ Prosecution Arguments: Length and detail of prosecution case
- ✅ Defense Arguments: Length and detail of defense case
- ✅ Balance: Are both sides presenting substantive arguments?

**Score Impact**:
- Normalized on length (assuming 1000+ chars = good argument)
- Averaged score between prosecution and defense
- Balanced arguments receive higher strength scores

### Verdict Quality Evaluation

Measures the quality of the judge's verdict and reasoning:

- ✅ Justification: Is the verdict well-justified?
- ✅ Reasoning Clarity: Is the reasoning clear and detailed?
- ✅ Confidence Calibration: Does confidence match verdict certainty?
- ✅ Precedent Adherence: Does verdict follow cited precedents?

**Score Impact**:
- Based on length and detail of findings and reasoning
- Confidence between 30-70% scores higher (more nuanced)
- Extreme confidence (0-20, 80-100%) scores lower
- Bonus points for citing precedents that match verdict

## Quality Benchmarks

### Excellent (85-100)
- Thorough case analysis with complete details
- Comprehensive legal research with relevant precedents
- Strong, well-articulated arguments from both sides
- Clear, well-justified verdict with nuanced reasoning
- Good confidence calibration

### Good (70-84)
- Most case details properly extracted
- Adequate legal research with some precedents
- Reasonable arguments from both sides
- Verdict is justified but reasoning could be clearer
- Moderate confidence calibration

### Acceptable (55-69)
- Basic case analysis with some gaps
- Legal research present but limited
- Arguments present but lack depth
- Verdict justified but minimal reasoning
- Weak confidence calibration

### Needs Improvement (<55)
- Incomplete case analysis
- Limited legal research
- Weak arguments
- Verdict not well-justified
- Poor confidence calibration

## Trend Analysis

### Questions You Can Answer

**Case Quality**
- "How has overall case quality changed over time?"
- "Which component has the most room for improvement?"
- "Are verdicts becoming more consistent?"

**Performance**
- "What's the average execution time?"
- "Which component takes the longest?"
- "Is system performance improving or degrading?"

**Patterns**
- "What's the conviction rate?"
- "Are guilty/not guilty verdicts of similar quality?"
- "Do confidence scores match actual verdict clarity?"

**System Behavior**
- "How well calibrated is the judge's confidence?"
- "Does the legal research quality correlate with verdict quality?"
- "Are arguments from both sides equally strong?"

## Integration Points

The evaluation system integrates at these points:

1. **Streaming Engine**: Tracks execution time for each node
2. **Simulation Completion**: Automatically evaluates completed cases
3. **Sidebar Dashboard**: Displays metrics and trends
4. **Export**: Allows CSV export for external analysis

## Best Practices

### Using Metrics for Improvement

1. **Monitor Quality Trends**
   - Check dashboard regularly
   - Look for declining trends
   - Investigate low-scoring cases

2. **Component Analysis**
   - Identify weak components
   - Focus improvement efforts
   - Track improvements over time

3. **Consistency Checking**
   - Use verdict distribution analysis
   - Compare similar cases
   - Ensure consistent application of law

4. **Performance Optimization**
   - Monitor execution times
   - Identify bottlenecks
   - Prioritize improvements

## Example Insights

### High-Quality Case
- Overall Score: 88/100
- All components score >85
- Confidence calibration excellent
- Clear precedent adherence
- Execution time reasonable

### Low-Quality Case  
- Overall Score: 62/100
- Case analysis weak (incomplete facts)
- Legal research limited (few precedents)
- Arguments lack depth
- Verdict reasoning unclear

## Advanced Analysis

### CSV Export
Export all metrics to CSV for analysis in Excel, Python, or other tools:

```bash
# From Python
from evaluation.metrics import MetricsCollector
collector = MetricsCollector()
collector.export_csv("analysis.csv")
```

### Custom Analysis
Load metrics for custom analysis:

```python
import pandas as pd
from evaluation.metrics import MetricsCollector

collector = MetricsCollector()
metrics = collector.get_all_metrics()

# Create DataFrame
df = pd.DataFrame([m.to_dict() for m in metrics])

# Analysis
print(df['overall_quality_score'].mean())
print(df.groupby('verdict')[['overall_quality_score']].mean())
```

## FAQ

**Q: Why did a case score low?**
A: Check the component scores in the summary. Look for weak areas (e.g., "verdict_quality" low suggests reasoning clarity issues).

**Q: How often should I check metrics?**
A: After every 5-10 cases, review the dashboard to catch trends early.

**Q: Can I improve scores?**
A: Scores reflect actual system quality. Improvements require enhancing the underlying agents.

**Q: What's a good overall score?**
A: 75+  = good, 85+ = excellent, 50-75 = needs work

## Summary

The evaluation system provides:
- ✅ Automatic, objective assessment of simulation quality
- ✅ Multi-dimensional scoring across key evaluation criteria
- ✅ Historical tracking for trend analysis
- ✅ Performance monitoring
- ✅ Visual dashboard for quick insights
- ✅ CSV export for detailed analysis

Use it to continuously monitor and improve the courtroom AI system.
