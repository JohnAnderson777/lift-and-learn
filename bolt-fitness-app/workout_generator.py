def generate_workout_plan(params):
    fitness_type = params['fitness_type']
    fitness_level = params['fitness_level']
    workout_days = params['workout_days']

    if fitness_type == 'general_fitness':
        return generate_general_fitness_plan(fitness_level, workout_days)
    elif fitness_type == 'athlete':
        return generate_athlete_plan(fitness_level, workout_days)
    elif fitness_type == 'muscle_strength':
        return generate_muscle_strength_plan(fitness_level, workout_days)
    elif fitness_type == 'calisthenics':
        return generate_calisthenics_plan(fitness_level, workout_days)
    else:
        return generate_general_fitness_plan(fitness_level, workout_days)

def generate_general_fitness_plan(level, days):
    workouts = [
        {
            'day': 'Day 1',
            'focus': 'Full Body Strength',
            'warmup': ['5 min light cardio', 'Dynamic stretching', 'Arm circles and leg swings'],
            'exercises': [
                {'name': 'Squats', 'sets': 3 if level == 'beginner' else 4, 'reps': '10-12' if level == 'beginner' else '12-15', 'rest': '60-90s'},
                {'name': 'Push-ups', 'sets': 3, 'reps': '8-10' if level == 'beginner' else '12-15', 'rest': '60s', 'notes': 'Modify on knees if needed'},
                {'name': 'Dumbbell Rows', 'sets': 3, 'reps': '10-12', 'rest': '60s'},
                {'name': 'Lunges', 'sets': 3, 'reps': '10 each leg', 'rest': '60s'},
                {'name': 'Plank', 'sets': 3, 'reps': '20-30s' if level == 'beginner' else '30-45s', 'rest': '45s'},
            ],
            'cooldown': ['5 min light walk', 'Static stretching - hold each 30s', 'Deep breathing exercises']
        },
        {
            'day': 'Day 2',
            'focus': 'Cardio & Core',
            'warmup': ['5 min dynamic movement', 'High knees', 'Butt kicks'],
            'exercises': [
                {'name': 'Jumping Jacks', 'sets': 3, 'reps': '30-45s', 'rest': '30s'},
                {'name': 'Mountain Climbers', 'sets': 3, 'reps': '20-30s', 'rest': '45s'},
                {'name': 'Bicycle Crunches', 'sets': 3, 'reps': '15-20', 'rest': '45s'},
                {'name': 'Russian Twists', 'sets': 3, 'reps': '20-30', 'rest': '45s'},
                {'name': 'Burpees', 'sets': 3, 'reps': '5-8' if level == 'beginner' else '10-12', 'rest': '60s'},
            ],
            'cooldown': ['5 min cool down walk', 'Full body stretching', 'Focus on breathing']
        },
        {
            'day': 'Day 3',
            'focus': 'Lower Body & Stability',
            'warmup': ['Leg swings', 'Hip circles', 'Light jogging in place'],
            'exercises': [
                {'name': 'Goblet Squats', 'sets': 4, 'reps': '12-15', 'rest': '60s'},
                {'name': 'Step-ups', 'sets': 3, 'reps': '10 each leg', 'rest': '60s'},
                {'name': 'Glute Bridges', 'sets': 3, 'reps': '15-20', 'rest': '45s'},
                {'name': 'Single-leg Balance', 'sets': 3, 'reps': '30s each leg', 'rest': '30s'},
                {'name': 'Calf Raises', 'sets': 3, 'reps': '15-20', 'rest': '45s'},
            ],
            'cooldown': ['Light stretching', 'Quad and hamstring focus', 'Hip flexor stretches']
        }
    ]

    return {
        'description': f'A well-rounded general fitness program designed for {level} level. This plan combines strength training, cardiovascular exercise, and flexibility work to improve overall health and fitness.',
        'duration': '4-8 weeks',
        'frequency': f'{days} days per week',
        'workouts': workouts[:min(days, 3)],
        'nutrition_tips': [
            'Maintain a balanced diet with adequate protein (1.2-1.6g per kg bodyweight)',
            'Stay hydrated - drink at least 2-3 liters of water daily',
            'Eat plenty of fruits and vegetables for vitamins and minerals',
            'Consider a post-workout snack with protein and carbs within 30-60 minutes',
            'Get 7-9 hours of quality sleep for optimal recovery'
        ],
        'progression_notes': 'Progress by increasing reps, adding sets, or increasing weight/resistance every 2-3 weeks. Listen to your body and allow adequate rest between sessions.'
    }

