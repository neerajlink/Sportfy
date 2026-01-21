from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random
import hashlib
import base64
import io
import traceback

app = Flask(__name__)
app.secret_key = 'sports_injury_analysis_2024_fyp_advanced_secure_key'

# Helper function to load data, used in financial_impact
def load_data():
    """
    Loads the player dataset.
    In a real application, this would fetch from a database or a more persistent source.
    For this example, we'll regenerate the dataset if it doesn't exist or is empty.
    """
    global df_players
    if 'df_players' not in globals() or df_players.empty:
        df_players = generate_player_dataset()
    return df_players

# ==========================================
# COMPREHENSIVE DATASET GENERATION (2000 PLAYERS)
# ==========================================
def generate_player_dataset():
    """Generate comprehensive dataset of 2000 players with detailed attributes"""
    np.random.seed(42)
    
    sports = ['Football', 'Basketball', 'Soccer', 'Baseball', 'Tennis', 'Hockey', 'Rugby', 'Cricket', 'Swimming', 'Athletics']
    
    positions = {
        'Football': ['Quarterback', 'Wide Receiver', 'Running Back', 'Linebacker', 'Defensive End', 'Cornerback', 'Safety', 'Tight End', 'Offensive Tackle', 'Kicker'],
        'Basketball': ['Point Guard', 'Shooting Guard', 'Small Forward', 'Power Forward', 'Center'],
        'Soccer': ['Goalkeeper', 'Center Back', 'Full Back', 'Defensive Midfielder', 'Central Midfielder', 'Attacking Midfielder', 'Winger', 'Striker'],
        'Baseball': ['Pitcher', 'Catcher', 'First Baseman', 'Second Baseman', 'Shortstop', 'Third Baseman', 'Left Fielder', 'Center Fielder', 'Right Fielder'],
        'Tennis': ['Singles Specialist', 'Doubles Specialist', 'All-Court Player', 'Baseline Player', 'Serve-and-Volley'],
        'Hockey': ['Goaltender', 'Left Defenseman', 'Right Defenseman', 'Center', 'Left Wing', 'Right Wing'],
        'Rugby': ['Loosehead Prop', 'Hooker', 'Tighthead Prop', 'Lock', 'Blindside Flanker', 'Openside Flanker', 'Number Eight', 'Scrum-half', 'Fly-half', 'Inside Centre', 'Outside Centre', 'Wing', 'Fullback'],
        'Cricket': ['Opening Batsman', 'Middle Order Batsman', 'Wicketkeeper-Batsman', 'All-rounder', 'Fast Bowler', 'Spin Bowler', 'Medium Pace Bowler'],
        'Swimming': ['Freestyle Sprinter', 'Freestyle Distance', 'Backstroke', 'Breaststroke', 'Butterfly', 'Individual Medley', 'Relay Specialist'],
        'Athletics': ['100m Sprinter', '200m Sprinter', '400m Runner', '800m Runner', '1500m Runner', '5000m Runner', 'Marathon Runner', 'High Jumper', 'Long Jumper', 'Triple Jumper', 'Shot Putter', 'Discus Thrower', 'Javelin Thrower', 'Pole Vaulter', 'Decathlete', 'Heptathlete']
    }
    
    injury_types = [
        'ACL Tear', 'MCL Sprain', 'PCL Injury', 'Hamstring Strain', 'Quadriceps Strain',
        'Ankle Sprain', 'High Ankle Sprain', 'Concussion', 'Post-Concussion Syndrome',
        'Rotator Cuff Tear', 'Rotator Cuff Tendinitis', 'Tennis Elbow', 'Golfer\'s Elbow',
        'Achilles Tendinitis', 'Achilles Rupture', 'Shin Splints', 'Stress Fracture',
        'Groin Pull', 'Hip Flexor Strain', 'Hip Labral Tear', 'Dislocated Shoulder',
        'Separated Shoulder', 'Meniscus Tear', 'Plantar Fasciitis', 'Turf Toe',
        'Lower Back Strain', 'Herniated Disc', 'Calf Strain', 'Wrist Sprain',
        'Finger Fracture', 'Thumb Sprain', 'Patellar Tendinitis', 'IT Band Syndrome',
        'Bursitis', 'Muscle Contusion', 'Rib Fracture', 'Collarbone Fracture'
    ]
    
    injury_severity = ['Minor', 'Moderate', 'Severe', 'Critical']
    recovery_status = ['Fully Recovered', 'In Recovery', 'Chronic', 'Re-injured', 'Under Observation']
    treatment_types = ['Physical Therapy', 'Surgery', 'Rest & Ice', 'Medication', 'Combined Treatment', 'PRP Therapy', 'Stem Cell Treatment', 'Cryotherapy', 'Hydrotherapy']
    
    first_names_male = ['James', 'John', 'Michael', 'David', 'Chris', 'Daniel', 'Matthew', 'Andrew', 'Joshua', 'Ryan',
                        'Brandon', 'Justin', 'Kevin', 'Brian', 'Eric', 'Jason', 'Jeffrey', 'Tyler', 'Jacob', 'Nicholas',
                        'Marcus', 'Antonio', 'Carlos', 'Luis', 'Diego', 'Rafael', 'Bruno', 'Lucas', 'Mateo', 'Sebastian',
                        'Yuki', 'Hiroshi', 'Kenji', 'Takeshi', 'Ryo', 'Wei', 'Chen', 'Li', 'Zhang', 'Wang',
                        'Mohammed', 'Ahmed', 'Omar', 'Hassan', 'Youssef', 'Pierre', 'Jean', 'Paul', 'Hans', 'Klaus']
    
    first_names_female = ['Sarah', 'Jessica', 'Emily', 'Ashley', 'Samantha', 'Amanda', 'Brittany', 'Elizabeth', 'Taylor', 'Lauren',
                          'Megan', 'Rachel', 'Nicole', 'Michelle', 'Jennifer', 'Stephanie', 'Christina', 'Heather', 'Amber', 'Melissa',
                          'Maria', 'Sofia', 'Isabella', 'Valentina', 'Camila', 'Ana', 'Lucia', 'Elena', 'Carmen', 'Rosa',
                          'Yuki', 'Sakura', 'Hana', 'Mei', 'Lin', 'Fatima', 'Aisha', 'Layla', 'Noor', 'Zara']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                  'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
                  'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
                  'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
                  'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts',
                  'Müller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Rossi', 'Ferrari', 'Esposito', 'Colombo', 'Romano',
                  'Tanaka', 'Yamamoto', 'Watanabe', 'Takahashi', 'Kobayashi', 'Kimura', 'Hayashi', 'Saito', 'Sasaki', 'Yamaguchi']
    
    teams_by_sport = {
        'Football': ['New England Patriots', 'Dallas Cowboys', 'Green Bay Packers', 'San Francisco 49ers', 'Chicago Bears', 'Miami Dolphins', 'Denver Broncos', 'Seattle Seahawks', 'Pittsburgh Steelers', 'Las Vegas Raiders'],
        'Basketball': ['Los Angeles Lakers', 'Boston Celtics', 'Chicago Bulls', 'Golden State Warriors', 'Miami Heat', 'San Antonio Spurs', 'New York Knicks', 'Philadelphia 76ers', 'Brooklyn Nets', 'Phoenix Suns'],
        'Soccer': ['Manchester United', 'Real Madrid', 'Barcelona', 'Bayern Munich', 'Liverpool', 'Paris Saint-Germain', 'Juventus', 'AC Milan', 'Manchester City', 'Inter Milan'],
        'Baseball': ['New York Yankees', 'Boston Red Sox', 'Los Angeles Dodgers', 'Chicago Cubs', 'San Francisco Giants', 'St. Louis Cardinals', 'Atlanta Braves', 'Houston Astros', 'Philadelphia Phillies', 'Detroit Tigers'],
        'Tennis': ['ATP Tour', 'WTA Tour', 'ITF Circuit', 'Grand Slam Events', 'Masters 1000', 'Premier Mandatory', 'International Series', 'Challenger Tour', 'Futures Tour', 'Davis Cup Team'],
        'Hockey': ['Toronto Maple Leafs', 'Montreal Canadiens', 'Boston Bruins', 'Detroit Red Wings', 'Chicago Blackhawks', 'New York Rangers', 'Pittsburgh Penguins', 'Edmonton Oilers', 'Colorado Avalanche', 'Tampa Bay Lightning'],
        'Rugby': ['New Zealand All Blacks', 'South Africa Springboks', 'England Rugby', 'Ireland Rugby', 'Wales Rugby', 'Australia Wallabies', 'France Rugby', 'Scotland Rugby', 'Argentina Pumas', 'Japan Brave Blossoms'],
        'Cricket': ['Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bangalore', 'Kolkata Knight Riders', 'Delhi Capitals', 'Rajasthan Royals', 'Punjab Kings', 'Sunrisers Hyderabad', 'Gujarat Titans', 'Lucknow Super Giants'],
        'Swimming': ['USA Swimming', 'Australian Dolphins', 'British Swimming', 'Italian Swimming', 'French Swimming', 'Japanese Swimming', 'Chinese Swimming', 'German Swimming', 'Dutch Swimming', 'Swedish Swimming'],
        'Athletics': ['USA Track & Field', 'Athletics Kenya', 'British Athletics', 'Athletics Australia', 'German Athletics', 'French Athletics', 'Japanese Athletics', 'Chinese Athletics', 'Ethiopian Athletics', 'Jamaican Athletics']
    }
    
    countries = ['USA', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'Spain', 'Brazil', 'Japan', 'China',
                 'Italy', 'Netherlands', 'Argentina', 'Mexico', 'South Korea', 'India', 'Russia', 'Sweden', 'Norway', 'Belgium',
                 'Portugal', 'Switzerland', 'Austria', 'Poland', 'Czech Republic', 'Denmark', 'Finland', 'Ireland', 'New Zealand', 'South Africa']
    
    data = []
    for i in range(2000):
        sport = random.choice(sports)
        position = random.choice(positions[sport])
        gender = random.choice(['Male', 'Female'])
        
        # Age distribution varies by sport
        if sport in ['Swimming', 'Athletics', 'Tennis']:
            age = np.random.randint(16, 38)
        elif sport in ['Football', 'Rugby']:
            age = np.random.randint(20, 36)
        else:
            age = np.random.randint(18, 42)
        
        # Physical attributes based on sport and gender
        if gender == 'Male':
            if sport in ['Basketball']:
                height = round(np.random.normal(198, 8), 1)
                weight = round(np.random.normal(100, 12), 1)
            elif sport in ['Football', 'Rugby']:
                height = round(np.random.normal(188, 10), 1)
                weight = round(np.random.normal(105, 20), 1)
            elif sport in ['Swimming']:
                height = round(np.random.normal(188, 7), 1)
                weight = round(np.random.normal(82, 8), 1)
            else:
                height = round(np.random.normal(180, 10), 1)
                weight = round(np.random.normal(78, 12), 1)
            first_name = random.choice(first_names_male)
        else:
            if sport in ['Basketball']:
                height = round(np.random.normal(180, 7), 1)
                weight = round(np.random.normal(72, 8), 1)
            elif sport in ['Swimming']:
                height = round(np.random.normal(175, 6), 1)
                weight = round(np.random.normal(65, 7), 1)
            else:
                height = round(np.random.normal(168, 8), 1)
                weight = round(np.random.normal(62, 10), 1)
            first_name = random.choice(first_names_female)
        
        # Ensure realistic bounds
        height = max(150, min(height, 230))
        weight = max(45, min(weight, 150))
        
        bmi = round(weight / ((height/100) ** 2), 1)
        
        # Generate injury history based on age and sport risk
        base_injury_rate = {'Football': 3.5, 'Rugby': 3.2, 'Soccer': 2.8, 'Basketball': 2.5, 
                           'Hockey': 2.7, 'Baseball': 2.0, 'Tennis': 2.2, 'Cricket': 1.8,
                           'Swimming': 1.5, 'Athletics': 2.3}
        
        years_pro = max(1, min(age - 18, np.random.randint(1, 22)))
        expected_injuries = int(years_pro * base_injury_rate.get(sport, 2.0) * np.random.uniform(0.3, 1.5))
        num_injuries = max(1, min(expected_injuries, 15))
        
        injury_list = random.sample(injury_types, min(num_injuries, len(injury_types)))
        
        # Current injury status
        has_current_injury = random.random() > 0.65
        current_injury = random.choice(injury_types) if has_current_injury else 'None'
        current_injury_severity = random.choice(injury_severity) if has_current_injury else 'N/A'
        
        # Risk score calculation based on multiple factors
        age_factor = 0.1 if age < 25 else (0.2 if age < 30 else (0.3 if age < 35 else 0.4))
        injury_factor = min(num_injuries * 0.05, 0.4)
        sport_factor = {'Football': 0.15, 'Rugby': 0.15, 'Soccer': 0.1, 'Basketball': 0.1, 
                       'Hockey': 0.12, 'Baseball': 0.08, 'Tennis': 0.08, 'Cricket': 0.06,
                       'Swimming': 0.05, 'Athletics': 0.08}.get(sport, 0.1)
        
        risk_score = round(min(age_factor + injury_factor + sport_factor + np.random.uniform(-0.1, 0.2), 1.0), 2)
        risk_score = max(0.05, risk_score)
        
        player = {
            'player_id': f'PLY{str(i+1).zfill(5)}',
            'first_name': first_name,
            'last_name': random.choice(last_names),
            'age': age,
            'gender': gender,
            'height_cm': height,
            'weight_kg': weight,
            'bmi': bmi,
            'sport': sport,
            'position': position,
            'team': random.choice(teams_by_sport[sport]),
            'country': random.choice(countries),
            'years_professional': years_pro,
            'training_hours_weekly': np.random.randint(10, 45),
            'current_injury': current_injury,
            'injury_severity': current_injury_severity,
            'injury_date': (datetime.now() - timedelta(days=np.random.randint(1, 180))).strftime('%Y-%m-%d') if has_current_injury else 'N/A',
            'recovery_status': random.choice(recovery_status),
            'treatment_type': random.choice(treatment_types),
            'total_injuries_career': num_injuries,
            'injury_history': ', '.join(injury_list),
            'days_missed_current_season': np.random.randint(0, 120) if has_current_injury else np.random.randint(0, 30),
            'risk_score': risk_score,
            'fitness_level': round(np.random.uniform(55, 100), 1),
            'previous_surgeries': np.random.randint(0, min(num_injuries // 2 + 1, 6)),
            'chronic_conditions': random.choice(['None', 'None', 'None', 'Arthritis', 'Tendinitis', 'Back Issues', 'Knee Issues', 'Shoulder Instability']),
            'last_medical_checkup': (datetime.now() - timedelta(days=np.random.randint(1, 120))).strftime('%Y-%m-%d'),
            'rehabilitation_progress': round(np.random.uniform(0, 100), 1) if has_current_injury else 100.0,
            'performance_index': round(np.random.uniform(45, 100), 1),
            'salary_usd': np.random.randint(50000, 15000000),
            'contract_years_remaining': np.random.randint(0, 7),
            'dominant_side': random.choice(['Right', 'Left', 'Ambidextrous']),
            'blood_type': random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
            'insurance_status': random.choice(['Fully Covered', 'Partially Covered', 'Premium Plan', 'Basic Plan']),
            'medical_clearance': random.choice(['Cleared', 'Pending', 'Restricted']) if has_current_injury else 'Cleared',
            'injury_status': 'Injured' if has_current_injury else 'Healthy', # New field for financial analysis
            'recovery_time': np.random.randint(7, 90) if has_current_injury else 0, # Simplified recovery time, will be refined
            'medical_cost': np.random.uniform(500, 20000) if has_current_injury else 0, # Simplified medical cost
            'lost_productivity_cost': np.random.uniform(1000, 50000) if has_current_injury else 0, # Simplified productivity cost
        }
        data.append(player)
    
    return pd.DataFrame(data)

# Initialize dataset
df = generate_player_dataset()
df_players = df # Assign to df_players for use in financial_impact

# ==========================================
# ADVANCED CHATBOT KNOWLEDGE BASE
# ==========================================
CHATBOT_KNOWLEDGE = {
    # Knee Injuries
    'acl': {
        'full_name': 'Anterior Cruciate Ligament (ACL) Tear',
        'description': 'The ACL is one of the four major ligaments of the knee. ACL injuries are among the most common and devastating sports injuries, particularly in sports involving cutting, pivoting, and sudden direction changes.',
        'symptoms': 'Immediate severe pain, a loud "pop" sound at the time of injury, rapid swelling within hours, loss of range of motion, feeling of instability or "giving way" in the knee, difficulty bearing weight',
        'causes': 'Sudden stops or direction changes, pivoting with foot firmly planted, awkward landings from jumps, direct collision or impact to the knee, hyperextension of the knee',
        'treatment': 'Initial RICE protocol (Rest, Ice, Compression, Elevation), anti-inflammatory medications, physical therapy for mild sprains, surgical reconstruction using grafts (patellar tendon, hamstring, or cadaver) for complete tears, extensive rehabilitation program post-surgery',
        'recovery_time': 'Non-surgical: 3-6 months with physical therapy. Surgical: 6-12 months for full return to sports, with some athletes taking up to 18 months for complete recovery',
        'prevention': 'Neuromuscular training programs, proper warm-up before activity, strengthening exercises for quadriceps and hamstrings, learning proper landing and cutting techniques, wearing appropriate footwear, using knee braces if recommended',
        'sports_at_risk': 'Soccer, basketball, football, skiing, volleyball, tennis, gymnastics',
        'statistics': 'Approximately 200,000 ACL injuries occur annually in the US. Female athletes are 2-8 times more likely to tear their ACL than male athletes in the same sports.',
        'long_term': "Increased risk of knee osteoarthritis, potential for re-injury (especially within first 2 years), may require lifestyle modifications for some athletes"
    },
    'mcl': {
        'full_name': 'Medial Collateral Ligament (MCL) Sprain',
        'description': 'The MCL runs along the inner side of the knee and prevents the knee from bending inward. MCL sprains are common in contact sports and skiing.',
        'symptoms': 'Pain on the inner side of the knee, swelling, stiffness, feeling of instability, tenderness along the inner knee, pain when bending the knee',
        'causes': 'Direct blow to the outer knee, twisting movements, valgus stress (force pushing knee inward)',
        'treatment': 'RICE protocol, hinged knee brace for stability, physical therapy, rarely requires surgery (usually heals well without surgical intervention)',
        'recovery_time': 'Grade 1: 1-3 weeks, Grade 2: 3-6 weeks, Grade 3: 6-10 weeks. Most MCL injuries heal without surgery.',
        'prevention': 'Strengthening inner thigh muscles, proper warm-up, using knee braces in high-risk activities',
        'sports_at_risk': 'Football, hockey, skiing, soccer, wrestling'
    },
    'meniscus': {
        'full_name': 'Meniscus Tear',
        'description': 'The menisci are two C-shaped pieces of cartilage that act as shock absorbers between the thighbone and shinbone. Tears can occur from acute trauma or degenerative changes over time.',
        'symptoms': 'Pain especially when twisting or rotating the knee, swelling and stiffness, difficulty straightening the knee fully, catching or locking sensation, feeling of instability',
        'causes': 'Forceful twisting or rotating of the knee, deep squatting, heavy lifting, degenerative changes with aging, direct trauma',
        'treatment': 'Conservative treatment with RICE, physical therapy, and anti-inflammatory medications. Surgical options include arthroscopic partial meniscectomy (removal of torn portion) or meniscus repair. Treatment depends on tear location, size, and patient factors.',
        'recovery_time': 'Conservative: 4-8 weeks. Partial meniscectomy: 3-6 weeks. Meniscus repair: 3-6 months',
        'prevention': 'Maintaining strong leg muscles, proper warm-up, avoiding deep squatting under heavy loads, using proper technique in sports',
        'sports_at_risk': 'Soccer, football, basketball, tennis, skiing'
    },
    'patellar': {
        'full_name': 'Patellar Tendinitis (Jumper\'s Knee)',
        'description': 'An overuse injury affecting the tendon connecting the kneecap to the shinbone. Common in sports requiring frequent jumping.',
        'symptoms': 'Pain at the base of the kneecap, pain that worsens with activity (especially jumping, running, or climbing stairs), stiffness after sitting, tenderness when pressing on the tendon',
        'causes': 'Repetitive stress from jumping and landing, sudden increase in training intensity, tight leg muscles, muscle imbalances',
        'treatment': 'Rest and activity modification, ice therapy, physical therapy focusing on eccentric exercises, patellar tendon straps, in severe cases: PRP injections or surgery',
        'recovery_time': 'Mild cases: 2-4 weeks. Moderate: 6-12 weeks. Severe/chronic: several months to over a year',
        'prevention': 'Gradual increase in training load, proper warm-up, stretching and strengthening exercises, appropriate footwear',
        'sports_at_risk': 'Basketball, volleyball, long jump, high jump, running'
    },
    
    # Ankle Injuries
    'ankle': {
        'full_name': 'Ankle Sprain',
        'description': 'One of the most common sports injuries, ankle sprains occur when the ligaments supporting the ankle stretch beyond their limits and tear. Most commonly affects the lateral (outside) ligaments.',
        'symptoms': 'Pain especially when bearing weight, swelling, bruising, restricted range of motion, instability, tenderness to touch, popping sensation at time of injury',
        'causes': 'Rolling, twisting, or turning the ankle awkwardly, landing incorrectly after a jump, walking or exercising on uneven surfaces, another person stepping on your foot',
        'treatment': 'RICE protocol immediately after injury, immobilization with brace or cast for severe sprains, physical therapy for rehabilitation, surgery rare but may be needed for chronic instability',
        'recovery_time': 'Grade 1 (mild): 1-3 weeks. Grade 2 (moderate): 3-6 weeks. Grade 3 (severe): 6-12 weeks or longer',
        'prevention': 'Ankle strengthening exercises, balance training, wearing appropriate footwear, ankle braces for high-risk activities, proper warm-up',
        'sports_at_risk': 'Basketball, soccer, volleyball, trail running, football, tennis'
    },
    'high_ankle': {
        'full_name': 'High Ankle Sprain (Syndesmosis Injury)',
        'description': 'Involves the ligaments above the ankle that connect the tibia and fibula. More severe than regular ankle sprains and takes longer to heal.',
        'symptoms': 'Pain above the ankle, pain when rotating the foot outward, difficulty pushing off while walking, swelling, bruising higher up the leg than typical ankle sprain',
        'causes': 'External rotation of the foot with leg fixed, twisting injury, direct impact',
        'treatment': 'Extended immobilization, walking boot, crutches, physical therapy, surgery if there is significant separation between tibia and fibula',
        'recovery_time': '6-12 weeks minimum, often 3-6 months for full return to sport',
        'prevention': 'Ankle stability exercises, proper technique in cutting and pivoting, appropriate footwear',
        'sports_at_risk': 'Football, hockey, soccer, skiing'
    },
    
    # Muscle Injuries
    'hamstring': {
        'full_name': 'Hamstring Strain',
        'description': 'A strain or tear to one or more of the three hamstring muscles at the back of the thigh. One of the most common and recurrent sports injuries.',
        'symptoms': 'Sudden sharp pain in the back of the thigh, popping or snapping sensation, swelling, bruising, weakness, difficulty walking or bending the knee',
        'causes': 'Overloading the muscle during sprinting or acceleration, inadequate warm-up, muscle fatigue, poor flexibility, muscle imbalances between quadriceps and hamstrings',
        'treatment': 'RICE protocol, gentle stretching when pain allows, progressive strengthening exercises, physical therapy, PRP injections for severe strains, surgery rarely needed for complete tears',
        'recovery_time': 'Grade 1: 1-3 weeks. Grade 2: 3-8 weeks. Grade 3: 3-6 months. Recurrence rate is high (up to 30%)',
        'prevention': 'Nordic hamstring exercises, proper warm-up, maintaining flexibility, gradual increase in training intensity, addressing muscle imbalances, adequate recovery between sessions',
        'sports_at_risk': 'Sprinting, soccer, football, basketball, tennis, track and field'
    },
    'quadriceps': {
        'full_name': 'Quadriceps Strain',
        'description': 'Injury to the large muscle group at the front of the thigh, responsible for knee extension and hip flexion.',
        'symptoms': 'Pain in front of thigh, swelling, bruising, weakness in knee extension, difficulty walking or climbing stairs',
        'causes': 'Forceful contraction during sprinting or kicking, direct impact, overstretching',
        'treatment': 'RICE, physical therapy, progressive strengthening, massage therapy',
        'recovery_time': 'Grade 1: 1-2 weeks. Grade 2: 2-6 weeks. Grade 3: 6-12 weeks',
        'prevention': 'Proper warm-up, stretching, balanced leg strengthening, gradual training progression',
        'sports_at_risk': 'Soccer, football, track and field, martial arts'
    },
    'groin': {
        'full_name': 'Groin Pull (Adductor Strain)',
        'description': 'Strain of the adductor muscles on the inner thigh, which help bring the legs together.',
        'symptoms': 'Pain and tenderness in the inner thigh and groin area, pain when bringing legs together, swelling, bruising, weakness',
        'causes': 'Sudden change of direction, overstretching during activities like kicking or skating, inadequate warm-up',
        'treatment': 'Rest, ice, compression, physical therapy, gradual return to activity',
        'recovery_time': 'Mild: 1-3 weeks. Moderate: 3-6 weeks. Severe: 6-12 weeks',
        'prevention': 'Hip flexibility exercises, adductor strengthening, proper warm-up, core stability work',
        'sports_at_risk': 'Soccer, hockey, football, tennis, swimming (breaststroke)'
    },
    'calf': {
        'full_name': 'Calf Strain (Gastrocnemius/Soleus)',
        'description': 'Strain to the calf muscles, often called "tennis leg" when occurring suddenly during activity.',
        'symptoms': 'Sudden pain in the back of the lower leg, popping sensation, difficulty walking or standing on toes, swelling, bruising',
        'causes': 'Sudden push-off movements, lunging forward, starting to sprint, jumping',
        'treatment': 'RICE, heel lifts initially, gradual stretching and strengthening, physical therapy',
        'recovery_time': 'Grade 1: 1-2 weeks. Grade 2: 3-6 weeks. Grade 3: 6-12 weeks',
        'prevention': 'Calf stretching and strengthening, proper warm-up, gradual training progression',
        'sports_at_risk': 'Tennis, running, soccer, basketball, sprinting'
    },
    
    # Shoulder Injuries
    'rotator_cuff': {
        'full_name': 'Rotator Cuff Injury',
        'description': 'The rotator cuff is a group of four muscles and tendons that stabilize the shoulder joint. Injuries range from inflammation (tendinitis) to partial or complete tears.',
        'symptoms': 'Pain at rest and at night especially when lying on affected shoulder, pain when lifting and lowering arm, weakness when lifting or rotating arm, crackling sensation with movement, limited range of motion',
        'causes': 'Repetitive overhead motions, throwing sports, weightlifting, acute trauma from falling, degenerative changes with age',
        'treatment': 'Rest and activity modification, ice and anti-inflammatory medications, physical therapy for strengthening, corticosteroid injections, surgical repair for complete tears or failed conservative treatment',
        'recovery_time': 'Conservative treatment: 6-12 weeks. Post-surgical recovery: 4-6 months for rehabilitation, 9-12 months for full return to sport',
        'prevention': 'Shoulder strengthening exercises, proper throwing mechanics, avoiding repetitive overhead activities, maintaining flexibility',
        'sports_at_risk': 'Baseball, tennis, swimming, volleyball, football (quarterbacks), weightlifting'
    },
    'shoulder_dislocation': {
        'full_name': 'Shoulder Dislocation',
        'description': 'Complete displacement of the humeral head from the glenoid socket. Most commonly occurs anteriorly (forward).',
        'symptoms': 'Intense pain, visible deformity, inability to move the arm, swelling, numbness or tingling in arm or fingers',
        'causes': 'Direct blow to shoulder, falling on outstretched arm, extreme rotation of the arm',
        'treatment': 'Immediate medical attention for reduction (putting joint back in place), immobilization in sling, physical therapy, surgery may be needed for recurrent dislocations',
        'recovery_time': 'Initial healing: 2-3 weeks. Full recovery: 3-4 months. Athletes with recurrent instability may need surgical stabilization.',
        'prevention': 'Shoulder strengthening, avoiding extreme ranges of motion, protective equipment in contact sports',
        'sports_at_risk': 'Football, hockey, rugby, skiing, basketball'
    },
    'labrum': {
        'full_name': 'Labral Tear (SLAP Tear)',
        'description': 'Tear of the labrum, the ring of cartilage surrounding the shoulder socket. SLAP stands for Superior Labrum Anterior to Posterior.',
        'symptoms': 'Deep aching pain in shoulder, pain with overhead activities, catching or locking sensation, decreased strength, clicking or popping',
        'causes': 'Repetitive overhead motions, falling on outstretched arm, forceful pulling or pushing',
        'treatment': 'Physical therapy, anti-inflammatory medications, activity modification, arthroscopic surgery for significant tears',
        'recovery_time': 'Conservative: 6-12 weeks. Post-surgical: 4-6 months',
        'prevention': 'Proper throwing mechanics, shoulder strengthening and flexibility, adequate rest between activities',
        'sports_at_risk': 'Baseball, tennis, swimming, volleyball, weightlifting'
    },
    
    # Head Injuries
    'concussion': {
        'full_name': 'Concussion (Mild Traumatic Brain Injury)',
        'description': 'A brain injury caused by a blow to the head or body that causes the brain to move rapidly within the skull. Effects are usually temporary but require proper management.',
        'symptoms': 'Headache or pressure in head, temporary loss of consciousness, confusion or "foggy" feeling, amnesia, dizziness, ringing in ears, nausea or vomiting, slurred speech, delayed response to questions, fatigue, concentration difficulties, memory problems, irritability, sensitivity to light and noise, sleep disturbances, depression or anxiety',
        'causes': 'Direct blow to the head, face, or neck; body impact that causes head to move rapidly; whiplash-type injuries',
        'treatment': 'Immediate removal from activity, cognitive and physical rest, gradual return-to-activity protocol supervised by healthcare professional, symptom management, neuropsychological testing',
        'recovery_time': 'Most symptoms resolve within 7-10 days, though adolescents may take longer. Some individuals experience post-concussion syndrome lasting weeks to months.',
        'prevention': 'Proper technique in contact sports, appropriate protective equipment (helmets), rule enforcement against dangerous plays, baseline concussion testing, education about symptoms',
        'red_flags': 'Seek emergency care immediately if: loss of consciousness for more than 30 seconds, seizures, repeated vomiting, worsening headache, slurred speech, confusion that worsens, weakness or numbness, unequal pupils',
        'sports_at_risk': 'Football, hockey, soccer, rugby, boxing, basketball, lacrosse, cycling',
        'return_to_play': 'Must be completely symptom-free at rest and during exertion before beginning graduated return-to-play protocol. Process typically takes minimum 1 week after becoming symptom-free.'
    },
    
    # Foot and Lower Leg
    'achilles': {
        'full_name': 'Achilles Tendon Injury',
        'description': 'Injuries to the Achilles tendon range from tendinitis (inflammation) to partial or complete rupture. The Achilles is the largest tendon in the body, connecting calf muscles to the heel.',
        'symptoms': 'Pain above the heel especially with walking or running, stiffness in morning, swelling, tenderness to touch. For rupture: sudden pop, severe pain, inability to push off or walk normally',
        'causes': 'Overuse, sudden increase in activity, tight calf muscles, bone spurs, improper footwear, certain medications (fluoroquinolone antibiotics)',
        'treatment': 'Tendinitis: RICE, heel lifts, physical therapy, eccentric exercises. Rupture: surgical repair or casting (functional treatment), followed by extensive rehabilitation',
        'recovery_time': 'Tendinitis: 6-12 weeks. Rupture: 6-12 months for full recovery',
        'prevention': 'Gradual training progression, calf stretching and strengthening, proper footwear, avoiding sudden increases in training',
        'sports_at_risk': 'Running, basketball, tennis, soccer, dance'
    },
    'plantar_fasciitis': {
        'full_name': 'Plantar Fasciitis',
        'description': 'Inflammation of the plantar fascia, a thick band of tissue running along the bottom of the foot connecting the heel to the toes.',
        'symptoms': 'Stabbing pain near the heel, especially with first steps in morning or after long periods of rest, pain that decreases with activity but may return after prolonged standing or activity',
        'causes': 'Overuse, tight calf muscles, high arches or flat feet, obesity, improper footwear, running on hard surfaces',
        'treatment': 'Rest, stretching exercises, night splints, orthotics, physical therapy, anti-inflammatory medications, corticosteroid injections, rarely surgery',
        'recovery_time': 'Several months to over a year for complete resolution. Most cases resolve within 10-12 months with conservative treatment.',
        'prevention': 'Proper footwear with arch support, maintaining healthy weight, stretching before activity, gradual increase in running distance',
        'sports_at_risk': 'Running, basketball, dancing, tennis'
    },
    'shin_splints': {
        'full_name': 'Shin Splints (Medial Tibial Stress Syndrome)',
        'description': 'Pain along the inner edge of the shinbone (tibia), caused by inflammation of muscles, tendons, and bone tissue around the tibia.',
        'symptoms': 'Pain along inner border of shin, mild swelling, pain during exercise that may improve with rest, tenderness along shinbone',
        'causes': 'Overuse, sudden increase in activity, flat feet, improper footwear, running on hard surfaces, biomechanical issues',
        'treatment': 'Rest, ice, anti-inflammatory medications, stretching and strengthening exercises, orthotics if needed, gradual return to activity',
        'recovery_time': '2-6 weeks with proper rest and treatment',
        'prevention': 'Gradual increase in training, proper footwear, cross-training, strengthening exercises, avoiding hard surfaces',
        'sports_at_risk': 'Running, dancing, military training, tennis, basketball'
    },
    'stress_fracture': {
        'full_name': 'Stress Fracture',
        'description': 'Small cracks in bone caused by repetitive force and overuse, commonly occurring in weight-bearing bones of the lower leg and foot.',
        'symptoms': 'Pain that develops gradually and worsens with activity, pain that improves with rest, swelling, tenderness at a specific spot',
        'causes': 'Repetitive impact activities, sudden increase in training, inadequate rest, poor nutrition (low calcium/vitamin D), biomechanical issues, improper footwear',
        'treatment': 'Rest (usually 6-8 weeks without weight-bearing activities), protective footwear, crutches if needed, adequate nutrition, gradual return to activity',
        'recovery_time': '6-8 weeks minimum, some locations (e.g., navicular, fifth metatarsal) may take 3-6 months',
        'prevention': 'Gradual training progression, proper footwear, adequate nutrition, cross-training, listening to body signals',
        'sports_at_risk': 'Running, basketball, track and field, gymnastics, dance, tennis'
    },
    
    # Elbow Injuries
    'tennis_elbow': {
        'full_name': 'Tennis Elbow (Lateral Epicondylitis)',
        'description': 'Overuse injury causing pain on the outside of the elbow, resulting from repetitive wrist and arm motions.',
        'symptoms': 'Pain on the outside of the elbow, weak grip strength, pain that worsens with forearm activities, stiffness in the elbow',
        'causes': 'Repetitive arm and wrist movements, improper technique in racket sports, repetitive computer mouse use, gripping activities',
        'treatment': 'Rest, ice, anti-inflammatory medications, physical therapy, forearm bracing, corticosteroid injections, rarely surgery',
        'recovery_time': '6-24 months for full recovery, though most improve significantly within 6-12 weeks with treatment',
        'prevention': 'Proper technique, appropriate equipment sizing, strengthening forearm muscles, taking breaks during repetitive activities',
        'sports_at_risk': 'Tennis, golf, baseball, racquetball, weightlifting'
    },
    'golfers_elbow': {
        'full_name': 'Golfer\'s Elbow (Medial Epicondylitis)',
        'description': 'Pain on the inside of the elbow caused by overuse of forearm muscles that flex the wrist and fingers.',
        'symptoms': 'Pain on the inside of elbow, weakness in hands and wrists, stiffness, numbness or tingling in fingers',
        'causes': 'Repetitive wrist flexion, gripping, or throwing movements',
        'treatment': 'Rest, ice, stretching, strengthening exercises, bracing, rarely surgery',
        'recovery_time': '6-12 weeks with proper treatment',
        'prevention': 'Proper technique, forearm strengthening, adequate rest between activities',
        'sports_at_risk': 'Golf, tennis, baseball, weightlifting, rock climbing'
    },
    
    # Back Injuries
    'lower_back': {
        'full_name': 'Lower Back Strain',
        'description': 'Injury to the muscles, tendons, or ligaments in the lower back region, often resulting from overuse, improper lifting, or sudden movements.',
        'symptoms': 'Pain in the lower back that may spread to the buttocks, muscle spasms, stiffness, pain that worsens with movement, difficulty standing straight',
        'causes': 'Heavy lifting with poor form, sudden movements, repetitive stress, poor posture, weak core muscles',
        'treatment': 'Rest initially, ice/heat, anti-inflammatory medications, physical therapy, core strengthening, posture correction, massage',
        'recovery_time': 'Most cases resolve within 2-6 weeks with proper treatment',
        'prevention': 'Proper lifting technique, core strengthening, maintaining flexibility, good posture, ergonomic workplace setup',
        'sports_at_risk': 'Weightlifting, golf, tennis, rowing, gymnastics'
    },
    'herniated_disc': {
        'full_name': 'Herniated Disc',
        'description': 'When the soft inner portion of a spinal disc pushes through a crack in the tougher exterior, potentially pressing on nearby nerves.',
        'symptoms': 'Arm or leg pain (depending on location), numbness or tingling, weakness in affected muscles, pain that worsens with certain movements',
        'causes': 'Gradual wear and tear, improper lifting, repetitive strain, sudden trauma',
        'treatment': 'Conservative treatment (rest, physical therapy, medications) in most cases, epidural injections, surgery for severe cases not responding to conservative treatment',
        'recovery_time': 'Conservative: 4-6 weeks to months. Surgical: several months for full recovery',
        'prevention': 'Proper lifting technique, core strengthening, maintaining healthy weight, good posture',
        'sports_at_risk': 'Weightlifting, golf, football, gymnastics'
    },
    
    # General Prevention and Recovery
    'prevention': {
        'general': '''**Comprehensive Injury Prevention Strategies:**

**1. Proper Warm-Up (10-15 minutes):**
- Light cardiovascular activity (jogging, cycling)
- Dynamic stretching (leg swings, arm circles, lunges)
- Sport-specific movements at gradually increasing intensity

**2. Cool-Down and Recovery:**
- Gradual decrease in activity intensity
- Static stretching
- Foam rolling for muscle recovery
- Adequate hydration and nutrition

**3. Progressive Training:**
- Follow the 10% rule: increase training load by no more than 10% per week
- Allow adequate rest between intense training sessions
- Periodize training (varying intensity throughout the season)

**4. Strength and Conditioning:**
- Focus on functional movements
- Address muscle imbalances
- Core stability training
- Sport-specific strength work

**5. Flexibility and Mobility:**
- Regular stretching routine
- Yoga or mobility work
- Address areas of restriction

**6. Proper Technique:**
- Work with qualified coaches
- Video analysis of movements
- Regular technique refinement

**7. Equipment and Environment:**
- Properly fitted shoes and equipment
- Appropriate protective gear
- Safe playing surfaces

**8. Nutrition and Hydration:**
- Adequate protein for muscle repair
- Calcium and vitamin D for bone health
- Anti-inflammatory foods (omega-3 fatty acids)
- Proper hydration before, during, and after activity

**9. Rest and Sleep:**
- 7-9 hours of quality sleep
- Rest days in training schedule
- Listen to your body''',
        'warmup': 'A proper warm-up should last 10-15 minutes and include: light cardiovascular activity to raise heart rate, dynamic stretching targeting major muscle groups, sport-specific movements at gradually increasing intensity, and mental preparation for activity.',
        'nutrition': '''**Nutrition for Injury Prevention and Recovery:**

- **Protein**: 1.2-2.0 g/kg body weight for athletes; essential for muscle repair
- **Calcium**: 1000-1300 mg daily for bone health
- **Vitamin D**: 600-800 IU daily; helps calcium absorption
- **Omega-3 Fatty Acids**: Reduce inflammation; found in fish, nuts, seeds
- **Vitamin C**: Supports collagen synthesis; important for tendons and ligaments
- **Zinc**: Supports immune function and tissue repair
- **Hydration**: Drink before you\'re thirsty; urine should be light yellow'''
    },
    'recovery': {
        'phases': '''**Recovery Phases:**

**1. Acute Phase (0-72 hours):**
- Goal: Control pain and inflammation
- PRICE protocol (Protection, Rest, Ice, Compression, Elevation)
- Avoid activities that worsen symptoms

**2. Subacute Phase (72 hours - 2 weeks):**
- Goal: Restore range of motion
- Gentle exercises within pain-free range
- Begin physical therapy
- Progress weight-bearing as tolerated

**3. Strengthening Phase (2-6+ weeks):**
- Goal: Rebuild strength and endurance
- Progressive resistance exercises
- Address muscle imbalances
- Cardiovascular conditioning maintenance

**4. Return to Sport Phase (varies):**
- Sport-specific training
- Gradual return to practice
- Full clearance for competition
- Ongoing maintenance program''',
        'tips': '''**Key Recovery Tips:**

1. **Follow Medical Advice**: Adhere to your healthcare provider\'s recommendations
2. **Be Patient**: Rushing return increases re-injury risk
3. **Stay Positive**: Mental attitude affects physical recovery
4. **Maintain Fitness**: Cross-train within restrictions
5. **Prioritize Sleep**: Growth hormone release occurs during deep sleep
6. **Optimize Nutrition**: Support healing with proper nutrients
7. **Attend Rehabilitation**: Complete all physical therapy sessions
8. **Communicate**: Report new symptoms or concerns promptly
9. **Plan Return**: Work with trainers on gradual return-to-play protocol
10. **Prevent Re-injury**: Continue maintenance exercises after recovery'''
    },
    'rice': {
        'description': '''**R.I.C.E. Protocol for Acute Injuries:**

**R - Rest:**
- Stop the activity immediately
- Avoid putting weight on injured area
- Use crutches or sling if necessary
- Duration: 24-48 hours minimum

**I - Ice:**
- Apply ice or cold pack wrapped in cloth
- 15-20 minutes every 2-3 hours
- Continue for 48-72 hours
- Never apply ice directly to skin

**C - Compression:**
- Use elastic bandage to wrap the injured area
- Should be snug but not too tight
- Loosen if numbness, tingling, or increased pain occurs
- Helps control swelling

**E - Elevation:**
- Raise injured area above heart level when possible
- Use pillows for support
- Helps reduce swelling by promoting fluid drainage

**Note:** Some experts now recommend P.R.I.C.E. (Protection, Rest, Ice, Compression, Elevation) or P.O.L.I.C.E. (Protection, Optimal Loading, Ice, Compression, Elevation) for modern approach.'''
    }
}

INJURY_IMAGE_ANALYSIS = {
    'bruise': {
        'name': 'Bruise / Contusion',
        'description': 'A bruise (contusion) occurs when small blood vessels under the skin break due to impact, causing blood to leak into surrounding tissues.',
        'severity_levels': {
            'mild': 'Small area, light purple/blue coloring, minimal swelling',
            'moderate': 'Medium-sized area, deep purple/blue, noticeable swelling',
            'severe': 'Large area, very dark coloring, significant swelling, possible underlying damage'
        },
        'immediate_care': [
            'Apply ice wrapped in cloth for 15-20 minutes every hour',
            'Elevate the injured area above heart level if possible',
            'Rest and avoid putting pressure on the bruised area',
            'Use compression bandage if swelling is present'
        ],
        'recovery_tips': [
            'After 48 hours, apply warm compress to increase blood flow',
            'Gentle massage around (not on) the bruise can help',
            'Arnica gel or cream may help reduce discoloration',
            'Most bruises heal within 2-4 weeks'
        ],
        'warning_signs': [
            'Bruise doesn\'t improve after 2 weeks',
            'Extremely painful or swelling increases',
            'Bruise appears without known injury',
            'Signs of infection (warmth, pus, fever)'
        ],
        'estimated_recovery': '1-4 weeks depending on severity'
    },
    'swelling': {
        'name': 'Swelling / Edema',
        'description': 'Swelling occurs when fluid accumulates in tissues, often as a response to injury, inflammation, or overuse.',
        'severity_levels': {
            'mild': 'Slight puffiness, normal skin color, minimal discomfort',
            'moderate': 'Noticeable swelling, some skin tightness, moderate discomfort',
            'severe': 'Significant swelling, skin appears stretched, severe discomfort or pain'
        },
        'immediate_care': [
            'Apply RICE protocol: Rest, Ice, Compression, Elevation',
            'Ice for 15-20 minutes every 2-3 hours',
            'Use elastic bandage for compression (not too tight)',
            'Keep the area elevated above heart level'
        ],
        'recovery_tips': [
            'Stay hydrated to help flush excess fluid',
            'Reduce salt intake to minimize fluid retention',
            'Gentle movement can help reduce swelling after initial phase',
            'Consider anti-inflammatory medication if approved by doctor'
        ],
        'warning_signs': [
            'Swelling doesn\'t reduce after 48-72 hours',
            'Numbness or tingling in the area',
            'Skin becomes very red, hot, or develops streaks',
            'Inability to move or bear weight on the affected area'
        ],
        'estimated_recovery': '2-7 days for mild, 1-3 weeks for moderate'
    },
    'cut': {
        'name': 'Cut / Laceration',
        'description': 'A cut or laceration is a wound caused by a sharp object that tears or punctures the skin.',
        'severity_levels': {
            'mild': 'Superficial, less than 1cm, minimal bleeding',
            'moderate': 'Deeper cut, 1-3cm, steady bleeding but controllable',
            'severe': 'Deep laceration, over 3cm, heavy bleeding, possible tendon/muscle damage'
        },
        'immediate_care': [
            'Apply direct pressure with clean cloth to stop bleeding',
            'Clean the wound gently with clean water',
            'Apply antibiotic ointment if available',
            'Cover with sterile bandage or clean cloth'
        ],
        'recovery_tips': [
            'Keep the wound clean and dry',
            'Change bandage daily or when wet/dirty',
            'Watch for signs of infection',
            'Avoid picking at scabs - let them fall off naturally'
        ],
        'warning_signs': [
            'Bleeding doesn\'t stop after 10-15 minutes of pressure',
            'Cut is deep or edges don\'t stay together',
            'Signs of infection: increasing redness, warmth, pus',
            'Cut is on face, hand, or over a joint',
            'Caused by dirty or rusty object (tetanus risk)'
        ],
        'estimated_recovery': '1-3 weeks depending on depth'
    },
    'sprain': {
        'name': 'Sprain (Visible Signs)',
        'description': 'A sprain is a stretching or tearing of ligaments. Visual signs include swelling, bruising, and limited mobility.',
        'severity_levels': {
            'grade_1': 'Mild stretching, slight swelling, minimal bruising',
            'grade_2': 'Partial tear, moderate swelling and bruising, joint instability',
            'grade_3': 'Complete tear, severe swelling and bruising, significant instability'
        },
        'immediate_care': [
            'Stop activity immediately',
            'Apply RICE protocol for the first 48-72 hours',
            'Use crutches or support if it\'s a lower limb injury',
            'Immobilize the joint with a brace or wrap'
        ],
        'recovery_tips': [
            'Follow physical therapy exercises when recommended',
            'Gradually return to activity',
            'Strengthen surrounding muscles to prevent re-injury',
            'Use supportive bracing during recovery'
        ],
        'warning_signs': [
            'Unable to bear weight at all',
            'Visible deformity of the joint',
            'Numbness or extreme pain',
            'No improvement after a few days of rest'
        ],
        'estimated_recovery': 'Grade 1: 1-3 weeks, Grade 2: 3-6 weeks, Grade 3: 8-12 weeks'
    },
    'strain': {
        'name': 'Muscle Strain (Visible Signs)',
        'description': 'A muscle strain occurs when muscle fibers are overstretched or torn. Visual signs may include swelling, bruising, and muscle spasms.',
        'severity_levels': {
            'grade_1': 'Mild stretching, minimal swelling, muscle tightness',
            'grade_2': 'Partial tear, moderate swelling, visible bruising, weakness',
            'grade_3': 'Complete rupture, severe swelling and bruising, complete loss of function'
        },
        'immediate_care': [
            'Stop activity and rest the muscle',
            'Apply ice for 15-20 minutes every 2-3 hours',
            'Use compression wrap for support',
            'Elevate the affected limb if possible'
        ],
        'recovery_tips': [
            'Gentle stretching once pain subsides',
            'Progressive strengthening exercises',
            'Heat therapy after initial inflammation reduces',
            'Massage therapy can help recovery'
        ],
        'warning_signs': [
            'Complete inability to move the muscle',
            'Significant gap or dent in the muscle',
            'Severe pain that doesn\'t improve',
            'Extensive bruising spreading rapidly'
        ],
        'estimated_recovery': 'Grade 1: 2-3 weeks, Grade 2: 2-3 months, Grade 3: 3+ months (may need surgery)'
    },
    'abrasion': {
        'name': 'Abrasion / Road Rash',
        'description': 'An abrasion is a wound caused by skin scraping against a rough surface, removing the top layers of skin.',
        'severity_levels': {
            'mild': 'Superficial scrape, minimal bleeding, small area',
            'moderate': 'Deeper scrape, moderate bleeding, larger area',
            'severe': 'Deep abrasion reaching dermis, significant bleeding, very large area'
        },
        'immediate_care': [
            'Clean the wound thoroughly with clean water',
            'Remove any debris gently',
            'Apply antibiotic ointment',
            'Cover with non-stick bandage'
        ],
        'recovery_tips': [
            'Keep the wound moist for faster healing',
            'Change dressing daily',
            'Protect from sun exposure to prevent scarring',
            'Stay hydrated and eat protein-rich foods for healing'
        ],
        'warning_signs': [
            'Signs of infection (increasing redness, warmth, pus)',
            'Red streaks extending from wound',
            'Fever or chills',
            'Embedded debris that cannot be removed'
        ],
        'estimated_recovery': '1-3 weeks depending on depth and size'
    },
    'joint_injury': {
        'name': 'Joint Injury (Visible Signs)',
        'description': 'Joint injuries can include sprains, dislocations, or other damage. Visual signs include swelling, deformity, bruising, and limited range of motion.',
        'severity_levels': {
            'mild': 'Minor swelling, full range of motion, minimal pain',
            'moderate': 'Significant swelling, reduced motion, moderate pain',
            'severe': 'Severe swelling/deformity, very limited motion, severe pain'
        },
        'immediate_care': [
            'Immobilize the joint immediately',
            'Apply ice to reduce swelling',
            'Do NOT try to pop a dislocated joint back in',
            'Seek medical attention for severe cases'
        ],
        'recovery_tips': [
            'Follow prescribed physical therapy',
            'Strengthen muscles around the joint',
            'Use bracing or taping as recommended',
            'Gradual return to sport activities'
        ],
        'warning_signs': [
            'Visible deformity or abnormal angle',
            'Unable to move the joint at all',
            'Numbness or loss of pulse below injury',
            'Joint locked in position'
        ],
        'estimated_recovery': 'Varies widely: 2 weeks to several months'
    },
    'general': {
        'name': 'General Sports Injury',
        'description': 'The uploaded image shows signs of a sports-related injury that may require professional evaluation.',
        'immediate_care': [
            'Stop activity and rest',
            'Apply RICE protocol if appropriate',
            'Monitor symptoms closely',
            'Seek medical attention if symptoms are severe'
        ],
        'recovery_tips': [
            'Follow the guidance of healthcare professionals',
            'Don\'t rush return to sport',
            'Complete rehabilitation exercises',
            'Address any underlying causes'
        ],
        'warning_signs': [
            'Severe pain or inability to bear weight',
            'Visible deformity',
            'Numbness or tingling',
            'Symptoms worsening over time'
        ],
        'estimated_recovery': 'Varies based on specific injury type and severity'
    }
}

def analyze_injury_image(image_data, description=''):
    """
    Analyze injury image and provide suggestions.
    In a production environment, this would use computer vision/AI.
    For now, we use keyword analysis from the description.
    """
    description_lower = description.lower()
    
    # Analyze description keywords to determine injury type
    injury_type = 'general'
    confidence = 0.6
    
    # Bruise detection
    if any(word in description_lower for word in ['bruise', 'purple', 'blue', 'black', 'discolor', 'contusion', 'bump']):
        injury_type = 'bruise'
        confidence = 0.85
    # Cut detection
    elif any(word in description_lower for word in ['cut', 'laceration', 'bleeding', 'wound', 'slice', 'gash']):
        injury_type = 'cut'
        confidence = 0.85
    # Swelling detection
    elif any(word in description_lower for word in ['swell', 'swollen', 'puffy', 'inflam', 'edema']):
        injury_type = 'swelling'
        confidence = 0.85
    # Sprain detection
    elif any(word in description_lower for word in ['sprain', 'twist', 'roll', 'ankle', 'wrist', 'ligament']):
        injury_type = 'sprain'
        confidence = 0.80
    # Strain detection
    elif any(word in description_lower for word in ['strain', 'pull', 'muscle', 'tear', 'hamstring', 'calf', 'quad']):
        injury_type = 'strain'
        confidence = 0.80
    # Abrasion detection
    elif any(word in description_lower for word in ['scrape', 'abrasion', 'road rash', 'graze', 'skin off']):
        injury_type = 'abrasion'
        confidence = 0.85
    # Joint injury detection
    elif any(word in description_lower for word in ['joint', 'knee', 'elbow', 'shoulder', 'disloc']):
        injury_type = 'joint_injury'
        confidence = 0.75
    
    injury_info = INJURY_IMAGE_ANALYSIS.get(injury_type, INJURY_IMAGE_ANALYSIS['general'])
    
    return {
        'injury_type': injury_type,
        'injury_name': injury_info['name'],
        'confidence': confidence,
        'description': injury_info['description'],
        'severity_levels': injury_info.get('severity_levels', {}),
        'immediate_care': injury_info['immediate_care'],
        'recovery_tips': injury_info['recovery_tips'],
        'warning_signs': injury_info['warning_signs'],
        'estimated_recovery': injury_info.get('estimated_recovery', 'Varies based on severity')
    }

# ==========================================
# CHATBOT HELPER FUNCTION
# ==========================================
def get_chatbot_response(message):
    """
    Process chatbot queries and return appropriate responses.
    """
    message_lower = message.lower().strip()
    
    # Greetings
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! I'm your Sports Injury Analysis Assistant. How can I help you today? You can ask about specific injuries, prevention tips, recovery protocols, or general sports medicine questions."
    
    # Goodbye
    if any(word in message_lower for word in ['bye', 'goodbye', 'exit', 'quit']):
        return "Thank you for using the Sports Injury Analysis Assistant. Stay safe and remember to consult with healthcare professionals for personalized medical advice!"
    
    # Injury-specific queries
    injury_keywords = {
        'acl': ['acl', 'anterior cruciate ligament', 'knee ligament'],
        'mcl': ['mcl', 'medial collateral ligament'],
        'meniscus': ['meniscus', 'cartilage', 'knee cartilage'],
        'ankle': ['ankle', 'ankle sprain'],
        'high_ankle': ['high ankle', 'syndesmosis'],
        'hamstring': ['hamstring', 'back of thigh'],
        'quadriceps': ['quadriceps', 'quad', 'front thigh'],
        'groin': ['groin', 'adductor'],
        'calf': ['calf', 'gastrocnemius', 'soleus'],
        'rotator_cuff': ['rotator cuff', 'shoulder tendon'],
        'shoulder_dislocation': ['shoulder dislocation', 'dislocated shoulder'],
        'labrum': ['labrum', 'slap tear'],
        'concussion': ['concussion', 'head injury', 'brain injury'],
        'achilles': ['achilles', 'heel tendon'],
        'plantar_fasciitis': ['plantar fasciitis', 'heel pain', 'foot arch'],
        'shin_splints': ['shin splints', 'tibia pain'],
        'stress_fracture': ['stress fracture', 'bone crack'],
        'tennis_elbow': ['tennis elbow', 'lateral epicondylitis'],
        'golfers_elbow': ['golfers elbow', 'golfer\'s elbow', 'medial epicondylitis'],
        'lower_back': ['lower back', 'back strain', 'back pain'],
        'herniated_disc': ['herniated disc', 'slipped disc', 'disc injury']
    }
    
    for key, keywords in injury_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            if key in CHATBOT_KNOWLEDGE:
                injury = CHATBOT_KNOWLEDGE[key]
                response = f"**{injury['full_name']}**\n\n"
                response += f"**Description:** {injury['description']}\n\n"
                
                if 'symptoms' in injury:
                    response += f"**Symptoms:** {injury['symptoms']}\n\n"
                if 'causes' in injury:
                    response += f"**Common Causes:** {injury['causes']}\n\n"
                if 'treatment' in injury:
                    response += f"**Treatment:** {injury['treatment']}\n\n"
                if 'recovery_time' in injury:
                    response += f"**Recovery Time:** {injury['recovery_time']}\n\n"
                if 'prevention' in injury:
                    response += f"**Prevention:** {injury['prevention']}\n\n"
                if 'sports_at_risk' in injury:
                    response += f"**Sports at Risk:** {injury['sports_at_risk']}\n\n"
                
                response += "*Note: This information is for educational purposes only. Always consult with a healthcare professional for proper diagnosis and treatment.*"
                return response
    
    # Prevention queries
    if any(word in message_lower for word in ['prevent', 'prevention', 'avoid injury', 'injury prevention']):
        if 'warmup' in message_lower or 'warm up' in message_lower:
            return CHATBOT_KNOWLEDGE['prevention']['warmup']
        elif 'nutrition' in message_lower or 'diet' in message_lower:
            return CHATBOT_KNOWLEDGE['prevention']['nutrition']
        else:
            return CHATBOT_KNOWLEDGE['prevention']['general']
    
    # Recovery queries
    if any(word in message_lower for word in ['recover', 'recovery', 'heal', 'rehab']):
        if 'phase' in message_lower or 'stage' in message_lower:
            return CHATBOT_KNOWLEDGE['recovery']['phases']
        else:
            return CHATBOT_KNOWLEDGE['recovery']['tips']
    
    # RICE protocol
    if 'rice' in message_lower or 'r.i.c.e.' in message_lower:
        return CHATBOT_KNOWLEDGE['rice']['description']
    
    # General sports medicine questions
    if any(word in message_lower for word in ['what is', 'tell me about', 'explain', 'how to']):
        return "I can provide information on various sports injuries, prevention strategies, and recovery protocols. Please be more specific about what you'd like to know. For example:\n- 'Tell me about ACL injuries'\n- 'How to prevent ankle sprains'\n- 'What is the RICE protocol?'\n- 'Recovery tips for muscle strains'"
    
    # Default response
    return "I'm here to help with sports injury information. You can ask me about:\n\n1. **Specific injuries** (ACL tears, ankle sprains, concussions, etc.)\n2. **Injury prevention** strategies\n3. **Recovery protocols** and timelines\n4. **Treatment options** for common sports injuries\n5. **General sports medicine** questions\n\nPlease ask your question in more detail so I can provide the most helpful information!"

# ==========================================
# ROUTES
# ==========================================

@app.route('/')
def home():
    """Dashboard/Home page with overview statistics"""
    stats = {
        'total_players': len(df),
        'total_sports': df['sport'].nunique(),
        'injured_players': len(df[df['current_injury'] != 'None']),
        'avg_risk_score': round(df['risk_score'].mean(), 2),
        'high_risk_players': len(df[df['risk_score'] > 0.7]),
        'total_countries': df['country'].nunique(),
        'total_teams': df['team'].nunique(),
        'avg_age': round(df['age'].mean(), 1)
    }
    
    # Recent injuries
    recent_injuries = df[df['current_injury'] != 'None'].sort_values('injury_date', ascending=False).head(8).to_dict('records')
    
    # Sport distribution
    sport_dist = df['sport'].value_counts().to_dict()
    
    # Injury severity distribution
    severity_dist = df[df['injury_severity'] != 'N/A']['injury_severity'].value_counts().to_dict()
    
    # Risk distribution
    risk_categories = pd.cut(df['risk_score'], bins=[0, 0.3, 0.5, 0.7, 1.0], labels=['Low', 'Moderate', 'High', 'Critical'])
    risk_dist = risk_categories.value_counts().to_dict()
    
    return render_template('home.html', 
                         stats=stats, 
                         recent_injuries=recent_injuries, 
                         sport_dist=sport_dist,
                         severity_dist=severity_dist,
                         risk_dist=risk_dist)

@app.route('/players')
def players():
    """Players database with advanced filtering and sorting"""
    page = request.args.get('page', 1, type=int)
    per_page = 25
    search = request.args.get('search', '')
    sport_filter = request.args.get('sport', '')
    injury_filter = request.args.get('injury', '')
    risk_filter = request.args.get('risk', '')
    country_filter = request.args.get('country', '')
    gender_filter = request.args.get('gender', '')
    sort_by = request.args.get('sort', 'player_id')
    sort_order = request.args.get('order', 'asc')
    
    filtered_df = df.copy()
    
    # Apply filters
    if search:
        filtered_df = filtered_df[
            filtered_df['first_name'].str.contains(search, case=False) |
            filtered_df['last_name'].str.contains(search, case=False) |
            filtered_df['player_id'].str.contains(search, case=False) |
            filtered_df['team'].str.contains(search, case=False)
        ]
    
    if sport_filter:
        filtered_df = filtered_df[filtered_df['sport'] == sport_filter]
    
    if injury_filter:
        if injury_filter == 'injured':
            filtered_df = filtered_df[filtered_df['current_injury'] != 'None']
        elif injury_filter == 'healthy':
            filtered_df = filtered_df[filtered_df['current_injury'] == 'None']
    
    if risk_filter:
        if risk_filter == 'low':
            filtered_df = filtered_df[filtered_df['risk_score'] <= 0.3]
        elif risk_filter == 'moderate':
            filtered_df = filtered_df[(filtered_df['risk_score'] > 0.3) & (filtered_df['risk_score'] <= 0.5)]
        elif risk_filter == 'high':
            filtered_df = filtered_df[(filtered_df['risk_score'] > 0.5) & (filtered_df['risk_score'] <= 0.7)]
        elif risk_filter == 'critical':
            filtered_df = filtered_df[filtered_df['risk_score'] > 0.7]
    
    if country_filter:
        filtered_df = filtered_df[filtered_df['country'] == country_filter]
    
    if gender_filter:
        filtered_df = filtered_df[filtered_df['gender'] == gender_filter]
    
    # Sorting
    if sort_by in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=(sort_order == 'asc'))
    
    total_players = len(filtered_df)
    total_pages = (total_players + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    players_list = filtered_df.iloc[start_idx:end_idx].to_dict('records')
    
    # Get unique values for filters
    sports = sorted(df['sport'].unique().tolist())
    countries = sorted(df['country'].unique().tolist())
    
    return render_template('players.html', 
                         players=players_list, 
                         page=page, 
                         total_pages=total_pages,
                         total_players=total_players,
                         sports=sports,
                         countries=countries,
                         search=search,
                         sport_filter=sport_filter,
                         injury_filter=injury_filter,
                         risk_filter=risk_filter,
                         country_filter=country_filter,
                         gender_filter=gender_filter,
                         sort_by=sort_by,
                         sort_order=sort_order)

@app.route('/player/<player_id>')
def player_detail(player_id):
    """Detailed player profile page"""
    player = df[df['player_id'] == player_id]
    if player.empty:
        return redirect(url_for('players'))
    
    player_data = player.iloc[0].to_dict()
    
    # Calculate additional metrics
    player_data['injury_rate'] = round(player_data['total_injuries_career'] / max(player_data['years_professional'], 1), 2)
    
    # Similar players (same sport and position)
    similar = df[(df['sport'] == player_data['sport']) & 
                 (df['position'] == player_data['position']) & 
                 (df['player_id'] != player_id)].head(6).to_dict('records')
    
    # Risk factors analysis
    risk_factors = []
    if player_data['age'] > 32:
        risk_factors.append({'factor': 'Age above 32', 'impact': 'High', 'description': 'Increased injury risk with age'})
    if player_data['previous_surgeries'] > 2:
        risk_factors.append({'factor': 'Multiple previous surgeries', 'impact': 'High', 'description': 'History of significant injuries'})
    if player_data['training_hours_weekly'] > 35:
        risk_factors.append({'factor': 'High training load', 'impact': 'Medium', 'description': 'Overtraining risk'})
    if player_data['bmi'] > 28:
        risk_factors.append({'factor': 'Elevated BMI', 'impact': 'Medium', 'description': 'Additional stress on joints'})
    if player_data['chronic_conditions'] != 'None':
        risk_factors.append({'factor': f'Chronic: {player_data["chronic_conditions"]}', 'impact': 'High', 'description': 'Pre-existing condition'})
    if player_data['total_injuries_career'] > 5:
        risk_factors.append({'factor': 'Injury history', 'impact': 'Medium', 'description': 'Multiple previous injuries'})
    
    return render_template('player_detail.html', 
                         player=player_data, 
                         similar_players=similar,
                         risk_factors=risk_factors)

@app.route('/analytics')
def analytics():
    """Advanced analytics dashboard"""
    # Injury by sport
    injury_by_sport = df.groupby('sport').agg({
        'total_injuries_career': 'sum',
        'risk_score': 'mean',
        'days_missed_current_season': 'sum',
        'player_id': 'count'
    }).round(2)
    injury_by_sport.columns = ['total_injuries', 'avg_risk', 'days_missed', 'player_count']
    injury_by_sport = injury_by_sport.to_dict('index')
    
    # Current injury distribution
    injury_distribution = df[df['current_injury'] != 'None']['current_injury'].value_counts().head(15).to_dict()
    
    # Severity distribution
    severity_dist = df[df['injury_severity'] != 'N/A']['injury_severity'].value_counts().to_dict()
    
    # Age vs injuries
    age_groups = pd.cut(df['age'], bins=[17, 22, 27, 32, 37, 45], labels=['18-22', '23-27', '28-32', '33-37', '38+'])
    injury_by_age = df.groupby(age_groups)['total_injuries_career'].mean().to_dict()
    
    # Recovery status
    recovery_status_dist = df['recovery_status'].value_counts().to_dict()
    
    # Risk distribution
    risk_categories = pd.cut(df['risk_score'], bins=[0, 0.3, 0.5, 0.7, 1.0], labels=['Low', 'Moderate', 'High', 'Critical'])
    risk_dist = risk_categories.value_counts().to_dict()
    
    # Monthly trend (simulated)
    monthly_trend = {}
    for i in range(12):
        month = (datetime.now() - timedelta(days=30*i)).strftime('%b %Y')
        monthly_trend[month] = np.random.randint(40, 160)
    
    # Treatment effectiveness
    treatment_eff = df.groupby('treatment_type').agg({
        'rehabilitation_progress': 'mean',
        'days_missed_current_season': 'mean'
    }).round(1).to_dict('index')
    
    # Position risk analysis
    position_risk = df.groupby(['sport', 'position'])['risk_score'].mean().round(3)
    top_risk_positions = position_risk.sort_values(ascending=False).head(15).to_dict()
    
    # Gender comparison
    gender_stats = df.groupby('gender').agg({
        'total_injuries_career': 'mean',
        'risk_score': 'mean',
        'fitness_level': 'mean'
    }).round(2).to_dict('index')
    
    return render_template('analytics.html',
                         injury_by_sport=injury_by_sport,
                         injury_distribution=injury_distribution,
                         severity_dist=severity_dist,
                         injury_by_age=injury_by_age,
                         recovery_status_dist=recovery_status_dist,
                         risk_dist=risk_dist,
                         monthly_trend=monthly_trend,
                         treatment_eff=treatment_eff,
                         top_risk_positions=top_risk_positions,
                         gender_stats=gender_stats)

@app.route('/statistics')
def statistics():
    """Comprehensive statistical analysis page"""
    # Basic statistics
    stats = {
        'total_players': len(df),
        'avg_age': round(df['age'].mean(), 1),
        'std_age': round(df['age'].std(), 1),
        'avg_height': round(df['height_cm'].mean(), 1),
        'avg_weight': round(df['weight_kg'].mean(), 1),
        'avg_bmi': round(df['bmi'].mean(), 1),
        'avg_training_hours': round(df['training_hours_weekly'].mean(), 1),
        'total_injuries': df['total_injuries_career'].sum(),
        'avg_injuries_per_player': round(df['total_injuries_career'].mean(), 2),
        'avg_risk_score': round(df['risk_score'].mean(), 2),
        'high_risk_count': len(df[df['risk_score'] > 0.7]),
        'currently_injured': len(df[df['current_injury'] != 'None']),
        'avg_days_missed': round(df['days_missed_current_season'].mean(), 1),
        'total_surgeries': df['previous_surgeries'].sum(),
        'chronic_conditions_count': len(df[df['chronic_conditions'] != 'None']),
        'avg_fitness': round(df['fitness_level'].mean(), 1),
        'avg_performance': round(df['performance_index'].mean(), 1),
        'avg_years_pro': round(df['years_professional'].mean(), 1),
        'total_salary': df['salary_usd'].sum()
    }
    
    # Top sports by injuries
    top_sports = df.groupby('sport')['total_injuries_career'].sum().sort_values(ascending=False).to_dict()
    
    # Country distribution
    country_dist = df['country'].value_counts().head(15).to_dict()
    
    # Gender distribution
    gender_dist = df['gender'].value_counts().to_dict()
    
    # Gender comparison statistics
    gender_stats = df.groupby('gender').agg({
        'total_injuries_career': 'mean',
        'risk_score': 'mean',
        'fitness_level': 'mean',
        'age': 'mean'
    }).round(2).to_dict('index')
    
    # Treatment effectiveness
    treatment_success = df.groupby('treatment_type').agg({
        'rehabilitation_progress': 'mean',
        'player_id': 'count'
    }).round(1)
    treatment_success.columns = ['avg_progress', 'patient_count']
    treatment_success = treatment_success.to_dict('index')
    
    # Age distribution
    age_dist = df['age'].value_counts().sort_index().to_dict()
    
    # Correlation analysis
    numeric_cols = ['age', 'bmi', 'training_hours_weekly', 'total_injuries_career', 'risk_score', 
                    'fitness_level', 'performance_index', 'days_missed_current_season']
    correlations = {
        'age_vs_injuries': round(df['age'].corr(df['total_injuries_career']), 3),
        'training_vs_risk': round(df['training_hours_weekly'].corr(df['risk_score']), 3),
        'bmi_vs_injuries': round(df['bmi'].corr(df['total_injuries_career']), 3),
        'fitness_vs_performance': round(df['fitness_level'].corr(df['performance_index']), 3),
        'age_vs_risk': round(df['age'].corr(df['risk_score']), 3),
        'years_pro_vs_injuries': round(df['years_professional'].corr(df['total_injuries_career']), 3)
    }
    
    # Descriptive statistics by sport
    sport_stats = df.groupby('sport').agg({
        'age': ['mean', 'std'],
        'total_injuries_career': ['mean', 'sum'],
        'risk_score': ['mean', 'std'],
        'fitness_level': 'mean'
    }).round(2)
    sport_stats.columns = ['avg_age', 'std_age', 'avg_injuries', 'total_injuries', 'avg_risk', 'std_risk', 'avg_fitness']
    sport_stats_dict = sport_stats.to_dict('index')
    
    return render_template('statistics.html',
                         stats=stats,
                         top_sports=top_sports,
                         country_dist=country_dist,
                         gender_dist=gender_dist,
                         gender_stats=gender_stats,
                         treatment_success=treatment_success,
                         age_dist=age_dist,
                         correlations=correlations,
                         sport_stats=sport_stats_dict)


@app.route('/injury-analysis')
def injury_analysis():
    """Injury Image Analysis page"""
    return render_template('injury_analysis.html')

@app.route('/api/analyze-injury', methods=['POST'])
def api_analyze_injury():
    """API endpoint for injury image analysis"""
    try:
        data = request.json
        image_data = data.get('image', '')
        description = data.get('description', '')
        
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Analyze the injury
        analysis = analyze_injury_image(image_data, description)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predictions')
def predictions():
    """Machine Learning predictions and risk assessment page"""
    # High risk players
    high_risk_players = df[df['risk_score'] > 0.7].sort_values('risk_score', ascending=False).head(25).to_dict('records')
    
    # Sport risk analysis
    sport_risk = df.groupby('sport').agg({
        'risk_score': ['mean', 'std', 'max'],
        'total_injuries_career': 'sum'
    }).round(3)
    sport_risk.columns = ['avg_risk', 'std_risk', 'max_risk', 'total_injuries']
    sport_risk = sport_risk.sort_values('avg_risk', ascending=False).to_dict('index')
    
    # Position risk analysis
    position_risk = df.groupby(['sport', 'position']).agg({
        'risk_score': 'mean',
        'player_id': 'count'
    }).round(3)
    position_risk.columns = ['avg_risk', 'player_count']
    position_risk = position_risk.sort_values('avg_risk', ascending=False).head(20)
    position_risk_list = [{'sport': idx[0], 'position': idx[1], **row.to_dict()} 
                          for idx, row in position_risk.iterrows()]
    
    # Age-based risk prediction
    age_risk = df.groupby(pd.cut(df['age'], bins=[17, 22, 25, 28, 32, 36, 45]))['risk_score'].mean().round(3)
    age_risk_clean = {str(k): v for k, v in age_risk.to_dict().items()}
    
    # ML-simulated predictions for sample players
    predictions_data = []
    for _, row in df.sample(100, random_state=42).iterrows():
        risk_factors = []
        risk_adjustments = 0
        
        if row['age'] > 32:
            risk_factors.append({'factor': 'Age > 32', 'weight': 0.1})
            risk_adjustments += 0.1
        if row['previous_surgeries'] > 2:
            risk_factors.append({'factor': 'Multiple surgeries', 'weight': 0.12})
            risk_adjustments += 0.12
        if row['training_hours_weekly'] > 35:
            risk_factors.append({'factor': 'High training load', 'weight': 0.08})
            risk_adjustments += 0.08
        if row['bmi'] > 28:
            risk_factors.append({'factor': 'Elevated BMI', 'weight': 0.06})
            risk_adjustments += 0.06
        if row['chronic_conditions'] != 'None':
            risk_factors.append({'factor': 'Chronic condition', 'weight': 0.15})
            risk_adjustments += 0.15
        if row['total_injuries_career'] > 5:
            risk_factors.append({'factor': 'Injury history', 'weight': 0.1})
            risk_adjustments += 0.1
        if row['fitness_level'] < 65:
            risk_factors.append({'factor': 'Low fitness', 'weight': 0.08})
            risk_adjustments += 0.08
        
        predicted_risk = min(row['risk_score'] + risk_adjustments * np.random.uniform(0.5, 1.0), 0.99)
        
        if predicted_risk > 0.8:
            recommendation = 'Immediate attention required'
            priority = 'Critical'
        elif predicted_risk > 0.6:
            recommendation = 'Close monitoring recommended'
            priority = 'High'
        elif predicted_risk > 0.4:
            recommendation = 'Regular check-ups advised'
            priority = 'Medium'
        else:
            recommendation = 'Standard monitoring'
            priority = 'Low'
        
        predictions_data.append({
            'player_id': row['player_id'],
            'name': f"{row['first_name']} {row['last_name']}",
            'sport': row['sport'],
            'position': row['position'],
            'current_risk': row['risk_score'],
            'predicted_risk': round(predicted_risk, 3),
            'risk_change': round(predicted_risk - row['risk_score'], 3),
            'risk_factors': risk_factors,
            'recommendation': recommendation,
            'priority': priority
        })
    
    predictions_data.sort(key=lambda x: x['predicted_risk'], reverse=True)
    
    # Injury probability by sport
    injury_prob = df.groupby('sport').apply(
        lambda x: len(x[x['current_injury'] != 'None']) / len(x) * 100
    ).round(1).sort_values(ascending=False).to_dict()
    
    return render_template('predictions.html',
                         high_risk_players=high_risk_players,
                         sport_risk=sport_risk,
                         position_risk=position_risk_list,
                         age_risk=age_risk_clean,
                         predictions=predictions_data[:50],
                         injury_prob=injury_prob)

@app.route('/reports')
def reports():
    """Comprehensive reports generation page"""
    # Injury summary by sport
    injury_summary = df.groupby('sport').agg({
        'total_injuries_career': ['sum', 'mean'],
        'days_missed_current_season': ['sum', 'mean'],
        'risk_score': ['mean', 'std'],
        'rehabilitation_progress': 'mean',
        'player_id': 'count'
    }).round(2)
    injury_summary.columns = ['Total Injuries', 'Avg Injuries', 'Total Days Missed', 'Avg Days Missed', 
                              'Avg Risk', 'Risk Std', 'Avg Rehab', 'Player Count']
    injury_summary = injury_summary.reset_index().to_dict('records')
    
    # Severity analysis by sport
    severity_by_sport = df[df['injury_severity'] != 'N/A'].groupby(['sport', 'injury_severity']).size().unstack(fill_value=0)
    severity_data = severity_by_sport.to_dict('index') if not severity_by_sport.empty else {}
    
    # Treatment outcomes
    treatment_outcomes = df.groupby('treatment_type').agg({
        'rehabilitation_progress': ['mean', 'std'],
        'days_missed_current_season': ['mean', 'std'],
        'player_id': 'count'
    }).round(1)
    treatment_outcomes.columns = ['Avg Progress', 'Std Progress', 'Avg Days Missed', 'Std Days', 'Patient Count']
    treatment_outcomes = treatment_outcomes.reset_index().to_dict('records')
    
    # Monthly report
    current_month = datetime.now().strftime('%B %Y')
    injured_this_month = df[df['current_injury'] != 'None']
    monthly_report = {
        'month': current_month,
        'total_players': len(df),
        'currently_injured': len(injured_this_month),
        'injury_rate': round(len(injured_this_month) / len(df) * 100, 1),
        'avg_risk_score': round(df['risk_score'].mean(), 2),
        'high_risk_count': len(df[df['risk_score'] > 0.7]),
        'critical_cases': len(df[df['injury_severity'] == 'Critical']),
        'in_recovery': len(df[df['recovery_status'] == 'In Recovery']),
        'fully_recovered': len(df[df['recovery_status'] == 'Fully Recovered']),
        'avg_fitness': round(df['fitness_level'].mean(), 1),
        'avg_performance': round(df['performance_index'].mean(), 1)
    }
    
    # Country analysis
    country_analysis = df.groupby('country').agg({
        'player_id': 'count',
        'total_injuries_career': 'sum',
        'risk_score': 'mean'
    }).round(2)
    country_analysis.columns = ['players', 'injuries', 'avg_risk']
    country_analysis = country_analysis.sort_values('players', ascending=False).head(15).to_dict('index')
    
    # Age group analysis
    age_analysis = df.groupby(pd.cut(df['age'], bins=[17, 22, 27, 32, 37, 45], 
                                     labels=['18-22', '23-27', '28-32', '33-37', '38+'])).agg({
        'player_id': 'count',
        'total_injuries_career': 'mean',
        'risk_score': 'mean',
        'fitness_level': 'mean'
    }).round(2)
    age_analysis.columns = ['players', 'avg_injuries', 'avg_risk', 'avg_fitness']
    age_analysis = age_analysis.to_dict('index')
    
    return render_template('reports.html',
                         injury_summary=injury_summary,
                         severity_data=severity_data,
                         treatment_outcomes=treatment_outcomes,
                         monthly_report=monthly_report,
                         country_analysis=country_analysis,
                         age_analysis=age_analysis)


@app.route('/treatment-timeline')
def treatment_timeline():
    """Treatment timeline visualizer page"""
    # Get players for dropdown
    players = df[['player_id', 'first_name', 'last_name', 'sport', 'current_injury']].to_dict('records')
    return render_template('treatment_timeline.html', players=players)

@app.route('/medication-tracker')
def medication_tracker():
    """Medication tracker page"""
    players = df[['player_id', 'first_name', 'last_name']].to_dict('records')
    return render_template('medication_tracker.html', players=players)

@app.route('/second-opinion')
def second_opinion():
    """Second opinion system page"""
    players = df[['player_id', 'first_name', 'last_name']].to_dict('records')
    return render_template('second_opinion.html', players=players)

# API endpoints for treatment timeline
@app.route('/api/treatment-timeline/<player_id>')
def get_treatment_timeline(player_id):
    """Get treatment timeline for a player"""
    # In real app, fetch from database
    # For now, return sample data
    player = df[df['player_id'] == player_id]
    if player.empty:
        return jsonify({'error': 'Player not found'}), 404
    
    player_data = player.iloc[0].to_dict()
    
    # Sample timeline data
    timeline = {
        'player_id': player_id,
        'player_name': f"{player_data['first_name']} {player_data['last_name']}",
        'injury': player_data['current_injury'] if player_data['current_injury'] != 'None' else 'General Injury',
        'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'expected_duration': '12 weeks',
        'phases': [
            {
                'id': 1,
                'name': 'Acute Phase',
                'duration': 'Week 1-2',
                'status': 'completed',
                'progress': 100,
                'goals': ['Pain control', 'Reduce swelling', 'Basic mobility'],
                'exercises': ['Ankle pumps', 'Quad sets', 'Heel slides'],
                'restrictions': ['Non-weight bearing', 'Use of crutches'],
                'notes': 'Focus on pain management'
            },
            {
                'id': 2,
                'name': 'Early Rehabilitation',
                'duration': 'Week 3-6',
                'status': 'active',
                'progress': 65,
                'goals': ['Increase range of motion', 'Begin weight bearing', 'Improve strength'],
                'exercises': ['Straight leg raises', 'Mini squats', 'Balance exercises'],
                'restrictions': ['Partial weight bearing', 'No running'],
                'notes': 'Progress based on pain tolerance'
            },
            {
                'id': 3,
                'name': 'Strengthening Phase',
                'duration': 'Week 7-12',
                'status': 'planned',
                'progress': 0,
                'goals': ['Full weight bearing', 'Normal gait', 'Strength training'],
                'exercises': ['Leg press', 'Step ups', 'Resistance band exercises'],
                'restrictions': ['No jumping', 'No cutting movements'],
                'notes': 'Focus on symmetrical strength'
            }
        ]
    }
    
    return jsonify(timeline)

@app.route('/api/medications/<player_id>')
def get_player_medications(player_id):
    """Get medications for a player"""
    # In real app, fetch from database
    # For now, return sample data
    player = df[df['player_id'] == player_id]
    if player.empty:
        return jsonify({'error': 'Player not found'}), 404
    
    # Sample medications data
    medications = [
        {
            'id': 1,
            'medication_name': 'Ibuprofen',
            'dosage': '400mg',
            'frequency': 'Three times daily',
            'type': 'Anti-inflammatory',
            'start_date': (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
            'prescribing_doctor': 'Dr. Smith',
            'status': 'active',
            'side_effects': ['Mild stomach discomfort']
        },
        {
            'id': 2,
            'medication_name': 'Acetaminophen',
            'dosage': '500mg',
            'frequency': 'As needed',
            'type': 'Pain relief',
            'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            'prescribing_doctor': 'Dr. Johnson',
            'status': 'active',
            'side_effects': []
        }
    ]
    
    return jsonify(medications)

@app.route('/api/consultations')
def get_consultations():
    """Get all consultations"""
    # In real app, fetch from database
    # For now, return sample data
    consultations = [
        {
            'id': 1,
            'player_id': 'PLY00001',
            'player_name': 'John Smith',
            'injury_type': 'ACL Tear',
            'specialist': 'Dr. Sarah Chen',
            'specialist_type': 'Orthopedic Surgeon',
            'status': 'scheduled',
            'date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'time': '14:00',
            'platform': 'Zoom',
            'notes': 'Second opinion on surgical approach'
        },
        {
            'id': 2,
            'player_id': 'PLY00002',
            'player_name': 'Mike Davis',
            'injury_type': 'Rotator Cuff Tear',
            'specialist': 'Dr. James Wilson',
            'specialist_type': 'Sports Medicine',
            'status': 'completed',
            'date': (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d'),
            'notes': 'Conservative treatment recommended'
        }
    ]
    
    return jsonify(consultations)

@app.route('/api/specialists')
def get_specialists():
    """Get available specialists"""
    specialists = [
        {
            'id': 'SP001',
            'name': 'Dr. Sarah Chen',
            'specialty': 'Orthopedic Surgery',
            'sub_specialty': 'Knee & Shoulder',
            'experience': '15 years',
            'hospital': 'Mayo Clinic',
            'rating': 4.9,
            'availability': 'Available this week',
            'languages': ['English', 'Mandarin'],
            'consultation_fee': '$350'
        },
        {
            'id': 'SP002',
            'name': 'Dr. James Wilson',
            'specialty': 'Sports Medicine',
            'sub_specialty': 'Non-surgical Treatment',
            'experience': '12 years',
            'hospital': 'Hospital for Special Surgery',
            'rating': 4.8,
            'availability': 'Available next week',
            'languages': ['English', 'Spanish'],
            'consultation_fee': '$300'
        }
    ]
    
    return jsonify(specialists)

# ==========================================
# API ENDPOINTS
# ==========================================

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """Chatbot API endpoint"""
    data = request.json
    message = data.get('message', '')
    response = get_chatbot_response(message)
    return jsonify({'response': response})

@app.route('/api/search')
def api_search():
    """API endpoint for global search functionality"""
    query = request.args.get('q', '').strip().lower()
    
    if len(query) < 2:
        return jsonify({'results': []})
    
    results = []
    
    # Search players
    player_matches = df[
        df['first_name'].str.lower().str.contains(query, na=False) |
        df['last_name'].str.lower().str.contains(query, na=False) |
        df['player_id'].str.lower().str.contains(query, na=False)
    ].head(5)
    
    for _, player in player_matches.iterrows():
        results.append({
            'title': f"{player['first_name']} {player['last_name']}",
            'type': 'Player',
            'meta': f"{player['sport']} • {player['team']}",
            'url': url_for('player_detail', player_id=player['player_id']),
            'icon': 'bi-person-circle'
        })
    
    # Search teams
    team_matches = df[df['team'].str.lower().str.contains(query, na=False)]['team'].unique()[:3]
    for team in team_matches:
        team_sport = df[df['team'] == team]['sport'].iloc[0]
        player_count = len(df[df['team'] == team])
        results.append({
            'title': team,
            'type': 'Team',
            'meta': f"{team_sport} • {player_count} players",
            'url': url_for('players', search=team),
            'icon': 'bi-people-fill'
        })
    
    # Search injuries
    injury_types = ['ACL', 'MCL', 'Hamstring', 'Ankle', 'Concussion', 'Shoulder', 'Knee']
    for injury_type in injury_types:
        if query in injury_type.lower():
            injury_count = len(df[df['current_injury'].str.contains(injury_type, case=False, na=False)])
            results.append({
                'title': f"{injury_type} Injuries",
                'type': 'Injury Type',
                'meta': f"{injury_count} active cases",
                'url': url_for('injury_analysis'),
                'icon': 'bi-bandaid-fill'
            })
    
    # Search sports
    sport_matches = [s for s in df['sport'].unique() if query in s.lower()][:3]
    for sport in sport_matches:
        sport_count = len(df[df['sport'] == sport])
        results.append({
            'title': sport,
            'type': 'Sport',
            'meta': f"{sport_count} athletes",
            'url': url_for('players', sport=sport),
            'icon': 'bi-trophy-fill'
        })
    
    return jsonify({'results': results[:10]})

@app.route('/api/stats/<stat_type>')
def get_stats(stat_type):
    """Statistics API endpoint"""
    if stat_type == 'injury_by_sport':
        data = df.groupby('sport')['total_injuries_career'].sum().to_dict()
    elif stat_type == 'risk_distribution':
        data = df['risk_score'].describe().to_dict()
    elif stat_type == 'age_distribution':
        data = df['age'].value_counts().sort_index().to_dict()
    elif stat_type == 'player_count_by_sport':
        data = df['sport'].value_counts().to_dict()
    elif stat_type == 'injury_severity':
        data = df[df['injury_severity'] != 'N/A']['injury_severity'].value_counts().to_dict()
    else:
        data = {}
    return jsonify(data)

@app.route('/api/player/<player_id>')
def get_player(player_id):
    """Get single player data API"""
    player = df[df['player_id'] == player_id]
    if player.empty:
        return jsonify({'error': 'Player not found'}), 404
    return jsonify(player.iloc[0].to_dict())

@app.route('/api/export/<format_type>')
def export_data(format_type):
    """Export data in various formats"""
    if format_type == 'json':
        return jsonify(df.to_dict('records'))
    elif format_type == 'summary':
        summary = {
            'total_players': len(df),
            'sports': df['sport'].unique().tolist(),
            'injury_statistics': {
                'total_injuries': int(df['total_injuries_career'].sum()),
                'currently_injured': len(df[df['current_injury'] != 'None']),
                'avg_risk_score': round(df['risk_score'].mean(), 3)
            }
        }
        return jsonify(summary)
    return jsonify({'error': 'Invalid format'}), 400

@app.route('/api/predict', methods=['POST'])
def predict_injury():
    """API endpoint for injury risk prediction"""
    try:
        data = request.json
        
        # Extract data from request
        sport = data.get('sport', '')
        age = int(data.get('age', 25))
        height = int(data.get('height', 180))
        weight = int(data.get('weight', 75))
        years_pro = int(data.get('years_pro', 5))
        training_hours = int(data.get('training_hours', 20))
        prev_injuries = int(data.get('prev_injuries', 0))
        surgeries = int(data.get('surgeries', 0))
        chronic_condition = data.get('chronic_condition', 'None')
        fitness = int(data.get('fitness', 85))
        current_injury = data.get('current_injury', 'None')
        
        # Calculate BMI
        height_m = height / 100
        bmi = round(weight / (height_m * height_m), 1)
        
        # Base risk calculation (similar to dataset generation)
        age_factor = 0.1 if age < 25 else (0.2 if age < 30 else (0.3 if age < 35 else 0.4))
        
        # Sport risk factors
        sport_factors = {
            'Football': 0.15, 'Rugby': 0.15, 'Hockey': 0.12,
            'Soccer': 0.10, 'Basketball': 0.10, 'Tennis': 0.08,
            'Baseball': 0.08, 'Athletics': 0.08, 'Cricket': 0.06,
            'Swimming': 0.05
        }
        sport_factor = sport_factors.get(sport, 0.08)
        
        # Injury history factor
        injury_factor = min(prev_injuries * 0.05, 0.4)
        
        # Calculate initial risk score
        risk_score = age_factor + injury_factor + sport_factor
        
        # Adjust for additional factors
        if surgeries > 0:
            risk_score += min(surgeries * 0.05, 0.15)
        
        if training_hours > 35:
            risk_score += 0.08
        elif training_hours > 25:
            risk_score += 0.04
        
        if chronic_condition != 'None':
            risk_score += 0.12
        
        if current_injury == 'Severe':
            risk_score += 0.10
        elif current_injury == 'Moderate':
            risk_score += 0.05
        elif current_injury == 'Minor':
            risk_score += 0.02
        
        if fitness < 60:
            risk_score += 0.08
        elif fitness < 70:
            risk_score += 0.04
        
        # Years professional factor
        risk_score += min(years_pro * 0.01, 0.05)
        
        # BMI factor
        if bmi > 28:
            risk_score += 0.06
        elif bmi < 18.5:
            risk_score += 0.04
        
        # Add small random factor for realism (±5%)
        risk_score += np.random.uniform(-0.05, 0.05)
        
        # Ensure score is between 0.05 and 0.95
        risk_score = max(0.05, min(0.95, risk_score))
        
        # Determine risk category
        risk_percent = risk_score * 100
        if risk_percent >= 70:
            risk_category = 'Critical'
            recommendation = 'Immediate medical evaluation recommended. Reduce training intensity by 50%.'
            priority = 'Critical'
        elif risk_percent >= 50:
            risk_category = 'High'
            recommendation = 'Schedule sports medicine consultation. Implement targeted strengthening exercises.'
            priority = 'High'
        elif risk_percent >= 30:
            risk_category = 'Moderate'
            recommendation = 'Continue training with monitoring. Focus on proprioception and balance training.'
            priority = 'Medium'
        else:
            risk_category = 'Low'
            recommendation = 'Continue current regimen. Maintain proper nutrition and hydration.'
            priority = 'Low'
        
        # Generate risk factors analysis
        risk_factors = []
        
        if age > 32:
            impact = 'High' if age > 35 else 'Medium'
            risk_factors.append({
                'factor': 'Age Factor',
                'impact': impact,
                'description': f'Age {age} increases injury susceptibility'
            })
        
        if prev_injuries > 2:
            impact = 'High' if prev_injuries > 4 else 'Medium'
            risk_factors.append({
                'factor': 'Injury History',
                'impact': impact,
                'description': f'{prev_injuries} previous injuries increase recurrence risk'
            })
        
        if surgeries > 0:
            impact = 'High' if surgeries > 1 else 'Medium'
            risk_factors.append({
                'factor': 'Surgical History',
                'impact': impact,
                'description': f'{surgeries} previous surgeries'
            })
        
        if chronic_condition != 'None':
            risk_factors.append({
                'factor': 'Chronic Condition',
                'impact': 'High',
                'description': chronic_condition
            })
        
        if training_hours > 35:
            risk_factors.append({
                'factor': 'Training Load',
                'impact': 'Medium',
                'description': f'{training_hours} hours/week may lead to overtraining'
            })
        
        if fitness < 60:
            impact = 'Medium' if fitness < 60 else 'Low'
            risk_factors.append({
                'factor': 'Fitness Level',
                'impact': impact,
                'description': f'Fitness score {fitness}% - Needs improvement'
            })
        
        if current_injury != 'None':
            impact = 'High' if current_injury == 'Severe' else 'Medium'
            risk_factors.append({
                'factor': 'Current Injury',
                'impact': impact,
                'description': f'{current_injury} injury present'
            })
        
        if bmi > 28 or bmi < 18.5:
            status = 'Overweight' if bmi > 28 else 'Underweight'
            risk_factors.append({
                'factor': 'BMI Factor',
                'impact': 'Medium',
                'description': f'BMI {bmi} ({status})'
            })
        
        # Generate recommendations list
        recommendations = []
        
        if risk_category == 'Critical':
            recommendations.append('Immediate medical evaluation recommended')
            recommendations.append('Reduce training intensity by 50%')
            recommendations.append('Consider rest period of 2-4 weeks')
            recommendations.append('Implement comprehensive injury prevention program')
        elif risk_category == 'High':
            recommendations.append('Schedule sports medicine consultation')
            recommendations.append('Implement targeted strengthening exercises')
            recommendations.append('Monitor training load closely')
            recommendations.append('Consider biomechanical assessment')
        elif risk_category == 'Moderate':
            recommendations.append('Continue training with monitoring')
            recommendations.append('Focus on proprioception and balance training')
            recommendations.append('Maintain proper warm-up and cool-down routines')
            recommendations.append('Regular flexibility and mobility work')
        else:
            recommendations.append('Continue current training regimen')
            recommendations.append('Maintain proper nutrition and hydration')
            recommendations.append('Regular injury prevention screening')
            recommendations.append('Annual comprehensive medical checkup')
        
        # Add sport-specific recommendations
        if sport in ['Football', 'Rugby']:
            recommendations.append('Focus on lower body strength and proprioception')
        elif sport == 'Basketball':
            recommendations.append('Implement landing mechanics training')
        elif sport in ['Tennis', 'Baseball']:
            recommendations.append('Implement throwing/shoulder maintenance program')
        elif sport == 'Swimming':
            recommendations.append('Focus on shoulder stability exercises')
        
        # Prepare response
        response = {
            'success': True,
            'risk_score': round(risk_score, 3),
            'risk_percentage': round(risk_percent, 1),
            'risk_category': risk_category,
            'priority': priority,
            'bmi': bmi,
            'recommendation': recommendation,
            'recommendations': recommendations,
            'risk_factors': risk_factors,
            'analysis': {
                'age_factor': round(age_factor, 3),
                'sport_factor': round(sport_factor, 3),
                'injury_factor': round(injury_factor, 3)
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error calculating risk prediction'
        }), 400

# Toggle theme route and context processor
@app.route('/toggle-theme', methods=['POST'])
def toggle_theme():
    """Toggle between light and dark theme"""
    data = request.get_json()
    theme = data.get('theme', 'dark')
    session['theme'] = theme
    return jsonify({'success': True, 'theme': theme})

@app.context_processor
def inject_theme():
    """Inject theme variable into all templates"""
    return {'theme': session.get('theme', 'dark')}

# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error_code=404, message='Page not found'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code=500, message='Internal server error'), 500

# ==========================================
# GAIT ANALYSIS ROUTE
# ==========================================

@app.route('/gait-analysis')
def gait_analysis():
    """Gait and Biomechanical Analysis with Video/Motion-Capture Analysis"""
    try:
        # Sample players for analysis
        sample_players = df.sample(min(15, len(df))).to_dict('records')
        
        analysis_sessions = []
        movement_issues = [
            'Improper Landing Mechanics', 'Knee Valgus', 'Hip Weakness',
            'Ankle Instability', 'Poor Core Activation', 'Asymmetric Movement',
            'Limited Hip Mobility', 'Overstriding', 'Crossover Gait'
        ]
        
        for player in sample_players:
            # Generate match readiness score
            biomech_score = np.random.randint(60, 98)
            movement_quality = np.random.randint(65, 95)
            injury_risk = round(1 - (biomech_score / 100), 2)
            
            # Determine match readiness
            if biomech_score >= 85 and injury_risk < 0.2:
                match_status = 'Ready'
                status_class = 'success'
            elif biomech_score >= 70:
                match_status = 'Caution'
                status_class = 'warning'
            else:
                match_status = 'Not Ready'
                status_class = 'danger'
            
            # Detected issues
            num_issues = np.random.randint(0, 3)
            detected_issues = np.random.choice(movement_issues, size=num_issues, replace=False).tolist() if num_issues > 0 else []
            
            # Prevention tips
            tips = []
            if 'Knee Valgus' in detected_issues:
                tips.append('Strengthen glutes with lateral band walks and clamshells')
            if 'Hip Weakness' in detected_issues:
                tips.append('Incorporate single-leg deadlifts and hip thrusts')
            if 'Ankle Instability' in detected_issues:
                tips.append('Practice balance exercises on unstable surfaces')
            if 'Poor Core Activation' in detected_issues:
                tips.append('Add anti-rotation exercises like Pallof presses')
            if not tips:
                tips = ['Maintain current training protocol', 'Continue mobility work']
            
            session = {
                'player_id': player['player_id'],
                'player_name': f"{player['first_name']} {player['last_name']}",
                'sport': player['sport'],
                'position': player['position'],
                'analysis_date': (datetime.now() - timedelta(days=np.random.randint(0, 14))).strftime('%Y-%m-%d'),
                'analysis_type': np.random.choice(['Video Analysis', 'Motion Capture', '3D Motion Scan', 'Force Plate + Video']),
                'biomech_score': biomech_score,
                'movement_quality': movement_quality,
                'injury_risk': injury_risk,
                'match_readiness': match_status,
                'status_class': status_class,
                'detected_issues': detected_issues,
                'prevention_tips': tips,
                'video_duration': f"{np.random.randint(3, 8)}:{np.random.randint(10, 59):02d}"
            }
            analysis_sessions.append(session)
        
        # Sort by biomechanical score (lowest first)
        analysis_sessions.sort(key=lambda x: x['biomech_score'])
        
        # Issues distribution for chart
        all_issues = [issue for session in analysis_sessions for issue in session['detected_issues']]
        issues_dist = {}
        for issue in set(all_issues):
            issues_dist[issue] = all_issues.count(issue)
        
        # Match readiness distribution
        readiness_dist = {'Ready': 0, 'Caution': 0, 'Not Ready': 0}
        for session in analysis_sessions:
            readiness_dist[session['match_readiness']] += 1
        
        # Sport-specific analysis
        sport_analysis = {}
        for sport in df['sport'].unique()[:8]:
            sport_sessions = [s for s in analysis_sessions if s['sport'] == sport]
            if sport_sessions:
                sport_analysis[sport] = {
                    'avg_biomech': round(sum(s['biomech_score'] for s in sport_sessions) / len(sport_sessions), 1),
                    'avg_movement': round(sum(s['movement_quality'] for s in sport_sessions) / len(sport_sessions), 1)
                }
        
        # Weekly trends
        weekly_data = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            weekly_data[day] = {
                'sessions': np.random.randint(8, 25),
                'avg_score': np.random.randint(75, 92)
            }
        
        return render_template('gait_analysis.html',
                             analysis_sessions=analysis_sessions,
                             issues_distribution=issues_dist,
                             readiness_distribution=readiness_dist,
                             sport_analysis=sport_analysis,
                             weekly_data=weekly_data,
                             total_sessions=len(analysis_sessions),
                             ready_count=readiness_dist['Ready'],
                             caution_count=readiness_dist['Caution'])
    
    except Exception as e:
        print(f"Error in gait_analysis: {str(e)}")
        traceback.print_exc()
        return render_template('error.html', message=f"Error loading gait analysis: {str(e)}"), 500


@app.route('/api/gait-detail/<player_id>')
def get_gait_detail(player_id):
    """Get detailed gait analysis with video/motion-capture data"""
    try:
        player = df[df['player_id'] == player_id].iloc[0]
        
        # Generate detailed biomechanical data
        detail = {
            'player_name': f"{player['first_name']} {player['last_name']}",
            'sport': player['sport'],
            'position': player['position'],
            'video_captures': [
                {'angle': 'Frontal View', 'duration': '2:34', 'quality': 'HD'},
                {'angle': 'Lateral View', 'duration': '2:41', 'quality': 'HD'},
                {'angle': 'Posterior View', 'duration': '2:28', 'quality': 'HD'}
            ],
            'biomech_metrics': {
                'knee_angle': round(np.random.uniform(15, 35), 1),
                'hip_flexion': round(np.random.uniform(20, 45), 1),
                'ankle_dorsiflexion': round(np.random.uniform(10, 25), 1),
                'trunk_lean': round(np.random.uniform(-5, 10), 1),
                'stride_length': round(np.random.uniform(1.2, 1.8), 2)
            },
            'movement_analysis': {
                'landing_pattern': np.random.choice(['Heel Strike', 'Midfoot Strike', 'Forefoot Strike']),
                'weight_distribution': f"{np.random.randint(48, 52)}% / {np.random.randint(48, 52)}%",
                'ground_contact_time': f"{np.random.randint(200, 280)}ms",
                'vertical_jump': f"{np.random.randint(45, 75)}cm"
            },
            'injury_prevention_program': [
                {'exercise': 'Hip Mobility Drills', 'sets': 3, 'duration': '10 min', 'frequency': 'Daily'},
                {'exercise': 'Single-Leg Balance', 'sets': 3, 'duration': '30 sec each', 'frequency': '5x/week'},
                {'exercise': 'Eccentric Hamstring Curls', 'sets': 3, 'reps': 12, 'frequency': '3x/week'},
                {'exercise': 'Plyometric Box Jumps', 'sets': 4, 'reps': 8, 'frequency': '2x/week'}
            ],
            'return_to_play_protocol': {
                'phase': 'Phase 3 - Sport-Specific Training',
                'clearance_percentage': np.random.randint(75, 95),
                'estimated_days': np.random.randint(7, 21),
                'cleared_activities': ['Light jogging', 'Change of direction drills', 'Non-contact practice'],
                'restricted_activities': ['Full contact', 'Maximum sprinting', 'Competition']
            }
        }
        
        return jsonify({'success': True, 'data': detail})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==========================================
# PERSONALIZED ACTIONABLE INSIGHTS ROUTE
# ==========================================

@app.route('/fitness-products')
def fitness_products():
    """Fitness Product Recommendations Page - Redirects to external shopping sites"""
    try:
        return render_template('fitness_products.html')
    except Exception as e:
        print(f"Error in fitness_products: {str(e)}")
        traceback.print_exc()
        return render_template('error.html', message=f"Error loading fitness products: {str(e)}"), 500


@app.route('/api/generate-insight/<player_id>')
def generate_player_insight(player_id):
    """Generate AI-powered personalized insight for a specific player"""
    try:
        # Ensure player_id is an integer for DataFrame lookup
        player_id_int = int(player_id)
        player = df[df['player_id'] == f'PLY{str(player_id_int).zfill(5)}'].iloc[0]
        
        risk_score = player['risk_score']
        
        # AI-generated recommendations based on player data
        recommendations = []
        
        if risk_score > 0.7:
            recommendations.append({
                'type': 'Critical',
                'title': 'Immediate Load Reduction Required',
                'description': f'Risk score of {round(risk_score, 2)} indicates high injury probability. Recommend 20-30% reduction in high-intensity workouts for 2 weeks.',
                'timeline': '1-2 weeks',
                'expected_outcome': 'Risk reduction to below 0.5'
            })
        
        if player['injury_status'] == 'Injured':
            recommendations.append({
                'type': 'Recovery',
                'title': 'Structured Rehabilitation Protocol',
                'description': f'Current injury: {player["current_injury"]}. Follow sport-specific rehab program with progressive loading.',
                'timeline': '4-8 weeks',
                'expected_outcome': 'Safe return to full activity'
            })
        
        if player['total_injuries_career'] > 3:
            recommendations.append({
                'type': 'Prevention',
                'title': 'Injury Pattern Analysis',
                'description': f'{player["total_injuries_career"]} previous injuries detected. Implement targeted prevention exercises for {player["current_injury"]} area.',
                'timeline': 'Ongoing',
                'expected_outcome': '40-60% reduction in re-injury risk'
            })
        
        # Add general wellness recommendations
        recommendations.append({
            'type': 'Wellness',
            'title': 'Optimize Recovery Strategies',
            'description': 'Ensure 8+ hours sleep, proper hydration, and nutrition timing for optimal recovery.',
            'timeline': 'Daily',
            'expected_outcome': 'Enhanced performance and recovery'
        })
        
        return jsonify({
            'success': True,
            'player': {
                'id': player_id_int,
                'name': f"{player['first_name']} {player['last_name']}",
                'sport': player['sport'],
                'risk_score': round(risk_score, 2)
            },
            'recommendations': recommendations,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        print(f"Error in generate_player_insight for player {player_id}: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==========================================
# FINANCIAL IMPACT CALCULATOR ROUTE
# ==========================================

@app.route('/financial-impact')
def financial_impact():
    """Financial Impact Calculator - Management Dashboard"""
    try:
        df_financial = load_data()
        if df_financial.empty:
            return render_template('error.html', message="No data available for financial analysis."), 500
        
        # Basic counts
        total_players = len(df_financial)
        injured_players_df = df_financial[df_financial['injury_status'] == 'Injured'].copy()
        total_injured = len(injured_players_df)
        
        # Initialize variables for the case with no injuries
        total_medical_costs = 0
        total_lost_productivity = 0
        total_prevention_investment_annual = 0
        potential_savings = 0
        roi_percentage = 0
        avg_recovery_days_base = 30
        insurance_covered_medical = 0
        out_of_pocket_medical = 0
        avg_cost_per_injury = 0
        cost_by_severity = {}
        sport_costs = {}  # Changed from list to dict for chart compatibility
        monthly_costs = []
        top_injury_costs_dict = []
        cost_trends = {}
        injury_prevention_impact = {}
        comparative_analysis = {}
        
        if total_injured > 0:
            # Calculate recovery days with fallback
            if 'recovery_time' in injured_players_df.columns and not injured_players_df['recovery_time'].isna().all():
                avg_recovery_days_base = int(injured_players_df['recovery_time'].mean())
            
            # Medical costs calculation
            if 'medical_cost' not in injured_players_df.columns:
                injured_players_df['medical_cost'] = injured_players_df.get('risk_score', 0.5) * 15000 + np.random.uniform(5000, 25000, size=len(injured_players_df))
            
            total_medical_costs = injured_players_df['medical_cost'].sum()
            
            # Lost productivity calculation
            avg_player_value_per_day = 5000
            if 'lost_productivity_cost' not in injured_players_df.columns:
                injured_players_df['lost_productivity_cost'] = injured_players_df.get('recovery_time', avg_recovery_days_base) * avg_player_value_per_day
            
            total_lost_productivity = injured_players_df['lost_productivity_cost'].sum()
            
            # Prevention program investment
            prevention_cost_per_player = 2500
            total_prevention_investment_annual = total_players * prevention_cost_per_player
            
            # ROI calculation
            injury_reduction_rate = 0.30
            potential_savings = (total_medical_costs + total_lost_productivity) * injury_reduction_rate
            roi_percentage = ((potential_savings - total_prevention_investment_annual) / total_prevention_investment_annual) * 100 if total_prevention_investment_annual > 0 else 0
            
            avg_cost_per_injury = (total_medical_costs / total_injured) if total_injured > 0 else 0
            
            # Cost breakdown by severity
            severity_mapping = {'Low': 0, 'Moderate': 1, 'High': 2, 'Critical': 3}
            if 'risk_score' in injured_players_df.columns:
                injured_players_df['severity'] = pd.cut(
                    injured_players_df['risk_score'],
                    bins=[0, 0.3, 0.6, 0.8, 1.0],
                    labels=['Low', 'Moderate', 'High', 'Critical']
                )
            else:
                injured_players_df['severity'] = 'Moderate'
            
            cost_by_severity = {}
            for severity in ['Low', 'Moderate', 'High', 'Critical']:
                severity_df = injured_players_df[injured_players_df['severity'] == severity]
                if not severity_df.empty:
                    cost_by_severity[severity] = {
                        'count': len(severity_df),
                        'total_cost': int(severity_df['medical_cost'].sum() + severity_df['lost_productivity_cost'].sum())
                    }
            
            sport_cost_data = injured_players_df.groupby('sport').agg({
                'medical_cost': 'sum',
                'lost_productivity_cost': 'sum',
                'player_id': 'count'
            }).round(0)
            
            for sport, row in sport_cost_data.iterrows():
                sport_costs[sport] = {
                    'total_cost': int(row['medical_cost'] + row['lost_productivity_cost']),
                    'injuries': int(row['player_id']),
                    'medical': int(row['medical_cost']),
                    'productivity': int(row['lost_productivity_cost'])
                }
            
            # Monthly costs
            current_date = datetime.now()
            monthly_costs = []
            for i in range(12):
                month_date = current_date - timedelta(days=30 * i)
                month_str = month_date.strftime('%b %Y')
                monthly_injuries_count = int(total_injured * (0.7 + np.random.uniform(0, 0.6)))
                monthly_injuries_count = max(0, monthly_injuries_count)
                
                if monthly_injuries_count > 0:
                    monthly_medical = (injured_players_df['medical_cost'].sample(min(monthly_injuries_count, len(injured_players_df)), replace=True)).sum()
                    monthly_productivity = (injured_players_df['lost_productivity_cost'].sample(min(monthly_injuries_count, len(injured_players_df)), replace=True)).sum()
                else:
                    monthly_medical = 0
                    monthly_productivity = 0
                    
                monthly_costs.insert(0, {
                    'month': month_str,
                    'injuries': monthly_injuries_count,
                    'medical_cost': int(monthly_medical),
                    'lost_productivity': int(monthly_productivity),
                    'cost': int(monthly_medical + monthly_productivity)
                })
            
            # Top cost contributors
            injury_type_costs = injured_players_df.groupby('current_injury').agg({
                'medical_cost': 'sum',
                'lost_productivity_cost': 'sum',
                'player_id': 'count'
            }).round(0)
            injury_type_costs.columns = ['total_medical_cost', 'total_lost_productivity', 'count']
            injury_type_costs['total_cost'] = injury_type_costs['total_medical_cost'] + injury_type_costs['total_lost_productivity']
            
            top_injury_costs_data = injury_type_costs.sort_values('total_cost', ascending=False).head(10)
            top_injury_costs_dict = []
            for injury_type, row in top_injury_costs_data.iterrows():
                top_injury_costs_dict.append({
                    'type': injury_type,
                    'count': int(row['count']),
                    'cost': int(row['total_cost'])
                })
            
            insurance_coverage_rate = 0.75
            out_of_pocket_medical = total_medical_costs * (1 - insurance_coverage_rate)
            insurance_covered_medical = total_medical_costs * insurance_coverage_rate
            
            # Cost Trends Analysis
            avg_monthly_cost = sum([m['cost'] for m in monthly_costs]) / 12 if monthly_costs else 0
            change_percent_value = round(((monthly_costs[-1]['cost'] - monthly_costs[-2]['cost']) / monthly_costs[-2]['cost'] * 100), 1) if len(monthly_costs) > 1 and monthly_costs[-2]['cost'] > 0 else 0
            cost_trends = {
                'current_month': monthly_costs[-1]['cost'] if monthly_costs else 0,
                'previous_month': monthly_costs[-2]['cost'] if len(monthly_costs) > 1 else 0,
                'avg_monthly': int(avg_monthly_cost),
                'trend': 'increasing' if len(monthly_costs) > 1 and monthly_costs[-1]['cost'] > monthly_costs[-2]['cost'] else 'decreasing',
                'change_percent': change_percent_value,
                'change_percent_abs': abs(change_percent_value)
            }
            
            # Injury Prevention Impact Analysis
            injury_prevention_impact = {
                'current_injury_rate': round((total_injured / total_players) * 100, 1),
                'target_injury_rate': round((total_injured / total_players) * 100 * 0.7, 1),
                'potential_reduction': int(total_injured * 0.3),
                'cost_savings_per_injury': int(avg_cost_per_injury),
                'total_preventable_cost': int(total_injured * 0.3 * avg_cost_per_injury)
            }
            
            # Comparative Analysis
            industry_avg_cost_per_injury = 35000
            industry_avg_injury_rate = 35.0
            comparative_analysis = {
                'vs_industry_cost': round(((avg_cost_per_injury - industry_avg_cost_per_injury) / industry_avg_cost_per_injury * 100), 1),
                'vs_industry_rate': round((((total_injured / total_players) * 100) - industry_avg_injury_rate), 1),
                'performing_better': avg_cost_per_injury < industry_avg_cost_per_injury,
                'cost_efficiency_score': round(min(100, max(0, 100 - ((avg_cost_per_injury - industry_avg_cost_per_injury) / industry_avg_cost_per_injury * 100))), 1)
            }
        
        roi_percentage_display = min(100, roi_percentage) if roi_percentage > 0 else 0
        
        return render_template('financial_impact.html',
                             total_players=total_players,
                             total_injured=total_injured,
                             total_medical_costs=int(total_medical_costs),
                             total_lost_productivity=int(total_lost_productivity),
                             total_prevention_investment=int(total_prevention_investment_annual),
                             potential_savings=int(potential_savings),
                             roi_percentage=round(roi_percentage, 1),
                             roi_percentage_display=round(roi_percentage_display, 1),
                             total_injuries=total_injured,
                             avg_recovery_days=avg_recovery_days_base,
                             insurance_covered=int(insurance_covered_medical),
                             out_of_pocket=int(out_of_pocket_medical),
                             avg_cost_per_injury=int(avg_cost_per_injury),
                             cost_by_severity=cost_by_severity,
                             sport_costs=sport_costs,
                             monthly_costs=monthly_costs,
                             top_injury_costs=top_injury_costs_dict,
                             cost_trends=cost_trends,
                             injury_prevention_impact=injury_prevention_impact,
                             comparative_analysis=comparative_analysis)
    
    except Exception as e:
        print(f"Error in financial_impact: {str(e)}")
        traceback.print_exc()
        return render_template('error.html', message=f"An error occurred during financial impact calculation: {str(e)}"), 500


@app.route('/return-to-play')
def return_to_play():
    """Return-to-Play Performance Analysis Dashboard"""
    df = load_data()
    
    # Get players with current injuries who have recovered
    recovered_players = df[df['recovery_status'] == 'Fully Recovered'].head(15)
    
    # Calculate RTP metrics
    rtp_data = {
        'total_rtp_cases': len(df[df['recovery_status'].isin(['Fully Recovered', 'In Recovery'])]),
        'successful_rtp': len(df[df['recovery_status'] == 'Fully Recovered']),
        'avg_recovery_days': int(df[df['recovery_status'] == 'Fully Recovered']['days_missed_current_season'].mean()),
        'rtp_success_rate': round((len(df[df['recovery_status'] == 'Fully Recovered']) / 
                                   max(len(df[df['recovery_status'].isin(['Fully Recovered', 'In Recovery'])]), 1)) * 100, 1)
    }
    
    # Sports-specific RTP data
    sports_rtp = df.groupby('sport').agg({
        'recovery_status': lambda x: (x == 'Fully Recovered').sum(),
        'performance_index': 'mean',
        'fitness_level': 'mean'
    }).round(1)
    
    # Top performers post-injury
    top_performers = recovered_players.nlargest(8, 'performance_index')[
        ['player_id', 'first_name', 'last_name', 'sport', 'position', 'performance_index', 
         'fitness_level', 'injury_date', 'recovery_status']
    ]
    
    return render_template('return_to_play.html',
                         rtp_data=rtp_data,
                         recovered_players=recovered_players.to_dict('records'),
                         top_performers=top_performers.to_dict('records'),
                         sports_rtp=sports_rtp.to_dict())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
