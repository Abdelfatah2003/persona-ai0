# API Documentation for AI Personality & Career Recommendation System

## Base URL
```
Production: https://api.persona-ai.com
Development: http://localhost:5000
```

## Authentication
All protected endpoints require JWT Bearer token in Authorization header:
```
Authorization: Bearer <token>
```

---

## Public Endpoints

### Health Check
```
GET /api/health
```
**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

---

## Authentication Endpoints

### Register
```
POST /api/auth/register
```
**Request Body:**
```json
{
  "name": "Ahmed Ali",
  "email": "ahmed@example.com",
  "password": "SecurePass123",
  "age": 22,
  "goal": "I want to become a software developer"
}
```
**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "_id": "...",
    "name": "Ahmed Ali",
    "email": "ahmed@example.com",
    "age": 22,
    "goal": "I want to become a software developer"
  }
}
```

### Login
```
POST /api/auth/login
```
**Request Body:**
```json
{
  "email": "ahmed@example.com",
  "password": "SecurePass123"
}
```
**Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "_id": "...",
    "name": "Ahmed Ali",
    "email": "ahmed@example.com",
    "age": 22,
    "goal": "I want to become a software developer"
  }
}
```

### Get User Profile
```
GET /api/auth/user/{email}
```
**Response (200):**
```json
{
  "_id": "...",
  "name": "Ahmed Ali",
  "email": "ahmed@example.com",
  "age": 22,
  "goal": "I want to become a software developer"
}
```

---

## Personality Analysis Endpoints

### Analyze Quiz Answers
```
POST /api/personality/analyze
Content-Type: application/json

{
  "answers": [4, 5, 3, 4, 5, 4, 3, 5, 4, 5, 5, 4, 4, 5, 4, 5, 4, 4, 5, 4, 
               3, 3, 4, 3, 4, 3, 3, 4, 3, 3, 5, 5, 4, 5, 5, 4, 5, 5, 4, 5, 
               2, 3, 2, 3, 2, 3, 2, 2, 3, 2]
}
```
**Response (200):**
```json
{
  "traits": {
    "openness": 82.0,
    "conscientiousness": 78.0,
    "extraversion": 62.0,
    "agreeableness": 84.0,
    "neuroticism": 36.0
  },
  "personality_type": "Explorer & Achiever"
}
```

### Analyze Text
```
POST /api/personality/analyze-text
Content-Type: application/json

{
  "text": "I enjoy solving technical problems and working on the computer. I prefer working alone and I like to analyze data."
}
```
**Response (200):**
```json
{
  "traits": {
    "openness": 68.5,
    "conscientiousness": 55.2,
    "extraversion": 42.3,
    "agreeableness": 51.8,
    "neuroticism": 48.5
  },
  "personality_type": "Explorer",
  "keywords": ["enjoy", "solving", "technical", "problems", "working"]
}
```

### Save Personality Results
```
POST /api/personality/save
Content-Type: application/json

{
  "email": "ahmed@example.com",
  "answers": [4, 5, 3, 4, 5, ...],
  "traits": {
    "openness": 82.0,
    "conscientiousness": 78.0,
    "extraversion": 62.0,
    "agreeableness": 84.0,
    "neuroticism": 36.0
  }
}
```
**Response (200):**
```json
{
  "message": "Personality saved successfully",
  "personality_type": "Explorer & Achiever",
  "traits": {
    "openness": 82.0,
    "conscientiousness": 78.0,
    "extraversion": 62.0,
    "agreeableness": 84.0,
    "neuroticism": 36.0
  }
}
```

### Get Personality
```
GET /api/personality/get/{user_id_or_email}
```
**Response (200):**
```json
{
  "_id": "...",
  "user_email": "ahmed@example.com",
  "openness": 82.0,
  "conscientiousness": 78.0,
  "extraversion": 62.0,
  "agreeableness": 84.0,
  "neuroticism": 36.0,
  "personality_type": "Explorer & Achiever"
}
```

---

## Recommendation Endpoints

### Get Career Recommendations
```
POST /api/recommendations/careers
Content-Type: application/json

{
  "openness": 82,
  "conscientiousness": 78,
  "extraversion": 62,
  "agreeableness": 84,
  "neuroticism": 36
}
```
**Response (200):**
```json
{
  "careers": [
    {
      "career": "Research Scientist",
      "match_score": 92.5,
      "profile": {
        "openness": 90,
        "conscientiousness": 75,
        "extraversion": 35,
        "agreeableness": 55,
        "neuroticism": 35
      }
    },
    {
      "career": "AI/ML Engineer",
      "match_score": 89.2,
      "profile": {...}
    }
  ]
}
```

### Get Skills for Career
```
GET /api/recommendations/skills/{career_name}
```
**Response (200):**
```json
{
  "skills": ["Python", "TensorFlow", "PyTorch", "Deep Learning", "NLP"]
}
```

### Get Similar Users
```
POST /api/recommendations/users
Content-Type: application/json

{
  "userId": "ahmed@example.com",
  "traits": {
    "openness": 82,
    "conscientiousness": 78,
    "extraversion": 62,
    "agreeableness": 84,
    "neuroticism": 36
  }
}
```
**Response (200):**
```json
{
  "similar_users": [
    {
      "user_id": "sara@example.com",
      "name": "Sara Hassan",
      "goal": "I want to become a data scientist",
      "initials": "SH",
      "similarity": 89.5,
      "traits": {...}
    }
  ]
}
```

### Get Similar Users by ID
```
GET /api/recommendations/similar-users/{user_id_or_email}
```
**Response (200):**
```json
{
  "similar_users": [...]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required field: email"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid credentials"
}
```

### 404 Not Found
```json
{
  "error": "User not found"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later.",
  "retry_after": "60"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| General API | 200/day, 50/hour |
| /api/auth/login | 10/minute |
| /api/personality/analyze | 30/minute |
| /api/recommendations/* | 30/minute |

---

## Big Five Personality Model

The system uses the Big Five (OCEAN) personality model:

| Trait | Description | High Score Indicates |
|-------|-------------|----------------------|
| Openness | Creativity, curiosity | Open to new experiences |
| Conscientiousness | Organization, discipline | Goal-oriented, reliable |
| Extraversion | Sociability, energy | Outgoing, assertive |
| Agreeableness | Cooperation, trust | Compassionate, helpful |
| Neuroticism | Emotional stability | Tendency toward negative emotions |

---

## Personality Types

Based on dominant traits, users are classified as:

- **Explorer**: High Openness
- **Achiever**: High Conscientiousness
- **Socializer**: High Extraversion
- **Helper**: High Agreeableness
- **Stabilizer**: Low Neuroticism
- **Architect**: High Openness + Conscientiousness
- **Mentor**: High Extraversion + Agreeableness
- **Balanced**: No dominant traits
