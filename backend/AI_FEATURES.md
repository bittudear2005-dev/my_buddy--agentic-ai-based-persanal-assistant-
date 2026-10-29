# 🤖 AI Features Guide

Complete guide to all AI-powered features in Cosmic Assistant.

## 🎯 Available AI Models

### 1. Groq (Llama 3.3)
- **Best for**: Fast responses, general chat
- **Model**: `llama-3.3-70b-versatile`
- **Speed**: Ultra-fast (< 1 second)
- **Cost**: Free (generous limits)
- **Rate Limit**: Very high

### 2. Google Gemini
- **Best for**: Complex analysis, structured data
- **Model**: `gemini-2.0-flash-exp`
- **Speed**: Fast (1-3 seconds)
- **Cost**: Free (1,500 requests/day)
- **Features**: JSON mode, structured output

### 3. OpenAI (Optional)
- **Best for**: Highest quality responses
- **Model**: `gpt-4o-mini`
- **Speed**: Moderate (2-5 seconds)
- **Cost**: Paid (affordable pricing)

---

## 📚 AI Features

### 1. General Chat (`/api/ai/chat`)

**Purpose**: Have natural conversations with AI about anything

**Request**:
```json
{
  "message": "How can I improve my productivity?",
  "model": "gemini",
  "temperature": 0.7,
  "max_tokens": 2048,
  "context": {
    "previous_topic": "time management"
  }
}
```

**Response**:
```json
{
  "response": "Here are 5 proven strategies...",
  "model": "gemini-2.0-flash-exp",
  "tokens_used": 245,
  "timestamp": "2025-01-20T10:30:00Z"
}
```

**Use Cases**:
- General productivity advice
- Question answering
- Brainstorming sessions
- Learning new concepts

---

### 2. Task Analysis (`/api/ai/analyze-task`)

**Purpose**: Get AI-powered insights for any task

**Request**:
```json
{
  "task_title": "Build a mobile app for task management",
  "task_description": "Create a cross-platform app with React Native",
  "context": {
    "team_size": 3,
    "deadline": "3 months"
  }
}
```

**Response**:
```json
{
  "analysis": {
    "priority": "high",
    "estimated_hours": 320,
    "subtasks": [
      "Set up React Native development environment",
      "Design UI/UX mockups",
      "Implement authentication",
      "Build task CRUD operations",
      "Add notifications",
      "Test on iOS and Android"
    ],
    "tips": [
      "Use Expo for faster development",
      "Implement proper state management",
      "Test on real devices early"
    ],
    "challenges": [
      "Cross-platform compatibility",
      "Performance optimization",
      "App store deployment"
    ],
    "category": "development"
  }
}
```

**What You Get**:
- ✅ Priority recommendation
- ⏱️ Time estimation
- 📋 Subtask breakdown
- 💡 Expert tips
- ⚠️ Potential challenges
- 🏷️ Category suggestion

---

### 3. Note Summarization (`/api/ai/summarize-note`)

**Purpose**: Extract key information from long notes

**Request**:
```json
{
  "note_content": "Long meeting notes about Q1 planning...",
  "summary_length": "medium"
}
```

**Response**:
```json
{
  "summary": {
    "summary": "The Q1 planning meeting covered three main areas: product roadmap, hiring plans, and budget allocation. Key decisions included...",
    "key_points": [
      "Launch 2 new features in Q1",
      "Hire 3 engineers by end of February",
      "Budget increased by 20% for marketing"
    ],
    "tags": ["planning", "q1", "meeting", "roadmap"],
    "word_count": 450
  }
}
```

**Summary Lengths**:
- `short`: 2-3 sentences
- `medium`: 1 paragraph (default)
- `long`: 2-3 paragraphs

**Use Cases**:
- Meeting notes summarization
- Article/research summaries
- Quick review of long documents
- Tag generation

---

### 4. Goal Planning (`/api/ai/generate-goal-plan`)

**Purpose**: Create comprehensive action plans for goals

**Request**:
```json
{
  "goal_title": "Learn machine learning and build an AI project",
  "goal_description": "Want to transition into ML engineering",
  "target_date": "2025-06-01",
  "current_skills": ["Python", "Basic statistics", "SQL"]
}
```

