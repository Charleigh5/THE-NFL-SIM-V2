#!/usr/bin/env python3
"""
AI Research Service
===================
Provides AI-powered research for implementation tasks using Context7 MCP patterns.

Context7 Best Practices:
- Async service layer
- Clear type definitions via dataclasses
- Dependency injection pattern
"""

import logging
import re
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class TaskComplexity(str, Enum):
    """Estimated complexity level for a task."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class ResearchResult:
    """Result of AI research for a task."""
    summary: str
    recommended_approach: str
    code_examples: list[str] = field(default_factory=list)
    complexity: TaskComplexity = TaskComplexity.MEDIUM
    sources: list[str] = field(default_factory=list)
    related_docs: list[str] = field(default_factory=list)


class AIResearchService:
    """
    Service for researching implementation best practices.

    In a full implementation, this would integrate with Context7 MCP.
    Currently provides pattern-based research templates.
    """

    # Common patterns and their research templates
    RESEARCH_PATTERNS = {
        r"button|click|hover": {
            "summary": "Button interactions should follow accessibility best practices.",
            "approach": "Use semantic HTML buttons with proper ARIA labels. Implement hover states with CSS transitions for smooth UX.",
            "complexity": TaskComplexity.LOW,
            "examples": [
                ".button { transition: all 0.2s ease; }\n.button:hover { transform: scale(1.02); }",
            ],
            "sources": ["https://react.dev/reference/react-dom/components/button"]
        },
        r"modal|dialog|popup": {
            "summary": "Modals require focus trapping and keyboard accessibility.",
            "approach": "Use createPortal for rendering outside DOM hierarchy. Implement focus trap and ESC key handling.",
            "complexity": TaskComplexity.MEDIUM,
            "examples": [
                "import { createPortal } from 'react-dom';\nreturn createPortal(<Modal />, document.body);",
            ],
            "sources": ["https://react.dev/reference/react-dom/createPortal"]
        },
        r"form|input|validation": {
            "summary": "Form handling with controlled components and validation.",
            "approach": "Use useState for controlled inputs. Implement validation on blur and submit events.",
            "complexity": TaskComplexity.MEDIUM,
            "examples": [
                "const [value, setValue] = useState('');\nconst handleChange = (e) => setValue(e.target.value);",
            ],
            "sources": ["https://react.dev/learn/managing-state"]
        },
        r"api|fetch|endpoint": {
            "summary": "API integration with proper error handling and loading states.",
            "approach": "Use async/await with try-catch. Implement loading and error states.",
            "complexity": TaskComplexity.MEDIUM,
            "examples": [
                "@router.post('/endpoint')\nasync def handler(request: Request):\n    return {'success': True}",
            ],
            "sources": ["https://fastapi.tiangolo.com/tutorial/first-steps/"]
        },
        r"animation|transition|motion": {
            "summary": "CSS transitions and animations for smooth visual effects.",
            "approach": "Use CSS transitions for simple state changes. CSS animations for complex sequences.",
            "complexity": TaskComplexity.LOW,
            "examples": [
                "@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }\n.element { animation: fadeIn 0.3s ease; }",
            ],
            "sources": ["https://developer.mozilla.org/en-US/docs/Web/CSS/animation"]
        },
        r"layout|grid|flex": {
            "summary": "Modern CSS layout with Flexbox and Grid.",
            "approach": "Use Flexbox for 1D layouts, Grid for 2D layouts. Combine for complex designs.",
            "complexity": TaskComplexity.LOW,
            "examples": [
                ".container { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }",
            ],
            "sources": ["https://css-tricks.com/snippets/css/complete-guide-grid/"]
        },
        r"table|list|data": {
            "summary": "Data display with virtualization for large datasets.",
            "approach": "Use semantic table elements. Consider virtual scrolling for large lists.",
            "complexity": TaskComplexity.MEDIUM,
            "examples": [
                "import { FixedSizeList } from 'react-window';\n<FixedSizeList height={400} itemCount={1000} itemSize={35}>",
            ],
            "sources": ["https://react.dev/learn/escape-hatches"]
        },
    }

    DEFAULT_RESEARCH = {
        "summary": "General UI improvement task.",
        "approach": "Follow React best practices with proper component structure, state management, and accessibility.",
        "complexity": TaskComplexity.MEDIUM,
        "examples": [],
        "sources": ["https://react.dev/learn"]
    }

    async def research_task(self, description: str) -> ResearchResult:
        """
        Research implementation best practices for a given task description.

        Args:
            description: The user's task description

        Returns:
            ResearchResult with summary, approach, examples, and complexity
        """
        logger.info(f"Researching task: {description[:50]}...")

        # Match against known patterns
        description_lower = description.lower()

        for pattern, research in self.RESEARCH_PATTERNS.items():
            if re.search(pattern, description_lower):
                return ResearchResult(
                    summary=research["summary"],
                    recommended_approach=research["approach"],
                    code_examples=research.get("examples", []),
                    complexity=research["complexity"],
                    sources=research.get("sources", []),
                    related_docs=[]
                )

        # Default fallback
        return ResearchResult(
            summary=self.DEFAULT_RESEARCH["summary"],
            recommended_approach=self.DEFAULT_RESEARCH["approach"],
            code_examples=self.DEFAULT_RESEARCH["examples"],
            complexity=self.DEFAULT_RESEARCH["complexity"],
            sources=self.DEFAULT_RESEARCH["sources"],
            related_docs=[]
        )

    def estimate_complexity(self, description: str) -> TaskComplexity:
        """
        Estimate task complexity based on description analysis.
        """
        description_lower = description.lower()

        # High complexity indicators
        high_indicators = ["integration", "migration", "refactor", "architecture", "security"]
        if any(ind in description_lower for ind in high_indicators):
            return TaskComplexity.HIGH

        # Low complexity indicators
        low_indicators = ["color", "padding", "margin", "font", "spacing", "typo"]
        if any(ind in description_lower for ind in low_indicators):
            return TaskComplexity.LOW

        return TaskComplexity.MEDIUM


# Global instance
ai_research_service = AIResearchService()
