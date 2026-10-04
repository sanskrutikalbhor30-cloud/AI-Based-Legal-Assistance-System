"""
Predefined legal knowledge base (offline fallback).

How it is used
--------------
* If the Gemini API is configured and working, Gemini answers the question.
* If the Gemini key is still the placeholder, or Gemini fails / times out,
  the chatbot falls back to the answers in this file.

How to add more questions
-------------------------
Append a new dictionary to KNOWLEDGE_BASE:

    {
        "topic": "Short name",
        "keywords": ["phrase one", "phrase two"],   # lower-case words / phrases
        "response": "Text shown to the user ..."
    }

Keywords are matched as whole words/phrases. The entry with the most keyword
matches wins. Use "•" for bullet points and **double stars** for bold.
"""

DISCLAIMER = (
    "This is general legal information, not legal advice. "
    "For a specific legal matter, consult a qualified legal professional."
)

GREETING_RESPONSE = (
    "Hello! I'm your AI Legal Assistance guide for Indian law.\n\n"
    "You can ask me about:\n\n"
    "• Rental agreements and tenancy\n"
    "• Property buying, registration and disputes\n"
    "• Cyber crime and online fraud\n"
    "• Consumer complaints and refunds\n"
    "• Divorce, maintenance, custody and other family matters\n"
    "• Employment, salary and workplace issues\n"
    "• FIR, arrest, bail, RTI, cheque bounce and more\n\n"
    "What would you like to know?"
)

THANKS_RESPONSE = "You're welcome! Feel free to ask another legal question anytime."

# Shown when nothing in the knowledge base matches
DEFAULT_RESPONSE = (
    "Your question has been received.\n\n"
    "I couldn't match it to a specific topic, so I can only give general guidance right now. "
    "The facts of your case and the applicable law need to be examined for a specific answer.\n\n"
    "Please try asking a more specific question, such as:\n\n"
    "• What is a rental agreement?\n"
    "• What should I do if I am a victim of online fraud?\n"
    "• How do I file a consumer complaint for a defective product?\n"
    "• What documents are needed to buy a property?\n"
    "• What is the process of divorce in India?\n"
    "• How do I file an FIR?\n"
    "• How do I file an RTI application?"
)

GREETING_KEYWORDS = ["hi", "hii", "hiii", "hello", "hey", "heyy", "hlo", "namaste", "namaskar", "good morning", "good afternoon", "good evening"]
THANKS_KEYWORDS = ["thanks", "thank you", "thankyou", "thx"]

