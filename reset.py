"""
Complete Database Reset Script
Run with: python reset.py
"""
from database.connection import get_db
from database.seed import seed_all

def reset_database():
    db = get_db()
    
    print("Deleting all data...")
    
    r = db.users.delete_many({})
    print(f"  - users: {r.deleted_count} deleted")
    
    r = db.personalities.delete_many({})
    print(f"  - personalities: {r.deleted_count} deleted")
    
    r = db.questions.delete_many({})
    print(f"  - questions: {r.deleted_count} deleted")
    
    r = db.careers.delete_many({})
    print(f"  - careers: {r.deleted_count} deleted")
    
    r = db.recommendations.delete_many({})
    print(f"  - recommendations: {r.deleted_count} deleted")
    
    try:
        r = db.quiz_history.delete_many({})
        print(f"  - quiz_history: {r.deleted_count} deleted")
    except:
        print("  - quiz_history: not found (OK)")
    
    print("\nSeeding fresh data...")
    seed_all()
    
    print("\n" + "="*60)
    print("  RESET COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    reset_database()
