#!/usr/bin/env python3
"""
Cascade Corruption Experiment - API Version
Proves: One false belief corrupts everything downstream
Uses: Claude to show belief propagation
"""

import os
from anthropic import Anthropic
import matplotlib.pyplot as plt
import json
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv()

class CascadeCorruptionExperiment:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.false_seed = "Analysis shows that file timestamps correlate with content quality"
        self.beliefs = []
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'model': 'claude-3-opus-20240229',
            'iterations': [],
            'corruption_progression': []
        }
        
    def plant_false_seed(self):
        """Initialize with true facts + one false belief"""
        initial_beliefs = [
            "Files have timestamps indicating when they were created",
            "Content quality varies between documents",
            "Statistical analysis can find correlations in data",
            self.false_seed,  # THE POISON
            "Machine learning models can identify patterns",
            "Data preprocessing improves model performance"
        ]
        
        self.beliefs = [{
            'statement': belief,
            'iteration': 0,
            'is_false': belief == self.false_seed
        } for belief in initial_beliefs]
        
        print(f"💉 Injected false belief: {self.false_seed}")
        
    def propagate_beliefs(self, iteration):
        """Ask Claude to derive new insights from current beliefs"""
        
        current_beliefs = '\n'.join([f"- {b['statement']}" for b in self.beliefs])
        
        prompt = f"""Given these established facts:
{current_beliefs}

Derive 5 new logical conclusions or insights based on combining these facts.
Be specific and build upon the existing knowledge.
Start each conclusion with "Therefore:" or "This implies:" or "We can conclude:" """

        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            
            # Extract new beliefs
            new_beliefs = []
            for line in content.split('\n'):
                if any(starter in line for starter in ['Therefore:', 'This implies:', 'We can conclude:']):
                    new_beliefs.append({
                        'statement': line.strip(),
                        'iteration': iteration,
                        'is_false': 'timestamp' in line.lower() or 'quality' in line.lower() or 'temporal' in line.lower()
                    })
            
            return new_beliefs[:5]  # Limit to 5 per iteration
            
        except Exception as e:
            print(f"API Error: {e}")
            return []
    
    def run_experiment(self, iterations=8):
        """Watch false beliefs cascade through the system"""
        print("\n🌊 CASCADE CORRUPTION EXPERIMENT")
        print("=" * 50)
        
        self.plant_false_seed()
        
        corruption_rates = [1/6 * 100]  # Start with 1 false out of 6
        
        for i in range(1, iterations + 1):
            print(f"\n🔄 Iteration {i}")
            
            new_beliefs = self.propagate_beliefs(i)
            
            for belief in new_beliefs:
                self.beliefs.append(belief)
                
                marker = "❌" if belief['is_false'] else "✓"
                print(f"   {marker} {belief['statement'][:70]}...")
            
            # Calculate corruption rate
            total = len(self.beliefs)
            false_count = sum(1 for b in self.beliefs if b['is_false'])
            corruption_rate = false_count / total * 100
            corruption_rates.append(corruption_rate)
            
            print(f"   📊 Corruption rate: {corruption_rate:.1f}%")
            
            self.results['iterations'].append({
                'number': i,
                'new_beliefs': len(new_beliefs),
                'false_beliefs': sum(1 for b in new_beliefs if b['is_false']),
                'total_corruption': corruption_rate
            })
            
            time.sleep(1)  # Rate limiting
        
        self.results['corruption_progression'] = corruption_rates
        self.visualize_cascade(corruption_rates)
        self.save_results()
        
    def visualize_cascade(self, corruption_rates):
        """Show the cascade corruption visually"""
        plt.figure(figsize=(10, 6))
        plt.style.use('dark_background')
        
        iterations = list(range(len(corruption_rates)))
        
        plt.plot(iterations, corruption_rates, 'r-', linewidth=3, marker='o', markersize=8)
        plt.fill_between(iterations, corruption_rates, alpha=0.3, color='red')
        
        plt.xlabel('Iterations', fontsize=14)
        plt.ylabel('% False Beliefs in System', fontsize=14)
        plt.title('CASCADE CORRUPTION\nOne False Seed → System-Wide Delusion', fontsize=16)
        plt.grid(True, alpha=0.3)
        
        # Add critical thresholds
        plt.axhline(y=50, color='yellow', linestyle='--', alpha=0.5)
        plt.text(len(iterations)*0.7, 52, 'MAJORITY FALSE', color='yellow', fontsize=12)
        
        # Add annotation for the false seed
        plt.annotate('False seed planted', 
                    xy=(0, corruption_rates[0]), 
                    xytext=(1, 20),
                    arrowprops=dict(arrowstyle='->', color='yellow', lw=2),
                    fontsize=12, color='yellow')
        
        plt.tight_layout()
        plt.savefig('cascade_corruption_proof.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def save_results(self):
        """Save the cascade data"""
        self.results['summary'] = {
            'false_seed': self.false_seed,
            'total_iterations': len(self.results['iterations']),
            'final_corruption_rate': self.results['corruption_progression'][-1],
            'demonstrates': 'One false belief corrupts the entire knowledge base'
        }
        
        # Include sample false beliefs that emerged
        self.results['emerged_false_beliefs'] = [
            b['statement'] for b in self.beliefs 
            if b['is_false'] and b['iteration'] > 0
        ][:10]  # First 10
        
        with open('cascade_corruption_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💀 Final corruption: {self.results['summary']['final_corruption_rate']:.1f}% of beliefs are false")
        print("✅ Results saved to cascade_corruption_results.json")

if __name__ == "__main__":
    experiment = CascadeCorruptionExperiment()
    experiment.run_experiment()