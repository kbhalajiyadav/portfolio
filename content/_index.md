---
title: ''
date: 2025-01-31
type: landing

profile: true
toc: true

sections:
  # ===== HERO SECTION =====
  - block: hero
    content:
      title: Bhalaji Yadav
      image:
        filename: avatar.jpg
      cta:
        label: 'Download CV'
        url: uploads/resume.pdf
      cta_alt:
        label: Contact Me
        url: '#contact'
      text: |
        **Materials Engineer & Researcher**
        
        Specializing in Soft Materials, Adhesion Mechanics, and Automated Data Analysis.
        M.S. Candidate at Virginia Commonwealth University.
    design:
      background:
        gradient_end: '#1565c0'
        gradient_start: '#0d47a1'
        text_color_light: true

  # ===== BIOGRAPHY SECTION =====
  - block: markdown
    id: about
    content:
      title: Biography
      text: |
        I am a Chemical & Life Science Engineering researcher bridging the gap between experimental mechanics and computational analysis. Currently pursuing my M.S. at **Virginia Commonwealth University**, I conduct research at the **Soft Functional Materials Lab** led by Dr. Christina Tang.
        
        My work focuses on the fracture mechanics of soft interfaces—specifically avoiding the "False Positive" trap in wearable adhesion. I leverage Python (Pandas, OpenCV) to automate mechanical data analysis, turning raw peel tests into actionable fracture energy insights.
    design:
      columns: '1'

  # ===== LATEST NEWS SECTION =====
  - block: markdown
    id: news
    content:
      title: Latest Updates
      text: |
        * **Dec 2025** — Attended Anton Paar XRD Workshop (XRDynamic 500) on total scattering and PDF analysis
        * **Sep 2025** — Selected participant for the 1st National Neutron Scattering School at Oak Ridge National Laboratory (ORNL)
        * **Aug 2025** — Presented "Adhesives for Personalized Wearable Devices" at ACS Fall 2025 (Washington, D.C.)
        * **Jun 2025** — Attended Anton Paar Rheo-Polarized Imaging Workshop with Photron high-speed camera integration
        * **Sep 2024** — Drafted successful $30,000 Commonwealth Cyber Initiative grant for thermochromic textile research
    design:
      columns: '1'

  # ===== PROJECTS SECTION =====
  - block: portfolio
    id: projects
    content:
      title: Selected Projects
      filters:
        folders:
          - project
      buttons:
        - name: All
          tag: '*'
        - name: Academic Research
          tag: Academic Research
        - name: Industry
          tag: Industry
    design:
      columns: '1'
      view: compact
      flip_alt_rows: false

  # ===== PUBLICATIONS SECTION =====
  - block: collection
    id: publications
    content:
      title: Publications
      filters:
        folders:
          - publication
    design:
      columns: '2'
      view: citation

  # ===== EXPERIENCE SECTION =====
  - block: experience
    id: experience
    content:
      title: Experience
      items:
        - title: Graduate Research Assistant
          company: VCU Soft Functional Materials Lab
          company_url: 'https://vcusoftmaterialslab.weebly.com/'
          location: Richmond, VA
          date_start: '2024-09-01'
          date_end: ''
          description: |
            * Drafted successful $30,000 grant proposal (Commonwealth Cyber Initiative) for thermochromic socks
            * Engineered Integrated Optical Metrology System (Python/OpenCV) increasing throughput by >300%
            * Received Graduate Assistantship (Full Tuition Waiver)

        - title: Technical Project Manager
          company: Kreative Organics Pvt. Ltd.
          company_url: 'https://kreativeorganics.com/'
          location: Hyderabad, India
          date_start: '2023-05-01'
          date_end: '2024-05-01'
          description: |
            *Recruited via Deep Thought Edutech. Mentors: Mr. Ravi Seelamsetty (CEO) & Tarun Ayitham.*
            * Directed CAPA/Root Cause Analysis initiatives ensuring FDA audit readiness
            * Executed SAP System Requalification with precision cutover

        - title: Technical Intern
          company: Deep Thought Edutech
          company_url: 'https://deepthought.education/'
          location: Remote
          date_start: '2022-04-01'
          date_end: '2022-10-01'
          description: |
            * Developed logic frameworks and documentation standards
            * Contributed to educational technology logic frameworks

        - title: Technical Project Intern
          company: Kreative Organics Pvt. Ltd.
          company_url: 'https://kreativeorganics.com/'
          location: Hyderabad, India
          date_start: '2022-10-01'
          date_end: '2023-04-01'
          description: |
            * Engineered Supply Chain Optimization Workflow reducing research time by 70%
            * Designed Standardized Chemical Data Protocol (Python/Docker) with 90% accuracy improvement
    design:
      columns: '2'

  # ===== SKILLS SECTION =====
  - block: features
    id: skills
    content:
      title: Technical Skills
      items:
        - name: Experimental Mechanics
          description: Universal Testing (Instron), T-Peel (ASTM D2724), Rheology, Microscopy
          icon: microscope
          icon_pack: fas
        - name: Computational & Data
          description: Python (Pandas, OpenCV, SciPy), MATLAB, Automated Pipelines
          icon: code
          icon_pack: fas
        - name: Quality & Regulatory
          description: FDA Compliance, cGMP, CAPA, Design of Experiments
          icon: clipboard-check
          icon_pack: fas
    design:
      columns: '3'

  # ===== CONTACT SECTION =====
  - block: contact
    id: contact
    content:
      title: Contact
      email: kbhalajiyadav22@gmail.com
      
      address:
        street: 401 W Main St
        city: Richmond
        region: VA
        postcode: '23284'
        country: United States
        country_code: US
      coordinates:
        latitude: '37.5465'
        longitude: '-77.4530'
      directions: VCU College of Engineering
      autolink: true
    design:
      columns: '2'
---
