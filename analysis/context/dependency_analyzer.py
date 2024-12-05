from typing import Dict, List, Optional
from datetime import datetime
import networkx as nx
from dataclasses import dataclass


@dataclass
class Dependency:
    """Represents an API dependency relationship."""
    source: str
    target: str
    criticality: float  # 0-1 scale
    latency_impact: float  # milliseconds
    error_rate: float  # 0-1 scale
    last_updated: datetime


class DependencyAnalyzer:
    """Analyzes API dependencies and their impact on monitoring."""

    def __init__(self):
        self.dependency_graph = nx.DiGraph()
        self.dependency_history: Dict[str, List[Dependency]] = {}

    def add_dependency(self, dependency: Dependency) -> None:
        """Add or update a dependency in the graph."""
        self.dependency_graph.add_edge(
            dependency.source,
            dependency.target,
            criticality=dependency.criticality,
            latency_impact=dependency.latency_impact,
            error_rate=dependency.error_rate,
            last_updated=dependency.last_updated
        )

        # Store in history
        key = f"{dependency.source}_{dependency.target}"
        if key not in self.dependency_history:
            self.dependency_history[key] = []
        self.dependency_history[key].append(dependency)

    def get_critical_path(self, api_name: str) -> List[str]:
        """Find the most critical dependency path for an API."""
        try:
            paths = nx.all_simple_paths(self.dependency_graph, api_name, None)
            critical_path = max(
                paths,
                key=lambda path: self._calculate_path_criticality(path)
            )
            return critical_path
        except (nx.NetworkXNoPath, ValueError):
            return [api_name]

    def get_impact_score(self, api_name: str) -> float:
        """Calculate the overall impact score for an API."""
        if api_name not in self.dependency_graph:
            return 0.0

        dependencies = list(self.dependency_graph.edges(api_name, data=True))
        if not dependencies:
            return 0.0

        # Calculate weighted impact
        total_impact = sum(
            self._calculate_dependency_impact(data)
            for _, _, data in dependencies
        )

        return min(total_impact / len(dependencies), 1.0)

    def get_dependent_apis(self, api_name: str) -> List[str]:
        """Get list of APIs that depend on the specified API."""
        try:
            return list(nx.ancestors(self.dependency_graph, api_name))
        except nx.NetworkXError:
            return []

    def analyze_cascading_impact(
            self,
            api_name: str,
            threshold: float = 0.5
    ) -> Dict[str, float]:
        """Analyze potential cascading impact of API issues."""
        impact_map = {}
        dependents = self.get_dependent_apis(api_name)

        for dependent in dependents:
            impact = self._calculate_cascading_impact(api_name, dependent)
            if impact >= threshold:
                impact_map[dependent] = impact

        return impact_map

    def get_health_impact_factor(self, api_name: str) -> float:
        """Calculate health impact factor for monitoring."""
        impact_score = self.get_impact_score(api_name)
        dependent_count = len(self.get_dependent_apis(api_name))

        # Consider both direct impact and number of dependents
        return min(
            (impact_score * 0.7 + (dependent_count / 10) * 0.3),
            1.0
        )

    def _calculate_dependency_impact(self, dependency_data: Dict) -> float:
        """Calculate impact score for a single dependency."""
        return (
                dependency_data['criticality'] * 0.4 +
                min(dependency_data['latency_impact'] / 1000, 1.0) * 0.3 +
                dependency_data['error_rate'] * 0.3
        )

    def _calculate_path_criticality(self, path: List[str]) -> float:
        """Calculate the criticality of a dependency path."""
        if len(path) < 2:
            return 0.0

        total_criticality = 0.0
        for i in range(len(path) - 1):
            edge_data = self.dependency_graph.get_edge_data(
                path[i],
                path[i + 1]
            )
            if edge_data:
                total_criticality += edge_data['criticality']

        return total_criticality / (len(path) - 1)

    def _calculate_cascading_impact(
            self,
            source: str,
            target: str
    ) -> float:
        """Calculate cascading impact between two APIs."""
        try:
            path = nx.shortest_path(
                self.dependency_graph,
                source=source,
                target=target,
                weight='criticality'
            )

            impact = 1.0
            for i in range(len(path) - 1):
                edge_data = self.dependency_graph.get_edge_data(
                    path[i],
                    path[i + 1]
                )
                if edge_data:
                    impact *= (1 - edge_data['criticality'])

            return 1 - impact
        except nx.NetworkXNoPath:
            return 0.0