<div align="center">

# ⚡ WorkWhiz

### Connecting Workers & Contractors — Seamlessly

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://workwhiz.onrender.com)

*A full-stack platform that bridges the gap between skilled workers and contractors. Workers showcase their expertise, contractors find the right talent — fast, reliable, and hassle-free.*

---

</div>

<div align="center">
  <h2>✨ Live Demo</h2>
  
  [![Live Demo](https://img.shields.io/badge/See_Live_Demo-4F46E5?style=for-the-badge&logo=github&logoColor=white)](https://workwhiz.onrender.com)
</div>

## 📸 Screenshots

### 🏠 Landing & Authentication

<details>
<summary>🏡 Home Page</summary>
<br>
<img src="projectSS/home page.jpeg" alt="Home Page" width="100%">
</details>

<details>
<summary>🔐 Login Page</summary>
<br>
<img src="projectSS/login page.jpeg" alt="Login Page" width="100%">
</details>

---

### 📊 Dashboards

<details>
<summary>🏗️ Contractor Dashboard</summary>
<br>
<img src="projectSS/contractor dashboard.jpeg" alt="Contractor Dashboard" width="100%">
</details>

<details>
<summary>👷 Worker Dashboard</summary>
<br>
<img src="projectSS/worker dashboard.jpeg" alt="Worker Dashboard" width="100%">
</details>

---

### 💼 Jobs & Applications

<details>
<summary>📝 Job Post Form</summary>
<br>
<img src="projectSS/jobPost form page.jpeg" alt="Job Post Form" width="100%">
</details>

<details>
<summary>📋 My Jobs</summary>
<br>
<img src="projectSS/my jobs page.jpeg" alt="My Jobs Page" width="100%">
</details>

<details>
<summary>📄 Job Application Form</summary>
<br>
<img src="projectSS/job application form.jpeg" alt="Job Application Form" width="100%">
</details>

<details>
<summary>📬 Job Applications</summary>
<br>
<img src="projectSS/job applications.jpeg" alt="Job Applications" width="100%">
</details>

<details>
<summary>📑 My Applications</summary>
<br>
<img src="projectSS/my applications page.jpeg" alt="My Applications Page" width="100%">
</details>

---

### 👤 Profile

<details>
<summary>🙍 User Profile</summary>
<br>
<img src="projectSS/user profile view page.jpeg" alt="User Profile View" width="100%">
</details>


---

## 🌟 Features

<table>
<tr>
<td width="50%">

### 👷 For Workers
- 📝 Create & manage professional profiles
- 🔍 Browse & apply for jobs matching your skills
- 👥 Add team members / sub-workers
- ⭐ Rate contractors & jobs
- 📊 Track application status in real-time
- 📍 Filter jobs by your location
- 🌐 Multi-language support (18 languages)

</td>
<td width="50%">

### 🏗️ For Contractors
- 📋 Post job listings with full details
- 🔎 Browse worker profiles by skill & location
- ✅ Accept / reject worker applications
- ⭐ Rate workers after completion
- 📈 Dashboard with job & applicant overview
- ✏️ Edit & manage posted jobs
- 🗑️ Delete job listings

</td>
</tr>
</table>

### 🔐 Authentication & Security
- User registration with role selection (Worker / Contractor)
- Secure login with password hashing
- Password reset via email with token validation
- Live password strength meter on signup
- Profile image upload with validation

### 🌐 Internationalization
- Google Translate integration supporting **18 regional languages**
- Language preference persistence via `localStorage`
- Includes: Hindi, Gujarati, Tamil, Marathi, Kannada, Telugu, Malayalam, Bengali, Punjabi, and more

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 5.x (Python 3.10+) |
| **Frontend** | HTML5, CSS3 (Custom Design System), Vanilla JavaScript |
| **Database** | PostgreSQL (Supabase) / SQLite (local dev) |
| **Media Storage** | Cloudinary (profile images & uploads) |
| **Static Files** | WhiteNoise (production-ready) |
| **Email** | SMTP via Gmail |
| **i18n** | Google Translate API |
| **Deployment** | Render |

---

## 📁 Project Structure

```
WorkWhiz/
├── WorkWhiz/              # Django project settings
│   ├── settings.py        # Configuration (DB, email, static files)
│   ├── urls.py            # Root URL routing
│   └── wsgi.py            # WSGI entry point
├── accounts/              # Main Django app
│   ├── models.py          # User, Job, Application, Rating models
│   ├── views.py           # All view logic
│   ├── forms.py           # Registration, profile, job, rating forms
│   ├── urls.py            # App URL patterns
│   └── admin.py           # Admin site configuration
├── templates/             # Django templates
│   ├── partials/          # Reusable template includes
│   │   ├── _google_translate.html
│   │   └── _navbar_unified.html
│   ├── accounts/          # Account-specific templates
│   │   ├── contractor_dashboard.html
│   │   ├── worker_dashboard.html
│   │   ├── contractor_profile.html
│   │   ├── worker_profile.html
│   │   ├── worker_detail.html
│   │   ├── post-job.html
│   │   ├── my-jobs.html
│   │   ├── rate_job.html
│   │   ├── rate_worker.html
│   │   └── rate_contractor.html
│   ├── index.html         # Landing page
│   ├── base.html          # Base template
│   ├── about_us.html      # Team page
│   ├── services.html      # Services overview
│   ├── help_center.html   # FAQ & contact
│   ├── edit_profile.html  # Profile editor
│   ├── log_in.html        # Login form
│   └── sign_up.html       # Registration form
├── static/
│   ├── css/
│   │   ├── styles.css       # Design system + responsive styles
│   │   └── style-signup.css # Signup-specific styles
│   └── images/            # Logos, team photos, defaults
├── media/                 # User-uploaded files (local dev only, Cloudinary in prod)
├── requirements.txt       # Python dependencies
├── build.sh               # Render build script
├── render.yaml            # Render deployment config
├── manage.py              # Django CLI
├── .env.example           # Environment variable template
└── .env                   # Environment variables (not committed)
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed
- **pip** package manager
- **Git** for version control

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/ARShaikh0801/WorkWhiz.git
cd WorkWhiz

# 2. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate         # Windows
# source venv/bin/activate    # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
#    Then edit .env with your actual values
```

```env
SECRET_KEY=your-secret-key-here
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
DATABASE_URL=                 # Leave empty for local SQLite
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
DEBUG=True
```

```bash
# 5. Run database migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create a superuser (optional, for admin access)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser.

---

## 📱 Responsive Design

WorkWhiz is fully responsive across all screen sizes:

| Breakpoint | Target |
|-----------|--------|
| `< 480px` | Mobile phones (portrait) |
| `481px – 768px` | Tablets & large phones |
| `> 769px` | Desktops & laptops |

All pages include the `<meta name="viewport">` tag and use CSS media queries for fluid layouts, flexible navigation wrapping, and touch-friendly targets.

---

## 🚀 Deployment (Render)

This project is configured for one-click deployment on [Render](https://render.com):

1. Fork this repository
2. Create a new **Web Service** on Render
3. Connect your GitHub repo
4. Render will auto-detect `render.yaml` and configure everything
5. Set the following environment variables in the Render dashboard:
   - `DATABASE_URL` — Supabase PostgreSQL connection string
   - `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` — Gmail SMTP
   - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` — Cloudinary media storage

---

## 👥 Team

<table>
<tr>
<td align="center"><strong>Shaikh Abdulrauf</strong><br>Backend Developer<br><em>Django, Python, C++</em></td>
<td align="center"><strong>Chauhan Dev</strong><br>Frontend Developer<br><em>HTML, CSS, JavaScript</em></td>
<td align="center"><strong>Shah Jinay</strong><br>Creative Developer<br><em>Web Dev, Animation, Design</em></td>
</tr>
</table>

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to your branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

<div align="center">

**Built with ❤️ by the WorkWhiz Team**

[GitHub](https://github.com/ARShaikh0801) • [LinkedIn](https://www.linkedin.com/in/shaikh-abdulrauf-asifparvez-b4485435a)

</div>
