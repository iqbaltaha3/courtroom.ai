"""Core evaluation logic for courtroom AI system."""

import time
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from ..agents.schemas import CaseIntake, LegalResearch, JudgeVerdict
from .metrics import EvaluationMetrics, MetricsCollector


class SystemEvaluator:
    """Evaluates various aspects of the courtroom AI system."""
    
    def __init__(self, metrics_collector: Optional[MetricsCollector] = None):
        """Initialize evaluator.
        
        Args:
            metrics_collector: MetricsCollector instance. Creates new one if None.
        """
        self.metrics_collector = metrics_collector or MetricsCollector()
        self.case_id = str(uuid.uuid4())[:8]
    
    def evaluate_case(self, 
                      state: Dict[str, Any],
                      execution_times: Optional[Dict[str, float]] = None) -> EvaluationMetrics:
        """Evaluate a complete case simulation.
        
        Args:
            state: The case state dict from the graph execution
            execution_times: Dict of {node_name: time_in_seconds}
        
        Returns:
            EvaluationMetrics object
        """
        execution_times = execution_times or {}
        
        # Evaluate each component
        case_quality = self._evaluate_case_analysis(state)
        legal_quality = self._evaluate_legal_research(state)
        argument_quality = self._evaluate_arguments(state)
        verdict_quality = self._evaluate_verdict(state)
        
        # Get timing info
        total_time = sum(execution_times.values())
        case_manager_time = execution_times.get("case_manager", 0)
        legal_research_time = execution_times.get("legal_research", 0)
        debate_time = sum(execution_times.get(k, 0) for k in ["prosecutor_r1", "defense_r1", "prosecutor_r2", "defense_r2"])
        judge_time = execution_times.get("judge", 0)
        
        # Calculate overall quality score
        overall_score = self._calculate_overall_score(
            case_quality,
            legal_quality,
            argument_quality,
            verdict_quality
        )
        
        # Extract case info
        case_intake = state.get("case_intake") or {}
        judge_verdict = state.get("judge_verdict") or {}
        
        metrics = EvaluationMetrics(
            timestamp=datetime.now().isoformat(),
            case_id=self.case_id,
            
            # Case Analysis
            case_extraction_completeness=case_quality["completeness"],
            fact_accuracy=case_quality["accuracy"],
            entity_recognition_accuracy=case_quality["entity_accuracy"],
            
            # Legal Research
            applicable_sections_relevance=legal_quality["sections_relevance"],
            precedent_relevance=legal_quality["precedent_relevance"],
            legal_research_completeness=legal_quality["completeness"],
            
            # Arguments
            prosecution_coherence=argument_quality["prosecution_coherence"],
            defense_coherence=argument_quality["defense_coherence"],
            argument_strength=argument_quality["strength"],
            
            # Verdict
            verdict_justification_quality=verdict_quality["justification"],
            confidence_calibration=verdict_quality["confidence_calibration"],
            reasoning_clarity=verdict_quality["reasoning_clarity"],
            
            # Performance
            total_execution_time=total_time,
            case_manager_time=case_manager_time,
            legal_research_time=legal_research_time,
            debate_time=debate_time,
            judge_time=judge_time,
            
            # Consistency
            consistency_score=self._evaluate_consistency(state),
            precedent_adherence=verdict_quality["precedent_adherence"],
            
            # Overall
            overall_quality_score=overall_score,
            
            # Metadata
            accused=case_intake.get("accused", "Unknown"),
            verdict=judge_verdict.get("verdict", "Unknown"),
            confidence=judge_verdict.get("confidence", 0),
        )
        
        # Store metrics
        self.metrics_collector.record_metrics(metrics)
        
        return metrics
    
    def _evaluate_case_analysis(self, state: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate case intake and analysis quality.
        
        Returns:
            Dict with completeness, accuracy, entity_accuracy scores (0-100)
        """
        case_intake = state.get("case_intake")
        
        if not case_intake:
            return {
                "completeness": 30,
                "accuracy": 40,
                "entity_accuracy": 35,
            }
        
        completeness = 0
        entity_count = 0
        missing_info = len(case_intake.get("missing_information", []))
        
        # Check field completeness
        required_fields = ["accused", "victim", "allegation", "facts"]
        for field in required_fields:
            if case_intake.get(field):
                completeness += 25
        
        # Bonus if facts are detailed
        facts = case_intake.get("facts", [])
        if len(facts) >= 5:
            completeness = min(100, completeness + 10)
        
        # Entity accuracy based on non-empty entities
        if case_intake.get("accused") and case_intake.get("accused") != "Unknown":
            entity_count += 1
        if case_intake.get("victim") and case_intake.get("victim") != "Unknown":
            entity_count += 1
        
        entity_accuracy = min(100, (entity_count / 2) * 100)
        
        # Accuracy penalized by missing info
        accuracy = max(30, 100 - (missing_info * 15))
        
        return {
            "completeness": min(100, completeness),
            "accuracy": accuracy,
            "entity_accuracy": entity_accuracy,
        }
    
    def _evaluate_legal_research(self, state: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate legal research quality.
        
        Returns:
            Dict with sections_relevance, precedent_relevance, completeness (0-100)
        """
        legal_research = state.get("legal_research")
        
        if not legal_research:
            return {
                "sections_relevance": 0,
                "precedent_relevance": 0,
                "completeness": 0,
            }
        
        sections = legal_research.get("applicable_sections", [])
        precedents = legal_research.get("precedents", [])
        evidentiary_notes = legal_research.get("evidentiary_notes", [])
        
        # Sections relevance (more sections = higher score, up to 100)
        sections_relevance = min(100, len(sections) * 20)
        
        # Precedents relevance (precedents are important in legal research)
        precedent_relevance = min(100, len(precedents) * 25)
        
        # Completeness based on all components
        completeness = min(
            100,
            (len(sections) * 15) + (len(precedents) * 25) + (len(evidentiary_notes) * 10)
        )
        
        return {
            "sections_relevance": sections_relevance,
            "precedent_relevance": precedent_relevance,
            "completeness": completeness,
        }
    
    def _evaluate_arguments(self, state: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate quality of prosecution and defense arguments.
        
        Returns:
            Dict with prosecution_coherence, defense_coherence, strength (0-100)
        """
        pros_r1 = state.get("pros_r1", "") or ""
        pros_r2 = state.get("pros_r2", "") or ""
        def_r1 = state.get("def_r1", "") or ""
        def_r2 = state.get("def_r2", "") or ""
        
        # Simple heuristic: longer, more detailed arguments are typically better
        pros_length = len(pros_r1) + len(pros_r2)
        def_length = len(def_r1) + len(def_r2)
        
        # Normalize to 0-100 (assuming good arguments are 1000+ chars each)
        prosecution_coherence = min(100, (pros_length / 2000) * 100)
        defense_coherence = min(100, (def_length / 2000) * 100)
        
        # Balanced strength when both sides present substantial arguments
        strength = (prosecution_coherence + defense_coherence) / 2
        
        return {
            "prosecution_coherence": prosecution_coherence,
            "defense_coherence": defense_coherence,
            "strength": strength,
        }
    
    def _evaluate_verdict(self, state: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate quality of judge verdict and reasoning.
        
        Returns:
            Dict with justification, confidence_calibration, reasoning_clarity, precedent_adherence (0-100)
        """
        judge_verdict = state.get("judge_verdict")
        legal_research = state.get("legal_research")
        
        if not judge_verdict:
            return {
                "justification": 0,
                "confidence_calibration": 0,
                "reasoning_clarity": 0,
                "precedent_adherence": 0,
            }
        
        reasoning = judge_verdict.get("reasoning", "") or ""
        findings = judge_verdict.get("findings", "") or ""
        confidence = judge_verdict.get("confidence", 50)
        sections_applied = judge_verdict.get("sections_applied", [])
        
        # Justification: based on reasoning length and detail
        justification = min(100, (len(reasoning) / 500) * 100)
        
        # Confidence calibration: verdicts with mid-range confidence are often more nuanced
        # Extreme confidence (0-20, 80-100) suggests polarized reasoning
        confidence_calibration = 100 - abs(confidence - 50)
        
        # Reasoning clarity: presence of findings and detailed reasoning
        reasoning_clarity = min(100, ((len(findings) + len(reasoning)) / 600) * 100)
        
        # Precedent adherence: check if cited sections are from legal research
        precedent_adherence = 50  # baseline
        if legal_research and sections_applied:
            legal_sections = {s.get("section", "") for s in legal_research.get("applicable_sections", [])}
            applied_sections = set(sections_applied)
            
            if applied_sections and legal_sections:
                overlap = len(applied_sections & legal_sections)
                precedent_adherence = min(100, (overlap / len(applied_sections)) * 100)
        
        return {
            "justification": justification,
            "confidence_calibration": confidence_calibration,
            "reasoning_clarity": reasoning_clarity,
            "precedent_adherence": precedent_adherence,
        }
    
    def _evaluate_consistency(self, state: Dict[str, Any]) -> float:
        """Evaluate consistency of verdict with arguments presented.
        
        Returns:
            Consistency score (0-100)
        """
        # Simple heuristic: check if judge addressed both sides
        judge_verdict = state.get("judge_verdict") or {}
        
        prosecution_assessment = judge_verdict.get("prosecution_assessment", "") or ""
        defense_assessment = judge_verdict.get("defense_assessment", "") or ""
        
        # Both assessments present = more balanced consideration
        both_addressed = (len(prosecution_assessment) > 50 and len(defense_assessment) > 50)
        
        return 80 if both_addressed else 60
    
    def _calculate_overall_score(self,
                                 case_quality: Dict[str, float],
                                 legal_quality: Dict[str, float],
                                 argument_quality: Dict[str, float],
                                 verdict_quality: Dict[str, float]) -> float:
        """Calculate weighted overall quality score.
        
        Returns:
            Overall score (0-100)
        """
        weights = {
            "case": 0.20,
            "legal": 0.25,
            "arguments": 0.25,
            "verdict": 0.30,
        }
        
        case_avg = sum(case_quality.values()) / len(case_quality)
        legal_avg = sum(legal_quality.values()) / len(legal_quality)
        argument_avg = sum(argument_quality.values()) / len(argument_quality)
        verdict_avg = sum(verdict_quality.values()) / len(verdict_quality)
        
        overall = (
            case_avg * weights["case"] +
            legal_avg * weights["legal"] +
            argument_avg * weights["arguments"] +
            verdict_avg * weights["verdict"]
        )
        
        return min(100, max(0, overall))
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all recorded metrics."""
        return self.metrics_collector.get_summary()
    
    def get_recent_cases(self, n: int = 5) -> list:
        """Get recent case evaluations."""
        return self.metrics_collector.get_recent_metrics(n)
