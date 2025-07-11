# Kongju University RAG Chatbot Development Context

## Project Overview
- **Goal**: Develop a RAG-based chatbot for Kongju University students
- **Information Provided**: Announcements, meal menus, academic calendar, shuttle bus, club information
- **Tech Stack**: Python, LangChain, ChromaDB, KoSimCSE, FastAPI

## Current Implementation Status

### ✅ Completed Features
1. **Data Modeling** (src/models.py:10-138)
   - Structured announcement data
   - Campus-based classification (Singwan/Cheonan/Yesan)
   - Category-based classification (Academic/Scholarship/Library, etc.)

2. **Korean Embedding System** (src/embeddings.py:11-54)
   - Uses KoSimCSE-RoBERTa-multitask model
   - Optimized for Korean language performance

3. **Document Processing Pipeline** (src/document_loader.py:7-36)
   - Document chunking and metadata management
   - LangChain Document conversion

4. **ChromaDB Vector Store** (src/vector_store.py:11-112)
   - Uses embedded mode (no separate server required)
   - Campus-based filtering support
   - Similarity search functionality

5. **RAG Search System** (src/rag_system.py:12-120)
   - OpenAI GPT model integration
   - Context-based answer generation
   - Source document tracking

6. **Test Code**
   - Basic functionality tests (tests/test_basic.py): ✅ Passed
   - RAG system tests (tests/test_rag.py): ✅ Fully passed

7. **Complete RAG System Built** 🎉
   - OpenAI API key setup completed
   - Full pipeline working: Question → Document search → GPT answer generation
   - Campus-based filtering functionality fully operational
   - Performance optimized with gpt-4o-mini model

8. **Event-based Messaging System** (src/messaging/)
   - Redis Pub/Sub based asynchronous messaging
   - Notice creation event (NOTICE_CREATED) support
   - Scalable event architecture (BaseEvent, NoticeEvent)
   - Type-safe Pydantic models
   - Foundation for real-time data synchronization

### 🚧 In Progress/Planned
- [ ] Event handler implementation (messaging system and RAG system integration)
- [ ] Real-time vector store update system
- [ ] FastAPI server setup
- [ ] Real data integration (crawling server integration)
- [ ] Redis cluster configuration (production environment)
- [ ] CLI interface
- [ ] Dependency warning resolution
- [ ] Add other information types (meals, shuttle bus, etc.)

## Technical Details

### Python Environment
- **Version Used**: Python 3.11 (packages installed)
- **Execution Command**: Must use `python3.11`
- **Dependencies**: Defined in requirements.txt

### ChromaDB Configuration
- **Mode**: Embedded mode (consider server mode for production)
- **Storage Location**: `./data/chroma_db`
- **Advantages**: Simple setup, no separate server required
- **Limitations**: Scalability constraints, single process access

### Test Execution Method
```bash
# Basic functionality tests
python3.11 tests/test_basic.py

# RAG system tests (requires OpenAI API key)
python3.11 tests/test_rag.py
```

### Known Issues
1. **Dependency Warnings**: LangChain version compatibility (no functional impact)
2. **Tokenizer Warnings**: Multiprocessing related (no functional impact)
3. **Performance Issues**: Document embedding recalculation each time (caching needed)

### Recent Achievements (2025-07-11)
- ✅ Complete RAG system built with OpenAI API key setup
- ✅ All tests passed (vector search, campus filtering, GPT answer generation)
- ✅ Functional chatbot completed
- ✅ Event-based messaging system added (Redis Pub/Sub)
- ✅ Scalability secured with microservices architecture foundation

## Development Direction
- **Incremental Approach**: Progressive development in small units
- **Test-Driven**: Writing test code for each feature
- **Scalable**: Modularized structure for easy feature addition

## Next Step Candidates
1. Event handler implementation (automatic vector store update on notice creation)
2. Message broker and RAG system integration testing
3. FastAPI server + messaging system integration
4. .env file template creation (including Redis configuration)
5. Simple CLI interface addition
6. Dependency warning resolution
7. Data model expansion (meals, shuttle bus, etc.)

## Messaging System Usage

### Event Publishing Specification (Publishing Server)
```json
{
  "topic": "notices.created",
  "payload": {
    "event_data": {
      "event_id": "uuid-here",
      "event_type": "notice_created",
      "timestamp": "2025-07-11T12:00:00Z",
      "source_service": "notice-crawler",
      "notice_id": "notice-12345",
      "title": "Notice Title",
      "content": "Notice Content",
      "url": "https://www.kongju.ac.kr/notice/12345",
      "campus": "CHEONAN",
      "category": "ACADEMIC",
      "published_date": "2025-07-11T10:00:00Z",
      "author": "Academic Affairs Team",
      "department": "Academic Affairs Office",
      "attachments": ["file1.pdf"]
    }
  }
}
```

### Redis Connection Configuration
- Default URL: `redis://localhost:6379`
- Production: Consider Redis cluster

# Important Instruction Reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.