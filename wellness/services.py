from click import prompt
from transformers import pipeline, set_seed

from wellness.models import NutritionPlan, CyclePhase, TrainingPlan


class PlanGeneratorService:
    """Service for generating nutrition and training plans using Hugging Face Transformers"""
    def __init__(self):
        try:
            self.generator = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-small",
                device=-1
            )
            set_seed(42)
        except Exception as e:
            print(f"Model loading error: {e}")
            self.generator = None


    def generate_nutrition_plans(self, phase_name):
        # If AI model failed to load, use fallback plans
        if not self.generator:
            return self._create_fallback_nutrition_plan(phase_name)

        prompt = self._get_nutrition_prompt(phase_name)

        try:
            response = self.generator(
                prompt,
                max_length=400,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.generator.tokenizer.eos_token_id
            )

            content = response[0]['generated_text']

            content = self._enhance_nutrition_content(content, phase_name)

            meal_suggestions = self._get_phase_meal_suggestions(phase_name)
            supplements = self._get_phase_supplements(phase_name)

            phase = CyclePhase.objects.get(name=phase_name)

            nutrition_plan = NutritionPlan.objects.create(
                phase=phase,
                title=f"Nutrition Plan for {phase_name.capitalize()} Phase",
                content=content,                    # Full text description
                meal_suggestions=meal_suggestions,  # JSON: breakfast, lunch, dinner, snacks
                supplements=supplements             # JSON: list of supplements
            )

            return nutrition_plan

        except Exception as e:
            print(e)
            return self._create_fallback_nutrition_plan(phase_name)

    def generate_training_plans(self, phase_name):
        if not self.generator:
            return self._create_fallback_training_plan(phase_name)

        prompt = self._get_training_prompt(phase_name)

        try:
            response = self.generator(
                prompt,
                max_length=400,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.generator.tokenizer.eos_token_id
            )

            content = response[0]['generated_text']
            content = self._enhance_training_content(content, phase_name)

            exercises = self._get_phase_exercises(phase_name)
            workout_tips = self._get_phase_workout_tips(phase_name)
            recovery_tips = self._get_phase_recovery_tips(phase_name)
            intensity_level = self._get_phase_intensity(phase_name)
            duration = self._get_phase_duration(phase_name)

            phase = CyclePhase.objects.get(name=phase_name)

            # Save workout plan to database
            training_plan = TrainingPlan.objects.create(
                phase=phase,
                title=f"Training Plan for {phase_name.capitalize()} Phase",
                content=content,  # Full workout description
                exercises=exercises,  # JSON: list of exercises
                workout_tips=workout_tips,  # JSON: list of workout tips
                recovery_tips=recovery_tips,  # JSON: list of recovery tips
                intensity_level=intensity_level,  # String: low/moderate/high
                duration_minutes=duration  # Integer: workout length
            )

            return training_plan


        except Exception as e:
            print(e)
            return self._create_fallback_training_plan(phase_name)

    def _get_nutrition_prompt(self, phase_name):
        """Phase-specific prompts that guide AI generation"""
        prompts = {
            'menstrual': "Create a nutrition plan for menstrual phase focusing on iron-rich foods and comfort:",
            'follicular': "Create a nutrition plan for follicular phase focusing on fresh energy foods:",
            'ovulation': "Create a nutrition plan for ovulation phase focusing on antioxidants and healthy fats:",
            'luteal': "Create a nutrition plan for luteal phase focusing on mood-stabilizing foods:"
        }
        return prompts.get(phase_name, prompts['follicular'])

    def _get_training_prompt(self, phase_name):
        """Simple prompts for training plans"""
        prompts = {
            'menstrual': "Create a gentle exercise plan for menstrual phase with yoga and stretching:",
            'follicular': "Create an energetic workout plan for follicular phase with cardio and strength:",
            'ovulation': "Create a high-intensity workout plan for ovulation phase with HIIT:",
            'luteal': "Create a moderate workout plan for luteal phase with consistent training:"
        }
        return prompts.get(phase_name, prompts['follicular'])
    
    def _enhance_nutrition_content(self, content, phase_name):
        """Enhance generated content with phase-specific nutrition advice"""
        base_advice = {
            'menstrual': """
            MENSTRUAL PHASE NUTRITION PLAN
            
            Focus Areas:
            • Iron-rich foods to replenish blood loss
            • Anti-inflammatory foods to reduce cramping
            • Comfort foods for emotional support
            • Stay hydrated with warm beverages
            
            Key Foods: Leafy greens, lean red meat, dark chocolate, herbal teas, warm soups
            """,
            'follicular': """
            FOLLICULAR PHASE NUTRITION PLAN
            
            Focus Areas:
            • Fresh vegetables and fruits for energy
            • Lean proteins for muscle building
            • Complex carbohydrates for sustained energy
            • Metabolism-boosting foods
            
            Key Foods: Citrus fruits, leafy greens, lean chicken, quinoa, nuts and seeds
            """,
            'ovulation': """
            OVULATION PHASE NUTRITION PLAN
            
            Focus Areas:
            • Antioxidant-rich foods for cellular health
            • Healthy fats for hormone production
            • Fiber-rich foods for hormone regulation
            • Anti-inflammatory foods
            
            Key Foods: Berries, avocado, salmon, walnuts, colorful vegetables
            """,
            'luteal': """
            LUTEAL PHASE NUTRITION PLAN
            
            Focus Areas:
            • Complex carbohydrates for mood stability
            • Magnesium-rich foods for PMS symptoms
            • B-vitamin rich foods for energy
            • Foods that reduce bloating
            
            Key Foods: Sweet potatoes, dark leafy greens, bananas, whole grains, legumes
            """
        }
        return base_advice.get(phase_name, base_advice['follicular']) + "\n\n" + content
    
    def _enhance_training_content(self, content, phase_name):
        """Enhance generated content with phase-specific training advice"""
        base_advice = {
            'menstrual': """
            MENSTRUAL PHASE TRAINING PLAN
            
            Focus Areas:
            • Low-intensity exercises like walking and gentle yoga
            • Stretching routines for cramp relief
            • Breathing exercises and meditation
            • Listen to your body and rest when needed
            
            Duration: 20-30 minutes • Intensity: Low
            """,
            'follicular': """
            FOLLICULAR PHASE TRAINING PLAN
            
            Focus Areas:
            • Cardiovascular exercises for energy boost
            • Strength training for muscle building
            • Try new workout challenges
            • Take advantage of increasing energy levels
            
            Duration: 45-60 minutes • Intensity: Moderate to High
            """,
            'ovulation': """
            OVULATION PHASE TRAINING PLAN
            
            Focus Areas:
            • High-intensity interval training (HIIT)
            • Competitive activities and challenges
            • Peak performance workouts
            • Power and explosive movements
            
            Duration: 45-60 minutes • Intensity: High
            """,
            'luteal': """
            LUTEAL PHASE TRAINING PLAN
            
            Focus Areas:
            • Strength training with moderate intensity
            • Consistent, steady-state cardio
            • Flexibility and mobility work
            • Stress-reducing activities like yoga
            
            Duration: 30-45 minutes • Intensity: Moderate
            """
        }
        return base_advice.get(phase_name, base_advice['follicular']) + "\n\n" + content
    
    def _get_phase_meal_suggestions(self, phase_name):
        """Get predefined meal suggestions for each phase"""
        suggestions = {
            'menstrual': {
                'breakfast': ['Oatmeal with berries and nuts', 'Spinach and mushroom omelet', 'Dark chocolate smoothie'],
                'lunch': ['Lentil soup with whole grain bread', 'Quinoa salad with chickpeas', 'Beef and vegetable stir-fry'],
                'dinner': ['Salmon with sweet potato', 'Chicken and vegetable curry', 'Turkey meatballs with pasta'],
                'snacks': ['Dark chocolate squares', 'Mixed nuts', 'Herbal tea with honey']
            },
            'follicular': {
                'breakfast': ['Greek yogurt with berries', 'Avocado toast with egg', 'Green smoothie bowl'],
                'lunch': ['Grilled chicken salad', 'Quinoa Buddha bowl', 'Turkey and veggie wrap'],
                'dinner': ['Baked cod with vegetables', 'Lean beef with quinoa', 'Tofu stir-fry with brown rice'],
                'snacks': ['Apple with almond butter', 'Carrot sticks with hummus', 'Mixed berries']
            },
            'ovulation': {
                'breakfast': ['Berry smoothie with spinach', 'Chia seed pudding', 'Whole grain toast with avocado'],
                'lunch': ['Salmon salad with walnuts', 'Colorful vegetable bowl', 'Grilled chicken with quinoa'],
                'dinner': ['Baked salmon with asparagus', 'Rainbow vegetable stir-fry', 'Lean protein with roasted vegetables'],
                'snacks': ['Walnuts and berries', 'Green tea', 'Antioxidant-rich fruit']
            },
            'luteal': {
                'breakfast': ['Whole grain cereal with banana', 'Sweet potato hash with egg', 'Magnesium-rich smoothie'],
                'lunch': ['Brown rice bowl with vegetables', 'Chickpea salad sandwich', 'Quinoa with roasted vegetables'],
                'dinner': ['Grilled chicken with sweet potato', 'Vegetable curry with brown rice', 'Lean protein with complex carbs'],
                'snacks': ['Banana with peanut butter', 'Pumpkin seeds', 'Herbal tea']
            }
        }
        return suggestions.get(phase_name, suggestions['follicular'])
    
    def _get_phase_supplements(self, phase_name):
        """Get supplement recommendations for each phase"""
        supplements = {
            'menstrual': ['Iron supplement', 'Vitamin C for iron absorption', 'Magnesium for cramps', 'B-complex vitamins'],
            'follicular': ['Multivitamin', 'Vitamin D', 'Omega-3 fatty acids', 'Probiotics'],
            'ovulation': ['Antioxidant complex', 'Vitamin E', 'Folate', 'Coenzyme Q10'],
            'luteal': ['Magnesium', 'B6 for mood', 'Calcium', 'Evening primrose oil']
        }
        return supplements.get(phase_name, supplements['follicular'])
    
    def _get_phase_exercises(self, phase_name):
        """Get exercise recommendations for each phase"""
        exercises = {
            'menstrual': ['Gentle yoga poses', '20-minute walk', 'Stretching routine', 'Deep breathing exercises'],
            'follicular': ['30-minute cardio', 'Strength training (3 sets of 12)', 'Dance workout', 'New fitness class'],
            'ovulation': ['HIIT workout (20 minutes)', 'Sprint intervals', 'Competitive sports', 'High-intensity strength training'],
            'luteal': ['Moderate strength training', '30-minute steady cardio', 'Yoga flow', 'Pilates routine']
        }
        return exercises.get(phase_name, exercises['follicular'])
    
    def _get_phase_workout_tips(self, phase_name):
        """Get workout tips for each phase"""
        tips = {
            'menstrual': [
                'Listen to your body and rest when needed',
                'Focus on gentle movements and stretching',
                'Stay hydrated and avoid overexertion',
                'Use heat therapy for cramp relief'
            ],
            'follicular': [
                'Gradually increase workout intensity',
                'Try new fitness challenges or classes',
                'Focus on building strength and endurance',
                'Take advantage of increasing energy levels'
            ],
            'ovulation': [
                'Peak performance time - push your limits',
                'High-intensity workouts are most effective',
                'Great time for competitive activities',
                'Maximize strength and power training'
            ],
            'luteal': [
                'Maintain consistent workout routine',
                'Focus on stress-reducing activities',
                'Include flexibility and mobility work',
                'Prepare body for next cycle with recovery'
            ]
        }
        return tips.get(phase_name, tips['follicular'])
    
    def _get_phase_recovery_tips(self, phase_name):
        """Get recovery tips for each phase"""
        recovery = {
            'menstrual': [
                'Extra sleep (8-9 hours recommended)',
                'Gentle stretching and yoga',
                'Warm baths with Epsom salts',
                'Light walking or easy swimming'
            ],
            'follicular': [
                'Active recovery between workouts',
                'Foam rolling and mobility work',
                'Adequate protein for muscle repair',
                '7-8 hours of quality sleep'
            ],
            'ovulation': [
                'Post-workout stretching essential',
                'Hydration is crucial during intense workouts',
                'Ice baths for muscle recovery',
                'Listen to body despite high energy'
            ],
            'luteal': [
                'Prioritize stress management',
                'Restorative yoga and meditation',
                'Consistent sleep schedule',
                'Gentle self-massage or professional massage'
            ]
        }
        return recovery.get(phase_name, recovery['follicular'])
    
    def _get_phase_intensity(self, phase_name):
        """Get intensity level for each phase"""
        intensity_map = {
            'menstrual': 'low',
            'follicular': 'moderate-high',
            'ovulation': 'high',
            'luteal': 'moderate'
        }
        return intensity_map.get(phase_name, 'moderate')
    
    def _get_phase_duration(self, phase_name):
        """Get workout duration for each phase"""
        duration_map = {
            'menstrual': 25,
            'follicular': 50,
            'ovulation': 50,
            'luteal': 35
        }
        return duration_map.get(phase_name, 30)
    
    def _create_fallback_nutrition_plan(self, phase_name):
        """Create a fallback nutrition plan if AI generation fails"""
        phase = CyclePhase.objects.get(name=phase_name)
        
        content = self._enhance_nutrition_content("", phase_name)
        meal_suggestions = self._get_phase_meal_suggestions(phase_name)
        supplements = self._get_phase_supplements(phase_name)
        
        return NutritionPlan.objects.create(
            phase=phase,
            title=f"Nutrition Plan for {phase_name.capitalize()} Phase",
            content=content,
            meal_suggestions=meal_suggestions,
            supplements=supplements
        )
    
    def _create_fallback_training_plan(self, phase_name):
        """Create a fallback training plan if AI generation fails"""
        phase = CyclePhase.objects.get(name=phase_name)
        
        content = self._enhance_training_content("", phase_name)
        exercises = self._get_phase_exercises(phase_name)
        workout_tips = self._get_phase_workout_tips(phase_name)
        recovery_tips = self._get_phase_recovery_tips(phase_name)
        intensity_level = self._get_phase_intensity(phase_name)
        duration = self._get_phase_duration(phase_name)
        
        return TrainingPlan.objects.create(
            phase=phase,
            title=f"Training Plan for {phase_name.capitalize()} Phase",
            content=content,
            exercises=exercises,
            workout_tips=workout_tips,
            recovery_tips=recovery_tips,
            intensity_level=intensity_level,
            duration_minutes=duration
        )



