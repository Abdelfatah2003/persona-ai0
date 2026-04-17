import json
import os
from database.connection import get_db, init_db
import bcrypt

def load_json(filename):
    schema_path = os.path.join(os.path.dirname(__file__), 'schemas', filename)
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def seed_users():
    db = get_db()
    data = load_json('users.json')
    
    for user in data['users']:
        if db.users.find_one({'email': user['email']}):
            print(f"User {user['email']} already exists, skipping...")
            continue
        
        user['password'] = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.users.insert_one(user)
        print(f"Created user: {user['email']}")

def seed_careers():
    db = get_db()
    data = load_json('careers.json')
    
    for career in data['careers']:
        if db.careers.find_one({'name': career['name']}):
            print(f"Career {career['name']} already exists, skipping...")
            continue
        
        db.careers.insert_one(career)
        print(f"Created career: {career['name']}")

def seed_questions():
    db = get_db()
    data = load_json('questions.json')
    
    if db.questions.count_documents({}) > 0:
        print("Questions already seeded, skipping...")
        return
    
    for question in data['questions']:
        db.questions.insert_one(question)
    
    print(f"Seeded {len(data['questions'])} questions")

def seed_sample_personalities():
    db = get_db()
    
    sample_personalities = [
        {
            'name': 'Technical Developer',
            'openness': 75, 'conscientiousness': 80, 'extraversion': 40,
            'agreeableness': 50, 'neuroticism': 35
        },
        {
            'name': 'Creative Designer',
            'openness': 90, 'conscientiousness': 55, 'extraversion': 65,
            'agreeableness': 70, 'neuroticism': 45
        },
        {
            'name': 'Team Leader',
            'openness': 60, 'conscientiousness': 85, 'extraversion': 75,
            'agreeableness': 80, 'neuroticism': 30
        }
    ]
    
    users = list(db.users.find().limit(3))
    for i, user in enumerate(users):
        if i < len(sample_personalities):
            personality = sample_personalities[i]
            personality['user_email'] = user['email']
            
            if not db.personalities.find_one({'user_email': user['email']}):
                db.personalities.insert_one(personality)
                print(f"Created personality profile for {user['email']}")

def seed_all():
    print("Initializing database...")
    init_db()
    
    print("\nCleaning up incorrectly saved personalities...")
    cleanup_personalities()
    
    print("\nSeeding users...")
    seed_users()
    
    print("\nSeeding careers...")
    seed_careers()
    
    print("\nSeeding questions...")
    seed_questions()
    
    print("\nSeeding sample personalities...")
    seed_sample_personalities()
    
    print("\nDatabase seeding completed!")

def cleanup_personalities():
    db = get_db()
    
    bad_personalities = list(db.personalities.find({'user_id': {'$exists': True}, 'user_email': {'$exists': False}}))
    
    for p in bad_personalities:
        user_id = p.get('user_id')
        if isinstance(user_id, str) and '@' in user_id:
            db.personalities.update_one(
                {'_id': p['_id']},
                {'$rename': {'user_id': 'user_email'}}
            )
            print(f"  Fixed: renamed user_id to user_email for {user_id}")
        else:
            db.personalities.delete_one({'_id': p['_id']})
            print(f"  Deleted: invalid personality record")
    
    if len(bad_personalities) == 0:
        print("  No cleanup needed")

if __name__ == '__main__':
    seed_all()
