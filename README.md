# ✨ Secret Spark 

Secret Spark is a Django-based web application designed to empower women through curated content and personalized wellness tools. 
In the diary section, women can reflect on their daily thoughts and track their mood. 
The integrated menstrual calendar visualizes the different phases of the cycle and highlights the user's current phase. 
For each phase, the app provides informative messages about physical and emotional changes, along with personalized nutrition and training recommendations - carefully tailored to support well-being throughout the cycle. 

🌐 **Live Demo**: https://secretspark.up.railway.app

## 🛠️ Technology Stack

- **Backend**: Django 5.2 with Django REST Framework
- **Database**: PostgreSQL with custom user model
- **AI Integration**: Hugging Face Transformers for personalized plan generation
- **Media Storage**: Cloudinary for production, local storage for development
- **Frontend**: Django templates with custom CSS and JavaScript
- **Authentication**: Custom email-based authentication backend
- **Deployment**: Railway with Gunicorn WSGI server and WhiteNoise for static files


### 🏗️ Core Applications

**👤 accounts/** - User Management System
- Custom user model with email-based authentication
- User profiles with location and profile picture support
- Authentication backend for email login

**📰 articles/** - Content Management System
- Article creation and management with rich content support
- Categorized articles across style, self-improvement, work and money

**📖 diary/** - Personal Wellness Journal
- Private diary entries with mood tracking integration
- Predefined mood choices (happy, calm, heartbroken, anger, in period)

**🌸 wellness/** - Advanced Wellness Tracking
- Menstrual cycle tracking with customizable phases
- AI-powered nutrition and training plan generation
- Phase-aware wellness recommendations
- Calendar integration for visual cycle tracking

**🏠 common/** - Shared Resources
- Homepage functionality and shared utilities
- Common templates and static resources
- Cross-application helper functions

### ⭐ Key Features

**🤖 AI-Powered Wellness Plans**
- Nutrition plans with meal suggestions and supplements
- Phase-specific training routines with exercises and recovery tips
- Intelligent recommendations based on menstrual cycle phases

**📅 Comprehensive Cycle Tracking**
- Visual calendar interface for cycle monitoring
- Customizable cycle and period lengths
- Phase-aware wellness insights (menstrual, follicular, ovulation, luteal)
- Integration with mood tracking and diary entries

**💼 Articles**
- Thoughtfully curated articles on a variety of topics, designed to empower, support, and inspire women in every aspect of life and throughout their personal journey. 


## 🗄️ Database Setup

### Option 1: Complete Database from SQL Dump 🚀

The project includes a full PostgreSQL database dump (`full_backup.sql`) containing:
-  Sample user accounts and profiles
-  Pre-populated articles across multiple wellness categories
-  Complete wellness tracking data with cycle phases
-  Generated nutrition and training plans
-  Mood tracking entries and diary data

**🐳 Docker Setup:**
```bash
# Set up environment variables in .env
cp .env .env

# Build and start services
docker-compose up --build

# Load complete database
docker-compose exec db psql -U postgres -d secretspark < full_backup.sql
```

**💻 Local Setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Configure .env with your database credentials
# Load complete database
psql -U your_db_user -d your_db_name < full_backup.sql

# Start development server
python manage.py runserver
```
## 🧪 Data for testing purposes
- **👥 Users**:
  - **📧 Email:** elenats@gmail.com; **🔑 password:** Elena123$$TS (superusers group)
  - **📧 Email:** ivayla_admin@gmail.com; **🔑 password:** Ivayla123!!AD (staff group)
  - **📧 Email:** lora@gmail.com; **🔑 password:** Lora123$$LL (basic user group)

## Groups & Permissions
- **Superusers**:
  - **Permissions**: 
    1. **FULL CRUD** operations and overall control
    2. **CAN give** permissions and access
- **Admins**:
  - **Permissions**: 
    1. Have access to the admin panel
    2. **CANNOT** delete users and profiles but have the ability to perform full CRUD operations with user's data
    3. **CAN** change permissions and give access to resources
- **Authenticated users**:
  - **Permissions**:
    1. **HAVE FULL** CRUD access to their content
    2. **HAVE ONLY** view permissions on the articles
- **Unauthenticated users**:
  - **Permissions**:
    1. **HAVE ONLY** get permissions - can access home page, can read articles 
    2. They can access the wellness page and try to submit their menstrual cycle data but their request will be handled after they login/create account


## 🚀 Deployment

This application is deployed on **Railway** with the following production setup:
- **WSGI Server**: Gunicorn for high-performance request handling
- **Static Files**: WhiteNoise for serving static files
- **Media Storage**: Cloudinary for image and file management
- **Database**: PostgreSQL hosted on Railway
- **Security**: Environment-based configuration with secure secrets management