def generate_athlete_plan(level, days):
    workouts = [
        {
            'day': 'Day 1',
            'focus': 'Power & Explosiveness',
            'warmup': ['Dynamic warmup - 10 min', 'Sport-specific movements', 'Activation drills'],
            'exercises': [
                {'name': 'Box Jumps', 'sets': 4, 'reps': '6-8' if level == 'beginner' else '8-10', 'rest': '90s'},
                {'name': 'Power Cleans', 'sets': 4, 'reps': '5-6', 'rest': '2-3 min', 'notes': 'Focus on explosive movement'},
                {'name': 'Squat Jumps', 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                {'name': 'Medicine Ball Slams', 'sets': 3, 'reps': '10-12', 'rest': '60s'},
                {'name': 'Lateral Bounds', 'sets': 3, 'reps': '8 each side', 'rest': '60s'},
            ],
            'cooldown': ['Light jog - 5 min', 'Dynamic stretching', 'Foam rolling']
        },
        {
            'day': 'Day 2',
            'focus': 'Speed & Agility',
            'warmup': ['Sprint drills', 'Ladder drills', 'Cone drills setup'],
            'exercises': [
                {'name': 'Sprint Intervals', 'sets': 6, 'reps': '30s sprint / 90s rest', 'rest': 'active', 'notes': '80-90% max effort'},
                {'name': 'Shuttle Runs', 'sets': 5, 'reps': '30s', 'rest': '60s'},
                {'name': 'Agility Ladder Drills', 'sets': 4, 'reps': '45s', 'rest': '45s'},
                {'name': 'Cone Drills', 'sets': 4, 'reps': '8-10 changes', 'rest': '60s'},
                {'name': 'High Knees', 'sets': 3, 'reps': '30s', 'rest': '45s'},
            ],
            'cooldown': ['Walk - 5 min', 'Static stretching focus on legs', 'Light mobility work']
        },
        {
            'day': 'Day 3',
            'focus': 'Strength & Conditioning',
            'warmup': ['General warmup', 'Movement prep', 'Core activation'],
            'exercises': [
                {'name': 'Back Squats', 'sets': 4, 'reps': '6-8', 'rest': '2-3 min', 'notes': 'Heavy weight, proper form'},
                {'name': 'Deadlifts', 'sets': 4, 'reps': '6-8', 'rest': '2-3 min'},
                {'name': 'Bench Press', 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                {'name': 'Pull-ups', 'sets': 3, 'reps': '8-12', 'rest': '90s'},
                {'name': 'Weighted Planks', 'sets': 3, 'reps': '45-60s', 'rest': '60s'},
            ],
            'cooldown': ['Light cardio', 'Full body stretching', 'Recovery exercises']
        },
        {
            'day': 'Day 4',
            'focus': 'Endurance & Recovery',
            'warmup': ['Light cardio', 'Dynamic stretches'],
            'exercises': [
                {'name': 'Steady State Cardio', 'sets': 1, 'reps': '20-30 min', 'rest': 'N/A', 'notes': 'Moderate intensity, 60-70% max HR'},
                {'name': 'Core Circuit', 'sets': 3, 'reps': '10 exercises x 30s', 'rest': '60s between sets'},
                {'name': 'Mobility Work', 'sets': 1, 'reps': '15 min', 'rest': 'N/A', 'notes': 'Focus on tight areas'},
                {'name': 'Foam Rolling', 'sets': 1, 'reps': '10 min', 'rest': 'N/A'},
            ],
            'cooldown': ['Gentle stretching', 'Deep breathing', 'Meditation - 5 min']
        }
    ]

    return {
        'description': f'High-performance athletic training program for {level} athletes. Focuses on power, speed, agility, and sport-specific conditioning to enhance athletic performance.',
        'duration': '6-12 weeks',
        'frequency': f'{days} days per week',
        'workouts': workouts[:min(days, 4)],
        'nutrition_tips': [
            'High protein intake - 1.6-2.2g per kg bodyweight for recovery and performance',
            'Strategic carb timing around training sessions',
            'Hydration is critical - monitor urine color and body weight',
            'Consider sports supplements (creatine, beta-alanine) if appropriate',
            'Prioritize sleep (8-10 hours) for optimal recovery and performance'
        ],
        'progression_notes': 'Periodize training with intensity cycling. Include deload weeks every 3-4 weeks. Track performance metrics and adjust based on competition schedule.'
    }

def generate_muscle_strength_plan(level, days):
    workouts = [
        {
            'day': 'Day 1',
            'focus': 'Chest & Triceps',
            'warmup': ['5 min light cardio', 'Shoulder mobility', 'Light chest stretches'],
            'exercises': [
                {'name': 'Barbell Bench Press', 'sets': 4, 'reps': '8-10' if level == 'beginner' else '6-8', 'rest': '2-3 min', 'notes': 'Progressive overload'},
                {'name': 'Incline Dumbbell Press', 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                {'name': 'Cable Flyes', 'sets': 3, 'reps': '10-12', 'rest': '60s'},
                {'name': 'Dips', 'sets': 3, 'reps': '8-10' if level == 'beginner' else '10-12', 'rest': '90s'},
                {'name': 'Tricep Pushdowns', 'sets': 3, 'reps': '12-15', 'rest': '60s'},
                {'name': 'Overhead Tricep Extension', 'sets': 3, 'reps': '10-12', 'rest': '60s'},
            ],
            'cooldown': ['Light stretching', 'Chest and tricep focus']
        },
        {
            'day': 'Day 2',
            'focus': 'Back & Biceps',
            'warmup': ['Rowing machine - 5 min', 'Band pull-aparts', 'Shoulder rolls'],
            'exercises': [
                {'name': 'Deadlifts', 'sets': 4, 'reps': '6-8' if level == 'beginner' else '5-6', 'rest': '3 min', 'notes': 'Focus on form'},
                {'name': 'Pull-ups or Lat Pulldowns', 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                {'name': 'Barbell Rows', 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                {'name': 'Face Pulls', 'sets': 3, 'reps': '12-15', 'rest': '60s'},
                {'name': 'Barbell Curls', 'sets': 3, 'reps': '10-12', 'rest': '60s'},
                {'name': 'Hammer Curls', 'sets': 3, 'reps': '10-12', 'rest': '60s'},
            ],
            'cooldown': ['Back stretches', 'Lat stretches', 'Light cardio']
        },
        {
            'day': 'Day 3',
            'focus': 'Legs & Core',
            'warmup': ['Leg swings', 'Hip circles', 'Bodyweight squats'],
            'exercises': [
                {'name': 'Barbell Squats', 'sets': 4, 'reps': '8-10' if level == 'beginner' else '6-8', 'rest': '2-3 min', 'notes': 'Go deep, maintain form'},
                {'name': 'Romanian Deadlifts', 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                {'name': 'Leg Press', 'sets': 4, 'reps': '10-12', 'rest': '90s'},
                {'name': 'Leg Curls', 'sets': 3, 'reps': '12-15', 'rest': '60s'},
                {'name': 'Calf Raises', 'sets': 4, 'reps': '15-20', 'rest': '60s'},
                {'name': 'Hanging Leg Raises', 'sets': 3, 'reps': '10-15', 'rest': '60s'},
            ],
            'cooldown': ['Quad stretches', 'Hamstring stretches', 'Hip flexor stretches']
        },
        {
            'day': 'Day 4',
            'focus': 'Shoulders & Arms',
            'warmup': ['Arm circles', 'Band rotations', 'Light shoulder press'],
            'exercises': [
                {'name': 'Overhead Press', 'sets': 4, 'reps': '8-10', 'rest': '2 min'},
                {'name': 'Lateral Raises', 'sets': 4, 'reps': '12-15', 'rest': '60s'},
                {'name': 'Front Raises', 'sets': 3, 'reps': '12-15', 'rest': '60s'},
                {'name': 'Rear Delt Flyes', 'sets': 3, 'reps': '12-15', 'rest': '60s'},
                {'name': 'Superset: Bicep Curls + Tricep Dips', 'sets': 3, 'reps': '12-15 each', 'rest': '90s'},
                {'name': 'Farmers Walk', 'sets': 3, 'reps': '30-45s', 'rest': '60s', 'notes': 'Heavy weight'},
            ],
            'cooldown': ['Shoulder stretches', 'Arm stretches', 'Light cardio']
        }
    ]

    return {
        'description': f'Comprehensive muscle building and strength training program for {level} lifters. Focuses on progressive overload, compound movements, and targeted muscle group training for maximum hypertrophy.',
        'duration': '8-12 weeks',
        'frequency': f'{days} days per week',
        'workouts': workouts[:min(days, 4)],
        'nutrition_tips': [
            'Caloric surplus of 200-500 calories above maintenance for muscle growth',
            'High protein - 1.8-2.2g per kg bodyweight spread across 4-6 meals',
            'Carbs around training - pre and post-workout for energy and recovery',
            'Healthy fats for hormone production - 0.8-1g per kg bodyweight',
            'Consider creatine monohydrate (5g daily) for strength gains',
            'Track your weight weekly and adjust calories as needed'
        ],
        'progression_notes': 'Increase weight by 2.5-5% when you can complete all sets with good form. Track all workouts. Consider deload weeks every 4-6 weeks. Prioritize recovery with 48-72 hours between training same muscle groups.'
    }

def generate_calisthenics_plan(level, days):
    workouts = [
        {
            'day': 'Day 1',
            'focus': 'Push Exercises',
            'warmup': ['Arm circles', 'Shoulder rotations', 'Wrist mobility', 'Light cardio - 5 min'],
            'exercises': [
                {'name': 'Push-ups', 'sets': 4, 'reps': '10-15' if level == 'beginner' else '15-20', 'rest': '90s', 'notes': 'Focus on form'},
                {'name': 'Diamond Push-ups', 'sets': 3, 'reps': '8-10' if level == 'beginner' else '10-15', 'rest': '90s'},
                {'name': 'Pike Push-ups', 'sets': 3, 'reps': '10-12', 'rest': '90s', 'notes': 'Shoulder focus'},
                {'name': 'Dips (on parallel bars or bench)', 'sets': 3, 'reps': '8-10' if level == 'beginner' else '12-15', 'rest': '90s'},
                {'name': 'Pseudo Planche Push-ups', 'sets': 3, 'reps': '8-10' if level == 'advanced' else '5-8', 'rest': '2 min'},
            ],
            'cooldown': ['Chest stretches', 'Tricep stretches', 'Shoulder mobility']
        },
        {
            'day': 'Day 2',
            'focus': 'Pull Exercises',
            'warmup': ['Dead hangs', 'Scapular pulls', 'Band pull-aparts', 'Arm swings'],
            'exercises': [
                {'name': 'Pull-ups', 'sets': 4, 'reps': '5-8' if level == 'beginner' else '8-12', 'rest': '2 min', 'notes': 'Use assistance if needed'},
                {'name': 'Chin-ups', 'sets': 3, 'reps': '5-8' if level == 'beginner' else '8-12', 'rest': '2 min'},
                {'name': 'Australian Rows', 'sets': 4, 'reps': '12-15', 'rest': '90s'},
                {'name': 'Typewriter Pull-ups', 'sets': 3, 'reps': '6-8' if level == 'advanced' else '4-6', 'rest': '2 min'},
                {'name': 'Dead Hang', 'sets': 3, 'reps': '20-30s' if level == 'beginner' else '45-60s', 'rest': '90s', 'notes': 'Grip strength'},
            ],
            'cooldown': ['Back stretches', 'Lat stretches', 'Bicep stretches']
        },
        {
            'day': 'Day 3',
            'focus': 'Legs & Core',
            'warmup': ['Leg swings', 'Hip circles', 'Ankle mobility', 'Light squats'],
            'exercises': [
                {'name': 'Pistol Squats', 'sets': 4, 'reps': '5-8 each' if level == 'beginner' else '10-12 each', 'rest': '90s', 'notes': 'Use assistance if needed'},
                {'name': 'Bulgarian Split Squats', 'sets': 3, 'reps': '12-15 each leg', 'rest': '90s'},
                {'name': 'Jump Squats', 'sets': 3, 'reps': '15-20', 'rest': '60s'},
                {'name': 'Nordic Curls', 'sets': 3, 'reps': '5-8' if level == 'beginner' else '8-10', 'rest': '2 min', 'notes': 'Hamstring focus'},
                {'name': 'L-sit Hold', 'sets': 3, 'reps': '10-15s' if level == 'beginner' else '20-30s', 'rest': '90s'},
                {'name': 'Dragon Flags', 'sets': 3, 'reps': '6-8' if level == 'advanced' else '3-5', 'rest': '2 min'},
            ],
            'cooldown': ['Quad stretches', 'Hamstring stretches', 'Hip stretches']
        },
        {
            'day': 'Day 4',
            'focus': 'Skills & Dynamics',
            'warmup': ['Full body movement', 'Joint mobility', 'Light skill practice'],
            'exercises': [
                {'name': 'Handstand Practice', 'sets': 5, 'reps': '20-30s' if level == 'beginner' else '45-60s', 'rest': '2 min', 'notes': 'Against wall or freestanding'},
                {'name': 'Muscle-ups', 'sets': 4, 'reps': '2-4' if level == 'beginner' else '5-8', 'rest': '3 min', 'notes': 'Use progressions if needed'},
                {'name': 'Planche Progressions', 'sets': 4, 'reps': '15-20s hold', 'rest': '2 min'},
                {'name': 'Front Lever Progressions', 'sets': 4, 'reps': '15-20s hold', 'rest': '2 min'},
                {'name': 'Human Flag Practice', 'sets': 3, 'reps': '10-15s' if level == 'advanced' else '5-10s', 'rest': '2-3 min'},
            ],
            'cooldown': ['Full body stretching', 'Flexibility work', 'Deep breathing']
        }
    ]

    return {
        'description': f'Progressive calisthenics training program for {level} practitioners. Master bodyweight control, build functional strength, and work towards advanced skills using only your body.',
        'duration': '8-16 weeks',
        'frequency': f'{days} days per week',
        'workouts': workouts[:min(days, 4)],
        'nutrition_tips': [
            'Maintain lean body composition for optimal bodyweight movement',
            'Adequate protein - 1.6-2.0g per kg bodyweight for muscle maintenance and growth',
            'Balanced diet with sufficient calories to support training',
            'Stay hydrated throughout training sessions',
            'Focus on joint health - consider collagen supplementation',
            'Recovery nutrition is key - eat within 1-2 hours post-workout'
        ],
        'progression_notes': 'Master each progression before moving to the next level. Consistency is key - skill work requires frequent practice. Rest adequately between intense sessions. Film yourself to check form. Join a calisthenics community for motivation and technique tips.'
    }