**Response**:
```json
{
  "plan": {
    "milestones": [
      {
        "title": "Foundation Phase",
        "description": "Master ML fundamentals",
        "timeline": "2 months"
      },
      {
        "title": "Practical Application",
        "description": "Build 3-5 ML projects",
        "timeline": "2 months"
      },
      {
        "title": "Specialization",
        "description": "Deep dive into specific area",
        "timeline": "1 month"
      }
    ],
    "actions": [
      "Complete Andrew Ng's ML course on Coursera",
      "Learn pandas and scikit-learn",
      "Build a classification project",
      "Deploy model with Flask/FastAPI",
      "Contribute to ML open source"
    ],
    "challenges": [
      "Mathematical concepts (linear algebra, calculus)",
      "Time management with full-time work",
      "Staying motivated through difficult topics"
    ],
    "resources": [
      "Coursera ML Specialization",
      "Kaggle datasets and competitions",
      "Fast.ai practical course",
      "ML communities on Discord/Reddit"
    ],
    "success_metrics": [
      "Complete 2 online courses",
      "Build 3 end-to-end ML projects",
      "Get ML job interviews"
    ]
  }
}
```

**What You Get**:
- 🎯 Milestone breakdown
- 📋 Actionable steps
- ⚠️ Potential challenges
- 📚 Resource recommendations
- 📊 Success metrics
- ⏰ Timeline suggestions

---

### 5. Smart Suggestions (`/api/ai/smart-suggestions`)

**Purpose**: Get context-aware suggestions

**Request**:
```json
{
  "context": "I'm a software developer interested in side projects",
  "suggestion_type": "goals"
}
```

**Suggestion Types**:
- `tasks`: Task suggestions
- `goals`: Goal ideas
- `categories`: Category suggestions
- `tags`: Relevant tags

**Response**:
```json
{
  "suggestions": [
    "Build a SaaS product in 3 months",
    "Contribute to 5 open source projects",
    "Launch a technical blog with 20 posts",
    "Create a mobile app with 1000 users",
    "Master a new programming language"
  ]
}
```

---

### 6. Brainstorming (`/api/ai/brainstorm`)

**Purpose**: Generate creative ideas on any topic

**Request**:
```json
{
  "topic": "SaaS ideas for developers",
  "num_ideas": 10
}
```

**Response**:
```json
{
  "ideas": "1. AI-powered code reviewer...\n2. Developer portfolio builder...",
  "topic": "SaaS ideas for developers"
}
```

**Use Cases**:
- Product ideas
- Content ideas
- Problem-solving
- Creative projects

---

### 7. Text Rewriting (`/api/ai/rewrite-text`)

**Purpose**: Rewrite text in different styles

**Request**:
```json
{
  "text": "Hey, can you fix the bug?",
  "style": "professional"
}
```

**Available Styles**:
- `professional`: Business emails, reports
- `casual`: Friendly conversations
- `formal`: Academic, official documents
- `creative`: Engaging, storytelling

**Response**:
```json
{
  "original": "Hey, can you fix the bug?",
  "rewritten": "Good morning, I would appreciate it if you could address the reported bug at your earliest convenience.",
  "style": "professional"
}
```

---

### 8. Action Item Extraction (`/api/ai/extract-action-items`)

**Purpose**: Extract tasks from text automatically

**Request**:
```json
{
  "text": "Meeting notes: John will prepare the presentation by Friday. Sarah needs to review the budget. We should schedule another meeting next week."
}
```

**Response**:
```json
{
  "action_items": [
    {
      "action": "Prepare the presentation",
      "assignee": "John",
      "deadline": "Friday"
    },
    {
      "action": "Review the budget",
      "assignee": "Sarah",
      "deadline": "Not specified"
    },
    {
      "action": "Schedule another meeting",
      "assignee": "Team",
      "deadline": "Next week"
    }
  ]
}
```

**Use Cases**:
- Meeting notes → tasks
- Email → action items
- Project requirements → todo list

---

### 9. Email Generation (`/api/ai/generate-email`)

**Purpose**: Draft professional emails quickly

