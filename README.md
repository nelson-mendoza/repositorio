ContratoExpress: Simple Services Contract Generator

Video Demo:

Why I Made This [+]: Real Need in Chiapas

I reside in Cacahoatán, Chiapas where technical and manual labor constitutes the local economy. But I discovered a common thread: nearly all electricians, plumbers, mechanics and freelancers solely run "on word of mouth." Well, we are a verbal agreement culture and this leaves us in a place of considerable danger.

I have seen other technicians lose money in situations where a client denies paying an agreed amount at the conclusion of a job, or goes even further and requests additional jobs that are not part of the initial quotation with the dirty trick argument: "that was included." I built ContratoExpress, not as a latent academic project for Harvard but rather my weapon to propel an economic justice agenda in my community. The idea was simple: Build a bit of software that enables virtually any worker to record an agreement in under 60 seconds from their phone producing a professional (PDF) document that provides both legal and moral backstop before you ever even pick up one tool.

Engineering and Design Choices

Making PDF with pdfkit vs FPDF — The Technical Conundrum & Details of what has within PDF Engine

Deciding how to create the contracts took a lot of time. My first approach I tried using the FPDF library since it is widely used in python world as lightweight and without complex external dependencies. However, I quickly became frustrated. Using FPDF, you are literally working with a Cartesian coordinate system (X, Y) which is painful to program in and made me throw out everything I knew about responsive web design.

I ended up choosing pdfkit (a wrapper around wkhtmltopdf). The reason for this choice was to be able to simply consider the contract like a webpage. Since the base of my template was developed using HTML5 and CSS3, we can make sure that the PDF output is exactly what the user sees on screen (WYSIWYG). This presented the problem of how to deal with external binaries on Linux, but I established visually gained flexibility at the cost of managing complications like that.

Security : Manual Building vs Automated Solutions

As CS50 taught us, security is not something tacked on at the end; it needs to be in the DNA of your code. I could have easily built an account management system with Flask-Login, but I endeavoured to roll something up from scratch so that I really knew what was going on with the data.

Password Hashing (hashlib library, SHA-256). I do not simply store the hash; each user generates an independent random salt. This is to avoid the rainbow table attacks and also even if someone would steal the database, original passwords are not readable.

Data Protection: I pioneered the use of manual validations at backend to mitigate the risk against SQL Injection and XSS. I also set the application to make sessions expire after a given timeout before being automatically signed out, which is very important if you are a technician using the application in shared computers or internet café.

The Clean Industrial Aesthetic and User Experience

As the majority of my time is spent in terminal and using Kali Linux, I am absolutely a fan of dark functional interfaces. I didn't want ContratoExpress to feel like a cookie-cutter site, I wanted it to feel like an engineering type product.

I adopted the concept of an Clean Industrial with Zinc and Amber color scheme, JetBrains Mono font. Not only about style, but it's a functional decision. Lots of technicians look at their contracts outdoors or in low-light scenarios, and this high-contrast scheme is easier for the eyes and makes things a lot easier to read. I also made sure that it was fully responsive, the form adapts actually nicely to fit both a laptop in an office and a smartphone way out in the middle of a construction site.

Project Structure (Modularity)

I split the responsibilities down to different files to keep it clean and scalable rather than having a monolithic app. py incomprehensible by anyone:

app. py: The orchestrating brain. This is where I am dealing with Flask routing, session logic, and connecting to the PDF engine as well.

rules. py: My custom validation module. I built all of the Regular Expressions (Regex) to validate that emails, phone numbers and amounts were valid before processed. This separates the business logic from the web logic.

static/js/script. js: Pure vanilla JavaScript. I used it for dynamic form: totals, subtotals and taxes are calculated on the fly without page reload which gives an impression of fast modern app.

templates/contract_template. HTML (Mother of PDF) It has been specifically optimized for print styles, so margins and logos will be perfect on A4 and Letter papers.

I am writing the Installation Guide (not to be confused with Headache On Linux)

One of the learning curves was tackling system dependencies. However, in environments such as GitHub Codespaces, pdfkit is not enough because the binary engine is missing. I also added dotNet.Config for making my project a shiny portable version. deb package in the repository.

Exact Steps:

Python Libraries: pip install -r requirements txt

Install PDF Engine: sudo dpkg -i wkhtmltopdf_0.12.6-2build2_amd64 deb

The Critical Step: sudo apt install -f This command is required. It took me a few attempts to realize that Linux doesn't install the font and rendering libraries the binary package needs in order for it to work without this.

Conclusion and Final Reflection

Months of studying CS50x and applying it to a reality I live every day in Chiapas results in ContratoExpress. Some peculiarities were not mentioned in the books, like encoding special characters (the 'ñ' and accents messed up the PDF) and temporary files when dealing with logos.

It shows that you do not need bulky frameworks to actually build something useful. I attempted to build a tool that really helps formalize my peoples work, I do have good design and on top of that sql and python basics. Creating this from the ground up empowered me that I could build complex things in software.
