-- ==========================
-- STUDENTS
-- ==========================

CREATE TABLE students (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    firstname TEXT NOT NULL,

    lastname TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    google_id TEXT,

    mobile TEXT,

    branch TEXT,

    semester TEXT,

    college TEXT,

    skills TEXT,

    about TEXT,

    address TEXT,

    profile_photo TEXT DEFAULT 'default.png',

    resume TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ==========================
-- COMPANIES
-- ==========================

CREATE TABLE companies(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_name TEXT NOT NULL,

    hr_name TEXT,

    email TEXT UNIQUE NOT NULL,

    phone TEXT,

    password TEXT NOT NULL,

    website TEXT,

    address TEXT,

    description TEXT,

    logo TEXT,

    status TEXT DEFAULT 'Pending',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- ==========================
-- ADMINS
-- ==========================

CREATE TABLE admins(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    email TEXT UNIQUE,

    password TEXT

);



-- ==========================
-- JOBS
-- ==========================

CREATE TABLE jobs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,

    title TEXT NOT NULL,

    category TEXT NOT NULL,

    location TEXT NOT NULL,

    job_type TEXT NOT NULL,

    salary TEXT,

    experience TEXT,

    vacancies INTEGER,

    last_date TEXT,

    skills TEXT,

    description TEXT,

    status TEXT DEFAULT 'Active',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(company_id) REFERENCES companies(id)

);



-- ==========================
-- APPLICATIONS
-- ==========================

CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    apply_date TEXT,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(job_id) REFERENCES jobs(id),
    FOREIGN KEY(company_id) REFERENCES companies(id)
);
-- ==========================================
-- Resume Master
-- ==========================================

CREATE TABLE IF NOT EXISTS resumes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_id INTEGER NOT NULL,

    resume_name TEXT NOT NULL,

    template TEXT DEFAULT 'ats',

    objective TEXT,

    linkedin TEXT,

    github TEXT,

    portfolio TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(student_id)
    REFERENCES students(id)

);

-- ==========================================
-- Resume Education
-- ==========================================

CREATE TABLE IF NOT EXISTS resume_education (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    resume_id INTEGER,

    degree TEXT,

    college TEXT,

    passing_year TEXT,

    cgpa TEXT,

    FOREIGN KEY(resume_id)
    REFERENCES resumes(id)

);

-- ==========================================
-- Resume Projects
-- ==========================================

CREATE TABLE IF NOT EXISTS resume_projects (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    resume_id INTEGER,

    title TEXT,

    description TEXT,

    technology TEXT,

    FOREIGN KEY(resume_id)
    REFERENCES resumes(id)

);

-- ==========================================
-- Resume Experience
-- ==========================================

CREATE TABLE IF NOT EXISTS resume_experience (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    resume_id INTEGER,

    company TEXT,

    role TEXT,

    duration TEXT,

    description TEXT,

    FOREIGN KEY(resume_id)
    REFERENCES resumes(id)

);

-- ==========================================
-- Resume Skills
-- ==========================================

CREATE TABLE IF NOT EXISTS resume_skills (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    resume_id INTEGER,

    skill TEXT,

    FOREIGN KEY(resume_id)
    REFERENCES resumes(id)

);

-- ==========================================
-- Resume Certificates
-- ==========================================

CREATE TABLE IF NOT EXISTS resume_certificates (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    resume_id INTEGER,

    certificate TEXT,

    organization TEXT,

    year TEXT,

    FOREIGN KEY(resume_id)
    REFERENCES resumes(id)

);

-- ==========================================
-- Resume Languages
-- ==========================================

CREATE TABLE IF NOT EXISTS resume_languages (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    resume_id INTEGER,

    language TEXT,

    FOREIGN KEY(resume_id)
    REFERENCES resumes(id)

);

-- ==========================================
-- Resume Achievements
-- ==========================================

CREATE TABLE IF NOT EXISTS resume_achievements (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    resume_id INTEGER,

    achievement TEXT,

    FOREIGN KEY(resume_id)
    REFERENCES resumes(id)

);

-- ==========================================
-- Resume Hobbies
-- ==========================================

CREATE TABLE IF NOT EXISTS resume_hobbies (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    resume_id INTEGER,

    hobby TEXT,

    FOREIGN KEY(resume_id)
    REFERENCES resumes(id)

);
CREATE TABLE saved_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS selection_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    application_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,

    event_type TEXT NOT NULL
        CHECK(event_type IN ('Interview', 'Test')),

    title TEXT NOT NULL,

    event_date TEXT NOT NULL,
    event_time TEXT NOT NULL,

    meeting_link TEXT,
    message TEXT,

    status TEXT DEFAULT 'Scheduled',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(application_id)
        REFERENCES applications(id),

    FOREIGN KEY(company_id)
        REFERENCES companies(id),

    FOREIGN KEY(student_id)
        REFERENCES students(id),

    FOREIGN KEY(job_id)
        REFERENCES jobs(id)
);