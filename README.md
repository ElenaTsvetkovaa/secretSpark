# Secret Spark

A comprehensive women's wellness and lifestyle platform built with Django. Secret Spark empowers women to track their personal wellness journey through mood tracking, diary entries, menstrual cycle management, and access to curated wellness articles with AI-powered personalized recommendations.

## Technology Stack

- **Backend**: Django 5.2 with Django REST Framework
- **Database**: PostgreSQL with custom user model
- **AI Integration**: Hugging Face Transformers for personalized plan generation
- **Media Storage**: Cloudinary for production, local storage for development
- **Frontend**: Django templates with custom CSS and JavaScript
- **Authentication**: Custom email-based authentication backend

## Project Structure

```
secretSpark/
├── accounts/           # User authentication & profile management
├── articles/           # Artcles content
├── diary/             # Personal diary & mood tracking
├── wellness/          # Cycle tracking & AI-powered wellness plans
├── common/            # Shared utilities & homepage
├── tests/             # Test suites for all applications
```

### Core Applications

**accounts/** - User Management System
- Custom user model with email-based authentication
- User profiles with location and profile picture support
- Authentication backend for email login

**articles/** - Content Management System
- Article creation and management with rich content support
- Categorized articles across style, self-improvement, work and money

**diary/** - Personal Wellness Journal
- Private diary entries with mood tracking integration
- Predefined mood choices (happy, calm, heartbroken, anger, in period)

**wellness/** - Advanced Wellness Tracking
- Menstrual cycle tracking with customizable phases
- AI-powered nutrition and training plan generation
- Phase-aware wellness recommendations
- Calendar integration for visual cycle tracking

**common/** - Shared Resources
- Homepage functionality and shared utilities
- Common templates and static resources
- Cross-application helper functions

### Key Features

**AI-Powered Wellness Plans**
- Personalized nutrition plans with meal suggestions and supplements
- Phase-specific training routines with exercises and recovery tips
- Intelligent recommendations based on menstrual cycle phases
- Fallback system for reliable plan generation

**Comprehensive Cycle Tracking**
- Visual calendar interface for cycle monitoring
- Customizable cycle and period lengths
- Phase-aware wellness insights (menstrual, follicular, ovulation, luteal)
- Integration with mood tracking and diary entries

**Content & User Management**
- Rich article system with media support
- Secure user authentication with profile customization
- Cloudinary integration for reliable media storage
- Mobile-responsive design with interactive elements

## Database Setup

### Option 1: Complete Database from SQL Dump (Recommended)

The project includes a full PostgreSQL database dump (`full_backup.sql`) containing:
- Sample user accounts and profiles
- Pre-populated articles across multiple wellness categories
- Complete wellness tracking data with cycle phases
- Generated nutrition and training plans
- Mood tracking entries and diary data

**Docker Setup:**
```bash
# Set up environment variables in .env
cp .env.example .env

# Build and start services
docker-compose up --build

# Load complete database
docker-compose exec db psql -U postgres -d secretspark < full_backup.sql
```

**Local Setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Configure .env with your database credentials
# Load complete database
psql -U your_db_user -d your_db_name < full_backup.sql

# Start development server
python manage.py runserver
```

The application will be available at `http://localhost:8000` with a comprehensive wellness platform ready for women's health tracking and AI-powered personalized recommendations.