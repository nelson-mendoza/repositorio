# ContratoExpress: Simple Services Contract Generator

#### Video Demo:

---

# Why I Made This [+]: Real Need in Chiapas

I reside in **Cacahoatán, Chiapas**, where technical and manual labor constitutes a major part of the local economy. However, I discovered a recurring pattern: nearly all electricians, plumbers, mechanics, and freelancers operate almost entirely through verbal agreements.

We live in a culture built heavily on trust and "word of mouth," but this also leaves workers in extremely vulnerable situations.

I have personally seen technicians lose money because clients denied agreed payments after a project was completed. In other cases, customers demanded additional work outside the original quotation using the classic argument:

> "That was included."

ContratoExpress was not built merely as an academic project for Harvard. I built it as a practical tool capable of bringing economic justice and professionalism into my community.

The idea was simple:

Build software that allows any worker to formalize an agreement in less than 60 seconds directly from a phone, generating a professional PDF document that acts as both a legal and moral safeguard before any work even begins.

---

# Engineering and Design Choices

## Making PDFs with `pdfkit` vs `FPDF`

Choosing the PDF generation system became one of the most technically challenging parts of the project.

My initial approach used the `FPDF` library because it is lightweight, widely used within the Python ecosystem, and avoids external binary dependencies.

However, I quickly became frustrated with its limitations.

Using `FPDF` means working directly with Cartesian coordinates (`X`, `Y`) for every element, which made development extremely rigid and incompatible with modern responsive design principles.

I ultimately selected `pdfkit` (a wrapper around `wkhtmltopdf`).

This architectural decision allowed me to treat contracts as actual webpages rendered with HTML5 and CSS3. As a result, the generated PDF output matches exactly what the user sees on screen, following the WYSIWYG principle ("What You See Is What You Get").

This choice introduced another technical challenge: managing external Linux binaries and rendering dependencies.

Nevertheless, the visual flexibility and design consistency gained from this approach far outweighed the complexity of dependency management.

---

## Security: Manual Building vs Automated Solutions

CS50 taught me that security is not something added at the end of development; it must exist within the DNA of the software architecture itself.

Although I could have used libraries such as `Flask-Login`, I intentionally decided to build the authentication and session system manually in order to fully understand the internal flow of user data.

### Password Protection

Passwords are secured using the `hashlib` library with **SHA-256** hashing.

Additionally, every user account generates an independent random salt before hashing. This protects against:

- Rainbow table attacks
- Credential reuse exposure
- Database leak scenarios

Even if the SQLite database were compromised, original passwords would remain cryptographically unreadable.

### Data Protection

I implemented strict backend validations to mitigate:

- SQL Injection
- Cross-Site Scripting (XSS)

The application also enforces automatic session expiration after inactivity, which is especially important for technicians using shared computers or internet cafés.

---

# The Clean Industrial Aesthetic and User Experience

Because I spend a significant amount of time working in terminals and environments like Kali Linux, I naturally gravitate toward dark and highly functional interfaces.

I did not want ContratoExpress to feel like a generic template website. I wanted it to feel engineered.

The application adopts a **Clean Industrial** visual identity using:

- Zinc and amber tones
- High-contrast dark themes
- `JetBrains Mono` typography

This decision was not purely aesthetic.

Many technicians read contracts outdoors or in low-light conditions, so the interface was optimized to reduce eye strain and improve readability in real-world environments.

The platform is also fully responsive and adapts seamlessly between:

- Smartphones on construction sites
- Laptops in offices
- Desktop workstations

---

# Project Structure (Modularity)

To maintain scalability and readability, I separated responsibilities into independent modules rather than building a monolithic application.

## `app.py`

Acts as the orchestrating brain of the application.

Handles:

- Flask routing
- Session management
- PDF engine communication
- Core business logic

---

## `rules.py`

Custom validation module containing advanced Regular Expressions (`Regex`) for validating:

- Emails
- Phone numbers
- Monetary amounts

This separation isolates validation logic from web application logic.

---

## `static/js/script.js`

Pure vanilla JavaScript used for dynamic frontend interactions.

Features include:

- Automatic totals
- Tax calculations
- Real-time updates without page reloads

This creates the impression of a fast modern web application.

---

## `templates/contract_template.html`

The "mother" of the PDF system.

This template was specifically optimized for print rendering, ensuring that:

- Margins
- Typography
- Logos
- Layout consistency

Remain correct across both A4 and Letter paper formats.

---

# Installation Guide (Also Known as Linux Headache)

One of the steepest learning curves involved managing Linux system dependencies.

In environments such as GitHub Codespaces, installing `pdfkit` alone is insufficient because the binary rendering engine is still missing.

To solve this portability issue, I included the `.deb` package directly inside the repository.

---

# Exact Installation Steps

## 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Install the PDF Engine

```bash
sudo dpkg -i wkhtmltopdf_0.12.6-2build2_amd64.deb
```

---

## 3. Critical Linux Dependency Step

```bash
sudo apt install -f
```

This command is essential.

It resolves the font libraries and rendering dependencies required for the PDF engine to function correctly under Linux.

It took several failed attempts before realizing this missing step was the root cause of the rendering problems.

---

# Conclusion and Final Reflection

ContratoExpress represents the result of applying months of CS50x learning directly into the real-world problems I experience daily in Chiapas.

Throughout development, I encountered challenges rarely discussed in textbooks, including:

- UTF-8 encoding issues
- Broken accent characters (`ñ`, accented vowels)
- Temporary file management for uploaded logos
- Linux rendering inconsistencies

This project demonstrated to me that useful software does not require massive frameworks or enterprise-scale tooling.

I wanted to build something genuinely capable of helping workers formalize their labor with professionalism and dignity.

Building ContratoExpress from the ground up gave me confidence that I am capable of engineering complex software systems using solid foundations in Python, SQL, security, and web development.
