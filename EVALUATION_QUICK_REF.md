# Quick Reference: Evaluation System

## 🚀 Quick Start

1. **Install dependencies** (if not already done):
   ```bash
   pip install plotly pandas
   ```

2. **Run the app**:
   ```bash
   streamlit run app.py
   ```

3. **Create cases** - Run simulations as normal

4. **View metrics** - Check sidebar: "📈 View Evaluation Metrics"

---

## 📊 Dashboard Sections

### Summary Statistics (Top Row)
- Total cases evaluated
- Average quality score (0-100)
- Average execution time
- Count of guilty verdicts

### Trends & Charts
1. **Quality Score Trend** - Overall quality over time
2. **Component Breakdown** - Average scores by component
3. **Verdict Distribution** - Pie chart of verdict types
4. **Execution Performance** - Time per component (stacked)
5. **Confidence Analysis** - Judge confidence calibration
6. **Recent Cases** - Table of last 10 cases

### Export
- **CSV Export** button - Save all metrics for analysis

---

## 📈 What Gets Measured

### Quality Scores (0-100)
- **Case Analysis** (20% weight)
  - Fact completeness
  - Entity recognition
  - Missing info detection

- **Legal Research** (25% weight)
  - Section relevance
  - Precedent quality
  - Evidence analysis

- **Arguments** (25% weight)
  - Prosecution quality
  - Defense quality
  - Balanced debate

- **Verdict** (30% weight)
  - Justification quality
  - Confidence calibration
  - Reasoning clarity

### Performance Metrics
- Case Manager: ___ seconds
- Legal Research: ___ seconds
- Debate: ___ seconds
- Judge: ___ seconds
- **Total**: ___ seconds

---

## 📂 Data Storage

```
evaluation/data/
├── metrics_history.jsonl    ← All metrics (append-only)
├── summary.json             ← Current stats
└── metrics_export.csv       ← From dashboard export
```

Each line in JSONL = one case evaluation

---

## 💻 Programmatic Access

### Python
```python
from evaluation.evaluator import SystemEvaluator
from evaluation.metrics import MetricsCollector

# Create instances
evaluator = SystemEvaluator()
collector = MetricsCollector()

# Get metrics
all_metrics = collector.get_all_metrics()
averages = collector.get_average_metrics()
recent = collector.get_recent_metrics(n=5)

# Export
collector.export_csv("my_analysis.csv")

# Get summary
summary = collector.get_summary()
print(f"Total cases: {summary['total_cases']}")
print(f"Avg score: {summary['average_scores']['overall_quality']}")
```

### Command Line
```bash
# View recent metrics
head -5 evaluation/data/metrics_history.jsonl

# View summary
cat evaluation/data/summary.json | python -m json.tool

# Count total cases
wc -l evaluation/data/metrics_history.jsonl
```

---

## 🎯 Benchmark Scores

| Range | Interpretation |
|-------|-----------------|
| 85-100 | ✅ Excellent (production-ready) |
| 70-84 | 👍 Good (acceptable) |
| 55-69 | ⚠️ Acceptable (needs work) |
| <55 | ❌ Poor (review required) |

---

## 🔍 Common Questions

**Q: Where can I see metrics?**  
A: Sidebar → Check "📈 View Evaluation Metrics"

**Q: Why did a case score low?**  
A: Check component scores. Look for weak areas (e.g., Legal Research 45% = limited precedents)

**Q: How do I export data?**  
A: Dashboard → "💾 Export Metrics as CSV" button

**Q: Where are metrics stored?**  
A: `evaluation/data/metrics_history.jsonl` (one JSON per line)

**Q: Can I access metrics programmatically?**  
A: Yes! See "Programmatic Access" section above

**Q: What's a good overall score?**  
A: 75+, ideally 80+. Below 60 needs investigation.

**Q: How often should I check metrics?**  
A: After every 5-10 cases, or whenever you notice something off.

**Q: Can I reset metrics?**  
A: Delete `evaluation/data/` folder (they're local-only)

---

## 🛠️ Integration Points

### In app.py
- **Sidebar toggle**: `show_metrics = st.checkbox(...)`
- **Evaluator**: `st.session_state.evaluator = SystemEvaluator()`
- **On completion**: `metrics = evaluator.evaluate_case(state, times)`
- **Timing**: Tracked in `st.session_state.node_times`

### Data Collection Flow
```
Simulation Streaming
    ↓ (track execution time)
Simulation Complete
    ↓ (call evaluator)
Auto-Evaluation
    ↓ (store metrics)
Update JSONL & Summary
    ↓ (display in dashboard)
Real-Time Analytics
```

---

## 📖 Full Documentation

See `EVALUATION.md` for:
- Detailed scoring methodology
- Complete metrics specification
- Example insights
- Advanced analysis techniques
- Best practices

---

## 🚀 Tips

1. **Monitor Trends**: Check dashboard every 5-10 cases
2. **Export Regularly**: Use CSV export for backup analysis
3. **Compare Components**: Identify consistently weak areas
4. **Track Confidence**: Watch calibration scores for judge reliability
5. **Profile Performance**: Check execution times for bottlenecks

---

## 📞 Support

Need help? Check these files:
- `EVALUATION.md` - Full documentation
- `EVALUATION_SETUP.md` - Detailed setup guide
- `evaluation/*.py` - Source code (well-commented)

---

**Happy analyzing!** 📊✨
