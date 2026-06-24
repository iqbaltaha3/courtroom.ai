"""Streamlit dashboard for evaluation metrics visualization."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List
from .metrics import MetricsCollector, EvaluationMetrics


def show_evaluation_dashboard():
    """Display evaluation metrics dashboard in Streamlit."""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #111116 0%, #0d0d12 100%); 
                padding: 20px; border-radius: 8px; border-left: 4px solid #d4af37; margin-bottom: 20px;">
        <h2 style="color: #ffffff; margin: 0;">📊 System Evaluation Dashboard</h2>
        <p style="color: #a0a0a0; margin: 5px 0 0 0;">AI Courtroom Performance Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    collector = MetricsCollector()
    all_metrics = collector.get_all_metrics()
    
    if not all_metrics:
        st.info("📈 No evaluation data yet. Run simulations to start collecting metrics.")
        return
    
    # Summary statistics
    st.markdown("### 📈 Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cases", len(all_metrics))
    
    with col2:
        avg_quality = collector.get_average_metrics(all_metrics).get("overall_quality", 0)
        st.metric("Avg Quality Score", f"{avg_quality:.1f}%")
    
    with col3:
        avg_time = sum(m.total_execution_time for m in all_metrics) / len(all_metrics)
        st.metric("Avg Execution Time", f"{avg_time:.1f}s")
    
    with col4:
        guilty_count = len([m for m in all_metrics if m.verdict == "Guilty"])
        st.metric("Guilty Verdicts", guilty_count)
    
    # Quality Score Trend
    st.markdown("### 📊 Quality Score Trend")
    
    df_quality = pd.DataFrame({
        "Case #": range(1, len(all_metrics) + 1),
        "Overall Quality": [m.overall_quality_score for m in all_metrics],
        "Case Analysis": [m.case_extraction_completeness for m in all_metrics],
        "Legal Research": [m.legal_research_completeness for m in all_metrics],
        "Verdict Quality": [m.verdict_justification_quality for m in all_metrics],
    })
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df_quality["Case #"],
        y=df_quality["Overall Quality"],
        mode='lines+markers',
        name='Overall Quality',
        line=dict(color='#d4af37', width=2),
        marker=dict(size=6)
    ))
    fig_trend.update_layout(
        title="Quality Score Over Time",
        xaxis_title="Case Number",
        yaxis_title="Score (0-100)",
        hovermode='x unified',
        template='plotly_dark',
        height=400
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Component Quality Breakdown
    st.markdown("### 🔍 Component Quality Breakdown")
    
    avg_scores = collector.get_average_metrics(all_metrics)
    
    fig_components = go.Figure(data=[
        go.Bar(
            x=list(avg_scores.keys()),
            y=list(avg_scores.values()),
            marker_color='#d4af37',
            text=[f"{v:.1f}%" for v in avg_scores.values()],
            textposition='auto',
        )
    ])
    fig_components.update_layout(
        title="Average Scores by Component",
        yaxis_title="Score (0-100)",
        template='plotly_dark',
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_components, use_container_width=True)
    
    # Verdict Distribution
    st.markdown("### ⚖️ Verdict Distribution")
    
    verdict_counts = {}
    for m in all_metrics:
        verdict_counts[m.verdict] = verdict_counts.get(m.verdict, 0) + 1
    
    fig_verdicts = go.Figure(data=[
        go.Pie(
            labels=list(verdict_counts.keys()),
            values=list(verdict_counts.values()),
            marker=dict(colors=['#d4af37', '#888888', '#c9a84c'])
        )
    ])
    fig_verdicts.update_layout(
        title="Verdict Distribution",
        template='plotly_dark',
        height=400
    )
    st.plotly_chart(fig_verdicts, use_container_width=True)
    
    # Performance Timeline
    st.markdown("### ⏱️ Execution Performance")
    
    df_perf = pd.DataFrame({
        "Case": range(1, len(all_metrics) + 1),
        "Case Manager": [m.case_manager_time for m in all_metrics],
        "Legal Research": [m.legal_research_time for m in all_metrics],
        "Debate": [m.debate_time for m in all_metrics],
        "Judge": [m.judge_time for m in all_metrics],
    })
    
    fig_perf = go.Figure()
    for col in ["Case Manager", "Legal Research", "Debate", "Judge"]:
        fig_perf.add_trace(go.Scatter(
            x=df_perf["Case"],
            y=df_perf[col],
            mode='lines',
            name=col,
            stackgroup='one'
        ))
    
    fig_perf.update_layout(
        title="Execution Time by Component",
        xaxis_title="Case Number",
        yaxis_title="Time (seconds)",
        template='plotly_dark',
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_perf, use_container_width=True)
    
    # Recent Cases Detail
    st.markdown("### 📋 Recent Cases")
    
    recent = collector.get_recent_metrics(10)
    recent_data = []
    
    for m in reversed(recent):
        recent_data.append({
            "Case ID": m.case_id[:8],
            "Timestamp": datetime.fromisoformat(m.timestamp).strftime("%Y-%m-%d %H:%M"),
            "Accused": m.accused[:20],
            "Verdict": m.verdict,
            "Confidence": f"{m.confidence}%",
            "Quality": f"{m.overall_quality_score:.1f}",
            "Time": f"{m.total_execution_time:.1f}s"
        })
    
    st.dataframe(pd.DataFrame(recent_data), use_container_width=True)
    
    # Confidence Calibration Analysis
    st.markdown("### 🎯 Confidence Calibration")
    
    df_conf = pd.DataFrame({
        "Case": range(1, len(all_metrics) + 1),
        "Judge Confidence": [m.confidence for m in all_metrics],
        "Calibration Score": [m.confidence_calibration for m in all_metrics],
    })
    
    fig_conf = go.Figure()
    fig_conf.add_trace(go.Scatter(
        x=df_conf["Case"],
        y=df_conf["Judge Confidence"],
        mode='lines+markers',
        name='Judge Confidence',
        line=dict(color='#d4af37')
    ))
    fig_conf.add_trace(go.Scatter(
        x=df_conf["Case"],
        y=df_conf["Calibration Score"],
        mode='lines+markers',
        name='Calibration Quality',
        line=dict(color='#888888')
    ))
    fig_conf.update_layout(
        title="Confidence vs Calibration Quality",
        xaxis_title="Case Number",
        yaxis_title="Score",
        template='plotly_dark',
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_conf, use_container_width=True)
    
    # Export options
    st.markdown("### 💾 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Metrics as CSV"):
            collector.export_csv()
            st.success("Metrics exported to `evaluation/metrics_export.csv`")
    
    with col2:
        if st.button("🔄 Refresh Dashboard"):
            st.rerun()
