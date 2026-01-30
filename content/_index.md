---
# Leave the homepage title empty to use the site title
title: ''
date: 2022-10-24
type: landing

sections:
  - block: hero
    content:
      title: |
        Bhalaji Yadav
        Kantepalle
      image:
        filename: avatar.png
      cta:
        label: '**Download CV**'
        url: uploads/resume.pdf
      cta_alt:
        label: Contact Me
        url: '#contact'
      text: |
        **Chemical Engineer | Materials Science Researcher**
        
        Bridging Materials Science and Regulated Quality Operations to advance healthcare innovation.
        
        Currently pursuing M.S. at VCU with focus on soft functional materials for medical applications.
    design:
      background:
        gradient_end: '#1976d2'
        gradient_start: '#004ba0'
        text_color_light: true

  - block: about.biography
    id: about
    content:
      title: About Me
      username: admin
    design:
      columns: '1'

  - block: experience
    content:
      title: Experience
      items:
        - title: Graduate Research Assistant
          company: VCU Soft Functional Materials Lab
          company_url: ''
          company_logo: vcu
          location: Richmond, VA
          date_start: '2024-09-01'
          date_end: ''
          description: |2-
            - Drafted a successful **$30,000 grant proposal** (Commonwealth Cyber Initiative) for thermochromic textiles research
            - Engineered an **Integrated Optical Metrology System** (Python/OpenCV) that increased throughput by **>300%**
            - Predicted device fatigue limits using **unsupervised Machine Learning (PCA)**
            - Developed high-throughput **Fracture Signal Analysis** protocol reducing analysis time by **>80%**
            - Extended Michel-Lévy interference chart for structural validation

        - title: Technical Project Manager
          company: Kreative Organics Pvt. Ltd.
          company_url: ''
          company_logo: org
          location: Hyderabad, India
          date_start: '2023-05-01'
          date_end: '2024-05-01'
          description: |2-
            - **Promoted from Intern to Manager** in 6 months for demonstrating high adaptability
            - Directed **CAPA/Root Cause Analysis** initiative ensuring US FDA audit readiness
            - Analyzed **FDA Drug Master Files (DMF)** to steer strategic new market entry
            - Executed **SAP System Requalification** with 5-hour precision cutover

        - title: Technical Project Intern
          company: Kreative Organics Pvt. Ltd.
          company_url: ''
          company_logo: org
          location: Hyderabad, India
          date_start: '2022-10-01'
          date_end: '2023-04-01'
          description: |2-
            - Engineered **Supply Chain Optimization Workflow** reducing research time by **70%**
            - Designed **Standardized Chemical Data Protocol** (Python/Docker) with **90%** accuracy improvement
            - Created **Stage-Gate Project Management Framework** adopted company-wide
    design:
      columns: '2'

  - block: portfolio
    id: projects
    content:
      title: Research Projects
      filters:
        folders:
          - project
      default_button_index: 0
      buttons:
        - name: All
          tag: '*'
        - name: Materials Science
          tag: Materials Science
        - name: Data Automation
          tag: Data Automation
        - name: Quality Systems
          tag: Quality Systems
    design:
      columns: '1'
      view: showcase
      flip_alt_rows: true

  - block: collection
    id: publications
    content:
      title: Publications & Presentations
      filters:
        folders:
          - publication
        exclude_featured: false
    design:
      columns: '2'
      view: citation

  - block: features
    id: skills
    content:
      title: Technical Skills
      items:
        - name: Material Characterization
          description: Adhesion Testing (ASTM D2724), Fatigue Analysis, Rheology, Microscopy, NMR, UV-Vis
          icon: microscope
          icon_pack: fas
        - name: Data & Automation
          description: Python (Data Mining, OpenCV), Power Automate, Tableau, Docker, Statistical Analysis (PCA)
          icon: code
          icon_pack: fas
        - name: Pharma Compliance
          description: cGMP Guidelines, CAPA Management, Root Cause Analysis (RCA), FDA Audit Preparation
          icon: certificate
          icon_pack: fas
        - name: Research & Strategy
          description: Technical Writing, Literature Review, Grant Writing, Market Intelligence, FDA Regulatory Analysis
          icon: pen-nib
          icon_pack: fas
        - name: Polymer Science
          description: Polymer Physics, Liquid Crystals, Electrospun Fiber Mats, Thermochromic Materials
          icon: atom
          icon_pack: fas
        - name: Process Systems
          description: SAP Business One (ERP), V-Model Validation, SOP Development, Project Management
          icon: cogs
          icon_pack: fas
    design:
      columns: '3'

  - block: accomplishments
    content:
      title: Achievements
      items:
        - title: Grant Award
          organization: Commonwealth Cyber Initiative
          date_start: '2024-09-01'
          date_end: ''
          description: '$30,000 grant for thermochromic textiles research in diabetic inflammation monitoring'
          icon: award
          icon_pack: fas
        - title: National Neutron Scattering School
          organization: Oak Ridge National Laboratory
          date_start: '2025-09-01'
          date_end: ''
          description: 'Selected participant for 1st National Neutron Scattering School'
          icon: atom
          icon_pack: fas
        - title: Graduate Assistantship Award
          organization: Virginia Commonwealth University
          date_start: '2024-08-01'
          date_end: ''
          description: 'Full Tuition Waiver & Stipend for M.S. program'
          icon: graduation-cap
          icon_pack: fas
        - title: Journal Publication
          organization: Polymers Journal
          date_start: '2025-01-01'
          date_end: ''
          description: '"Mechanical Properties of Dual-Layer Electrospun Fiber Mats" - Polymers 17(13), 1777'
          icon: file-alt
          icon_pack: fas
    design:
      columns: '2'

  - block: contact
    id: contact
    content:
      title: Contact
      subtitle: ''
      text: |
        Feel free to reach out for collaborations, research opportunities, or just to connect!
      email: kbhalajiyadav22@gmail.com
      phone: +1 (804) 310-4169
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