**Request**:
```json
{
  "purpose": "Request a meeting with the design team",
  "key_points": [
    "Discuss Q1 roadmap",
    "Review user feedback",
    "Plan sprint priorities"
  ],
  "tone": "professional"
}
```

**Response**:
```json
{
  "email": "Subject: Meeting Request - Q1 Roadmap Discussion\n\nDear Design Team,\n\nI hope this email finds you well...",
  "purpose": "Request a meeting",
  "tone": "professional"
}
```

**Tones Available**:
- `professional`: Standard business
- `friendly`: Warm but professional
- `formal`: Very professional

---

### 10. Conversation History (`/api/ai/conversations`)

**Purpose**: View and manage chat history

**Request**:
```
GET /api/ai/conversations?limit=50&model=gemini
```

**Response**:
```json
[
  {
    "id": "uuid",
    "user_message": "How can I improve productivity?",
    "ai_response": "Here are 5 strategies...",
    "model": "gemini",
    "created_at": "2025-01-20T10:30:00Z"
  }
]
```

---

### 11. AI Usage Statistics (`/api/ai/stats`)

**Purpose**: Track your AI usage

**Response**:
```json
{
  "total_conversations": 150,
  "by_model": {
    "groq": 50,
    "gemini": 100
  },
  "recent_activity": {
    "last_7_days": 25
  }
}
```

---

## 💡 Best Practices

### 1. Choose the Right Model

**Groq (Fast)**:
- Quick questions
- Simple tasks
- Real-time chat
- High volume usage

**Gemini (Powerful)**:
- Complex analysis
- Structured output
- Detailed planning
- JSON responses

### 2. Provide Context

Better results with context:
```json
{
  "message": "Help me plan my day",
  "context": {
    "role": "software developer",
    "goals": ["ship feature", "learn React"],
    "meetings": 2
  }
}
```

### 3. Use Specific Prompts

❌ "Help me"
✅ "Create a detailed plan to launch my SaaS product in 3 months"

### 4. Leverage Temperature

- `0.0-0.3`: Consistent, factual
- `0.4-0.7`: Balanced (default)
- `0.8-1.0`: Creative, varied

### 5. Batch Related Tasks

Instead of 5 separate API calls:
```json
{
  "message": "Analyze these 3 tasks and suggest priorities..."
}
```

---

## 🎓 Example Workflows

### Workflow 1: Task Management
1. **Create task** manually
2. **Analyze task** → Get subtasks & estimation
3. **Extract action items** from description
4. **Track** in tasks list

### Workflow 2: Meeting Notes
1. **Take notes** during meeting
2. **Summarize** → Get key points
3. **Extract action items** → Convert to tasks
4. **Generate email** → Send summary to team

### Workflow 3: Goal Achievement
1. **Set goal** manually
2. **Generate plan** → Get detailed roadmap
3. **Break down** → Convert milestones to tasks
4. **Get suggestions** → Weekly task ideas

---

## 🔧 Advanced Features

### Conversation Context

AI remembers conversation context automatically:
```json
{
  "message": "What about for mobile apps?",
  "context": {
    "previous_topic": "productivity tools"
  }
}
```

### Multi-turn Conversations

Build complex interactions:
1. User: "I want to build a SaaS"
2. AI: "What problem does it solve?"
3. User: "Team communication"
4. AI: "Here's a plan..."

### Custom System Prompts

For special use cases, contact support to enable custom system prompts.

---

## 📊 Rate Limits

### Free Tier
- Groq: Very high (thousands/day)
- Gemini: 1,500 requests/day
- Storage: Unlimited conversations

### Tips to Stay Within Limits
- Use Groq for simple tasks
- Cache common responses
- Batch similar requests

---

## 🆘 Troubleshooting

### "AI model not enabled"
→ Check `.env` file: `enable_gemini=true`

### "API key invalid"
→ Verify your API keys in `.env`

### "Rate limit exceeded"
→ Wait or switch to different model

### Slow responses
→ Use Groq for faster responses

---

## 🚀 Coming Soon

- [ ] Image analysis with vision models
- [ ] Voice input/output
- [ ] PDF document analysis
- [ ] Multi-language support
- [ ] Custom AI assistants
- [ ] Team collaboration features

---

**Need help? Check `/api/docs` for interactive testing!**