KNOWLEDGE_BASE = [
    # ------------------------------------------------------------------
    # ORIGINAL TOPICS (kept, slightly expanded)
    # ------------------------------------------------------------------
    {
        "topic": "Rental agreement",
        "keywords": ["rental agreement", "rent agreement", "rent", "tenant", "landlord", "tenancy",
                     "leave and license", "lease", "security deposit", "eviction", "evict"],
        "response": (
            "A rental agreement is a legal agreement between a landlord and a tenant.\n\n"
            "It normally contains:\n\n"
            "• Names of landlord and tenant\n"
            "• Property address\n"
            "• Monthly rent and due date\n"
            "• Security deposit and how it is refunded\n"
            "• Duration of the tenancy and renewal terms\n"
            "• Responsibilities of both parties (repairs, maintenance, utilities)\n"
            "• Rules for termination and notice period\n\n"
            "**Useful points**\n\n"
            "• Rent agreements longer than 11 months generally need to be registered; many people use an 11-month agreement (leave and licence in Maharashtra).\n"
            "• Stamp duty and rent-control rules differ from state to state.\n"
            "• A tenant cannot normally be evicted without following the legal process and giving proper notice.\n"
            "• Keep rent receipts and proof of deposit."
        ),
    },
    {
        "topic": "Cyber crime",
        "keywords": ["cyber crime", "cybercrime", "cyber", "hacking", "hacked", "phishing", "online fraud",
                     "suspicious message", "bank details", "identity theft", "otp", "upi fraud",
                     "scam", "sextortion", "cyberstalking", "morphed"],
        "response": (
            "Cyber crime means an illegal activity carried out using a computer, mobile phone, network or the internet.\n\n"
            "Examples include online fraud, identity theft, hacking, cyberstalking, phishing and unauthorized access to accounts.\n\n"
            "**What to do if you are a victim**\n\n"
            "1. If money was lost, call the national cyber crime helpline **1930** immediately - quick reporting improves the chance of freezing the money.\n"
            "2. Report the incident on the official portal **cybercrime.gov.in**.\n"
            "3. Inform your bank and block cards / UPI / net banking.\n"
            "4. Preserve evidence: messages, emails, screenshots, transaction IDs, phone numbers, URLs.\n"
            "5. Change passwords and enable two-factor authentication.\n"
            "6. You can also visit the nearest cyber crime police station.\n\n"
            "Relevant law: the Information Technology Act, 2000 and the Bharatiya Nyaya Sanhita, 2023."
        ),
    },
    {
        "topic": "Consumer law",
        "keywords": ["consumer", "defective product", "defective", "refund", "seller", "warranty",
                     "consumer court", "consumer complaint", "consumer forum", "faulty",
                     "misleading advertisement", "overcharged", "overcharging", "e-commerce", "damaged product"],
        "response": (
            "Consumer law protects people who purchase goods or services. In India the main law is the Consumer Protection Act, 2019.\n\n"
            "Consumers have rights relating to defective goods, poor-quality (deficient) services, unfair trade practices, misleading advertisements and overcharging.\n\n"
            "**How to complain**\n\n"
            "1. Keep the bill, receipts, warranty and all messages as evidence.\n"
            "2. Complain in writing to the seller / service provider and ask for a refund, replacement or repair.\n"
            "3. Call the National Consumer Helpline **1915** (or use the NCH app / portal) for mediation.\n"
            "4. If unresolved, send a legal notice and file a complaint before the Consumer Commission - online through **e-Daakhil**.\n\n"
            "Commissions: District (claims up to ₹50 lakh), State (₹50 lakh to ₹2 crore), National (above ₹2 crore). "
            "A complaint should generally be filed within 2 years of the cause of action. No court fee is charged for claims up to ₹5 lakh."
        ),
    },
    {
        "topic": "Family law",
        "keywords": ["family law", "family", "domestic matters", "adoption", "adopt", "marriage",
                     "married", "marry", "wedding", "marriage registration"],
        "response": (
            "Family law deals with legal matters relating to family and personal relationships.\n\n"
            "It may include marriage, divorce, maintenance, child custody, adoption, guardianship and domestic matters.\n\n"
            "**Key points**\n\n"
            "• In India, family law often depends on your religion: Hindu Marriage Act 1955, Muslim personal law, Indian Christian Marriage / Divorce Acts, Parsi laws.\n"
            "• The Special Marriage Act, 1954 allows marriage between people of any religion or interfaith couples (30 days' public notice period).\n"
            "• Marriages should be registered - it is useful proof for passports, visas, insurance and inheritance.\n"
            "• Adoption of children is governed by the Juvenile Justice Act and the CARA (Central Adoption Resource Authority) process; Hindus can also adopt under the Hindu Adoptions and Maintenance Act, 1956.\n\n"
            "Tell me the specific issue (divorce, custody, maintenance, etc.) and I can explain further."
        ),
    },
    {
        "topic": "Divorce",
        "keywords": ["divorce", "separation", "mutual consent", "mutual divorce", "contested divorce",
                     "talaq", "annulment", "judicial separation"],
        "response": (
            "Divorce is the legal ending of a marriage. In India the procedure depends on the personal law that applies (Hindu Marriage Act, Special Marriage Act, Muslim law, Christian / Parsi law).\n\n"
            "**1. Divorce by mutual consent** (e.g. Section 13B, Hindu Marriage Act)\n\n"
            "• Both spouses agree; they must generally have lived separately for at least one year.\n"
            "• A joint petition is filed in the Family Court, followed by a cooling-off period (normally 6 months, which the court may waive in suitable cases) and a second motion.\n\n"
            "**2. Contested divorce**\n\n"
            "• One spouse files on legal grounds such as cruelty, desertion, adultery, conversion, mental disorder or other grounds allowed by the applicable law.\n"
            "• It involves evidence, hearings and can take longer.\n\n"
            "**Related issues** decided along with divorce: maintenance / alimony, child custody and division of property.\n\n"
            "**Documents usually needed:** marriage certificate, ID and address proof, photographs, proof of separation, income details and relevant evidence."
        ),
    },
    {
        "topic": "Child custody",
        "keywords": ["child custody", "custody", "guardianship", "visitation", "guardian"],
        "response": (
            "Child custody is decided mainly on the principle of the **welfare of the child**, not the parents' wishes.\n\n"
            "• Laws involved: Guardians and Wards Act, 1890 and Hindu Minority and Guardianship Act, 1956 (or the applicable personal law).\n"
            "• Courts consider the child's age, safety, education, emotional bond and each parent's ability to provide care.\n"
            "• Types: physical custody, joint custody, and visitation rights for the other parent.\n"
            "• A child's preference may be considered if the child is old enough to express it.\n"
            "• Custody orders can be modified later if the child's circumstances change.\n\n"
            "Custody petitions are filed in the Family Court or the district court with jurisdiction. Keep records of the child's school, medical and expense details."
        ),
    },
    {
        "topic": "Maintenance / alimony",
        "keywords": ["maintenance", "alimony", "financial support", "wife maintenance", "section 125",
                     "child support", "section 144"],
        "response": (
            "Maintenance is financial support paid to a spouse, child or dependent parent who cannot support themselves.\n\n"
            "• Under criminal law (earlier Section 125 CrPC, now Section 144 of the Bharatiya Nagarik Suraksha Sanhita, 2023) a wife, minor children and parents unable to maintain themselves can claim maintenance.\n"
            "• Personal laws (for example Section 24 and 25 of the Hindu Marriage Act) allow interim and permanent alimony in divorce cases.\n"
            "• The Domestic Violence Act, 2005 also allows monetary relief.\n"
            "• The amount depends on the income and assets of both spouses, standard of living, and needs of children.\n\n"
            "Keep proof of income, expenses, bank statements and marriage details ready when applying."
        ),
    },
    {
        "topic": "Property law",
        "keywords": ["property", "property law", "land", "house", "ownership", "flat", "plot",
                     "sale deed", "buy property", "buying property", "selling property",
                     "title deed", "mutation", "encumbrance", "registration of property", "stamp duty"],
        "response": (
            "Property law deals with legal rights and responsibilities relating to property.\n\n"
            "**Common matters:** buying and selling, ownership disputes, property documents, transfer of property, rent and tenancy, inheritance.\n\n"
            "**Before buying property, verify:**\n\n"
            "• Title deed and the chain of previous ownership (usually 30 years)\n"
            "• Encumbrance Certificate (to check loans / legal claims)\n"
            "• Mutation / khata records and property tax receipts\n"
            "• Approved building plan and occupancy certificate\n"
            "• RERA registration for under-construction projects\n"
            "• No pending litigation on the property\n\n"
            "A sale of immovable property must be done by a **registered sale deed** at the Sub-Registrar office after paying stamp duty and registration charges (rates differ by state).\n\n"
            "Keep original documents safely and get them checked by a property lawyer before paying any money."
        ),
    },

    # ------------------------------------------------------------------
    # NEW TOPICS
    # ------------------------------------------------------------------
    {
        "topic": "Inheritance and will",
        "keywords": ["make a will", "last will", "write a will", "will deed", "registered will", "inheritance", "inherit", "succession", "ancestral property", "legal heir",
                     "heir", "coparcener", "daughter share", "partition", "probate", "intestate", "nominee"],
        "response": (
            "**Will:** A will is a legal document stating how a person's property should be distributed after death.\n\n"
            "• It must be made by a sound-minded adult, signed by the person, and attested by at least two witnesses.\n"
            "• Registration is not compulsory but is strongly recommended.\n"
            "• The Indian Succession Act, 1925 governs wills.\n\n"
            "**Without a will (intestate succession):**\n\n"
            "• Hindus, Buddhists, Jains and Sikhs are governed by the Hindu Succession Act, 1956 - daughters have equal rights as sons in ancestral property (2005 amendment).\n"
            "• Muslims, Christians and Parsis follow their respective personal laws / succession rules.\n\n"
            "**After a death:** obtain the death certificate, then a legal heir certificate or succession certificate, and apply for mutation of property and transfer of bank accounts.\n\n"
            "A nominee in a bank account or policy is only a trustee - the legal heirs still have rights to the money."
        ),
    },
    {
        "topic": "FIR and police complaint",
        "keywords": ["fir", "file fir", "police complaint", "police station", "zero fir", "e-fir",
                     "police refused", "police not registering", "complaint against police", "lodge complaint"],
        "response": (
            "**How to file an FIR (First Information Report)**\n\n"
            "1. Go to the police station and give the information about a cognizable offence orally or in writing.\n"
            "2. Ensure the officer records it, read it carefully and sign it.\n"
            "3. You have the right to a **free copy** of the FIR.\n\n"
            "**Important rights**\n\n"
            "• A **Zero FIR** can be registered at any police station, regardless of where the crime happened; it is then transferred.\n"
            "• Many states allow e-FIR / online complaints, especially for theft and lost items.\n"
            "• If the police refuse to register your FIR, send the complaint in writing to the Superintendent of Police, or approach the Magistrate.\n"
            "• Registration of FIR is mandatory for cognizable offences.\n\n"
            "Under the new criminal laws (Bharatiya Nagarik Suraksha Sanhita, 2023), FIR procedure is covered mainly under Section 173."
        ),
    },
    {
        "topic": "Arrest and bail",
        "keywords": ["arrest", "arrested", "bail", "anticipatory bail", "custody police", "remand",
                     "bailable", "non bailable", "non-bailable", "rights of arrested"],
        "response": (
            "**Rights of an arrested person (Article 22 of the Constitution and Supreme Court guidelines)**\n\n"
            "• To be told the grounds of arrest\n"
            "• To inform a family member or friend\n"
            "• To meet and consult a lawyer\n"
            "• To be produced before a Magistrate within **24 hours**\n"
            "• To a medical examination and to not be tortured or ill-treated\n"
            "• Free legal aid if you cannot afford a lawyer (NALSA helpline **15100**)\n\n"
            "**Bail**\n\n"
            "• In a **bailable** offence, bail is a right and can be granted by the police or court.\n"
            "• In a **non-bailable** offence, bail is at the court's discretion.\n"
            "• **Anticipatory bail** can be sought from the Sessions Court / High Court if you fear arrest.\n\n"
            "If you or someone you know is arrested, contact a criminal lawyer immediately."
        ),
    },
    {
        "topic": "Cheque bounce",
        "keywords": ["cheque bounce", "cheque bounced", "check bounce", "dishonoured cheque", "dishonour",
                     "section 138", "negotiable instruments", "cheque"],
        "response": (
            "A bounced (dishonoured) cheque can be a criminal offence under **Section 138 of the Negotiable Instruments Act, 1881**.\n\n"
            "**Steps**\n\n"
            "1. Get the bank's cheque return memo stating the reason.\n"
            "2. Send a written **legal demand notice** to the drawer within **30 days** of receiving the return memo.\n"
            "3. The drawer has **15 days** from receiving the notice to pay.\n"
            "4. If not paid, file a complaint in the Magistrate court within **1 month** after that 15-day period ends.\n\n"
            "Punishment can include imprisonment up to 2 years and/or a fine up to twice the cheque amount. "
            "The cheque must have been issued for a legally enforceable debt and be presented within its validity (3 months).\n\n"
            "Keep the cheque, return memo, notice, postal proof and proof of the underlying debt."
        ),
    },
    {
        "topic": "RTI",
        "keywords": ["rti", "right to information", "information act", "pio", "public information officer"],
        "response": (
            "The **Right to Information Act, 2005** lets any Indian citizen request information from public authorities.\n\n"
            "**How to file**\n\n"
            "1. Write an application to the Public Information Officer (PIO) of the department (or apply online at rtionline.gov.in for central departments).\n"
            "2. Pay the fee (usually ₹10; free for Below Poverty Line applicants).\n"
            "3. The PIO must reply within **30 days** (48 hours for matters of life and liberty).\n\n"
            "**If you are not satisfied**\n\n"
            "• File a **first appeal** with the First Appellate Authority within 30 days.\n"
            "• Then a **second appeal** to the Central / State Information Commission within 90 days.\n\n"
            "Some information is exempt (e.g. national security, personal information with no public interest)."
        ),
    },
    {
        "topic": "Domestic violence and dowry",
        "keywords": ["domestic violence", "dowry", "dowry harassment", "cruelty", "498a", "husband beating",
                     "abusive husband", "in-laws harassment", "wife harassment", "protection order"],
        "response": (
            "If you are facing violence or harassment at home, your safety comes first.\n\n"
            "**Immediate help**\n\n"
            "• Emergency: **112**\n"
            "• Women helpline: **181**\n"
            "• Police women's helpline: **1091**\n\n"
            "**Legal remedies**\n\n"
            "• **Protection of Women from Domestic Violence Act, 2005:** protection orders, residence rights (right to stay in the shared home), monetary relief and custody orders. A complaint can be made to the Protection Officer, police or Magistrate.\n"
            "• **Cruelty and dowry harassment** are criminal offences (earlier IPC 498A, now under the Bharatiya Nyaya Sanhita, 2023). Dowry demand is also punishable under the Dowry Prohibition Act, 1961.\n"
            "• You can seek maintenance and file for divorce.\n\n"
            "Keep evidence such as medical reports, photos, messages and call records, and reach out to a trusted person or NGO. Free legal aid is available through the District Legal Services Authority."
        ),
    },
    {
        "topic": "Employment and salary",
        "keywords": ["employment", "employer", "employee", "salary", "unpaid salary", "wages", "termination",
                     "fired", "layoff", "notice period", "resignation", "gratuity", "provident fund", "pf",
                     "labour", "labor", "appointment letter", "job", "workplace", "wrongful termination"],
        "response": (
            "Employment matters depend on your contract, the type of establishment and applicable labour laws (India is moving to consolidated Labour Codes, so check which rules currently apply to you).\n\n"
            "**Common issues and steps**\n\n"
            "• **Unpaid salary:** send a written demand to the employer / HR, keep salary slips and bank statements, then complain to the Labour Commissioner / Labour Office.\n"
            "• **Termination:** check your appointment letter for notice period and terms. Termination without proper process or notice may be challenged; workmen are protected by the Industrial Disputes Act.\n"
            "• **Provident Fund (PF):** track your account on the EPFO portal; file grievances on the EPFiGMS portal.\n"
            "• **Gratuity:** generally payable after 5 years of continuous service under the Payment of Gratuity Act, 1972.\n\n"
            "**Keep:** appointment letter, salary slips, offer/resignation emails, ID card, and written communication with the employer."
        ),
    },
    {
        "topic": "Sexual harassment at workplace",
        "keywords": ["sexual harassment", "posh", "workplace harassment", "internal committee", "icc",
                     "harassed at work", "eve teasing", "molestation"],
        "response": (
            "Sexual harassment at the workplace is prohibited under the **Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)**.\n\n"
            "• Every employer with 10 or more employees must set up an **Internal Committee (IC)**; smaller workplaces fall under the Local Committee at district level.\n"
            "• A written complaint should generally be filed within **3 months** of the incident (extendable by 3 months for valid reasons).\n"
            "• The committee inquires and can recommend action against the offender; conciliation is possible only if the complainant requests it.\n"
            "• You can also file a police complaint - such conduct can be a criminal offence under the Bharatiya Nyaya Sanhita.\n\n"
            "Keep messages, emails, witness names and dates. You can also call the women's helpline **181** or emergency **112**."
        ),
    },
    {
        "topic": "Legal notice",
        "keywords": ["legal notice", "send notice", "notice to", "demand notice"],
        "response": (
            "A legal notice is a formal written communication informing a person or organisation about a grievance and demanding a remedy within a stated time.\n\n"
            "**A good legal notice includes:**\n\n"
            "• Sender's and recipient's details\n"
            "• Facts of the dispute in order\n"
            "• The legal basis / wrong committed\n"
            "• The specific demand (payment, refund, stop an act) and a deadline (commonly 15-30 days)\n"
            "• Warning of legal action if the demand is not met\n\n"
            "It is usually drafted by a lawyer and sent by registered post / speed post with acknowledgment (and email). "
            "It is compulsory in some cases (e.g. cheque bounce, suits against the government) and useful before consumer or civil cases."
        ),
    },
    {
        "topic": "Legal aid",
        "keywords": ["legal aid", "free lawyer", "free legal", "nalsa", "cannot afford lawyer", "legal services authority",
                     "lok adalat", "afford a lawyer"],
        "response": (
            "Free legal aid is available in India under the **Legal Services Authorities Act, 1987**.\n\n"
            "**Who is eligible:** women, children, SC/ST members, victims of trafficking, persons with disabilities, industrial workmen, persons in custody, and people whose income is below the limit set by their state.\n\n"
            "**How to get it**\n\n"
            "• Visit the District Legal Services Authority (DLSA) in your district court complex, or the State Legal Services Authority.\n"
            "• Call the NALSA helpline **15100**.\n"
            "• Apply online at nalsa.gov.in.\n\n"
            "**Lok Adalats** offer quick, free settlement of disputes, and the decision is final and binding."
        ),
    },
    {
        "topic": "Loan recovery harassment",
        "keywords": ["loan", "recovery agent", "loan harassment", "emi", "bank harassment", "credit card",
                     "debt", "loan app", "cibil", "harassing for money", "rbi ombudsman"],
        "response": (
            "Lenders and recovery agents must follow the law and RBI guidelines - they cannot harass or threaten you.\n\n"
            "**Not allowed:** abusive language, threats, calls at odd hours, contacting your family / employer to shame you, or public humiliation.\n\n"
            "**What you can do**\n\n"
            "1. Note dates, numbers and keep recordings / screenshots of harassing messages.\n"
            "2. Complain to the bank / lender's Grievance Redressal Officer in writing.\n"
            "3. If not resolved in 30 days, file a complaint on the **RBI Integrated Ombudsman** portal (cms.rbi.org.in).\n"
            "4. For threats or blackmail (including from illegal loan apps), file a police complaint and report at **cybercrime.gov.in** / call **1930**.\n\n"
            "If you are unable to pay, talk to the lender about restructuring - early communication helps."
        ),
    },
    {
        "topic": "Traffic challan and accidents",
        "keywords": ["challan", "traffic fine", "e-challan", "driving licence", "driving license", "accident",
                     "motor vehicle", "hit and run", "traffic police", "vehicle", "insurance claim"],
        "response": (
            "**Traffic challan**\n\n"
            "• Check and pay e-challans at the Parivahan / state traffic police portal.\n"
            "• If you believe the challan is wrong, you can contest it in the traffic court or through the virtual court / Lok Adalat.\n"
            "• Always carry your driving licence, RC, insurance and pollution certificate (digital copies on DigiLocker are valid).\n\n"
            "**After a road accident**\n\n"
            "1. Call **112** or **108** for help and get medical care first.\n"
            "2. Inform the police and get an FIR / accident report.\n"
            "3. Inform your insurance company promptly.\n"
            "4. Victims or their families can claim compensation before the Motor Accident Claims Tribunal (MACT) under the Motor Vehicles Act, 1988."
        ),
    },
    {
        "topic": "Defamation",
        "keywords": ["defamation", "defame", "slander", "libel", "false allegations", "false accusation",
                     "reputation", "fake post", "false rumour"],
        "response": (
            "Defamation means harming someone's reputation through false statements - spoken, written, published or posted online.\n\n"
            "• It can be a **criminal offence** (Section 356 of the Bharatiya Nyaya Sanhita, 2023) and also a **civil wrong** where damages can be claimed.\n"
            "• Truth made for the public good, fair comment and statements in good faith are recognised defences.\n\n"
            "**What to do:** save screenshots / URLs of the defamatory content, send a legal notice asking for removal and an apology, report the content on the platform, and consult a lawyer about a criminal complaint or civil suit. For online abuse, also use **cybercrime.gov.in**."
        ),
    },
    {
        "topic": "Builder delay and RERA",
        "keywords": ["rera", "builder", "builder delay", "possession delay", "flat not delivered",
                     "under construction", "real estate", "developer", "housing project"],
        "response": (
            "The **Real Estate (Regulation and Development) Act, 2016 (RERA)** protects homebuyers.\n\n"
            "• Projects above the prescribed size must be registered with the state RERA authority. Check the registration number on your state RERA website before booking.\n"
            "• If the builder delays possession, you may claim **interest** on the amount paid or seek a refund.\n"
            "• Builders must not take more than 10% of the price as an advance before signing the agreement to sell.\n"
            "• Complaints are filed with the state RERA authority; you can also approach the Consumer Commission.\n\n"
            "Keep the allotment letter, agreement, payment receipts and all correspondence."
        ),
    },
    {
        "topic": "Senior citizens and parents",
        "keywords": ["senior citizen", "parents maintenance", "old age", "elderly", "abandoned by children",
                     "maintenance of parents"],
        "response": (
            "Senior citizens are protected by the **Maintenance and Welfare of Parents and Senior Citizens Act, 2007**.\n\n"
            "• Parents / senior citizens can claim monthly maintenance from their children or relatives who will inherit their property.\n"
            "• Apply to the Maintenance Tribunal (usually at the Sub-Divisional Officer level) - no lawyer is required.\n"
            "• A transfer of property made on the condition of care can be cancelled if the recipient fails to look after the senior citizen.\n"
            "• Elder helpline: **14567**."
        ),
    },
    {
        "topic": "Child protection",
        "keywords": ["child abuse", "pocso", "child helpline", "child labour", "minor abuse", "1098"],
        "response": (
            "Children are protected by laws such as the **POCSO Act, 2012** (sexual offences against children) and the Juvenile Justice Act.\n\n"
            "• Call **Childline 1098** (or 112) to report abuse, neglect or child labour.\n"
            "• Reporting a suspected sexual offence against a child is a legal duty under POCSO.\n"
            "• The identity of the child must be kept confidential.\n"
            "• The police must record the statement in a child-friendly manner, and special courts try such cases.\n\n"
            "If a child is in danger, contact the police or Childline immediately."
        ),
    },
    {
        "topic": "Data privacy",
        "keywords": ["data privacy", "privacy", "personal data", "data protection", "dpdp", "data leak", "data breach"],
        "response": (
            "Privacy is a fundamental right in India (Puttaswamy judgment, 2017). Personal data is protected by the **Digital Personal Data Protection Act, 2023** and the IT Act, 2000.\n\n"
            "• Companies must obtain valid consent before processing your personal data and use it only for the stated purpose.\n"
            "• You have rights to access, correct and erase your data and to raise grievances.\n"
            "• For a data breach or misuse, first complain to the company's grievance officer, then approach the regulator / adjudicating authority, or report at **cybercrime.gov.in**."
        ),
    },
    {
        "topic": "Marriage registration",
        "keywords": ["register marriage", "marriage certificate", "court marriage", "special marriage act",
                     "love marriage", "interfaith marriage", "inter-caste marriage"],
        "response": (
            "**Marriage registration**\n\n"
            "• Marriages under personal laws (e.g. Hindu Marriage Act, Section 8) can be registered with the local Marriage Registrar / Sub-Registrar.\n"
            "• **Court marriage** under the Special Marriage Act, 1954: give a notice of intended marriage to the Marriage Officer, wait 30 days for objections, then marry with 3 witnesses.\n\n"
            "**Documents usually needed:** ID and age proof of both partners, address proof, passport-size photos, wedding invitation / photos (for personal law registration), witness IDs and application form.\n\n"
            "Requirements and fees vary by state - check your local Sub-Registrar office or state e-registration portal."
        ),
    },

    {
        "topic": "Copyright, trademark and patents",
        "keywords": ["copyright", "trademark", "trade mark", "patent", "intellectual property", "ipr",
                     "plagiarism", "piracy", "brand name", "logo", "royalty"],
        "response": (
            "Intellectual property (IP) protects creations of the mind. In India the main laws are:\n\n"
            "• **Copyright** (Copyright Act, 1957): protects original literary, artistic, musical and cinematic works, software and sound recordings. It arises automatically when the work is created; registration is optional but useful as proof. Generally it lasts for the author's life plus 60 years.\n"
            "• **Trademark** (Trade Marks Act, 1999): protects brand names, logos and slogans. Register with the Trade Marks Registry (ipindia.gov.in) for the strongest protection.\n"
            "• **Patent** (Patents Act, 1970): protects new inventions that are novel, involve an inventive step and are industrially applicable. Protection generally lasts 20 years from filing.\n"
            "• **Design** (Designs Act, 2000): protects the look and shape of a product.\n\n"
            "**If someone copies your work:** collect proof of your ownership and of the copying, send a legal notice, and you may file a civil suit for injunction and damages or a criminal complaint. Copying small parts for criticism, review, research or education may be allowed as \"fair dealing\"."
        ),
    },
    {
        "topic": "Contracts and agreements",
        "keywords": ["contract", "agreement", "breach of contract", "breach", "mou", "non compete",
                     "non-compete", "void contract", "terms and conditions", "sign agreement", "affidavit"],
        "response": (
            "A contract is a legally enforceable agreement under the **Indian Contract Act, 1872**.\n\n"
            "**A valid contract needs:** an offer and acceptance, lawful consideration (something of value), parties who are adults of sound mind, free consent (no fraud, coercion or undue influence) and a lawful purpose.\n\n"
            "**If the other side breaks the contract:**\n\n"
            "1. Read the clauses on breach, notice and dispute resolution (many contracts require arbitration).\n"
            "2. Send a written legal notice giving a deadline.\n"
            "3. You can claim compensation for the loss suffered, or in some cases ask the court for specific performance.\n\n"
            "Keep signed copies, emails and payment proof. Agreements on stamp paper of the correct value are better evidence in court."
        ),
    },
    {
        "topic": "Income tax and GST notice",
        "keywords": ["income tax", "itr", "tax notice", "gst", "income tax notice", "tds", "tax refund"],
        "response": (
            "**If you receive an income tax or GST notice**\n\n"
            "1. Don't ignore it - note the section, the reason and the reply deadline.\n"
            "2. Verify it is genuine by logging in to the official portal (incometax.gov.in or gst.gov.in); fake tax-refund emails and SMS are a common scam.\n"
            "3. Collect the supporting documents (returns filed, Form 26AS / AIS, invoices, bank statements).\n"
            "4. Reply online through the portal within the time given, or take help from a Chartered Accountant or tax lawyer.\n\n"
            "You have appeal rights against assessment orders. Filing returns on time avoids penalties and interest."
        ),
    },
    {
        "topic": "Lost documents, passport and Aadhaar",
        "keywords": ["lost passport", "passport", "lost aadhaar", "aadhaar", "aadhar", "lost documents",
                     "lost driving licence", "lost id", "lost pan", "police verification", "name change"],
        "response": (
            "**If you lose an important document**\n\n"
            "1. File a complaint / lost-report at the police station (many states have an online lost-article report).\n"
            "2. **Passport:** report it and apply for a re-issue on the Passport Seva portal (passportindia.gov.in).\n"
            "3. **Aadhaar:** you can download it from uidai.gov.in or order a reprint.\n"
            "4. **PAN / driving licence / RC:** apply for a duplicate through the respective official portals (incometax.gov.in / Parivahan).\n"
            "5. **Bank cards or cheque books:** block them immediately with the bank.\n\n"
            "For a legal **change of name**, follow the process for a gazette notification along with an affidavit and newspaper publication as required in your state."
        ),
    },
    {
        "topic": "Civil suit and court process",
        "keywords": ["civil suit", "civil case", "civil", "file a case", "file case", "court case", "sue", "suit", "court fee",
                     "limitation period", "limitation", "petition", "high court", "supreme court", "pil",
                     "injunction", "summons"],
        "response": (
            "**Basic steps in a civil case in India**\n\n"
            "1. Try to settle first - send a legal notice; mediation and Lok Adalats are quicker and cheaper.\n"
            "2. File a plaint in the court with proper jurisdiction (based on where the defendant lives or where the cause of action arose) and pay the court fee.\n"
            "3. The court issues summons to the defendant, who files a written statement.\n"
            "4. Issues are framed, evidence is led, arguments are heard, and the court passes a judgment.\n"
            "5. Appeals lie to the higher court.\n\n"
            "**Limitation:** every claim has a time limit under the Limitation Act, 1963 (for example, 3 years for most money recovery claims), so don't delay. "
            "You can track case status on the eCourts portal (ecourts.gov.in). If you can't afford a lawyer, ask the District Legal Services Authority for free legal aid."
        ),
    },
    {
        "topic": "Theft, cheating and criminal offences",
        "keywords": ["theft", "stolen", "robbery", "cheating", "fraud", "forgery", "extortion", "threat",
                     "threatened", "blackmail", "assault", "murder", "crime", "bns", "ipc", "bharatiya nyaya sanhita",
                     "criminal case", "criminal complaint"],
        "response": (
            "Criminal offences are now defined mainly in the **Bharatiya Nyaya Sanhita, 2023 (BNS)**, which replaced the Indian Penal Code from 1 July 2024. "
            "Procedure is covered by the Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) and evidence by the Bharatiya Sakshya Adhiniyam, 2023.\n\n"
            "**What to do if you are a victim of theft, cheating, threats or assault**\n\n"
            "1. If anyone is in danger, call **112**.\n"
            "2. Get medical help and a medical report if you're injured.\n"
            "3. Report to the police and get an FIR registered (you're entitled to a free copy).\n"
            "4. Preserve evidence - photos, messages, CCTV details, bills, witness names.\n"
            "5. If the police don't act, write to the Superintendent of Police or approach the Magistrate.\n\n"
            "For online cheating or blackmail, also use **cybercrime.gov.in** or call **1930**."
        ),
    },
    {
        "topic": "Ragging and education",
        "keywords": ["ragging", "college", "university", "school admission", "fees refund", "student", "exam",
                     "education", "rte", "scholarship"],
        "response": (
            "**Students' rights**\n\n"
            "• **Ragging** is a criminal offence. Report it to the college anti-ragging committee, the UGC anti-ragging helpline **1800-180-5522** (antiragging.in) or the police.\n"
            "• **Right to Education Act, 2009:** free and compulsory education for children aged 6-14, and 25% reservation for economically weaker children in private unaided schools.\n"
            "• **Fee refund:** colleges must follow UGC / AICTE refund rules when a student withdraws; if refused, complain to the regulator or approach the Consumer Commission or High Court.\n"
            "• Serious grievances can also go to the state education department or the university grievance cell."
        ),
    },
    {
        "topic": "Lawyer / how this system works",
        "keywords": ["are you a lawyer", "who are you", "what can you do", "how does this work",
                     "replace lawyer", "legal advice", "reliable", "how to find lawyer", "hire lawyer"],
        "response": (
            "I'm an AI-based legal guidance assistant. I can explain legal concepts under Indian law, suggest documents to keep, and describe the usual steps for common problems.\n\n"
            "I am **not** a lawyer and cannot replace one. For court cases, contracts, disputes or criminal matters, please consult a qualified advocate. "
            "If you cannot afford one, free legal aid is available through the District Legal Services Authority (NALSA helpline **15100**)."
        ),
    },
]
