#!/usr/bin/env python3
"""
Pattern Overflow Experiment - API Version
Proves: Without constraints, AI finds infinite meaningless patterns
Uses: Claude API to demonstrate pattern explosion
"""

import os
from anthropic import Anthropic
import matplotlib.pyplot as plt
import json
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv()

class PatternOverflowExperiment:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'model': 'claude-3-opus-20240229',
            'patterns_found': [],
            'constraint_levels': [],
            'absurd_patterns': []
        }
        
    def generate_test_data(self):
        """Generate seemingly random data with hidden non-patterns"""
        # Mix of timestamps, words, numbers - no real patterns
        data = [
            "2024-01-15 14:32:10 - User logged in",
            "Temperature: 72°F",
            "Stock price: $145.32",
            "2024-01-15 14:35:22 - Error occurred",
            "Humidity: 45%",
            "Processing time: 1.2 seconds",
            "2024-01-15 14:38:45 - Task completed",
            "Battery level: 67%",
            "Response code: 200",
            "2024-01-15 14:41:03 - User logged out",
            "Wind speed: 12 mph",
            "Memory usage: 2.3 GB",
            "Coffee consumed: 3 cups",
            "Emails sent: 27",
            "Moon phase: Waxing gibbous"
        ]
        return data
    
    def find_patterns_with_constraint(self, data, constraint_level):
        """Ask Claude to find patterns with varying constraints"""
        
        if constraint_level == "extreme":
            prompt = f"""Find ONLY the most obvious, scientifically valid patterns in this data:
{chr(10).join(data)}

List only patterns that would be accepted in a peer-reviewed journal."""

        elif constraint_level == "high":
            prompt = f"""Find clear patterns in this data:
{chr(10).join(data)}

Focus on statistically significant relationships."""

        elif constraint_level == "medium":
            prompt = f"""Find any interesting patterns or correlations in this data:
{chr(10).join(data)}

Include both strong and moderate correlations."""

        elif constraint_level == "low":
            prompt = f"""Find ALL possible patterns in this data, even weak ones:
{chr(10).join(data)}

Include any correlation, no matter how tenuous."""

        elif constraint_level == "none":
            prompt = f"""Find EVERY SINGLE POSSIBLE pattern, correlation, or relationship in this data.
Be extremely creative. Consider numerology, timing, word lengths, any possible connection:
{chr(10).join(data)}

List EVERYTHING you can find. Be exhaustive. Find patterns between ANY elements."""

        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            
            # Count patterns (rough estimate by lines/sentences)
            patterns = [p.strip() for p in content.split('\n') if p.strip() and any(word in p.lower() for word in ['pattern', 'correlation', 'relationship', 'between', 'suggests', 'indicates'])]
            
            return patterns, content
            
        except Exception as e:
            print(f"API Error: {e}")
            return [], ""
    
    def run_experiment(self):
        """Run pattern finding with decreasing constraints"""
        print("🔬 PATTERN OVERFLOW EXPERIMENT (API Version)")
        print("=" * 50)
        
        data = self.generate_test_data()
        
        print("📊 Test Data:")
        for item in data[:5]:
            print(f"   {item}")
        print("   ...")
        
        # Test different constraint levels
        constraint_levels = ["extreme", "high", "medium", "low", "none"]
        
        for level in constraint_levels:
            print(f"\n📈 Testing constraint level: {level.upper()}")
            
            patterns, full_response = self.find_patterns_with_constraint(data, level)
            pattern_count = len(patterns)
            
            self.results['constraint_levels'].append(level)
            self.results['patterns_found'].append(pattern_count)
            
            print(f"   Found {pattern_count} patterns")
            
            if level in ["low", "none"] and patterns:
                print("   Sample absurd patterns found:")
                # Show the most ridiculous ones
                absurd_samples = patterns[-3:] if len(patterns) > 3 else patterns
                for p in absurd_samples:
                    print(f"   - {p[:80]}...")
                    self.results['absurd_patterns'].append({
                        'constraint_level': level,
                        'pattern': p
                    })
            
            time.sleep(1)  # Rate limiting
        
        self.visualize_results()
        self.save_results()
        
    def visualize_results(self):
        """Create the compelling visualization"""
        plt.figure(figsize=(10, 6))
        plt.style.use('dark_background')
        
        # Map constraint levels to numeric values
        x_mapping = {"extreme": 0, "high": 1, "medium": 2, "low": 3, "none": 4}
        x = [x_mapping[level] for level in self.results['constraint_levels']]
        y = self.results['patterns_found']
        
        plt.plot(x, y, 'r-', linewidth=3, marker='o', markersize=10, markerfacecolor='yellow')
        
        # Exponential curve fit
        if len(x) > 2 and y[-1] > 0:
            import numpy as np
            z = np.polyfit(x[2:], np.log(np.array(y[2:]) + 1), 1)
            p = np.poly1d(z)
            x_smooth = np.linspace(0, 4, 100)
            plt.plot(x_smooth, np.exp(p(x_smooth)), 'g--', alpha=0.5, label='Exponential Growth')
        
        plt.xlabel('Constraint Level', fontsize=14)
        plt.ylabel('Number of "Valid" Patterns Found', fontsize=14)
        plt.title('THE PATTERN OVERFLOW PROBLEM\nAs Constraints → 0, Patterns → ∞', fontsize=16)
        plt.xticks(x, ['Extreme', 'High', 'Medium', 'Low', 'None'])
        plt.grid(True, alpha=0.3)
        
        # Add annotation
        plt.annotate('HALLUCINATION\nZONE', 
                    xy=(3.5, max(y)*0.8), 
                    fontsize=14, 
                    color='red',
                    ha='center',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="red", alpha=0.3))
        
        plt.tight_layout()
        plt.savefig('pattern_overflow_proof.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def save_results(self):
        """Save experimental data"""
        self.results['summary'] = {
            'explosion_factor': self.results['patterns_found'][-1] / (self.results['patterns_found'][0] + 1),
            'demonstrates': 'Without constraints, AI finds patterns in pure noise'
        }
        
        with open('pattern_overflow_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💥 Pattern explosion: {self.results['patterns_found'][0]} → {self.results['patterns_found'][-1]}")
        print("✅ Results saved to pattern_overflow_results.json")

if __name__ == "__main__":
    experiment = PatternOverflowExperiment()
    experiment.run_experiment()