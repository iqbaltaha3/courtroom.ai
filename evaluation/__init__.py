"""Evaluation module for courtroom AI system."""

from .evaluator import SystemEvaluator
from .metrics import MetricsCollector, EvaluationMetrics

__all__ = ["SystemEvaluator", "MetricsCollector", "EvaluationMetrics"]
