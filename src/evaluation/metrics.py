"""Metrics storage and tracking for evaluation analytics."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class EvaluationMetrics:
    """Container for all evaluation metrics from a single simulation."""
    
    # Timestamps
    timestamp: str
    case_id: str
    
    # Case Analysis Quality (0-100)
    case_extraction_completeness: float
    fact_accuracy: float
    entity_recognition_accuracy: float
    
    # Legal Research Quality (0-100)
    applicable_sections_relevance: float
    precedent_relevance: float
    legal_research_completeness: float
    
    # Argument Quality (0-100)
    prosecution_coherence: float
    defense_coherence: float
    argument_strength: float
    
    # Verdict Quality (0-100)
    verdict_justification_quality: float
    confidence_calibration: float  # How well confidence score matches verdict clarity
    reasoning_clarity: float
    
    # System Performance
    total_execution_time: float  # seconds
    case_manager_time: float
    legal_research_time: float
    debate_time: float
    judge_time: float
    
    # Consistency & Patterns
    consistency_score: float  # 0-100, compared to similar cases
    precedent_adherence: float  # Does verdict align with cited precedents?
    
    # Overall
    overall_quality_score: float  # Weighted average of all scores
    
    # Metadata
    accused: str
    verdict: str
    confidence: int
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    def get_quality_summary(self) -> Dict[str, float]:
        """Get summary of quality scores."""
        return {
            "case_analysis": self.case_extraction_completeness,
            "legal_research": self.legal_research_completeness,
            "argument_quality": self.argument_strength,
            "verdict_quality": self.verdict_justification_quality,
            "system_coherence": self.confidence_calibration,
            "overall": self.overall_quality_score,
        }


class MetricsCollector:
    """Collects and stores evaluation metrics."""
    
    def __init__(self, storage_dir: str = "evaluation/data"):
        """Initialize metrics collector.
        
        Args:
            storage_dir: Directory to store metrics JSON files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.metrics_file = self.storage_dir / "metrics_history.jsonl"
        self.summary_file = self.storage_dir / "summary.json"
    
    def record_metrics(self, metrics: EvaluationMetrics) -> None:
        """Record a single evaluation metric set.
        
        Args:
            metrics: EvaluationMetrics object
        """
        # Append to JSONL file for historical tracking
        with open(self.metrics_file, "a") as f:
            f.write(json.dumps(metrics.to_dict()) + "\n")
        
        # Update summary
        self._update_summary()
    
    def get_all_metrics(self) -> List[EvaluationMetrics]:
        """Load all recorded metrics."""
        if not self.metrics_file.exists():
            return []
        
        metrics = []
        with open(self.metrics_file, "r") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    metrics.append(EvaluationMetrics(**data))
        return metrics
    
    def get_metrics_by_verdict(self, verdict: str) -> List[EvaluationMetrics]:
        """Get metrics filtered by verdict type."""
        all_metrics = self.get_all_metrics()
        return [m for m in all_metrics if m.verdict == verdict]
    
    def get_recent_metrics(self, n: int = 10) -> List[EvaluationMetrics]:
        """Get last N metric records."""
        all_metrics = self.get_all_metrics()
        return all_metrics[-n:]
    
    def get_average_metrics(self, metrics_list: Optional[List[EvaluationMetrics]] = None) -> Dict[str, float]:
        """Calculate average metrics.
        
        Args:
            metrics_list: List of metrics to average. If None, uses all metrics.
        
        Returns:
            Dictionary with averaged scores
        """
        if metrics_list is None:
            metrics_list = self.get_all_metrics()
        
        if not metrics_list:
            return {}
        
        scores = {
            "case_extraction": [],
            "fact_accuracy": [],
            "legal_research": [],
            "prosecution_coherence": [],
            "defense_coherence": [],
            "verdict_quality": [],
            "confidence_calibration": [],
            "reasoning_clarity": [],
            "overall_quality": [],
        }
        
        for m in metrics_list:
            scores["case_extraction"].append(m.case_extraction_completeness)
            scores["fact_accuracy"].append(m.fact_accuracy)
            scores["legal_research"].append(m.legal_research_completeness)
            scores["prosecution_coherence"].append(m.prosecution_coherence)
            scores["defense_coherence"].append(m.defense_coherence)
            scores["verdict_quality"].append(m.verdict_justification_quality)
            scores["confidence_calibration"].append(m.confidence_calibration)
            scores["reasoning_clarity"].append(m.reasoning_clarity)
            scores["overall_quality"].append(m.overall_quality_score)
        
        return {
            key: sum(values) / len(values) if values else 0
            for key, values in scores.items()
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get current summary statistics."""
        if self.summary_file.exists():
            with open(self.summary_file, "r") as f:
                return json.load(f)
        return {}
    
    def _update_summary(self) -> None:
        """Update the summary file with current statistics."""
        all_metrics = self.get_all_metrics()
        
        if not all_metrics:
            return
        
        avg_metrics = self.get_average_metrics(all_metrics)
        
        guilty_count = len(self.get_metrics_by_verdict("Guilty"))
        not_guilty_count = len(self.get_metrics_by_verdict("Not Guilty"))
        partial_count = len(self.get_metrics_by_verdict("Partially Liable"))
        
        summary = {
            "total_cases": len(all_metrics),
            "last_updated": datetime.now().isoformat(),
            "verdict_distribution": {
                "Guilty": guilty_count,
                "Not Guilty": not_guilty_count,
                "Partially Liable": partial_count,
            },
            "average_scores": avg_metrics,
            "latest_case": {
                "timestamp": all_metrics[-1].timestamp,
                "case_id": all_metrics[-1].case_id,
                "accused": all_metrics[-1].accused,
                "verdict": all_metrics[-1].verdict,
                "overall_quality": all_metrics[-1].overall_quality_score,
            }
        }
        
        with open(self.summary_file, "w") as f:
            json.dump(summary, f, indent=2)
    
    def export_csv(self, output_path: str = "evaluation/metrics_export.csv") -> None:
        """Export all metrics to CSV for external analysis.
        
        Args:
            output_path: Path to write CSV file
        """
        import csv
        
        all_metrics = self.get_all_metrics()
        if not all_metrics:
            return
        
        fieldnames = list(asdict(all_metrics[0]).keys())
        
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for m in all_metrics:
                writer.writerow(m.to_dict())
