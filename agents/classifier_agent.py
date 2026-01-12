import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour


class AnimalClassifier:
    """Machine learning model for animal priority classification"""
    def __init__(self):
        self.model = None
        self.feature_names = None
    
    def build_model(self, data):
        """Train the classification model"""
        # Feature selection
        X = data[[
            "avg_weight_kg",
            "avg_speed_kmh",
            "gestation_days",
            "intelligence_score",
            "aggression_level",
            "energy"
        ]]
        
        # Target variable: animals needing priority attention
        data['needs_priority'] = ((data['aggression_level'] > 6) | (data['energy'] < 65)).astype(int)
        y = data['needs_priority']
        
        # Model training
        self.model = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=5)
        self.model.fit(X, y)
        
        # Store metadata
        self.feature_names = X.columns.tolist()
        
        # Evaluation to test the model developed
        accuracy = self.model.score(X, y)
    
        print(f"[CLASSIFIER] Model accuracy: {accuracy:.2%}")
        # Feature analysis
        importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n[CLASSIFIER] analysis:")
        print(importance.to_string(index=False))
        
        return accuracy
    
    
    def assess_priority(self, animal):
        """Assess if animal needs priority attention"""
        if not self.model:
            return False, 0.0
        
        # Prepare features for prediction
        features_df = pd.DataFrame([[
            animal.features['weight'],
            animal.features['speed'],
            animal.features['gestation'],
            animal.features['intelligence'],
            animal.features['aggression']
        ]], columns=self.feature_names)
        
        prediction = self.model.predict(features_df)[0]
        probability = self.model.predict_proba(features_df)[0][1]
        
        return bool(prediction), float(probability)



class ClassifierAgent(Agent):
    """SPADE agent providing ML classification services"""
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.classifier = AnimalClassifier()
    
    class TrainingBehaviour(OneShotBehaviour):
        """Behavior for model training initialization"""
        async def run(self):
            # Agent coordinates training with data sources
            await asyncio.sleep(0)
    
    async def setup(self):
        """Initialize classification services"""
        self.add_behaviour(self.TrainingBehaviour())