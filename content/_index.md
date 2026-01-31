---
# Leave the homepage title empty to use the site title
title: ''
date: 2024-01-30
type: landing

sections:
  # 1. THE HERO
  - block: hero
    content:
      title: |
        Bhalaji Yadav
      image:
        filename: avatar.png
      cta:
        label: '**Download CV**'
        url: uploads/resume.pdf
      cta_alt:
        label: Contact Me
        url: '#contact'
      text: |
        **Materials Engineer & Researcher**

        Specialized in Soft Materials, Adhesion Mechanics, and Automated Data Analysis.
        
        Currently bridging the gap between experimental mechanics and computational analysis as an M.S. Candidate at VCU.
    design:
      background:
        gradient_end: '#1976d2'
        gradient_start: '#004ba0'
        text_color_light: true

  # 2. BIOGRAPHY
  - block: about.biography
    id: about
    content:
      title: Biography
      username: admin
    design:
      columns: '1'

  # 3. SKILLS
  - block: features
    id: skills
    content:
      title: Technical Expertise
      items:
        - name: Experimental Mechanics
          description: Universal Testing (Instron), T-Peel & Shear Testing (ASTM), Rheology, Soft Material Fracture, Microscopy.
          icon: microscope
          icon_pack: fas
        
        - name: Computational & Data
          description: Python (Pandas, OpenCV, SciPy), MATLAB, Automated Data Pipelines, Statistical Analysis (PCA).
          icon: code
          icon_pack: fas
          
        - name: Quality & Regulatory
          description: FDA Compliance, cGMP Guidelines, CAPA/Root Cause Analysis, Design of Experiments (DoE).
          icon: clipboard-check
          icon_pack: fas
    design:
      columns: '1'
      view: 3

  # 4. EXPERIENCE (Fixed: Removed missing logos)
  - block: experience
    id: experience
    content:
      title: Experience
      items:
        - title: Graduate Research Assistant
          company: VCU Soft Functional Materials Lab
          company_url: ''
          location: Richmond, VA
          date_start: '2024-09-01'
          date_end: ''
          description: |2-
            *Focus: Fracture mechanics of soft materials & testing protocols.*
            - Drafted successful **$30,000 grant proposal** (Commonwealth Cyber Initiative) for thermochromic textiles.
            - Engineered an **Integrated Optical Metrology System** (Python/OpenCV) increasing throughput by **>300%**.
            - Developed high-throughput **Fracture Signal Analysis** protocol reducing analysis time by **>80%**.

        - title: Technical Project Manager
          company: Kreative Organics Pvt. Ltd.
          company_url: ''
          location: Hyderabad, India
          date_start: '2023-05-01'
          date_end: '2024-05-01'
          description: |2-
            *Promoted from Intern to Manager in 6 months.*
            - Directed **CAPA/Root Cause Analysis** initiatives ensuring US FDA audit readiness.
            - Analyzed **FDA Drug Master Files (DMF)** to steer strategic new market entry.
            - Executed **SAP System Requalification** with precision cutover.

        - title: Technical Project Intern
          company: Kreative Organics Pvt. Ltd.
          company_url: ''
          location: Hyderabad, India
          date_start: '2022-10-01'
          date_end: '2023-04-01'
          description: |2-
            - Engineered **Supply Chain Optimization Workflow** reducing research time by **70%**.
            - Designed **Standardized Chemical Data Protocol** (Python/Docker) with **90%** accuracy improvement.
    design:
      columns: '2'

  # 5. PROJECTS
  - block: portfolio
    id: projects
    content:
      title: Featured Projects
      filters:
        folders:
          - project
      buttons:
        - name: All
          tag: '*'
    design:
      columns: '1'
      view: showcase
      flip_alt_rows: true

  # 6. PUBLICATIONS
  - block: collection
    id: publications
    content:
      title: Publications & Presentations
      filters:
        folders:
          - publication
    design:
      columns: '2'
      view: citation

  # 7. ACHIEVEMENTS
  - block: accomplishments
    content:
      title: Achievements
      items:
        - title: Grant Award ($30,000)
          organization: Commonwealth Cyber Initiative
          date_start: '2024-09-01'
          description: 'For thermochromic textiles research in diabetic inflammation monitoring.'
          icon: award
          icon_pack: fas
        - title: National Neutron Scattering School
          organization: Oak Ridge National Laboratory
          date_start: '2025-09-01'
          description: 'Selected participant for training in advanced material characterization.'
          icon: atom
          icon_pack: fas
        - title: Graduate Assistantship
          organization: Virginia Commonwealth University
          date_start: '2024-08-01'
          description: 'Full Tuition Waiver & Stipend.'
          icon: graduation-cap
          icon_pack: fas
    design:
      columns: '2'

  # 8. CONTACT
  - block: contact
    id: contact
    content:
      title: Contact
      text: |
        Open to collaborations in Materials Science and Data-Driven R&D.
      email: kbhalajiyadav22@gmail.com
      phone: +1 (804) 310-4169
      address:
        street: 401 W Main St (VCU Engineering)
        city: Richmond
        region: VA
        postcode: '23284'
        country: United States
        country_code: US
    design:
      columns: '2'
---
