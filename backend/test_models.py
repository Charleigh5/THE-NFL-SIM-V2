"""
Vertex AI Model Performance Testing Script

This script tests different Gemini models to measure:
- Latency (response time)
- Token usage (cost tracking)
- Output quality

Usage:
    python test_models.py
"""

import time
import os
from typing import Dict, List
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from google.cloud import aiplatform

# Initialize Vertex AI
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)


class ModelTester:
    """Test and compare Vertex AI model performance."""

    def __init__(self):
        self.models = {
            "flash-002": "gemini-1.5-flash-002",
            "pro-002": "gemini-1.5-pro-002",
            "flash-exp": "gemini-2.0-flash-exp",
        }
        self.results = []

    def test_commentary_generation(self, model_name: str) -> Dict:
        """Test model for play-by-play commentary generation."""
        model = GenerativeModel(self.models[model_name])

        prompt = """Generate exciting play-by-play commentary for this play:

        Play: Run, RB Harris rushes up the middle for 8 yards. Tackled by LB #52 Johnson.
        Game Context: 3rd Quarter, Score 14-10, 2nd and 2 from the opponent's 35-yard line.

        Make it sound like a TV announcer. Keep it under 50 words."""

        start_time = time.time()

        response = model.generate_content(
            prompt,
            generation_config=GenerationConfig(
                max_output_tokens=100,
                temperature=0.7,
            )
        )

        latency = time.time() - start_time

        return {
            "model": model_name,
            "task": "commentary",
            "latency_ms": round(latency * 1000, 2),
            "output": response.text,
            "input_tokens": response.usage_metadata.prompt_token_count,
            "output_tokens": response.usage_metadata.candidates_token_count,
        }

    def test_gm_trade_logic(self, model_name: str) -> Dict:
        """Test model for complex GM trade evaluation."""
        model = GenerativeModel(self.models[model_name])

        prompt = """You are the GM of the Dallas Cowboys. Evaluate this trade offer:

        RECEIVE: QB Patrick Mahomes (Overall: 99, Age: 29, Contract: 3 years, $45M/year)
        GIVE: QB Dak Prescott (Overall: 88, Age: 31, Contract: 2 years, $40M/year) + 2026 1st Round Pick

        Team Context:
        - Current Record: 8-4, playoff contender
        - Cap Space: $15M
        - Needs: Edge Rusher, Secondary depth

        Respond in JSON format with:
        {
          "accept": boolean,
          "confidence": 0-100,
          "reasoning": "2-3 sentences",
          "counterOffer": "suggested alternative or null"
        }"""

        start_time = time.time()

        response = model.generate_content(
            prompt,
            generation_config=GenerationConfig(
                response_mime_type="application/json",
                temperature=0.3,
            )
        )

        latency = time.time() - start_time

        return {
            "model": model_name,
            "task": "gm_logic",
            "latency_ms": round(latency * 1000, 2),
            "output": response.text,
            "input_tokens": response.usage_metadata.prompt_token_count,
            "output_tokens": response.usage_metadata.candidates_token_count,
        }

    def calculate_cost(self, result: Dict) -> float:
        """Calculate estimated cost for the request."""
        model = result["model"]

        # Pricing per 1M tokens (USD) - as of Dec 2024
        pricing = {
            "flash-002": {"input": 0.0375, "output": 0.15},
            "pro-002": {"input": 1.25, "output": 5.0},
            "flash-exp": {"input": 0.0, "output": 0.0},  # Free during preview
        }

        input_cost = (result["input_tokens"] / 1_000_000) * pricing[model]["input"]
        output_cost = (result["output_tokens"] / 1_000_000) * pricing[model]["output"]

        return round(input_cost + output_cost, 6)

    def run_all_tests(self):
        """Run all tests for all models."""
        print("=" * 80)
        print("VERTEX AI MODEL PERFORMANCE TEST")
        print("=" * 80)
        print()

        for model_name in self.models.keys():
            print(f"Testing {model_name}...")

            # Test commentary
            commentary_result = self.test_commentary_generation(model_name)
            commentary_result["cost_usd"] = self.calculate_cost(commentary_result)
            self.results.append(commentary_result)

            # Test GM logic
            gm_result = self.test_gm_trade_logic(model_name)
            gm_result["cost_usd"] = self.calculate_cost(gm_result)
            self.results.append(gm_result)

            print(f"  ✓ {model_name} complete\n")

        self.print_results()

    def print_results(self):
        """Print formatted test results."""
        print("\n" + "=" * 80)
        print("RESULTS SUMMARY")
        print("=" * 80)

        # Group by task
        for task in ["commentary", "gm_logic"]:
            print(f"\n{task.upper().replace('_', ' ')}:")
            print("-" * 80)
            print(f"{'Model':<15} {'Latency (ms)':<15} {'Tokens (in/out)':<20} {'Cost ($)':<10}")
            print("-" * 80)

            task_results = [r for r in self.results if r["task"] == task]
            for result in task_results:
                tokens = f"{result['input_tokens']}/{result['output_tokens']}"
                print(
                    f"{result['model']:<15} "
                    f"{result['latency_ms']:<15} "
                    f"{tokens:<20} "
                    f"{result['cost_usd']:<10.6f}"
                )

        print("\n" + "=" * 80)
        print("RECOMMENDATIONS:")
        print("=" * 80)

        # Find fastest and cheapest for each task
        commentary_models = [r for r in self.results if r["task"] == "commentary"]
        fastest_commentary = min(commentary_models, key=lambda x: x["latency_ms"])
        cheapest_commentary = min(commentary_models, key=lambda x: x["cost_usd"])

        gm_models = [r for r in self.results if r["task"] == "gm_logic"]
        fastest_gm = min(gm_models, key=lambda x: x["latency_ms"])
        cheapest_gm = min(gm_models, key=lambda x: x["cost_usd"])

        print(f"✓ Commentary (High Volume): Use '{cheapest_commentary['model']}' (${cheapest_commentary['cost_usd']:.6f}/call)")
        print(f"✓ GM Logic (Complex): Use '{fastest_gm['model']}' for best reasoning")
        print()


if __name__ == "__main__":
    tester = ModelTester()
    tester.run_all_tests()
